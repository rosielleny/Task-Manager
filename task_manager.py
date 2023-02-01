# Note use the following username and password to access the admin rights 
# username: admin
# password: password
#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
task_num = 0
for t_str in task_data:
    curr_t = {}
    task_num += 1
    curr_t['task number'] = task_num
    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file.
    - Use a while loop to validate your user name and password.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

def task_overview(): # Called by 'gr' or 'ds' in the main menu | Generates task statistics and writes them to a file of the same name
    completed = 0 # Stores number of completed tasks
    incomplete = 0 # Stores number of incomplete tasks
    incomp_overdue = 0 # Stores number of incomplete and overdue tasks
    for c in task_list: 
        if c['completed'] == True:
            completed += 1 # Counts completed tasks
        else:
            incomplete += 1 # Counts incomplete taks
            if datetime.now() > c['due_date']:
                incomp_overdue += 1 # Counts incomplete and overdue tasks
    
    perc_incomp = f"{(incomplete/len(task_list))*100}%" # Calculates the percentage of tasks incomplete: ([number incomplete] ÷ [total number]) x 100
    perc_overdue = f"{(incomp_overdue/len(task_list))*100}%" # Calculates the percentage of tasks incomplete and overdue 

    with open('task_overview.txt', 'w') as tasko: # Writes the above data to task_overview.txt in a comprehensible manner
        tasko.write(f"""Total number of tasks: {len(task_list)}
Total completed: {completed}
Total incomplete: {incomplete}
Total incomplete and overdue: {incomp_overdue}
Percentage of tasks incomplete: {perc_incomp}
Percentage of tasks incomplete and overdue: {perc_overdue}""")

def user_overview(): # Called by 'gr' or 'ds' in the main menu | Generates user statistics and writes them to a file of the same name
    num_tasks = 0 # Sets a variable to store the total number of tasks 
    num_user = 0 # Stores the total number of users

    for t in task_list: # Counts the number of tasks
        num_tasks += 1

    with open('user.txt', 'r') as them: # Reads the user list and stores it in a variable
        alloem = them.read()

    alloem = alloem.split('\n') # Splits 'alloem', turning it into a list where each user/password combo is an item

    for u in alloem: # Counts the items in the alloem list, thus counting the number of users
        num_user += 1

    user_list = [] # Creats a list in which to store each user as they are encountered in the task list

    with open('user_overview.txt','w') as usero:
        usero.write(f'Total number of tasks: {num_tasks}\nTotal number of users: {num_user}\n') # Writes the total number of tasks and users at the top of the user_overview file

    for u in task_list: # Iterates through task_list
        user = u['username'] # Assigns the user associated with the current task to the variable 'user'
        completed = 0 # Creates variables to store the upcoming counts
        incomplete = 0
        overdue = 0
        tot = 0
        if user not in user_list: # If the user is not in user_list, their task data has not yet been written
            
            for v in task_list: # Iterates through task_list

                if v['username'] == user: # If the current task is a match for the user whose data we are gathering
                    tot += 1 # Adds 1 to this user's total number of tasks
                    user_list.append(user) # Adds the user to user_list, preventing this data gathering/writing section from running multiple times for one user

                    if v['completed'] == True:
                        completed += 1 # Adds 1 to this user's total completed tasks

                    else:
                        incomplete += 1 # Adds 1 to this user's total incomplete tasks

                        if datetime.now() > v['due_date']: # Checks if the incomplete task is overdue, if so adds 1 to the overdue count
                            overdue += 1
                    # Below dictionary stores the gathered data, with necessary calculations accounted for
                    inner_dict = {'\nUser': f'{user}','Total tasks assigned to user': f"{tot}", 'Percentage of total tasks': f"{(tot/len(task_list))*100}%", 'Percentage of assigned tasks completed': f"{(completed/tot)*100}%", 'Percentage incomplete': f"{(incomplete/tot)*100}%", 'Percentage overdue': f"{(overdue/tot)*100}%",}

            with open("user_overview.txt", 'a') as usero: # Opens user_overview.txt to append this new info
                for key, value in inner_dict.items():
                    usero.write('%s: %s\n' % (key, value)) # Writes inner_dict to the file in the form "Key: Value [new line] Key: Value...etc."

def rewrite_txt(task_list): # Called by the edit_task function | A function isolating the task writing part of the add_task function so this part may be called again for different functions.
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Tasks updated.")

def reg_user(): # Called by 'r' in the main menu | Adds a new user's username and password to user.txt

    reg_bool = True

    while reg_bool is True:

        new_username = input("New Username: ").lower()  
        
        if new_username.lower() in username_password:
            print("User already exists.")
            continue

        new_password = input("New Password: ")   
        confirm_password = input("Confirm Password: ")
  
        if new_password == confirm_password: # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
                reg_bool = False
   
        else:         # - Otherwise you present a relevant message.
            print("Passwords do no match")
            return None

def add_task(task_num): # Called by 'a' in the main menu | Adds a new task to tasks.txt
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return None
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
            continue
         # - Then get the current date.
    curr_date = date.today()
        # - Add the data to the file task.txt and
        # - You must remember to include the 'No' to indicate if the task is complete.
    new_task = {
            "task number": task_num,
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }
    task_num += 1


    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all(): # Called by 'va' in the main menu | Displays all tasks in tasks.txt
    print("-----------------------------------")
    for t in task_list:
        disp_str = f"Task: {t['task number']} \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)
        print("-----------------------------------")
    
