"""
Auto-launch agents without user confirmation for Claude Code environment
"""

from agent_work_launcher import AgentWorkLauncher

def auto_launch():
    """Launch agents automatically"""
    launcher = AgentWorkLauncher()
    
    print("="*60)
    print("AUTO-LAUNCHING AUTONOMOUS AGENT WORK SESSION")
    print("="*60)
    
    # Get current task analysis
    print("Analyzing current tasks for agent assignment...")
    review_analysis = launcher.task_identifier.identify_review_tasks()
    
    if not review_analysis:
        print("Unable to analyze tasks. Check ClickUp connection.")
        return
    
    # Categorize tasks by agent type
    agent_assignments = launcher._categorize_tasks_for_agents(review_analysis)
    
    # Show assignment plan
    launcher._present_assignment_plan(agent_assignments)
    
    # Auto-launch without confirmation
    print("\nAuto-launching agents...")
    session_id = launcher.meta_agent.start_simultaneous_work(agent_assignments)
    
    print(f"\nAgent work session launched successfully!")
    print(f"Session ID: {session_id}")
    print(f"Agents are now working simultaneously on assigned tasks.")
    print(f"Meta-agent will monitor progress and prepare founder review report.")
    
    return session_id

if __name__ == "__main__":
    auto_launch()