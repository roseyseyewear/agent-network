import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClickUpManager:
    def __init__(self):
        self.api_key = os.getenv('CLICKUP_API_KEY')
        self.workspace_id = os.getenv('CLICKUP_WORKSPACE_ID')
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
    
    def test_connection(self):
        """Test API connection and get workspace info"""
        try:
            response = requests.get(f"{self.base_url}/team", headers=self.headers)
            if response.status_code == 200:
                teams = response.json()['teams']
                print(f"Connected to ClickUp successfully!")
                for team in teams:
                    print(f"  Team: {team['name']} (ID: {team['id']})")
                return True
            else:
                print(f"Connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error connecting to ClickUp: {e}")
            return False
    
    def get_spaces(self, team_id):
        """Get all spaces in a team"""
        try:
            response = requests.get(f"{self.base_url}/team/{team_id}/space", headers=self.headers)
            if response.status_code == 200:
                return response.json()['spaces']
            return []
        except Exception as e:
            print(f"Error getting spaces: {e}")
            return []
    
    def get_tasks(self, list_id=None, assignee=None, status=None):
        """Get tasks from ClickUp"""
        try:
            # If no list_id provided, get from first available list
            if not list_id:
                teams = requests.get(f"{self.base_url}/team", headers=self.headers).json()['teams']
                team_id = teams[0]['id']
                spaces = self.get_spaces(team_id)
                if spaces:
                    folders = requests.get(f"{self.base_url}/space/{spaces[0]['id']}/folder", headers=self.headers).json()['folders']
                    if folders:
                        lists = requests.get(f"{self.base_url}/folder/{folders[0]['id']}/list", headers=self.headers).json()['lists']
                        if lists:
                            list_id = lists[0]['id']
            
            if list_id:
                params = {}
                if assignee:
                    params['assignees[]'] = assignee
                if status:
                    params['statuses[]'] = status
                
                response = requests.get(f"{self.base_url}/list/{list_id}/task", 
                                      headers=self.headers, params=params)
                if response.status_code == 200:
                    return response.json()['tasks']
            return []
        except Exception as e:
            print(f"Error getting tasks: {e}")
            return []
    
    def create_task(self, list_id, name, description="", assignee=None, priority=None):
        """Create a new task"""
        try:
            data = {
                "name": name,
                "description": description,
            }
            if assignee:
                data["assignees"] = [assignee]
            if priority:
                data["priority"] = priority
            
            response = requests.post(f"{self.base_url}/list/{list_id}/task", 
                                   headers=self.headers, json=data)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error creating task: {e}")
            return None
    
    def update_task_status(self, task_id, status):
        """Update task status"""
        try:
            data = {"status": status}
            response = requests.put(f"{self.base_url}/task/{task_id}", 
                                  headers=self.headers, json=data)
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating task status: {e}")
            return False
    
    def get_workspace_structure(self):
        """Get complete workspace structure for setup"""
        structure = {}
        try:
            # Get teams
            teams_response = requests.get(f"{self.base_url}/team", headers=self.headers)
            if teams_response.status_code == 200:
                teams = teams_response.json()['teams']
                
                for team in teams:
                    team_id = team['id']
                    team_name = team['name']
                    structure[team_name] = {"id": team_id, "spaces": {}}
                    
                    # Get spaces
                    spaces = self.get_spaces(team_id)
                    for space in spaces:
                        space_id = space['id']
                        space_name = space['name']
                        structure[team_name]["spaces"][space_name] = {"id": space_id, "folders": {}}
                        
                        # Get folders
                        folders_response = requests.get(f"{self.base_url}/space/{space_id}/folder", headers=self.headers)
                        if folders_response.status_code == 200:
                            folders = folders_response.json()['folders']
                            for folder in folders:
                                folder_id = folder['id']
                                folder_name = folder['name']
                                structure[team_name]["spaces"][space_name]["folders"][folder_name] = {"id": folder_id, "lists": {}}
                                
                                # Get lists
                                lists_response = requests.get(f"{self.base_url}/folder/{folder_id}/list", headers=self.headers)
                                if lists_response.status_code == 200:
                                    lists = lists_response.json()['lists']
                                    for list_item in lists:
                                        list_id = list_item['id']
                                        list_name = list_item['name']
                                        structure[team_name]["spaces"][space_name]["folders"][folder_name]["lists"][list_name] = list_id
            
            return structure
        except Exception as e:
            print(f"Error getting workspace structure: {e}")
            return {}

if __name__ == "__main__":
    clickup = ClickUpManager()
    print("Testing ClickUp connection...")
    
    if clickup.test_connection():
        print("\nGetting workspace structure...")
        structure = clickup.get_workspace_structure()
        print(json.dumps(structure, indent=2))