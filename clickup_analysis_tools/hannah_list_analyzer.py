import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class HannahListAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('CLICKUP_API_KEY')
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
    
    def get_hannah_list_tasks(self):
        """Get all tasks from Hannah's list in current-staff space"""
        try:
            # Get the current-staff space ID (we know it's 90113722087 from earlier)
            space_id = "90113722087"
            
            # Get folders in current-staff space
            folders_response = requests.get(f"{self.base_url}/space/{space_id}/folder", headers=self.headers)
            folders = folders_response.json().get('folders', [])
            
            # Also check for folderless lists
            folderless_response = requests.get(f"{self.base_url}/space/{space_id}/list", headers=self.headers)
            folderless_lists = folderless_response.json().get('lists', [])
            
            hannah_list_id = None
            
            # Check folderless lists first
            for list_item in folderless_lists:
                if list_item['name'].lower() == 'hannah':
                    hannah_list_id = list_item['id']
                    print(f"Found Hannah list (folderless): {list_item['name']} (ID: {hannah_list_id})")
                    break
            
            # If not found, check folders
            if not hannah_list_id:
                for folder in folders:
                    folder_id = folder['id']
                    lists_response = requests.get(f"{self.base_url}/folder/{folder_id}/list", headers=self.headers)
                    lists = lists_response.json().get('lists', [])
                    
                    for list_item in lists:
                        if list_item['name'].lower() == 'hannah':
                            hannah_list_id = list_item['id']
                            print(f"Found Hannah list in folder '{folder['name']}': {list_item['name']} (ID: {hannah_list_id})")
                            break
                    
                    if hannah_list_id:
                        break
            
            if not hannah_list_id:
                print("Hannah list not found in current-staff space")
                return []
            
            # Get tasks from Hannah's list
            tasks_response = requests.get(f"{self.base_url}/list/{hannah_list_id}/task", headers=self.headers)
            if tasks_response.status_code != 200:
                print(f"Error getting tasks: {tasks_response.status_code}")
                return []
            
            tasks = tasks_response.json().get('tasks', [])
            print(f"Found {len(tasks)} tasks in Hannah's list")
            
            return tasks
            
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def categorize_tasks_for_automation(self, tasks):
        """Categorize Hannah's tasks by automation potential"""
        categories = {
            'high_automation': {
                'description': 'Tasks that can be fully automated',
                'keywords': ['schedule', 'calendar', 'book', 'update', 'input', 'data', 'check status', 'monitor', 'track'],
                'tasks': []
            },
            'medium_automation': {
                'description': 'Tasks that can be partially automated with human oversight',
                'keywords': ['email', 'respond', 'follow up', 'research', 'find', 'draft', 'review'],
                'tasks': []
            },
            'low_automation': {
                'description': 'Tasks requiring human judgment and creativity',
                'keywords': ['negotiate', 'creative', 'strategy', 'decision', 'complex analysis'],
                'tasks': []
            },
            'human_only': {
                'description': 'Tasks requiring personal touch or sensitive handling',
                'keywords': ['personal', 'confidential', 'sensitive', 'relationship'],
                'tasks': []
            }
        }
        
        for task in tasks:
            task_text = (task['name'] + ' ' + task.get('description', '')).lower()
            categorized = False
            
            for category, info in categories.items():
                if any(keyword in task_text for keyword in info['keywords']):
                    info['tasks'].append(task)
                    categorized = True
                    break
            
            # Default to medium automation if no specific keywords found
            if not categorized:
                categories['medium_automation']['tasks'].append(task)
        
        return categories
    
    def suggest_specialized_agents(self, tasks):
        """Suggest specific agent types based on Hannah's task patterns"""
        agent_types = {
            'Calendar & Scheduling Agent': {
                'keywords': ['schedule', 'calendar', 'meeting', 'appointment', 'book', 'time'],
                'capabilities': ['Schedule meetings', 'Manage calendar conflicts', 'Send meeting reminders', 'Book appointments'],
                'tasks': []
            },
            'Email Management Agent': {
                'keywords': ['email', 'respond', 'reply', 'follow up', 'message', 'contact'],
                'capabilities': ['Draft email responses', 'Schedule follow-ups', 'Sort and prioritize emails', 'Template responses'],
                'tasks': []
            },
            'Research & Information Agent': {
                'keywords': ['research', 'find', 'search', 'lookup', 'investigate', 'gather'],
                'capabilities': ['Web research', 'Data gathering', 'Report compilation', 'Fact checking'],
                'tasks': []
            },
            'Data Management Agent': {
                'keywords': ['update', 'input', 'enter', 'database', 'spreadsheet', 'crm'],
                'capabilities': ['Data entry', 'Database updates', 'Report generation', 'Data validation'],
                'tasks': []
            },
            'Task Coordination Agent': {
                'keywords': ['coordinate', 'organize', 'manage', 'track', 'monitor', 'status'],
                'capabilities': ['Project tracking', 'Status updates', 'Deadline monitoring', 'Task delegation'],
                'tasks': []
            },
            'Document Management Agent': {
                'keywords': ['document', 'file', 'organize', 'archive', 'prepare', 'format'],
                'capabilities': ['Document organization', 'File management', 'Template creation', 'Format standardization'],
                'tasks': []
            }
        }
        
        for task in tasks:
            task_text = (task['name'] + ' ' + task.get('description', '')).lower()
            
            for agent_name, agent_info in agent_types.items():
                if any(keyword in task_text for keyword in agent_info['keywords']):
                    agent_info['tasks'].append(task)
        
        return agent_types

