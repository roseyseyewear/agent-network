import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class HannahTaskOrganizer:
    def __init__(self):
        self.api_key = os.getenv('CLICKUP_API_KEY')
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
    
    def get_hannah_tasks_detailed(self):
        """Get all tasks from Hannah's list with detailed information"""
        try:
            # Hannah's list ID from previous analysis
            list_id = "901110057030"
            
            # Get tasks with more details
            params = {
                'include_closed': 'true',  # Include completed tasks
                'include_subtasks': 'true'
            }
            
            tasks_response = requests.get(
                f"{self.base_url}/list/{list_id}/task", 
                headers=self.headers, 
                params=params
            )
            
            if tasks_response.status_code != 200:
                print(f"Error getting tasks: {tasks_response.status_code}")
                return []
            
            tasks = tasks_response.json().get('tasks', [])
            
            # Enhance each task with additional details
            enhanced_tasks = []
            for task in tasks:
                enhanced_task = {
                    'id': task['id'],
                    'name': task['name'],
                    'status': task['status']['status'],
                    'status_type': task['status']['type'],  # 'open', 'closed', 'custom'
                    'priority': self._get_priority_level(task.get('priority')),
                    'assignees': [a.get('username', a.get('name', 'Unknown')) for a in task.get('assignees', [])],
                    'description': task.get('description', ''),
                    'date_created': task.get('date_created'),
                    'date_updated': task.get('date_updated'),
                    'date_closed': task.get('date_closed'),
                    'due_date': task.get('due_date'),
                    'url': task.get('url', ''),
                    'tags': [tag['name'] for tag in task.get('tags', [])],
                    'time_estimate': task.get('time_estimate'),
                    'time_spent': task.get('time_spent'),
                    'is_completed': task['status']['type'] == 'closed'
                }
                enhanced_tasks.append(enhanced_task)
            
            return enhanced_tasks
            
        except Exception as e:
            print(f"Error: {e}")
            return []
    
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
    
    def organize_tasks_by_status(self, tasks):
        """Organize tasks by completion status and active status"""
        organization = {
            'completed_tasks': [],
            'active_tasks': {
                'in_progress': [],
                'ready_for_work': [],
                'review': [],
                'backlog': [],
                'pending': [],
                'other_active': []
            },
            'blocked_or_waiting': []
        }
        
        for task in tasks:
            if task['is_completed']:
                organization['completed_tasks'].append(task)
            else:
                status = task['status'].lower().replace(' ', '_')
                
                if status in organization['active_tasks']:
                    organization['active_tasks'][status].append(task)
                else:
                    # Handle custom statuses
                    if 'progress' in status or 'working' in status:
                        organization['active_tasks']['in_progress'].append(task)
                    elif 'ready' in status or 'todo' in status:
                        organization['active_tasks']['ready_for_work'].append(task)
                    elif 'review' in status or 'waiting' in status:
                        organization['active_tasks']['review'].append(task)
                    elif 'backlog' in status:
                        organization['active_tasks']['backlog'].append(task)
                    elif 'pending' in status:
                        organization['active_tasks']['pending'].append(task)
                    else:
                        organization['active_tasks']['other_active'].append(task)
        
        return organization
    
    def prioritize_active_tasks(self, active_tasks):
        """Prioritize active tasks by urgency and importance"""
        priority_order = {'urgent': 1, 'high': 2, 'normal': 3, 'low': 4, 'none': 5}
        status_urgency = {
            'in_progress': 1,      # Highest - already started
            'review': 2,           # High - waiting for review
            'ready_for_work': 3,   # Medium - ready to start
            'pending': 4,          # Lower - waiting on something
            'backlog': 5,          # Lowest - future work
            'other_active': 3      # Medium - unknown status
        }
        
        prioritized = {}
        
        for status, tasks in active_tasks.items():
            if isinstance(tasks, list):  # Handle case where tasks is already a list
                task_list = tasks
            else:
                task_list = tasks.get('tasks', tasks)
            
            # Sort tasks within each status by priority, then by creation date
            sorted_tasks = sorted(task_list, key=lambda x: (
                priority_order.get(x['priority'], 5),
                x['date_created'] or '0'
            ))
            
            prioritized[status] = {
                'urgency_level': status_urgency.get(status, 3),
                'task_count': len(sorted_tasks),
                'tasks': sorted_tasks
            }
        
        return prioritized
    
    def analyze_task_patterns(self, tasks):
        """Analyze patterns in Hannah's tasks for agent optimization"""
        patterns = {
            'recurring_themes': {},
            'common_assignees': {},
            'priority_distribution': {'urgent': 0, 'high': 0, 'normal': 0, 'low': 0, 'none': 0},
            'status_trends': {},
            'time_analysis': {
                'avg_time_to_complete': None,
                'tasks_with_estimates': 0,
                'estimated_vs_actual': []
            }
        }
        
        # Analyze themes in task names
        for task in tasks:
            words = task['name'].lower().split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    patterns['recurring_themes'][word] = patterns['recurring_themes'].get(word, 0) + 1
        
        # Priority distribution
        for task in tasks:
            priority = task['priority']
            patterns['priority_distribution'][priority] += 1
        
        # Status distribution
        for task in tasks:
            status = task['status']
            patterns['status_trends'][status] = patterns['status_trends'].get(status, 0) + 1
        
        # Common assignees
        for task in tasks:
            for assignee in task['assignees']:
                patterns['common_assignees'][assignee] = patterns['common_assignees'].get(assignee, 0) + 1
        
        return patterns
    
    def create_agent_management_structure(self, organized_tasks, patterns):
        """Create a structure for an agent to manage Hannah's tasks"""
        # Calculate totals safely
        active_task_count = sum(len(tasks) if isinstance(tasks, list) else len(tasks.get('tasks', [])) for tasks in organized_tasks['active_tasks'].values())
        completed_task_count = len(organized_tasks['completed_tasks'])
        total_tasks = active_task_count + completed_task_count
        
        agent_structure = {
            'task_summary': {
                'total_tasks': total_tasks,
                'active_tasks': active_task_count,
                'completed_tasks': completed_task_count,
                'completion_rate': (completed_task_count / total_tasks * 100) if total_tasks > 0 else 0
            },
            'priority_actions': {
                'immediate_attention': [],
                'this_week': [],
                'next_week': [],
                'future': []
            },
            'agent_recommendations': {
                'task_delegation': {},
                'automation_opportunities': {},
                'workflow_improvements': []
            }
        }
        
        # Identify priority actions from prioritized data
        status_urgency = {
            'in_progress': 1,
            'review': 2,
            'ready_for_work': 3,
            'pending': 4,
            'backlog': 5,
            'other_active': 3
        }
        
        for status, task_list in organized_tasks['active_tasks'].items():
            urgency = status_urgency.get(status, 3)
            if urgency <= 2:  # High urgency
                tasks_to_process = task_list[:3] if len(task_list) > 3 else task_list  # Top 3 tasks
                for task in tasks_to_process:
                    agent_structure['priority_actions']['immediate_attention'].append({
                        'task': task['name'],
                        'status': task['status'],
                        'priority': task['priority'],
                        'assignees': task['assignees'],
                        'action_needed': self._suggest_action(task, status)
                    })
        
        # Suggest task delegation based on patterns
        for theme, count in sorted(patterns['recurring_themes'].items(), key=lambda x: x[1], reverse=True)[:5]:
            if count >= 3:  # Theme appears in 3+ tasks
                agent_structure['agent_recommendations']['task_delegation'][theme] = {
                    'frequency': count,
                    'suggested_agent': self._suggest_agent_type(theme),
                    'automation_potential': self._assess_automation_potential(theme)
                }
        
        return agent_structure
    
    def _suggest_action(self, task, status):
        """Suggest specific action based on task and status"""
        if status == 'review':
            return 'Follow up on review status'
        elif status == 'in_progress':
            return 'Check progress and provide support'
        elif status == 'ready_for_work':
            return 'Begin work or assign to appropriate agent'
        elif status == 'pending':
            return 'Identify and resolve blocking dependencies'
        else:
            return 'Evaluate and prioritize'
    
    def _suggest_agent_type(self, theme):
        """Suggest agent type based on task theme"""
        agent_mapping = {
            'research': 'Research & Information Agent',
            'find': 'Research & Information Agent',
            'schedule': 'Calendar & Scheduling Agent',
            'calendar': 'Calendar & Scheduling Agent',
            'email': 'Email Management Agent',
            'follow': 'Email Management Agent',
            'roseys': 'Business Operations Agent',
            'luna': 'Business Operations Agent',
            'plan': 'Project Planning Agent',
            'report': 'Data & Reporting Agent'
        }
        return agent_mapping.get(theme, 'General Assistant Agent')
    
    def _assess_automation_potential(self, theme):
        """Assess automation potential for a theme"""
        high_automation = ['schedule', 'calendar', 'track', 'monitor', 'update', 'report']
        medium_automation = ['research', 'find', 'email', 'follow']
        
        if theme in high_automation:
            return 'High'
        elif theme in medium_automation:
            return 'Medium'
        else:
            return 'Low'

