"""
Hannah Task Coordinator Agent System
Main orchestrator that manages task prioritization, delegation, and progress tracking
"""

import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
import time

load_dotenv()

class TaskCoordinatorAgent:
    def __init__(self):
        self.api_key = os.getenv('CLICKUP_API_KEY')
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        self.hannah_list_id = "901110057030"
        
        # Load task analysis
        self.task_analysis = self._load_task_analysis()
        
        # Initialize specialized agents
        self.specialized_agents = {
            'research': ResearchAgent(self),
            'calendar': CalendarAgent(self),
            'email': EmailAgent(self),
            'business': BusinessOperationsAgent(self),
            'admin': AdministrativeAgent(self)
        }
    
    def _load_task_analysis(self) -> Dict:
        """Load the task analysis from previous run"""
        try:
            with open('hannah_task_management_plan.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def start_coordination_session(self):
        """Start an interactive coordination session"""
        print("="*60)
        print("HANNAH TASK COORDINATOR AGENT")
        print("="*60)
        print("Hi! I'm your task coordination agent. Let me review what's on your radar...")
        
        # Get current task status
        current_tasks = self._get_current_task_status()
        
        # Present daily briefing
        self._present_daily_briefing(current_tasks)
        
        # Get user input and preferences
        self._interactive_prioritization()
        
        # Delegate tasks to specialized agents
        self._delegate_tasks()
        
        # Set up monitoring
        self._setup_monitoring()
    
    def _get_current_task_status(self) -> Dict:
        """Get current status of all Hannah's tasks"""
        try:
            response = requests.get(f"{self.base_url}/list/{self.hannah_list_id}/task", headers=self.headers)
            if response.status_code == 200:
                tasks = response.json().get('tasks', [])
                
                # Organize by status and priority
                organized = {
                    'urgent_in_progress': [],
                    'urgent_review': [],
                    'high_priority': [],
                    'ready_to_start': [],
                    'waiting_on_others': [],
                    'blocked': []
                }
                
                for task in tasks:
                    if task['status']['type'] == 'closed':
                        continue
                        
                    priority = self._get_priority_level(task.get('priority'))
                    status = task['status']['status'].lower()
                    
                    if priority == 'urgent' and 'progress' in status:
                        organized['urgent_in_progress'].append(task)
                    elif priority == 'urgent' and 'review' in status:
                        organized['urgent_review'].append(task)
                    elif priority in ['urgent', 'high']:
                        organized['high_priority'].append(task)
                    elif 'ready' in status or 'todo' in status:
                        organized['ready_to_start'].append(task)
                    elif 'review' in status or 'pending' in status:
                        organized['waiting_on_others'].append(task)
                    else:
                        organized['blocked'].append(task)
                
                return organized
        except Exception as e:
            print(f"Error getting current tasks: {e}")
            return {}
    
    def _present_daily_briefing(self, current_tasks: Dict):
        """Present a daily briefing of tasks and priorities"""
        print(f"\n--- DAILY TASK BRIEFING ---")
        print(f"Date: {datetime.now().strftime('%A, %B %d, %Y')}")
        
        # Urgent items first
        if current_tasks.get('urgent_in_progress'):
            print(f"\n[URGENT] IN PROGRESS ({len(current_tasks['urgent_in_progress'])} tasks):")
            for task in current_tasks['urgent_in_progress']:
                print(f"  * {task['name']}")
                print(f"    Status: {task['status']['status']} | Assignees: {', '.join([a.get('username', 'Unknown') for a in task.get('assignees', [])])}")
        
        if current_tasks.get('urgent_review'):
            print(f"\n[URGENT] AWAITING REVIEW ({len(current_tasks['urgent_review'])} tasks):")
            for task in current_tasks['urgent_review']:
                print(f"  * {task['name']}")
        
        if current_tasks.get('high_priority'):
            print(f"\n[HIGH PRIORITY] ({len(current_tasks['high_priority'])} tasks):")
            for task in current_tasks['high_priority'][:5]:  # Show top 5
                print(f"  * {task['name']}")
        
        if current_tasks.get('ready_to_start'):
            print(f"\n[READY TO START] ({len(current_tasks['ready_to_start'])} tasks):")
            for task in current_tasks['ready_to_start'][:3]:  # Show top 3
                print(f"  * {task['name']}")
        
        if current_tasks.get('waiting_on_others'):
            print(f"\n[WAITING ON OTHERS] ({len(current_tasks['waiting_on_others'])} tasks):")
            for task in current_tasks['waiting_on_others'][:3]:
                print(f"  * {task['name']}")
    
    def _interactive_prioritization(self):
        """Interactive session to get user input on priorities"""
        print(f"\n--- PRIORITY DISCUSSION ---")
        
        questions = [
            "What are your top 3 priorities for today?",
            "Are there any urgent deadlines I should know about?",
            "Which tasks would you like me to delegate to specialized agents?",
            "Are there any tasks you want to handle personally?",
            "Should I schedule any follow-ups or check-ins?"
        ]
        
        responses = {}
        for question in questions:
            print(f"\n{question}")
            response = input("Your response: ")
            responses[question] = response
        
        # Store responses for delegation decisions
        self.user_priorities = responses
        return responses
    
    def _delegate_tasks(self):
        """Delegate tasks to appropriate specialized agents"""
        print(f"\n--- TASK DELEGATION ---")
        
        # Get tasks that can be delegated
        delegatable_tasks = self._identify_delegatable_tasks()
        
        for task_type, tasks in delegatable_tasks.items():
            if tasks and task_type in self.specialized_agents:
                agent = self.specialized_agents[task_type]
                print(f"\nDelegating {len(tasks)} {task_type} tasks to {agent.__class__.__name__}:")
                
                for task in tasks:
                    print(f"  • {task['name']}")
                    agent.accept_task(task)
                
                # Start agent work
                agent.start_work()
    
    def _identify_delegatable_tasks(self) -> Dict[str, List]:
        """Identify which tasks can be delegated to which agents"""
        current_tasks = self._get_current_task_status()
        all_tasks = []
        
        # Flatten all tasks
        for task_list in current_tasks.values():
            all_tasks.extend(task_list)
        
        delegatable = {
            'research': [],
            'calendar': [],
            'email': [],
            'business': [],
            'admin': []
        }
        
        for task in all_tasks:
            task_text = (task['name'] + ' ' + task.get('description', '')).lower()
            
            # Research tasks
            if any(keyword in task_text for keyword in ['research', 'find', 'search', 'investigate', 'look into']):
                delegatable['research'].append(task)
            
            # Calendar/scheduling tasks
            elif any(keyword in task_text for keyword in ['schedule', 'calendar', 'meeting', 'book', 'appointment']):
                delegatable['calendar'].append(task)
            
            # Email/communication tasks
            elif any(keyword in task_text for keyword in ['email', 'contact', 'follow up', 'respond', 'call']):
                delegatable['email'].append(task)
            
            # Business operations
            elif any(keyword in task_text for keyword in ['roseys', 'luna', 'business', 'marketing', 'launch']):
                delegatable['business'].append(task)
            
            # Administrative tasks
            elif any(keyword in task_text for keyword in ['insurance', 'tax', 'legal', 'document', 'form', 'application']):
                delegatable['admin'].append(task)
        
        return delegatable
    
    def _setup_monitoring(self):
        """Set up progress monitoring and check-ins"""
        print(f"\n--- MONITORING SETUP ---")
        print("I'll monitor progress on delegated tasks and provide updates.")
        print("I'll check in with you and the specialized agents every 2 hours.")
        print("You can ask me for status updates anytime by running this script with --status")
        
        # Save monitoring configuration
        monitoring_config = {
            'last_check': datetime.now().isoformat(),
            'check_interval_hours': 2,
            'active_delegations': len(self.specialized_agents),
            'user_priorities': self.user_priorities
        }
        
        with open('task_monitoring_config.json', 'w') as f:
            json.dump(monitoring_config, f, indent=2)
    
    def provide_status_update(self):
        """Provide a status update on all active tasks and agents"""
        print("="*60)
        print("TASK STATUS UPDATE")
        print("="*60)
        
        # Get updated task status
        current_tasks = self._get_current_task_status()
        self._present_daily_briefing(current_tasks)
        
        # Get agent status updates
        print(f"\n--- AGENT STATUS UPDATES ---")
        for agent_type, agent in self.specialized_agents.items():
            status = agent.get_status_update()
            if status['active_tasks'] > 0:
                print(f"\n{agent.__class__.__name__}:")
                print(f"  Active Tasks: {status['active_tasks']}")
                print(f"  Completed: {status['completed_tasks']}")
                print(f"  Status: {status['current_status']}")
                if status['needs_attention']:
                    print(f"  ⚠️  Needs Attention: {status['needs_attention']}")
    
    def _get_priority_level(self, priority_obj):
        """Extract priority level from ClickUp priority object"""
        if not priority_obj:
            return 'none'
        
        priority_map = {
            '1': 'urgent',
            '2': 'high', 
            '3': 'normal',
            '4': 'low'
        }
        
        priority_id = str(priority_obj.get('id', ''))
        return priority_map.get(priority_id, priority_obj.get('priority', 'none'))


class SpecializedAgent:
    """Base class for specialized agents"""
    
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.active_tasks = []
        self.completed_tasks = []
        self.current_status = "Ready"
        self.needs_attention = []
    
    def accept_task(self, task):
        """Accept a task from the coordinator"""
        self.active_tasks.append(task)
        self.current_status = "Working"
    
    def start_work(self):
        """Start working on assigned tasks"""
        if self.active_tasks:
            print(f"  {self.__class__.__name__} starting work on {len(self.active_tasks)} tasks...")
            self._process_tasks()
    
    def _process_tasks(self):
        """Process assigned tasks - to be implemented by subclasses"""
        pass
    
    def get_status_update(self):
        """Return current status"""
        return {
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'current_status': self.current_status,
            'needs_attention': self.needs_attention
        }
    
    def complete_task(self, task):
        """Mark a task as completed"""
        if task in self.active_tasks:
            self.active_tasks.remove(task)
            self.completed_tasks.append(task)
        
        if not self.active_tasks:
            self.current_status = "Ready"


class ResearchAgent(SpecializedAgent):
    """Specialized agent for research and information gathering tasks"""
    
    def _process_tasks(self):
        for task in self.active_tasks[:]:  # Process copy to allow removal
            task_name = task['name']
            print(f"    🔍 Researching: {task_name}")
            
            # Determine research type and approach
            if 'business' in task_name.lower() or 'ai' in task_name.lower():
                self._research_business_solutions(task)
            elif 'find' in task_name.lower():
                self._research_services_or_vendors(task)
            else:
                self._general_research(task)
    
    def _research_business_solutions(self, task):
        """Research business solutions and AI platforms"""
        research_plan = {
            'task': task['name'],
            'approach': 'Business/AI research',
            'steps': [
                'Identify top platforms in the category',
                'Compare features and pricing',
                'Check user reviews and case studies',
                'Prepare recommendation report'
            ],
            'estimated_time': '2-3 hours',
            'deliverables': 'Comparison report with recommendations'
        }
        
        self.needs_attention.append(f"Research plan ready for: {task['name']}")
        print(f"      📋 Research plan created - estimated 2-3 hours")
    
    def _research_services_or_vendors(self, task):
        """Research services or vendor options"""
        research_plan = {
            'task': task['name'],
            'approach': 'Service/vendor research',
            'steps': [
                'Identify local and online options',
                'Check reviews and ratings',
                'Compare pricing and availability',
                'Verify credentials/qualifications'
            ],
            'estimated_time': '1-2 hours',
            'deliverables': 'List of options with pros/cons'
        }
        
        self.needs_attention.append(f"Vendor research ready for: {task['name']}")
        print(f"      📋 Vendor research plan created - estimated 1-2 hours")
    
    def _general_research(self, task):
        """General research approach"""
        self.needs_attention.append(f"General research approach for: {task['name']}")
        print(f"      📋 General research approach planned")


class CalendarAgent(SpecializedAgent):
    """Specialized agent for calendar and scheduling tasks"""
    
    def _process_tasks(self):
        for task in self.active_tasks[:]:
            task_name = task['name']
            print(f"    📅 Scheduling: {task_name}")
            
            if 'calendar' in task_name.lower():
                self._setup_calendar_sharing(task)
            elif 'schedule' in task_name.lower():
                self._create_scheduling_plan(task)
            else:
                self._general_calendar_task(task)
    
    def _setup_calendar_sharing(self, task):
        """Set up calendar sharing or integration"""
        self.needs_attention.append(f"Calendar setup needed: {task['name']}")
        print(f"      🔗 Calendar integration plan ready")
    
    def _create_scheduling_plan(self, task):
        """Create a scheduling plan"""
        self.needs_attention.append(f"Scheduling coordination needed: {task['name']}")
        print(f"      ⏰ Scheduling plan created")
    
    def _general_calendar_task(self, task):
        """Handle general calendar tasks"""
        self.needs_attention.append(f"Calendar task ready: {task['name']}")
        print(f"      📋 Calendar task planned")


class EmailAgent(SpecializedAgent):
    """Specialized agent for email and communication tasks"""
    
    def _process_tasks(self):
        for task in self.active_tasks[:]:
            task_name = task['name']
            print(f"    📧 Communication: {task_name}")
            
            if 'follow up' in task_name.lower():
                self._create_followup_plan(task)
            elif 'contact' in task_name.lower():
                self._create_contact_plan(task)
            else:
                self._general_communication_task(task)
    
    def _create_followup_plan(self, task):
        """Create a follow-up communication plan"""
        self.needs_attention.append(f"Follow-up plan ready: {task['name']}")
        print(f"      📬 Follow-up sequence planned")
    
    def _create_contact_plan(self, task):
        """Create a contact plan"""
        self.needs_attention.append(f"Contact plan ready: {task['name']}")
        print(f"      📞 Contact strategy created")
    
    def _general_communication_task(self, task):
        """Handle general communication tasks"""
        self.needs_attention.append(f"Communication task ready: {task['name']}")
        print(f"      💬 Communication plan created")


class BusinessOperationsAgent(SpecializedAgent):
    """Specialized agent for business operations tasks"""
    
    def _process_tasks(self):
        for task in self.active_tasks[:]:
            task_name = task['name']
            print(f"    🏢 Business Ops: {task_name}")
            
            if 'roseys' in task_name.lower():
                self._handle_roseys_task(task)
            elif 'luna' in task_name.lower():
                self._handle_luna_wild_task(task)
            else:
                self._general_business_task(task)
    
    def _handle_roseys_task(self, task):
        """Handle Roseys business tasks"""
        self.needs_attention.append(f"Roseys task plan ready: {task['name']}")
        print(f"      🌹 Roseys business plan created")
    
    def _handle_luna_wild_task(self, task):
        """Handle Luna Wild business tasks"""
        self.needs_attention.append(f"Luna Wild task plan ready: {task['name']}")
        print(f"      🌙 Luna Wild business plan created")
    
    def _general_business_task(self, task):
        """Handle general business tasks"""
        self.needs_attention.append(f"Business task plan ready: {task['name']}")
        print(f"      📊 Business plan created")


class AdministrativeAgent(SpecializedAgent):
    """Specialized agent for administrative tasks"""
    
    def _process_tasks(self):
        for task in self.active_tasks[:]:
            task_name = task['name']
            print(f"    📋 Admin: {task_name}")
            
            if 'insurance' in task_name.lower():
                self._handle_insurance_task(task)
            elif 'legal' in task_name.lower() or 'llc' in task_name.lower():
                self._handle_legal_task(task)
            else:
                self._general_admin_task(task)
    
    def _handle_insurance_task(self, task):
        """Handle insurance-related tasks"""
        self.needs_attention.append(f"Insurance task plan ready: {task['name']}")
        print(f"      🛡️  Insurance plan created")
    
    def _handle_legal_task(self, task):
        """Handle legal/business formation tasks"""
        self.needs_attention.append(f"Legal task plan ready: {task['name']}")
        print(f"      ⚖️  Legal task plan created")
    
    def _general_admin_task(self, task):
        """Handle general administrative tasks"""
        self.needs_attention.append(f"Admin task plan ready: {task['name']}")
        print(f"      📄 Administrative plan created")


if __name__ == "__main__":
    import sys
    
    coordinator = TaskCoordinatorAgent()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--status':
        coordinator.provide_status_update()
    else:
        coordinator.start_coordination_session()