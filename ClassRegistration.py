
# display the main menu options
def display_menu():
    print("\n To-Do List ")
    print("1. Add Task")
    print("2. Show Tasks")
    print("3. Mark Task as Done")
    print("4. Delete Task")
    print("5. Exit")

# add a new task to the list
def add_task(tasks):
    task = input("Enter the task: ")  # enter a task
    tasks.append(task)  # add the task to the list
    print("Task added!")  # display that the task has been added

# display all tasks in the list
def show_tasks(tasks):
    for index, task in enumerate(tasks):
        print(f"{index + 1}. {task}")  # display each task with its number

# mark a specific task as completed
def mark_task_done(tasks):
    show_tasks(tasks)  # display all tasks
    task_index = int(input("Enter the task number to mark as done: ")) - 1  # select a task
    if 0 <= task_index < len(tasks):
        tasks[task_index] += " (completed)"  # mark it complete
        print("Task marked as done!")
    else:
        print("Invalid task number.")  # make sure the number is valid

# delete a task from the list
def delete_task(tasks):
    show_tasks(tasks)  # display all tasks
    task_index = int(input("Enter the task number to delete: ")) - 1  # ask user to select a task
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)  # remove the task from the list
        print("Task deleted!")
    else:
        print("Invalid task number.")  # make sure the number is valid

# main function
def main():
    tasks = []  # initialize a list to store tasks
    while True:
        display_menu()  # display the main menu
        choice = input("Enter your choice: ")  # ask user to select an option

        if choice == '1':
            add_task(tasks)  # add a new task
        elif choice == '2':
            show_tasks(tasks)  # show all tasks
        elif choice == '3':
            mark_task_done(tasks)  # mark a task as done
        elif choice == '4':
            delete_task(tasks)  # delete a task
        elif choice == '5':
            print("Exiting the To-Do List.")  # exit
            break
        else:
            print("Invalid choice. Please try again.")  # make sure the number is valid

if __name__ == "__main__":
    main()
