import tkinter as tk
from tkinter import Spinbox, ttk, messagebox
import json
import pyperclip
import subprocess
import threading
import os


# Function to run the command in a separate thread
def run_command(command):
   subprocess.run(f"cmd /c {command}", shell=True)
   messagebox.showinfo("Pyinstall", "The app was created, check for the exe file in the dist folder")
def run_cmd():
   # Get the current directory where the script is located
   global current_directory
   current_directory = os.path.dirname(os.path.realpath(__file__))
   # Change the directory to the current one using the 'cd' command in cmd.exe
   subprocess.run(f'start cmd /k cd /d "{current_directory}"', shell=True)
   
# Create the main window

# Function to execute run_command in a separate thread
def execute_in_thread(command):
   command_thread = threading.Thread(target=run_command, args=(command,))
   command_thread.start()
def execute_in_cd_thread(command):
   command_thread = threading.Thread(target=run_cmd, args=(current_directory,))
   command_thread.start()
# Function to load the version from a JSON file
def load_version():
   try:
       with open('version.json', 'r') as file:
           data = json.load(file)
           return data['version']
   except (FileNotFoundError, json.JSONDecodeError):
       return "1.96"  # Default version if file does not exist or is invalid
# Function to copy the command to clipboard
# Function to load hidden imports from a JSON file
def load_hidden_imports():
   try:
       with open('hidden_imports.json', 'r') as file:
           data = json.load(file)
           return data['hidden_imports']
   except (FileNotFoundError, json.JSONDecodeError):
       # Return an empty list if file does not exist or is invalid
       return []
# Function to save the hidden imports to a JSON file
def save_hidden_imports(hidden_imports):
   with open('hidden_imports.json', 'w') as file:
       json.dump({'hidden_imports': hidden_imports}, file)
def copy_to_clipboard(command):
   pyperclip.copy(command)
   print("Command copied to clipboard!")
# Function to save the version to a JSON file
def save_version(version):
   with open('version.json', 'w') as file:
       json.dump({'version': version}, file)
# Function to update the command with the new version
def update_command(version, additional_module):
   # Load the hidden imports
   hidden_imports = load_hidden_imports()
   # Split the input on space
   input_parts = additional_module.split()
   # Check if the input is meant to delete the last hidden import
   if additional_module.lower() == "del" and hidden_imports:
       hidden_imports.pop()  # Remove the last item from the list
   # Check if the input is meant to delete a specific hidden import
   elif len(input_parts) == 2 and input_parts[1].lower() == "del":
       module_to_delete = input_parts[0]
       if module_to_delete in hidden_imports:
           hidden_imports.remove(module_to_delete)  # Delete the specified module
   # If there's an additional module, add it to the list
   elif additional_module and "del" not in input_parts:
       hidden_imports.append(additional_module)
   # Save the updated hidden imports list
   save_hidden_imports(hidden_imports)
   save_version(version)  # Save the version when updated
   # Split the command template before and after 'main.py'
   command_template_before_main = "pyinstaller --name=App_Name{} --distpath=dist --splash=bin/images/splash.png --icon=bin/icons/sprx.ico --onefile"
   command_template_after_main = "main.py"
   
   ## If there's an additional module, add it to the list
   #if additional_module:
   #    hidden_imports.append(additional_module)
   # Join all hidden imports with the '--hidden-import=' prefix
   hidden_imports_str = " --hidden-import=".join(hidden_imports)
   # Combine everything into the updated command
   updated_command = f"{command_template_before_main} --hidden-import={hidden_imports_str} {command_template_after_main}".format(version)
    # Save the updated hidden imports list
   save_hidden_imports(hidden_imports)

   
   # Save the updated command to a JSON file
   with open('updated_command.json', 'w') as file:
       json.dump({'updated_command': updated_command}, file)
   # Call the copy function with the updated command
   copy_to_clipboard(updated_command)
   
    # Ask the user if they want to run the command
   answer = messagebox.askyesno("Pyinstall", f"You are about to deploy a new version of {command_template_before_main[19:30]} {version} with a hooks list: {hidden_imports_str} and {command_template_after_main}. Proceed?")
   if answer:
       # Execute the updated command in a separate thread
       execute_in_thread(updated_command)
       messagebox.showinfo("Pyinstall", "The app is beaing created, watch the process in the console instance!")
# Function to update the Spinbox with the current version
def set_spinbox_value(spinbox, value):
   spinbox.delete(0, 'end')  # Remove the current value
   spinbox.insert(0, value)  # Insert the new value

# Create the main window
root = tk.Tk()
root.title("App Version Deployer")
# Load the current version from the JSON file
current_version = load_version()

descripiption_frame = ttk.Frame(root)
descripiption_frame.pack()
description_label = ttk.Label(descripiption_frame, text="Choose the version to deploy it:")
description_label.pack(side="left")
description_right_label = ttk.Label(descripiption_frame, text="Or just press 'Enter' to deploy current version")
description_right_label.pack(side="right")
# Create a Spinbox widget for version update

version_spinbox = Spinbox(root, from_=0, to=99, format="%.2f", increment=0.01, command=lambda: update_command(version_spinbox.get(), additional_module_entry.get()))
set_spinbox_value(version_spinbox, current_version)  # Set the loaded version using the new function
version_spinbox.pack(pady=20)

description_frame = ttk.Frame(root)
description_frame.pack()
entry_description_label = ttk.Label(description_frame, text="To add a new hidden import just type it in the entry and it will appear with the next deploy;", wraplength=200)
entry_description_label.pack(side="left", padx=20)
entry_description_right_label = ttk.Label(description_frame, text="To delete a hidden import type the name of it and 'del', to delete the last one element, just type 'del'", wraplength=200)
entry_description_right_label.pack(side="right")
# Create an Entry widget to input additional module
additional_module_entry = ttk.Entry(root)
additional_module_entry.pack(pady=10)
version_spinbox.bind("<Return>", lambda event: update_command(version_spinbox.get(), additional_module_entry.get()))
additional_module_entry.bind("<Return>", lambda event: update_command(version_spinbox.get(), additional_module_entry.get()))
run_button = tk.Button(root, text="Run CMD", command=run_cmd)
run_button.pack(pady=20)
# Run the application
root.mainloop()