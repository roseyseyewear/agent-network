"""
Automated Feedback System for Task Management Agents
Provides intelligent feedback, progress tracking, and escalation
"""

import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

load_dotenv()

class AgentFeedbackSystem:
    def __init__(self):
        self.api_key = os.getenv('CLICKUP_API_KEY')
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        self.hannah_list_id = "901110057030"
        
        # Feedback rules and thresholds
        self.feedback_rules = {
            'task_stuck_hours': 24,          # Task stuck in same status for 24+ hours
            'high_priority_check_hours': 4,  # Check high priority tasks every 4 hours
            'overdue_immediate': True,       # Immediate escalation for overdue tasks
            'completion_rate_threshold': 0.3 # Escalate if completion rate drops below 30%
        }
    
    def analyze_task_progress(self) -> Dict[str, Any]:
        """Analyze progress across all tasks and provide feedback"""
        
        # Get current tasks
        current_tasks = self._get_tasks_with_history()
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'overall_health': 'good',
            'alerts': [],
            'recommendations': [],
            'agent_performance': {},
            'priority_escalations': [],
            'automated_actions': []
        }
        
        # Analyze each task
        for task in current_tasks:
            task_feedback = self._analyze_individual_task(task)
            
            if task_feedback['needs_attention']:
                analysis['alerts'].append(task_feedback)
            
            if task_feedback['escalate_to_human']:
                analysis['priority_escalations'].append(task_feedback)
        
        # Generate overall recommendations
        analysis['recommendations'] = self._generate_recommendations(current_tasks)
        
        # Assess agent performance
        analysis['agent_performance'] = self._assess_agent_performance()
        
        # Determine overall health
        analysis['overall_health'] = self._calculate_overall_health(analysis)
        
        return analysis
    
    def _get_tasks_with_history(self) -> List[Dict]:
        """Get tasks with their update history"""
        try:
            response = requests.get(f"{self.base_url}/list/{self.hannah_list_id}/task", headers=self.headers)
            if response.status_code == 200:
                tasks = response.json().get('tasks', [])
                
                # Enhance each task with history analysis
                enhanced_tasks = []
                for task in tasks:
                    if task['status']['type'] != 'closed':  # Only active tasks
                        enhanced_task = self._enhance_task_with_analysis(task)
                        enhanced_tasks.append(enhanced_task)
                
                return enhanced_tasks
        except Exception as e:
            print(f"Error getting tasks: {e}")
            return []
    
    def _enhance_task_with_analysis(self, task: Dict) -> Dict:
        """Enhance task with progress analysis"""
        enhanced = task.copy()
        
        # Calculate time in current status
        last_updated = datetime.fromisoformat(task.get('date_updated', task.get('date_created', '')).replace('Z', '+00:00'))
        time_in_status = datetime.now() - last_updated.replace(tzinfo=None)
        
        enhanced['analysis'] = {
            'time_in_current_status_hours': time_in_status.total_seconds() / 3600,
            'priority_level': self._get_priority_level(task.get('priority')),
            'is_stuck': time_in_status.total_seconds() / 3600 > self.feedback_rules['task_stuck_hours'],
            'assignee_count': len(task.get('assignees', [])),
            'has_due_date': bool(task.get('due_date')),
            'estimated_effort': self._estimate_task_effort(task)
        }
        
        return enhanced
    
    def _analyze_individual_task(self, task: Dict) -> Dict:
        """Analyze individual task and provide feedback"""
        analysis = task['analysis']
        feedback = {
            'task_id': task['id'],
            'task_name': task['name'],
            'current_status': task['status']['status'],
            'needs_attention': False,
            'escalate_to_human': False,
            'feedback_type': 'none',
            'suggested_actions': [],
            'agent_feedback': ''
        }
        
        # Check if task is stuck
        if analysis['is_stuck']:
            feedback['needs_attention'] = True
            feedback['feedback_type'] = 'stuck_task'
            feedback['suggested_actions'].append('Review blockers and dependencies')
            feedback['agent_feedback'] = f"Task has been in '{task['status']['status']}' status for {analysis['time_in_current_status_hours']:.1f} hours"
            
            if analysis['priority_level'] in ['urgent', 'high']:
                feedback['escalate_to_human'] = True
        
        # Check high priority tasks
        if analysis['priority_level'] in ['urgent', 'high'] and analysis['time_in_current_status_hours'] > self.feedback_rules['high_priority_check_hours']:
            feedback['needs_attention'] = True
            feedback['feedback_type'] = 'high_priority_check'
            feedback['suggested_actions'].append('Prioritize this task')
            feedback['agent_feedback'] = f"High priority task needs attention - {analysis['time_in_current_status_hours']:.1f} hours without progress"
        
        # Check for overdue tasks
        if task.get('due_date'):
            due_date = datetime.fromtimestamp(int(task['due_date']) / 1000)
            if due_date < datetime.now():
                feedback['needs_attention'] = True
                feedback['escalate_to_human'] = True
                feedback['feedback_type'] = 'overdue'
                feedback['suggested_actions'].append('Immediate attention required')
                feedback['agent_feedback'] = f"Task is overdue by {(datetime.now() - due_date).days} days"
        
        # Check for unassigned high priority tasks
        if analysis['priority_level'] in ['urgent', 'high'] and analysis['assignee_count'] == 0:
            feedback['needs_attention'] = True
            feedback['feedback_type'] = 'unassigned_priority'
            feedback['suggested_actions'].append('Assign task to appropriate person or agent')
            feedback['agent_feedback'] = "High priority task is unassigned"
        
        return feedback
    
    def _generate_recommendations(self, tasks: List[Dict]) -> List[str]:
        """Generate overall recommendations based on task analysis"""
        recommendations = []
        
        # Analyze status distribution
        status_counts = {}
        priority_counts = {'urgent': 0, 'high': 0, 'normal': 0, 'low': 0, 'none': 0}
        stuck_tasks = 0
        
        for task in tasks:
            status = task['status']['status']
            status_counts[status] = status_counts.get(status, 0) + 1
            
            priority = task['analysis']['priority_level']
            priority_counts[priority] += 1
            
            if task['analysis']['is_stuck']:
                stuck_tasks += 1
        
        # Generate recommendations based on patterns
        if stuck_tasks > 3:
            recommendations.append(f"🚨 {stuck_tasks} tasks appear stuck - consider reassigning or breaking down")
        
        if priority_counts['urgent'] > 5:
            recommendations.append(f"⚠️  You have {priority_counts['urgent']} urgent tasks - consider delegating some")
        
        if status_counts.get('review', 0) > 4:
            recommendations.append(f"📋 {status_counts['review']} tasks awaiting review - schedule review session")
        
        if status_counts.get('backlog', 0) > 10:
            recommendations.append(f"📦 Large backlog ({status_counts['backlog']} tasks) - consider prioritization session")
        
        return recommendations
    
    def _assess_agent_performance(self) -> Dict[str, Any]:
        """Assess how well specialized agents are performing"""
        
        # Load agent assignments if available
        agent_performance = {
            'research_agent': {'tasks_assigned': 0, 'tasks_completed': 0, 'avg_completion_time': None, 'feedback': 'No data'},
            'calendar_agent': {'tasks_assigned': 0, 'tasks_completed': 0, 'avg_completion_time': None, 'feedback': 'No data'},
            'email_agent': {'tasks_assigned': 0, 'tasks_completed': 0, 'avg_completion_time': None, 'feedback': 'No data'},
            'business_agent': {'tasks_assigned': 0, 'tasks_completed': 0, 'avg_completion_time': None, 'feedback': 'No data'},
            'admin_agent': {'tasks_assigned': 0, 'tasks_completed': 0, 'avg_completion_time': None, 'feedback': 'No data'}
        }
        
        # This would be enhanced with actual tracking data
        # For now, provide placeholder feedback
        for agent in agent_performance:
            agent_performance[agent]['feedback'] = "Performance tracking in development"
        
        return agent_performance
    
    def _calculate_overall_health(self, analysis: Dict) -> str:
        """Calculate overall task management health"""
        alert_count = len(analysis['alerts'])
        escalation_count = len(analysis['priority_escalations'])
        
        if escalation_count > 0:
            return 'critical'
        elif alert_count > 5:
            return 'poor'
        elif alert_count > 2:
            return 'fair'
        else:
            return 'good'
    
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
    
    def _estimate_task_effort(self, task: Dict) -> str:
        """Estimate task effort based on description and type"""
        description = task.get('description', '') + ' ' + task['name']
        
        if any(word in description.lower() for word in ['research', 'investigate', 'analyze']):
            return 'medium'
        elif any(word in description.lower() for word in ['call', 'email', 'schedule', 'book']):
            return 'low'
        elif any(word in description.lower() for word in ['plan', 'strategy', 'develop', 'create']):
            return 'high'
        else:
            return 'medium'
    
    def provide_automated_feedback(self) -> str:
        """Provide automated feedback report"""
        analysis = self.analyze_task_progress()
        
        report = []
        report.append("="*60)
        report.append("AUTOMATED TASK FEEDBACK REPORT")
        report.append("="*60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Overall Health: {analysis['overall_health'].upper()}")
        
        if analysis['priority_escalations']:
            report.append(f"\n🚨 PRIORITY ESCALATIONS ({len(analysis['priority_escalations'])}):")
            for escalation in analysis['priority_escalations']:
                report.append(f"  • {escalation['task_name']}")
                report.append(f"    {escalation['agent_feedback']}")
                report.append(f"    Actions: {', '.join(escalation['suggested_actions'])}")
        
        if analysis['alerts']:
            report.append(f"\n⚠️  ALERTS ({len(analysis['alerts'])}):")
            for alert in analysis['alerts']:
                if not alert['escalate_to_human']:  # Don't duplicate escalations
                    report.append(f"  • {alert['task_name']}")
                    report.append(f"    {alert['agent_feedback']}")
        
        if analysis['recommendations']:
            report.append(f"\n💡 RECOMMENDATIONS:")
            for rec in analysis['recommendations']:
                report.append(f"  {rec}")
        
        report.append(f"\n📊 AGENT PERFORMANCE:")
        for agent, perf in analysis['agent_performance'].items():
            report.append(f"  {agent.replace('_', ' ').title()}: {perf['feedback']}")
        
        return '\n'.join(report)
    
    def save_feedback_report(self):
        """Save detailed feedback report to file"""
        analysis = self.analyze_task_progress()
        
        with open('agent_feedback_report.json', 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        return "agent_feedback_report.json"


if __name__ == "__main__":
    feedback_system = AgentFeedbackSystem()
    
    print(feedback_system.provide_automated_feedback())
    
    report_file = feedback_system.save_feedback_report()
    print(f"\nDetailed report saved to: {report_file}")