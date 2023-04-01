# camiregu
# 2023-mar-22
import config
import json
import os
import shutil


# functions
def start_menu() -> str:
    print(instructions)
    command = ask_for_command()
    result = commands[command]()

    while not isinstance(result,str): #by the time this function is done, a path name will have been produced
        print(instructions)
        command = ask_for_command()
        result = commands[command]()

    return result

def ask_for_command() -> str:
    command = input("Please select a command: ").lower()
    while command not in commands.keys():
        print("I don't recognize that command.")
        command = input("Please select a command: ").lower()
    return command


def load_map() -> str | None:
    with open(config.STORAGE_FILENAME, "r") as storage:
        storage_dict: dict = json.load(storage)

    if len(storage_dict) == 0:
        print("You haven't created any worlds!")
        return

    print("Here are your worlds:")
    world_names = list(storage_dict.keys())
    for i in range(len(world_names)):
        print(str(i) + ") " + world_names[i])

    user_input = input("Select a world by typing its number: ")
    while not (user_input.isdecimal() and 0 <= int(user_input) < len(world_names)): #input validation
        print("Enter an integer between 0 and " + str(len(world_names) - 1))
        user_input = input("Select a world by typing its number: ")
    i = int(user_input)

    path = storage_dict[world_names[i]]
    return path #return the path listed in the json


def create_map() -> str | None:
    map_name = remove_illegal_chars(input("What is your world called? "))

    with open(config.STORAGE_FILENAME, "r") as storage:
        storage_dict: dict = json.load(storage)

    if map_name in storage_dict.keys():
        print("That map already exists.")
        return
        
    os.mkdir(map_name)
    path = os.path.join(map_name, "")
    storage_dict.update({map_name: path})

    with open(config.STORAGE_FILENAME, "w") as storage:
        json.dump(storage_dict, storage)

    with open(path + config.TILEMAP_FILENAME, "w") as tilemap_file: #TODO review
        json.dump({str((0,0,0))[1:-1]: "plains"}, tilemap_file)

    return path


def delete_map() -> None:
    with open(config.STORAGE_FILENAME, "r") as storage:
        storage_dict: dict = json.load(storage)

    print("Here are your worlds:")
    world_names = list(storage_dict.keys())
    for i in range(len(world_names)):
        print(str(i) + ") " + world_names[i])

    user_input = input("Select a world by typing its number: ")
    while not (user_input.isdecimal() and 0 <= int(user_input) < len(world_names)):
        print("Enter an integer between 0 and " + str(len(world_names) - 1))
        user_input = input("Select a world by typing its number: ")
    i = int(user_input)

    if input("Are you sure you want to delete " + world_names[i] + "? (Y/N) ").lower() == "y":
        path = storage_dict.pop(world_names[i])
        shutil.rmtree(path)

        with open(config.STORAGE_FILENAME, "w") as storage:
            json.dump(storage_dict, storage)

        print("Succesfully deleted world map.")
    else:
        print("Operation cancelled.")


def rename_map() -> None:
    with open(config.STORAGE_FILENAME, "r") as storage:
        storage_dict: dict = json.load(storage)

    print("Here are your worlds:")
    world_names = list(storage_dict.keys())
    for i in range(len(world_names)):
        print(str(i) + ") " + world_names[i])

    user_input = input("Select a world by typing its number: ")
    while not (user_input.isdecimal() and 0 <= int(user_input) < len(world_names)):
        print("Enter an integer between 0 and " + str(len(world_names) - 1))
        user_input = input("Select a world by typing its number: ")
    world = int(user_input)

    if input("Are you sure you want to rename " + world_names[world] + "? (Y/N) ").lower() == "y":
        new_name = remove_illegal_chars(input("What would you like to rename it to? "))
        while new_name in storage_dict.keys():
            print("That map already exists.")
            new_name = remove_illegal_chars(input("What would you like to rename it to? "))
    
        old_path = storage_dict.pop(world_names[world])
        os.rename(old_path,new_name)
        new_path = os.path.join(new_name, "")
        storage_dict.update({new_name: new_path})

        with open(config.STORAGE_FILENAME, "w") as storage:
            json.dump(storage_dict, storage)
        print("Succesfully renamed " + world_names[world] + " to " + new_name + ".")
    else:
        print("Operation cancelled.")

def remove_illegal_chars(string: str) -> str:
    return string.replace("<","").replace(">","").replace(":","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","").strip(" .")


# command reference
commands = {
    "l": load_map,
    "c": create_map,
    "d": delete_map,
    "r": rename_map,
    "q": quit
}


# instructions text
instructions = """\nWelcome to Fantasy World Map Generator.
    L)oad a world map from your local files
    C)reate a new world map with custom settings
    D)elete an existing world map
    R)ename an existing world map
    Q)uit the program"""