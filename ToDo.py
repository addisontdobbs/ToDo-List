#!/usr/bin/env python3
"""
Simple Terminal To-Do List Manager
Allows adding, removing, viewing tasks with persistent file storage
"""

import json
import os
from datetime import datetime

class TodoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file if it exists"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
                print(f"✓ Loaded {len(self.tasks)} task(s) from {self.filename}")
            except Exception as e:
                print(f"⚠ Error loading tasks: {e}")
                self.tasks = []
        else:
            print(f"No saved tasks found. Starting fresh!")
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=2)
            print(f"✓ Tasks saved to {self.filename}")
        except Exception as e:
            print(f"⚠ Error saving tasks: {e}")
    
    def add_task(self, description):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'completed': False,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.tasks.append(task)
        print(f"✓ Added task #{task['id']}: {description}")
        self.save_tasks()
    
    def remove_task(self, task_id):
        """Remove a task by ID"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                removed = self.tasks.pop(i)
                print(f"✓ Removed task #{task_id}: {removed['description']}")
                self.save_tasks()
                return
        print(f"⚠ Task #{task_id} not found")
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                print(f"✓ Marked task #{task_id} as completed")
                self.save_tasks()
                return
        print(f"⚠ Task #{task_id} not found")
    
    def view_tasks(self):
        """Display all tasks"""
        if not self.tasks:
            print("\n📝 No tasks yet! Add one to get started.\n")
            return
        
        print("\n" + "="*60)
        print("📝 YOUR TO-DO LIST")
        print("="*60)
        
        for task in self.tasks:
            status = "✓" if task['completed'] else "○"
            task_text = task['description']
            if task['completed']:
                task_text = f"\033[9m{task_text}\033[0m"  # Strikethrough
            
            print(f"{status} [{task['id']}] {task_text}")
            print(f"    Created: {task['created']}")
        
        print("="*60 + "\n")
    
    def export_to_file(self, export_filename):
        """Export tasks to a custom text file"""
        try:
            with open(export_filename, 'w') as f:
                f.write("MY TO-DO LIST\n")
                f.write("=" * 50 + "\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for task in self.tasks:
                    status = "[DONE]" if task['completed'] else "[TODO]"
                    f.write(f"{status} {task['description']}\n")
                    f.write(f"       Created: {task['created']}\n\n")
            
            print(f"✓ Tasks exported to {export_filename}")
        except Exception as e:
            print(f"⚠ Error exporting: {e}")


def print_menu():
    """Display the main menu"""
    print("\n" + "="*40)
    print("   TO-DO LIST MANAGER")
    print("="*40)
    print("1. View all tasks")
    print("2. Add a task")
    print("3. Complete a task")
    print("4. Remove a task")
    print("5. Export to text file")
    print("6. Exit")
    print("="*40)


def main():
    """Main program loop"""
    todo = TodoList()
    
    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()
        
        if choice == '1':
            todo.view_tasks()
        
        elif choice == '2':
            description = input("Enter task description: ").strip()
            if description:
                todo.add_task(description)
            else:
                print("⚠ Task description cannot be empty")
        
        elif choice == '3':
            todo.view_tasks()
            try:
                task_id = int(input("Enter task ID to complete: "))
                todo.complete_task(task_id)
            except ValueError:
                print("⚠ Please enter a valid number")
        
        elif choice == '4':
            todo.view_tasks()
            try:
                task_id = int(input("Enter task ID to remove: "))
                todo.remove_task(task_id)
            except ValueError:
                print("⚠ Please enter a valid number")
        
        elif choice == '5':
            filename = input("Enter filename (e.g., my_tasks.txt): ").strip()
            if filename:
                todo.export_to_file(filename)
            else:
                print("⚠ Filename cannot be empty")
        
        elif choice == '6':
            print("\n👋 Goodbye! Your tasks are saved.\n")
            break
        
        else:
            print("⚠ Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()