import sys
import os
PATH=os.environ.get("PATH")

def exists_and_executable(command):
    # Go through PATH
    path_dirs = PATH.split(":")
    for dir in path_dirs:
        path = f"{dir}/{command}"
        if os.path.exists(path) and os.access(path, os.X_OK):
            print(f"{command} is {dir}/{command}")
            return True
        
    return False

def main():
    while True:

        sys.stdout.write("$ ")

        command = input()

        # exit
        if command == "exit":
            break

        # type
        valid_builitins = ["exit", "echo", "type"]
        if command.startswith("type "):
            builtin = command.split(" ")
            if builtin[1] in valid_builitins:
                print(f"{builtin[1]} is a shell builtin")
                break
            else:
                if not exists_and_executable(builtin[1]):
                    print(f"{builtin[1]}: not found")

        # echo
        elif command.startswith("echo "):
            print(command[5:])
        else:
            print(f"{command}: command not found")
        




if __name__ == "__main__":
    main()