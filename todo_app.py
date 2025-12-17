import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Todo App")
        self.tasks = []

        self.setup_UI()

    def setup_UI(self):
        # Frame for entry widget and buttons
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=10)

        self.task_entry = tk.Entry(self.entry_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.entry_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        # Frame for the list of tasks
        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.pack(pady=10)

        self.tasks_listbox = tk.Listbox(self.tasks_frame, width=50, height=10)
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.tasks_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.tasks_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tasks_listbox.yview)

        # Frame for control buttons
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.edit_button = tk.Button(self.control_frame, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.control_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.update_tasks_display()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task entry cannot be empty.")

    def edit_task(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            new_task = self.task_entry.get().strip()
            if new_task:
                self.tasks[selected_index] = new_task
                self.update_tasks_display()
                self.task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", "Task entry cannot be empty.")
        except IndexError:
            messagebox.showwarning("Warning", "No task selected.")

    def delete_task(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_tasks_display()
        except IndexError:
            messagebox.showwarning("Warning", "No task selected.")

    def update_tasks_display(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.tasks_listbox.insert(tk.END, task)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