if __name__ == "__main__":
    analyzer = HannahListAnalyzer()
    
    print("Getting tasks from Hannah's list...")
    tasks = analyzer.get_hannah_list_tasks()
    
    if not tasks:
        print("No tasks found in Hannah's list")
        exit()
    
    print(f"\nAnalyzing {len(tasks)} tasks...")
    
    # Show all tasks first
    print("\n" + "="*50)
    print("ALL TASKS IN HANNAH'S LIST")
    print("="*50)
    
    for i, task in enumerate(tasks, 1):
        status = task['status']['status']
        assignees = [a.get('username', a.get('name', 'Unknown')) for a in task.get('assignees', [])]
        assignee_str = ', '.join(assignees) if assignees else 'Unassigned'
        
        print(f"{i}. {task['name']}")
        print(f"   Status: {status} | Assignee: {assignee_str}")
        if task.get('description'):
            try:
                print(f"   Description: {task['description'][:100]}...")
            except UnicodeEncodeError:
                print(f"   Description: [Contains special characters - {len(task['description'])} chars]")
        print()
    
    # Categorize by automation potential
    categories = analyzer.categorize_tasks_for_automation(tasks)
    
    print("\n" + "="*50)
    print("AUTOMATION POTENTIAL ANALYSIS")
    print("="*50)
    
    for category, info in categories.items():
        if info['tasks']:
            print(f"\n{category.upper().replace('_', ' ')} ({len(info['tasks'])} tasks)")
            print(f"Description: {info['description']}")
            for task in info['tasks']:
                print(f"  - {task['name']}")
    
    # Suggest specialized agents
    agents = analyzer.suggest_specialized_agents(tasks)
    
    print("\n" + "="*50)
    print("SPECIALIZED AGENT RECOMMENDATIONS")
    print("="*50)
    
    for agent_name, agent_info in agents.items():
        if agent_info['tasks']:
            print(f"\n{agent_name} ({len(agent_info['tasks'])} suitable tasks)")
            print("Capabilities:")
            for capability in agent_info['capabilities']:
                print(f"  • {capability}")
            print("Matching tasks:")
            for task in agent_info['tasks']:
                print(f"  - {task['name']}")
    
    # Save analysis
    analysis = {
        'total_tasks': len(tasks),
        'automation_categories': {k: len(v['tasks']) for k, v in categories.items()},
        'agent_recommendations': {k: len(v['tasks']) for k, v in agents.items() if v['tasks']},
        'detailed_analysis': {
            'categories': categories,
            'agents': agents,
            'all_tasks': tasks
        }
    }
    
    with open('hannah_list_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    print(f"\nDetailed analysis saved to hannah_list_analysis.json")