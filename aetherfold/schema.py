from typing import Annotated, List, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

class FileInfo(BaseModel):
    name: str
    path: str
    content_peek: Optional[str] = None
    suggested_folder: Optional[str] = None
    reasoning: Optional[str] = None
    should_trash: Optional[bool] = False

class MovePlan(BaseModel):
    source: str
    destination: str
    category: str
    is_deletion: bool = False

class AgentState(TypedDict):
    files: List[FileInfo]
    move_plan: List[MovePlan]
    approved: bool
    error: Optional[str] = None
