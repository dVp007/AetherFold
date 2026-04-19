import os
from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from .schema import AgentState, FileInfo, MovePlan
from .tools import scan_desktop, peek_file, execute_move

class FileCategorization(BaseModel):
    category: str = Field(description="The logical folder for this file (Work, Finance, Media, Personal, etc.)")
    reasoning: str = Field(description="Brief explanation of why this file belongs in this category")
    should_trash: bool = Field(description="True if this file is junk, temporary, or redundant and should be moved to Trash")

def create_agent():
    # Load environment variables (assumes load_dotenv() is called in main.py)
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)
    llm_structured = llm.with_structured_output(FileCategorization)

    def scanner_node(state: AgentState) -> Dict[str, Any]:
        desktop_path = os.getenv("DESKTOP_PATH", os.path.expanduser("~/Desktop"))
        files = scan_desktop(desktop_path)
        # Peek for files to get context
        for file in files:
            file.content_peek = peek_file(file.path)
        return {"files": files}

    def categorizer_node(state: AgentState) -> Dict[str, Any]:
        processed_files = []
        for file in state["files"]:
            prompt = f"""Categorize this file based on its name and content:
            Name: {file.name}
            Peek: {file.content_peek}
            
            Return a logical category, reasoning, and whether it should be trashed. 
            Trash candidates: Screenshots, temporary installers (.dmg, .pkg, .exe) that seem redundant, empty or clearly useless files.
            """
            result = llm_structured.invoke(prompt)
            file.suggested_folder = result.category
            file.reasoning = result.reasoning
            file.should_trash = result.should_trash
            processed_files.append(file)
        return {"files": processed_files}

    def proposer_node(state: AgentState) -> Dict[str, Any]:
        storage_base = os.getenv("AETHER_FOLD_STORAGE", os.path.expanduser("~/Documents/AetherFold"))
        move_plan = []
        for file in state["files"]:
            category = "Trash" if file.should_trash else file.suggested_folder
            dest_path = os.path.join(storage_base, category, file.name)
            move_plan.append(MovePlan(
                source=file.path,
                destination=dest_path,
                category=category,
                is_deletion=file.should_trash
            ))
        return {"move_plan": move_plan}

    def executor_node(state: AgentState) -> Dict[str, Any]:
        if state.get("approved", False):
            execute_move(state["move_plan"])
            return {"approved": True}
        return {"error": "Move not approved"}

    # Define Graph
    workflow = StateGraph(AgentState)
    workflow.add_node("scanner", scanner_node)
    workflow.add_node("categorizer", categorizer_node)
    workflow.add_node("proposer", proposer_node)
    workflow.add_node("executor", executor_node)

    workflow.set_entry_point("scanner")
    workflow.add_edge("scanner", "categorizer")
    workflow.add_edge("categorizer", "proposer")
    
    # Breakpoint before execution
    workflow.add_edge("proposer", "executor")
    workflow.add_edge("executor", END)

    # Use checkpointer for persistence
    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer, interrupt_before=["executor"])
