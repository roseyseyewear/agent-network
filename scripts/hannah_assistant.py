#!/usr/bin/env python3
"""
Hannah Assistant Launcher
Main entry point for the task management and agent coordination system
"""

import sys
import os
from task_coordinator_agent import TaskCoordinatorAgent
from agent_feedback_system import AgentFeedbackSystem

def print_help():
    """Print help information"""
    print("""
Hannah Assistant - Task Management & Agent Coordination System

USAGE:
  python hannah_assistant.py [COMMAND]

COMMANDS:
  start           Start interactive task coordination session (default)
  status          Get current status update from all agents
  feedback        Run automated feedback analysis
  help            Show this help message

EXAMPLES:
  python hannah_assistant.py                 # Start coordination session
  python hannah_assistant.py status          # Quick status check
  python hannah_assistant.py feedback        # Get automated feedback

DESCRIPTION:
  The Hannah Assistant system helps prioritize and execute tasks through:
  
  🎯 Main Coordinator Agent:
     - Reviews your daily task priorities
     - Discusses what's on your radar
     - Gets your input on priorities and preferences
     - Delegates tasks to specialized agents
     - Monitors progress and provides updates
  
  🤖 Specialized Agents:
     - Research Agent: Handles research and information gathering
     - Calendar Agent: Manages scheduling and calendar tasks
     - Email Agent: Handles communication and follow-ups
     - Business Agent: Manages Roseys and Luna Wild business tasks
     - Admin Agent: Handles administrative and legal tasks
  
  📊 Automated Feedback System:
     - Monitors task progress and identifies stuck tasks
     - Escalates urgent items that need attention
     - Provides recommendations for better task flow
     - Tracks agent performance and suggests improvements

The system integrates with your ClickUp workspace and provides intelligent
automation while keeping you in control of priorities and decisions.
""")

def main():
    """Main entry point"""
    
    # Parse command line arguments
    command = sys.argv[1] if len(sys.argv) > 1 else 'start'
    
    if command == 'help' or command == '--help' or command == '-h':
        print_help()
        return
    
    try:
        if command == 'start':
            print("Starting Hannah Assistant Task Coordination Session...")
            coordinator = TaskCoordinatorAgent()
            coordinator.start_coordination_session()
            
        elif command == 'status':
            print("Getting status update from all agents...")
            coordinator = TaskCoordinatorAgent()
            coordinator.provide_status_update()
            
        elif command == 'feedback':
            print("Running automated feedback analysis...")
            feedback_system = AgentFeedbackSystem()
            print(feedback_system.provide_automated_feedback())
            
        else:
            print(f"Unknown command: {command}")
            print("Use 'python hannah_assistant.py help' for usage information")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nSession ended by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check your ClickUp API configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()