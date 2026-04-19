import os
from dotenv import load_dotenv
from aetherfold.agent import create_agent
from aetherfold.schema import AgentState

def main():
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return

    agent = create_agent()
    
    # Run the agent up to the breakpoint
    config = {"configurable": {"thread_id": "aetherfold_session"}}
    
    # Initial run
    initial_state = {"files": [], "move_plan": [], "approved": False}
    print("Scanning Desktop and Categorizing Files...")
    
    # Run until interrupt
    for event in agent.stream(initial_state, config):
        for value in event.values():
            if "move_plan" in value:
                print("\nProposed Move Plan:")
                print("-" * 50)
                for move in value["move_plan"]:
                    prefix = "[TRASH/DELETE]" if move.is_deletion else "[MOVE]"
                    print(f"{prefix} Source: {move.source}")
                    print(f"To:     {move.destination}")
                    print(f"Cat:    {move.category}")
                    print("-" * 20)

    # Ask for approval
    approval = input("\nDo you approve these moves? (y/n): ").strip().lower()
    
    if approval == 'y':
        print("Executing moves...")
        # Update state to approve
        agent.update_state(config, {"approved": True})
        # Resume from breakpoint
        for event in agent.stream(None, config):
            pass
        print("Done!")
    else:
        print("Move plan rejected. No changes made.")

if __name__ == "__main__":
    main()