def view_mine(): # Called by 'vm' in the main menu | Displays all tasks associated with current user
    print("-----------------------------------")

    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task: {t['task number']} \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            print("-----------------------------------")  

def edit_task(): # Called by 'vm' in the main menu | Allows user to edit the completion status or username and/or date of a task
    user_num = int(input("Select a task to edit by entering the corresponding number, or enter '-1' to exit. ")) # Recieves user input for next course of action
    if user_num == -1: # When the user enters '-1' to exit, this returns '-1', resulting in the program going back to the main menu while loop
        return '-1'     

    elif user_num >0:
       
        for c in task_list:
            if c['task number'] == user_num:
                if c['completed'] == True:
                    print("\nThis task has been completed and can no longer be edited.")
                    return '-1'

        print("\nSelect one of the following options below:\n\tc – Mark task as complete\n\tet – Edit task") # Prints a menu for the user to choose their next course of action
        choices = input(":")

        if choices == 'c': # If they choose to mark the task as complete

            complete = input("\nMark task as complete? yes/no ") # Confirms their choice

            if complete.lower() == 'yes': 
                for n in task_list: # Iterates through task_list to find the relevant task by number 
                    if n['task number'] == user_num:
                        n['completed'] = True # Marks the task as complete
                        rewrite_txt(task_list) # Calls the rewrite_txt function to update tasks.txt
                        return '-1' # Returns -1, thus sending the user back into the main menu while loop

            elif complete.lower() == 'no': # Tells the user no changes have been made and returns them to the main menu
                    print('No changes made.')
                    return '-1'

        elif choices == 'et': # If they choose to edit the task 
            
            o_bool = True

            while o_bool: # While loop that will loop until a valid user name is entered, or the user opts to not change the assigned user

                name = input("\nWould you like to change the user assigned to this task? yes/no ")

                if name.lower() == 'yes':

                    for o in task_list: # Iterates through task_list and finds the task matching the number entered by the user
                       
                        if o['task number'] == user_num:
                            new_name = input("\nWhich user would you like to assign to this task? ")

                            if new_name not in username_password: # Checks the user is valid, goes back to the top of the while loop if not
                                print("\nUser does not exist. ")
                                continue 
                            else: # Rewrites tasks.txt with the updated info
                                o['username'] = new_name
                                o_bool = False
                                rewrite_txt(task_list)

                elif name.lower() == 'no': # Exits the while loop if user selects 'no' to editting 
                    o_bool = False

                else: # Prints error messages if neither yes nor no are entered
                    print("\nPlease enter a valid option. 'yes' or 'no'")

            p_bool = True
            while p_bool: # While loop will repeat until the user enters a valid choice to the following question

                due = input("\nWould you like to change the due date of this task? yes/no ")

                if due.lower() == 'yes': # If the user wants to change the date
                   
                    for p in task_list: # Iterates through task_list and finds the task matching the user's selected number
                       
                        if p['task number'] == user_num: 
                           
                            while True: # Requests the new due date and checks it is in the correct format, requesting again if not
                                try:
                                    new_due = input("\nWhat is the new due date? YYYY-MM-DD ")
                                    new_due_time = datetime.strptime(new_due, DATETIME_STRING_FORMAT)
                                    break
                                except ValueError:
                                    print("\nInvalid datetime format. Please use the format specified")
                                    continue

                            p['due_date'] = new_due_time 
                            rewrite_txt(task_list) # Updates the task.txt file 
                            p_bool = False # Exits the while loop

                elif due.lower() == 'no': # Exits the while loop if the user does not wish to edit the date
                    p_bool = False
                else: # Prints error message if the user has not enter 'yes' or 'no' and loops back to the top of the while loop
                    print("\nPlease enter a valid option. 'yes' or 'no'")

            if due.lower == 'no' and name.lower() == 'no': # If no changes were made, prints a message saying so and returns to the main menu
               
                print("\nNo changes have been made.")
                return '-1'

            elif due.lower == 'yes' or name.lower() == 'yes': # If one or more changes were made, prints that the changes have been saved and returns to the main menu
                print("\nYour changes have been saved.")
                return '-1'
   

while True:
    #presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case.
    print()
    menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr – generate report
    ds – display statistics
    e - Exit
    : ''').lower()

    if menu == 'r':

        reg_user() # Calls the reg_user function 
        if reg_user == None: # Re-enters the while loop when the function returns None
            continue

    elif menu == 'a':

        add_task(task_num)
        if add_task == None: # Re-enters the while loop when the function returns None
            continue

    elif menu == 'va':

        view_all()

    elif menu == 'vm':

        view_mine() # Calls view_mine function
        if edit_task() == '-1': # Calls edit_task fucntion and re-enters the while loop when the function returns -1
            continue
    
    elif menu == 'gr':
        task_overview() # Calls task_overview function to generate stats and write them to a file
        user_overview() # Calls user_overview function to generate stats and write them to a file
    
    elif menu == 'ds':

        task_overview() # As above
        user_overview() # As above

        with open('task_overview.txt', 'r') as taskys: # Reads file and stores it in variable
            task_stats = taskys.read()

        with open('user_overview.txt', 'r') as useys: # Reads file and stores it in variable
            user_stats = useys.read()

        print(f"\nTask Statistics\n\n{task_stats}\n\nUser Statistics\n\n{user_stats}") # Prints the contents of the files

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")