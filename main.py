import tkinter as tk
from tkinter import ttk
import pandas as pd
import os.path

script_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(script_directory, "database.csv")


def display_todo_list():
    todo_list.delete(*todo_list.get_children())

    if os.path.isfile(database_path):
        df = pd.read_csv(database_path)
        for index, row in df.iterrows():
            todo_list.insert("", tk.END, values=(row["Task"], row["Date"]))


def add_task():
    task = input_task.get()
    date = input_date.get()
    if task and date:
        if os.path.isfile(database_path):
            df = pd.read_csv(database_path)
        else:
            df = pd.DataFrame(columns=["Task", "Date"])
        new_row = pd.DataFrame([[task, date]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(database_path, index=False)
        todo_list.insert("", tk.END, values=(task, date))
        input_task.delete(0, tk.END)
        input_date.delete(0, tk.END)


def clear_list():
    todo_list.delete(*todo_list.get_children())
    df = pd.DataFrame(columns=["Task", "Date"])
    df.to_csv(database_path, index=False)


def delete_selected():
    selected_items = todo_list.selection()  # Get the selected item(s)
    if selected_items:
        df = pd.read_csv(database_path)
        for item in selected_items:
            task = todo_list.item(item, "values")[0]  # Get the task text from the selected item
            index = df[df["Task"] == task].index[0]  # Find the index of the task in the DataFrame
            df.drop(index=index, inplace=True)
        df.to_csv(database_path, index=False)
        display_todo_list()


def modify_selected():
    selected_items = todo_list.selection()
    if selected_items:
        current_task = todo_list.item(selected_items[0], "values")[0]
        current_date = todo_list.item(selected_items[0], "values")[1]

        modify_window = tk.Toplevel()
        modify_window.title("Modify Task")
        modify_window.geometry("300x150")
        modify_window.resizable(False, False)

        new_task_label = tk.Label(modify_window, text="New Task:")
        new_task_label.pack()
        new_task_entry = tk.Entry(modify_window, width=30)
        new_task_entry.pack()

        new_date_label = tk.Label(modify_window, text="New Date:")
        new_date_label.pack()
        new_date_entry = tk.Entry(modify_window, width=30)
        new_date_entry.pack()

        new_task_entry.insert(tk.END, current_task)
        new_date_entry.insert(tk.END, current_date)

        def modify_task():
            new_task = new_task_entry.get()
            new_date = new_date_entry.get()
            if new_task and new_date:
                df = pd.read_csv(database_path)
                for item in selected_items:
                    task = todo_list.item(item, "values")[0]
                    index = df[df["Task"] == task].index[0]
                    df.at[index, "Task"] = new_task
                    df.at[index, "Date"] = new_date
                df.to_csv(database_path, index=False)
                display_todo_list()
                modify_window.destroy()

        modify_button = tk.Button(modify_window, text="Modify", command=modify_task)
        modify_button.pack()

def create_gui():
    global todo_list, input_date, input_task
    window = tk.Tk()
    window.geometry("500x400")
    window.title("TODO List")
    window.configure(padx=60, pady=10)
    
    enter_work_label = tk.Label(text="Enter TODO:")
    enter_work_label.grid(row=0, column=0, sticky="nw")
    
    enter_date_label = tk.Label(text="Enter Date:")
    enter_date_label.configure(padx=5)
    enter_date_label.grid(row=0, column=1, sticky="nw")

    input_task = tk.Entry(window, width=35)
    input_task.grid(row=1, column=0, sticky="w")

    add_task_button = tk.Button(window, text="Add Task", command=add_task)
    add_task_button.grid(row=2, column=0, sticky="w", pady=5)

    input_date = tk.Entry(window, width=15)
    input_date.grid(row=1, column=1, sticky="w")

    todo_list = ttk.Treeview(window, columns=("Task", "Date"), show="headings")
    todo_list.grid(row=4, column=0, columnspan=2, sticky="w")
    todo_list.heading("Task", text="Tasks")
    todo_list.heading("Date", text="Date")
    todo_list.column("Task", width=280)
    todo_list.column("Date", width=80)

    clear_list_button = tk.Button(window, text="Clear", command=clear_list)
    clear_list_button.grid(row=5, column=2, sticky="w", pady=10)

    modify_selected_button = tk.Button(window, text="Modify", command=modify_selected)
    modify_selected_button.grid(row=5, column=1, sticky="e", pady=10)

    delete_selected_button = tk.Button(window, text="Delete Selected", command=delete_selected)
    delete_selected_button.grid(row=5, column=0, sticky="w", pady=10)

    display_todo_list()

    window.mainloop()


if __name__ == "__main__":
    create_gui()
