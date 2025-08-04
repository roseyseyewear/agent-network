"""
Agent Work Launcher
Launches autonomous agents to work on actual ClickUp tasks simultaneously
"""

import requests
import json
from autonomous_working_agents import MetaAgentSupervisor
from review_tasks_identifier import ReviewTasksIdentifier
from dotenv import load_dotenv

load_dotenv()

class AgentWorkLauncher:
    def __init__(self):
        self.meta_agent = MetaAgentSupervisor()
        self.task_identifier = ReviewTasksIdentifier()
    
    def launch_autonomous_work_session(self):
        """Launch autonomous agents to work on Hannah's tasks"""
        print("="*60)
        print("LAUNCHING AUTONOMOUS AGENT WORK SESSION")
        print("="*60)
        
        # Get current task analysis
        print("Analyzing current tasks for agent assignment...")
        review_analysis = self.task_identifier.identify_review_tasks()
        
        if not review_analysis:
            print("Unable to analyze tasks. Check ClickUp connection.")
            return
        
        # Categorize tasks by agent type
        agent_assignments = self._categorize_tasks_for_agents(review_analysis)
        
        # Show assignment plan
        self._present_assignment_plan(agent_assignments)
        
        # Confirm launch
        if self._confirm_launch():
            print("\nLaunching agents...")
            session_id = self.meta_agent.start_simultaneous_work(agent_assignments)
            return session_id
        else:
            print("Launch cancelled.")
            return None
    
    def _categorize_tasks_for_agents(self, review_analysis):
        """Categorize tasks for different agent types"""
        
        # Get all tasks that assistant can execute or need joint review
        assistant_tasks = review_analysis.get('assistant_review_needed', [])
        joint_tasks = review_analysis.get('joint_review_needed', [])
        
        # Combine operational tasks
        workable_tasks = []
        for task in assistant_tasks + joint_tasks:
            if isinstance(task, dict) and 'name' in task:
                workable_tasks.append(task)
            else:
                # Handle case where task might be from different structure
                workable_tasks.extend([t for t in assistant_tasks + joint_tasks if isinstance(t, dict)])
                break
        
        assignments = {
            'research': [],
            'vendor_selection': [],
            'business_analysis': [],
            'financial_research': [],
            'scheduling_coordination': []
        }
        
        # Assign tasks based on keywords and content
        for task in workable_tasks:
            task_text = task['name'].lower()
            task_obj = {
                'id': task.get('task_id', task.get('id', 'unknown')),
                'name': task['name'],
                'status': task.get('status', 'unknown'),
                'priority': task.get('priority', 'none')
            }
            
            # Research tasks
            if any(keyword in task_text for keyword in ['research', 'ai business', 'screen printing', 'shopping agents', 'investigate']):
                assignments['research'].append(task_obj)
            
            # Vendor selection tasks  
            elif any(keyword in task_text for keyword in ['hair stylist', 'pa for mum', 'health plan', 'find', 'hire']):
                assignments['vendor_selection'].append(task_obj)
            
            # Business analysis tasks
            elif any(keyword in task_text for keyword in ['business plan', 'marketing', 'launch', 'strategy', 'roseys', 'luna']):
                assignments['business_analysis'].append(task_obj)
            
            # Financial research tasks
            elif any(keyword in task_text for keyword in ['insurance', 'llc', 'financial', 'tax', 'cost']):
                assignments['financial_research'].append(task_obj)
            
            # Scheduling tasks
            elif any(keyword in task_text for keyword in ['calendar', 'schedule', 'planning', 'coordination']):
                assignments['scheduling_coordination'].append(task_obj)
            
            # Default to research for unmatched
            else:
                assignments['research'].append(task_obj)
        
        # Remove empty categories
        assignments = {k: v for k, v in assignments.items() if v}
        
        return assignments
    
    def _present_assignment_plan(self, assignments):
        """Present the agent assignment plan"""
        print(f"\n--- AGENT ASSIGNMENT PLAN ---")
        
        total_tasks = sum(len(tasks) for tasks in assignments.values())
        print(f"Total tasks to be processed: {total_tasks}")
        
        for agent_type, tasks in assignments.items():
            if tasks:
                agent_name = agent_type.replace('_', ' ').title() + " Agent"
                print(f"\n{agent_name} ({len(tasks)} tasks):")
                for task in tasks:
                    print(f"  * {task['name']} (Priority: {task['priority']})")
        
        if not assignments:
            print("No tasks suitable for autonomous agents found.")
    
    def _confirm_launch(self):
        """Confirm launch with user"""
        print(f"\n--- LAUNCH CONFIRMATION ---")
        print("Agents will work simultaneously on assigned tasks.")
        print("Meta-agent will monitor progress and assess readiness for your review.")
        print("Estimated total work time: 2-4 hours per agent")
        
        response = input("\nLaunch autonomous agent work session? (y/N): ")
        return response.lower().startswith('y')
    
    def get_session_status(self, session_id=None):
        """Get status of active or recent sessions"""
        if session_id:
            print(f"Getting status for session {session_id}...")
        else:
            print("Getting status of all recent sessions...")
        
        # This would show active sessions and progress
        print("Session status functionality available in meta-agent.")

if __name__ == "__main__":
    import sys
    
    launcher = AgentWorkLauncher()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        session_id = sys.argv[2] if len(sys.argv) > 2 else None
        launcher.get_session_status(session_id)
    else:
        launcher.launch_autonomous_work_session()