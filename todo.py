import tkinter as tk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        # List to store tasks
        self.tasks = []

        # Frame for the listbox and scrollbar
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Listbox widget
        self.task_listbox = tk.Listbox(
            frame,
            width=50,
            height=10,
            bd=0,
            selectbackground="#a6a6a6",
            activestyle="none"
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Entry box for adding new tasks
        self.task_entry = tk.Entry(
            self.root,
            font=("Arial", 12)
        )
        self.task_entry.pack(pady=20)

        # Buttons for adding and deleting tasks
        add_task_btn = tk.Button(
            self.root,
            text="Add Task",
            command=self.add_task
        )
        add_task_btn.pack(pady=5)

        delete_task_btn = tk.Button(
            self.root,
            text="Delete Task",
            command=self.delete_task
        )
        delete_task_btn.pack(pady=5)

    def add_task(self):
        task = self.task_entry.get()
        if task != "":
            self.tasks.append(task)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
        except IndexError:
            pass

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()