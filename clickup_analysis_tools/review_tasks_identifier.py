"""
Review Tasks Identifier
Specifically identifies tasks that need Founder and Personal Assistant review
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class ReviewTasksIdentifier:
    def __init__(self):
        self.api_key = os.getenv('CLICKUP_API_KEY')
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        self.hannah_list_id = "901110057030"
    
    def identify_review_tasks(self):
        """Identify tasks requiring founder and assistant review"""
        try:
            response = requests.get(f"{self.base_url}/list/{self.hannah_list_id}/task", headers=self.headers)
            if response.status_code != 200:
                print(f"Error getting tasks: {response.status_code}")
                return
            
            tasks = response.json().get('tasks', [])
            
            review_analysis = {
                'founder_review_needed': [],
                'assistant_review_needed': [],
                'joint_review_needed': [],
                'urgent_decisions': [],
                'strategic_decisions': [],
                'operational_decisions': []
            }
            
            for task in tasks:
                if task['status']['type'] == 'closed':
                    continue
                    
                task_analysis = self._analyze_task_for_review(task)
                
                if task_analysis['needs_founder_review']:
                    review_analysis['founder_review_needed'].append(task_analysis)
                
                if task_analysis['needs_assistant_review']:
                    review_analysis['assistant_review_needed'].append(task_analysis)
                
                if task_analysis['needs_joint_review']:
                    review_analysis['joint_review_needed'].append(task_analysis)
                
                if task_analysis['urgency_level'] == 'urgent':
                    review_analysis['urgent_decisions'].append(task_analysis)
                
                if task_analysis['decision_type'] == 'strategic':
                    review_analysis['strategic_decisions'].append(task_analysis)
                elif task_analysis['decision_type'] == 'operational':
                    review_analysis['operational_decisions'].append(task_analysis)
            
            self._present_review_analysis(review_analysis)
            return review_analysis
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def _analyze_task_for_review(self, task):
        """Analyze individual task to determine review needs"""
        task_text = (task['name'] + ' ' + task.get('description', '')).lower()
        status = task['status']['status'].lower()
        priority = self._get_priority_level(task.get('priority'))
        
        analysis = {
            'task_id': task['id'],
            'name': task['name'],
            'status': task['status']['status'],
            'priority': priority,
            'assignees': [a.get('username', a.get('name', 'Unknown')) for a in task.get('assignees', [])],
            'needs_founder_review': False,
            'needs_assistant_review': False,
            'needs_joint_review': False,
            'urgency_level': 'normal',
            'decision_type': 'operational',
            'review_reason': [],
            'suggested_action': ''
        }
        
        # Determine urgency level
        if priority in ['urgent', 'high'] or 'urgent' in task_text:
            analysis['urgency_level'] = 'urgent'
        elif priority == 'high':
            analysis['urgency_level'] = 'high'
        
        # Check if currently in review status
        if 'review' in status:
            analysis['needs_founder_review'] = True
            analysis['review_reason'].append('Currently in review status')
        
        # Strategic business decisions (Founder review needed)
        strategic_keywords = ['business plan', 'strategy', 'launch', 'marketing', 'investment', 'legal', 'contract', 'partnership']
        if any(keyword in task_text for keyword in strategic_keywords):
            analysis['needs_founder_review'] = True
            analysis['decision_type'] = 'strategic'
            analysis['review_reason'].append('Strategic business decision')
        
        # Financial decisions (Founder review needed)
        financial_keywords = ['insurance', 'tax', 'financial', 'investment', 'budget', 'cost', 'expense', 'llc']
        if any(keyword in task_text for keyword in financial_keywords):
            analysis['needs_founder_review'] = True
            analysis['review_reason'].append('Financial decision required')
        
        # High-value vendor/service decisions (Joint review)
        vendor_keywords = ['hire', 'service', 'vendor', 'contractor', 'professional', 'consultant']
        if any(keyword in task_text for keyword in vendor_keywords):
            analysis['needs_joint_review'] = True
            analysis['review_reason'].append('Vendor/service selection')
        
        # Personal/lifestyle decisions (Founder input needed)
        personal_keywords = ['personal', 'health', 'travel', 'holiday', 'vacation', 'home', 'house']
        if any(keyword in task_text for keyword in personal_keywords):
            analysis['needs_founder_review'] = True
            analysis['review_reason'].append('Personal decision required')
        
        # Operational tasks (Assistant can handle)
        operational_keywords = ['research', 'find', 'schedule', 'book', 'order', 'contact', 'organize']
        if any(keyword in task_text for keyword in operational_keywords) and not analysis['needs_founder_review']:
            analysis['needs_assistant_review'] = True
            analysis['decision_type'] = 'operational'
            analysis['review_reason'].append('Operational task - assistant can execute')
        
        # Complex research or analysis (Joint review for direction)
        complex_keywords = ['analyze', 'evaluate', 'compare', 'assess', 'investigate']
        if any(keyword in task_text for keyword in complex_keywords):
            analysis['needs_joint_review'] = True
            analysis['review_reason'].append('Complex analysis - direction needed')
        
        # Generate suggested action
        if analysis['needs_founder_review'] and analysis['urgency_level'] == 'urgent':
            analysis['suggested_action'] = 'IMMEDIATE founder review required'
        elif analysis['needs_founder_review']:
            analysis['suggested_action'] = 'Schedule founder review session'
        elif analysis['needs_joint_review']:
            analysis['suggested_action'] = 'Brief coordination meeting needed'
        elif analysis['needs_assistant_review']:
            analysis['suggested_action'] = 'Assistant can proceed with execution'
        else:
            analysis['suggested_action'] = 'Status unclear - needs triage'
        
        return analysis
    
    def _present_review_analysis(self, analysis):
        """Present the review analysis in a clear format"""
        print("="*60)
        print("HANNAH TASKS - REVIEW & DECISION ANALYSIS")
        print("="*60)
        print(f"Analysis Date: {datetime.now().strftime('%A, %B %d, %Y at %H:%M')}")
        
        # Urgent decisions first
        if analysis['urgent_decisions']:
            print(f"\n[URGENT DECISIONS NEEDED] ({len(analysis['urgent_decisions'])} tasks)")
            print("These require immediate attention:")
            for task in analysis['urgent_decisions'][:5]:
                print(f"\n  * {task['name']}")
                print(f"    Priority: {task['priority']} | Status: {task['status']}")
                print(f"    Reason: {', '.join(task['review_reason'])}")
                print(f"    Action: {task['suggested_action']}")
        
        # Founder review needed
        if analysis['founder_review_needed']:
            print(f"\n[FOUNDER REVIEW NEEDED] ({len(analysis['founder_review_needed'])} tasks)")
            print("These require your personal input/decision:")
            for task in analysis['founder_review_needed']:
                print(f"\n  * {task['name']}")
                print(f"    Priority: {task['priority']} | Status: {task['status']}")
                print(f"    Reason: {', '.join(task['review_reason'])}")
                print(f"    Assignees: {', '.join(task['assignees']) if task['assignees'] else 'Unassigned'}")
        
        # Joint review needed  
        if analysis['joint_review_needed']:
            print(f"\n[JOINT REVIEW NEEDED] ({len(analysis['joint_review_needed'])} tasks)")
            print("These need brief discussion between you and Hannah:")
            for task in analysis['joint_review_needed']:
                print(f"\n  * {task['name']}")
                print(f"    Priority: {task['priority']} | Status: {task['status']}")
                print(f"    Reason: {', '.join(task['review_reason'])}")
        
        # Assistant can handle
        if analysis['assistant_review_needed']:
            print(f"\n[ASSISTANT CAN EXECUTE] ({len(analysis['assistant_review_needed'])} tasks)")
            print("Hannah can proceed with these (operational tasks):")
            for task in analysis['assistant_review_needed'][:5]:  # Show first 5
                print(f"  * {task['name']} ({task['status']})")
            if len(analysis['assistant_review_needed']) > 5:
                print(f"  ... and {len(analysis['assistant_review_needed']) - 5} more operational tasks")
        
        # Strategic vs Operational breakdown
        strategic_count = len(analysis['strategic_decisions'])
        operational_count = len(analysis['operational_decisions'])
        
        print(f"\n[DECISION TYPE BREAKDOWN]")
        print(f"Strategic Decisions (need founder input): {strategic_count}")
        print(f"Operational Tasks (assistant can handle): {operational_count}")
        
        # Summary recommendations
        print(f"\n[RECOMMENDED ACTIONS]")
        if analysis['urgent_decisions']:
            print(f"1. IMMEDIATE: Review {len(analysis['urgent_decisions'])} urgent decisions")
        if analysis['founder_review_needed']:
            print(f"2. Schedule 30-min founder review session for {len(analysis['founder_review_needed'])} strategic tasks")
        if analysis['joint_review_needed']:
            print(f"3. Brief 15-min coordination meeting for {len(analysis['joint_review_needed'])} joint decisions")
        if analysis['assistant_review_needed']:
            print(f"4. Hannah can proceed with {len(analysis['assistant_review_needed'])} operational tasks")
    
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

if __name__ == "__main__":
    identifier = ReviewTasksIdentifier()
    result = identifier.identify_review_tasks()
    
    if result:
        # Save detailed analysis
        with open('review_tasks_analysis.json', 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\nDetailed analysis saved to review_tasks_analysis.json")