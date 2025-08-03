import requests
import json
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

class HannahTaskAnalyzer:
    def __init__(self):
        self.api_key = os.getenv('CLICKUP_API_KEY')
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
    
    def search_hannah_tasks(self):
        """Search for all tasks assigned to or mentioning Hannah"""
        all_tasks = []
        
        try:
            # Get all teams
            teams_response = requests.get(f"{self.base_url}/team", headers=self.headers)
            teams = teams_response.json()['teams']
            
            for team in teams:
                team_id = team['id']
                print(f"Searching team: {team['name']}")
                
                # Get all spaces
                spaces_response = requests.get(f"{self.base_url}/team/{team_id}/space", headers=self.headers)
                if spaces_response.status_code != 200:
                    continue
                    
                spaces = spaces_response.json()['spaces']
                
                for space in spaces:
                    space_id = space['id']
                    print(f"  Searching space: {space['name']}")
                    
                    # Search tasks in this space with Hannah keyword
                    search_params = {
                        'space_ids': [space_id],
                        'query': 'Hannah'
                    }
                    
                    search_response = requests.get(
                        f"{self.base_url}/team/{team_id}/task/search",
                        headers=self.headers,
                        params=search_params
                    )
                    
                    if search_response.status_code == 200:
                        search_results = search_response.json()
                        if 'tasks' in search_results:
                            for task in search_results['tasks']:
                                task['space_name'] = space['name']
                                all_tasks.append(task)
                    
                    # Also get all tasks to check assignees
                    folders_response = requests.get(f"{self.base_url}/space/{space_id}/folder", headers=self.headers)
                    if folders_response.status_code == 200:
                        folders = folders_response.json()['folders']
                        
                        for folder in folders:
                            folder_id = folder['id']
                            lists_response = requests.get(f"{self.base_url}/folder/{folder_id}/list", headers=self.headers)
                            
                            if lists_response.status_code == 200:
                                lists = lists_response.json()['lists']
                                
                                for list_item in lists:
                                    list_id = list_item['id']
                                    tasks_response = requests.get(f"{self.base_url}/list/{list_id}/task", headers=self.headers)
                                    
                                    if tasks_response.status_code == 200:
                                        tasks = tasks_response.json()['tasks']
                                        
                                        for task in tasks:
                                            # Check if Hannah is mentioned in task name, description, or assignees
                                            hannah_related = False
                                            
                                            if 'hannah' in task['name'].lower():
                                                hannah_related = True
                                            
                                            if task.get('description') and 'hannah' in task['description'].lower():
                                                hannah_related = True
                                            
                                            if task.get('assignees'):
                                                for assignee in task['assignees']:
                                                    if 'hannah' in assignee.get('username', '').lower() or 'hannah' in assignee.get('name', '').lower():
                                                        hannah_related = True
                                            
                                            if hannah_related:
                                                task['space_name'] = space['name']
                                                task['list_name'] = list_item['name']
                                                all_tasks.append(task)
        
        except Exception as e:
            print(f"Error searching tasks: {e}")
        
        return all_tasks
    
    def categorize_tasks(self, tasks):
        """Categorize tasks by type for agent vs human analysis"""
        categories = {
            'data_entry': [],
            'scheduling': [],
            'research': [],
            'communication': [],
            'content_creation': [],
            'analysis': [],
            'administrative': [],
            'creative': [],
            'technical': [],
            'other': []
        }
        
        keywords = {
            'data_entry': ['input', 'enter', 'update', 'database', 'spreadsheet', 'form'],
            'scheduling': ['schedule', 'calendar', 'meeting', 'appointment', 'book'],
            'research': ['research', 'find', 'search', 'investigate', 'analyze'],
            'communication': ['email', 'call', 'message', 'respond', 'follow up'],
            'content_creation': ['write', 'create', 'draft', 'blog', 'content'],
            'analysis': ['analyze', 'report', 'review', 'evaluate', 'assess'],
            'administrative': ['file', 'organize', 'process', 'admin', 'paperwork'],
            'creative': ['design', 'creative', 'brainstorm', 'concept'],
            'technical': ['code', 'develop', 'bug', 'system', 'technical']
        }
        
        for task in tasks:
            task_text = (task['name'] + ' ' + task.get('description', '')).lower()
            categorized = False
            
            for category, category_keywords in keywords.items():
                if any(keyword in task_text for keyword in category_keywords):
                    categories[category].append(task)
                    categorized = True
                    break
            
            if not categorized:
                categories['other'].append(task)
        
        return categories
    
    def analyze_for_automation(self, categories):
        """Analyze which tasks can be automated vs need human intervention"""
        automation_potential = {
            'high': ['data_entry', 'scheduling', 'research', 'analysis'],
            'medium': ['communication', 'content_creation', 'administrative'],
            'low': ['creative', 'technical'],
            'human_only': []
        }
        
        recommendations = {}
        
        for category, tasks in categories.items():
            if not tasks:
                continue
                
            automation_level = 'low'
            for level, categories_list in automation_potential.items():
                if category in categories_list:
                    automation_level = level
                    break
            
            recommendations[category] = {
                'task_count': len(tasks),
                'automation_potential': automation_level,
                'tasks': tasks,
                'suggested_agents': []
            }
            
            # Suggest specific agent types
            if category == 'data_entry':
                recommendations[category]['suggested_agents'] = ['Data Input Agent', 'CRM Update Agent']
            elif category == 'scheduling':
                recommendations[category]['suggested_agents'] = ['Calendar Agent', 'Meeting Coordinator Agent']
            elif category == 'research':
                recommendations[category]['suggested_agents'] = ['Research Agent', 'Information Gathering Agent']
            elif category == 'communication':
                recommendations[category]['suggested_agents'] = ['Email Response Agent', 'Follow-up Agent']
            elif category == 'content_creation':
                recommendations[category]['suggested_agents'] = ['Content Writer Agent', 'Social Media Agent']
            elif category == 'analysis':
                recommendations[category]['suggested_agents'] = ['Data Analysis Agent', 'Report Generator Agent']
        
        return recommendations

if __name__ == "__main__":
    analyzer = HannahTaskAnalyzer()
    
    print("Searching for Hannah's tasks...")
    tasks = analyzer.search_hannah_tasks()
    print(f"Found {len(tasks)} Hannah-related tasks")
    
    print("\nCategorizing tasks...")
    categories = analyzer.categorize_tasks(tasks)
    
    print("\nAnalyzing automation potential...")
    recommendations = analyzer.analyze_for_automation(categories)
    
    # Print summary
    print("\n" + "="*50)
    print("HANNAH TASK OPTIMIZATION ANALYSIS")
    print("="*50)
    
    for category, data in recommendations.items():
        if data['task_count'] > 0:
            print(f"\n{category.upper()}: {data['task_count']} tasks")
            print(f"Automation Potential: {data['automation_potential']}")
            if data['suggested_agents']:
                print(f"Suggested Agents: {', '.join(data['suggested_agents'])}")
            
            print("Sample tasks:")
            for task in data['tasks'][:3]:  # Show first 3 tasks
                print(f"  - {task['name']} (Space: {task.get('space_name', 'Unknown')})")
    
    # Save detailed results
    with open('hannah_task_analysis.json', 'w') as f:
        json.dump({
            'total_tasks': len(tasks),
            'categories': {k: {'count': v['task_count'], 'automation': v['automation_potential'], 'agents': v['suggested_agents']} for k, v in recommendations.items()},
            'detailed_tasks': tasks
        }, f, indent=2)
    
    print(f"\nDetailed analysis saved to hannah_task_analysis.json")