if __name__ == "__main__":
    organizer = HannahTaskOrganizer()
    
    print("Getting detailed task information...")
    tasks = organizer.get_hannah_tasks_detailed()
    
    print(f"Found {len(tasks)} total tasks")
    
    print("\nOrganizing tasks by status...")
    organized = organizer.organize_tasks_by_status(tasks)
    
    print("\nPrioritizing active tasks...")
    prioritized_active = organizer.prioritize_active_tasks(organized['active_tasks'])
    
    print("\nAnalyzing task patterns...")
    patterns = organizer.analyze_task_patterns(tasks)
    
    print("\nCreating agent management structure...")
    agent_structure = organizer.create_agent_management_structure(organized, patterns)
    
    # Print organized summary
    print("\n" + "="*60)
    print("HANNAH'S TASK ORGANIZATION & MANAGEMENT PLAN")
    print("="*60)
    
    print(f"\nTASK SUMMARY:")
    print(f"Total Tasks: {agent_structure['task_summary']['total_tasks']}")
    print(f"Active Tasks: {agent_structure['task_summary']['active_tasks']}")
    print(f"Completed Tasks: {agent_structure['task_summary']['completed_tasks']}")
    print(f"Completion Rate: {agent_structure['task_summary']['completion_rate']:.1f}%")
    
    print(f"\nCOMPLETED TASKS ({len(organized['completed_tasks'])}):")
    for task in organized['completed_tasks']:
        print(f"  * {task['name']}")
    
    print(f"\nACTIVE TASKS BY PRIORITY & STATUS:")
    
    # Sort statuses by urgency
    sorted_statuses = sorted(prioritized_active.items(), key=lambda x: x[1]['urgency_level'])
    
    for status, data in sorted_statuses:
        if data['tasks']:
            urgency_marker = "[HIGH]" if data['urgency_level'] <= 2 else "[MED]" if data['urgency_level'] <= 3 else "[LOW]"
            print(f"\n{urgency_marker} {status.upper().replace('_', ' ')} ({data['task_count']} tasks)")
            
            for i, task in enumerate(data['tasks'], 1):
                priority_marker = "[URG]" if task['priority'] == 'urgent' else "[HI]" if task['priority'] == 'high' else "[NOR]" if task['priority'] == 'normal' else "[LO]" if task['priority'] == 'low' else "[--]"
                assignee_str = ', '.join(task['assignees']) if task['assignees'] else 'Unassigned'
                print(f"    {i}. {priority_marker} {task['name']}")
                print(f"       Assignee: {assignee_str} | Priority: {task['priority']}")
                if task['due_date']:
                    print(f"       Due: {task['due_date']}")
    
    print(f"\nIMMEDIATE ACTIONS NEEDED:")
    for action in agent_structure['priority_actions']['immediate_attention']:
        print(f"  * {action['task']} - {action['action_needed']}")
    
    print(f"\nAGENT DELEGATION RECOMMENDATIONS:")
    for theme, data in agent_structure['agent_recommendations']['task_delegation'].items():
        print(f"  * {theme.title()} tasks ({data['frequency']} instances) -> {data['suggested_agent']}")
        print(f"    Automation Potential: {data['automation_potential']}")
    
    # Save comprehensive analysis
    complete_analysis = {
        'timestamp': datetime.now().isoformat(),
        'task_organization': {
            'completed': organized['completed_tasks'],
            'active_by_status': organized['active_tasks'],
            'prioritized_active': prioritized_active
        },
        'patterns': patterns,
        'agent_structure': agent_structure,
        'management_recommendations': {
            'focus_areas': list(agent_structure['agent_recommendations']['task_delegation'].keys()),
            'urgent_tasks': len(agent_structure['priority_actions']['immediate_attention']),
            'completion_rate': agent_structure['task_summary']['completion_rate']
        }
    }
    
    with open('hannah_task_management_plan.json', 'w') as f:
        json.dump(complete_analysis, f, indent=2, default=str)
    
    print(f"\nComplete analysis saved to hannah_task_management_plan.json")