import json
import os
from datetime import datetime, time

class TodoWithScheduler:
    def __init__(self):
        self.tasks = []
        self.schedule = {}
        self.filename = "todo_schedule.json"
        self.load_data()

    def add_task(self, task, priority="medium", scheduled_time=None):
        """Add a new task to the to-do list"""
        task_id = len(self.tasks) + 1
        new_task = {
            "id": task_id,
            "task": task,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.tasks.append(new_task)
        
        # If a time is scheduled, add to schedule
        if scheduled_time:
            self.schedule_task(task_id, scheduled_time)
            
        print(f"Task '{task}' added with ID: {task_id}")
        return task_id

    def remove_task(self, task_id):
        """Remove a task by ID"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                removed_task = self.tasks.pop(i)
                print(f"Task '{removed_task['task']}' removed.")
                
                # Remove from schedule if it exists
                for time_slot in list(self.schedule.keys()):
                    if task_id in self.schedule[time_slot]:
                        self.schedule[time_slot].remove(task_id)
                        if not self.schedule[time_slot]:  # If empty list
                            del self.schedule[time_slot]
                return True
        print(f"Task with ID {task_id} not found.")
        return False

    def mark_complete(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                print(f"Task '{task['task']}' marked as completed.")
                return True
        print(f"Task with ID {task_id} not found.")
        return False

    def schedule_task(self, task_id, time_str):
        """Schedule a task for a specific time"""
        try:
            # Parse time string (format: HH:MM)
            task_time = datetime.strptime(time_str, "%H:%M").time().strftime("%H:%M")
            
            # Create schedule entry if it doesn't exist
            if task_time not in self.schedule:
                self.schedule[task_time] = []
                
            # Add task to schedule if not already there
            if task_id not in self.schedule[task_time]:
                self.schedule[task_time].append(task_id)
                
            # Find task name for confirmation message
            task_name = ""
            for task in self.tasks:
                if task["id"] == task_id:
                    task_name = task["task"]
                    break
                    
            print(f"Task '{task_name}' scheduled for {time_str}")
            return True
        except ValueError:
            print("Invalid time format. Please use HH:MM format (e.g., 14:30)")
            return False

    def unschedule_task(self, task_id):
        """Remove a task from the schedule"""
        task_found = False
        for time_slot in list(self.schedule.keys()):
            if task_id in self.schedule[time_slot]:
                self.schedule[time_slot].remove(task_id)
                if not self.schedule[time_slot]:  # If empty list
                    del self.schedule[time_slot]
                task_found = True
        
        if task_found:
            # Find task name for confirmation message
            task_name = ""
            for task in self.tasks:
                if task["id"] == task_id:
                    task_name = task["task"]
                    break
            print(f"Task '{task_name}' removed from schedule.")
            return True
        else:
            print(f"Task with ID {task_id} not found in schedule.")
            return False

    def view_tasks(self):
        """Display all tasks"""
        if not self.tasks:
            print("No tasks found.")
            return
            
        print("\n===== TO-DO LIST =====")
        for task in self.tasks:
            status = "✓" if task["completed"] else " "
            priority_symbol = {"high": "❗", "medium": "•", "low": "◦"}.get(task["priority"], "•")
            
            # Find scheduled time if any
            scheduled_time = ""
            for time_slot, task_ids in self.schedule.items():
                if task["id"] in task_ids:
                    scheduled_time = f" @ {time_slot}"
                    break
                    
            print(f"[{status}] {task['id']}. {priority_symbol} {task['task']}{scheduled_time}")
        print("=====================\n")

    def view_schedule(self):
        """Display the day's schedule"""
        if not self.schedule:
            print("No scheduled tasks for today.")
            return
            
        print("\n===== TODAY'S SCHEDULE =====")
        # Sort time slots
        sorted_times = sorted(self.schedule.keys(), key=lambda x: datetime.strptime(x, "%H:%M").time())
        
        for time_slot in sorted_times:
            print(f"\n{time_slot}:")
            for task_id in self.schedule[time_slot]:
                for task in self.tasks:
                    if task["id"] == task_id:
                        status = "✓" if task["completed"] else " "
                        priority_symbol = {"high": "❗", "medium": "•", "low": "◦"}.get(task["priority"], "•")
                        print(f"  [{status}] {task_id}. {priority_symbol} {task['task']}")
                        break
        print("===========================\n")

    def save_data(self):
        """Save tasks and schedule to a file"""
        data = {
            "tasks": self.tasks,
            "schedule": self.schedule
        }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {self.filename}")

    def load_data(self):
        """Load tasks and schedule from a file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.schedule = data.get("schedule", {})
                print(f"Data loaded from {self.filename}")
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Error loading data from {self.filename}")
                self.tasks = []
                self.schedule = {}


def show_menu():
    """Display the menu options"""
    print("\n===== TO-DO LIST MENU =====")
    print("1. Add a task")
    print("2. Remove a task")
    print("3. Mark a task as completed")
    print("4. Schedule a task")
    print("5. Remove a task from schedule")
    print("6. View all tasks")
    print("7. View today's schedule")
    print("8. Save and exit")
    print("==========================")
    return input("Choose an option (1-8): ")


def main():
    todo = TodoWithScheduler()
    
    print("Welcome to Your To-Do List with Day Scheduler!")
    
    while True:
        choice = show_menu()
        
        if choice == "1":  # Add a task
            task = input("Enter task description: ")
            priority = input("Enter priority (high/medium/low) [default: medium]: ").lower()
            if priority not in ["high", "medium", "low"]:
                priority = "medium"
                
            schedule_now = input("Do you want to schedule this task? (y/n): ").lower()
            if schedule_now == "y":
                time_str = input("Enter time (HH:MM, 24-hour format): ")
                task_id = todo.add_task(task, priority)
                todo.schedule_task(task_id, time_str)
            else:
                todo.add_task(task, priority)
                
        elif choice == "2":  # Remove a task
            todo.view_tasks()
            try:
                task_id = int(input("Enter task ID to remove: "))
                todo.remove_task(task_id)
            except ValueError:
                print("Please enter a valid task ID (number).")
                
        elif choice == "3":  # Mark as completed
            todo.view_tasks()
            try:
                task_id = int(input("Enter task ID to mark as completed: "))
                todo.mark_complete(task_id)
            except ValueError:
                print("Please enter a valid task ID (number).")
                
        elif choice == "4":  # Schedule a task
            todo.view_tasks()
            try:
                task_id = int(input("Enter task ID to schedule: "))
                time_str = input("Enter time (HH:MM, 24-hour format): ")
                todo.schedule_task(task_id, time_str)
            except ValueError:
                print("Please enter a valid task ID (number).")
                
        elif choice == "5":  # Remove from schedule
            todo.view_schedule()
            try:
                task_id = int(input("Enter task ID to remove from schedule: "))
                todo.unschedule_task(task_id)
            except ValueError:
                print("Please enter a valid task ID (number).")
                
        elif choice == "6":  # View all tasks
            todo.view_tasks()
            input("Press Enter to continue...")
            
        elif choice == "7":  # View schedule
            todo.view_schedule()
            input("Press Enter to continue...")
                       
        elif choice == "8":  # Save and exit
            todo.save_data()
            print("Thank you for using the To-Do List with Day Scheduler. Goodbye!")
            break
            
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()