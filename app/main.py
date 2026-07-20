import sys
import subprocess

import os
PATH=os.environ.get("PATH")

def exists_and_executable(command):
    """
    Iterates through the PATH and finds if a file exists and is executable
    """
    path_dirs = PATH.split(":")
    for dir in path_dirs:
        path = f"{dir}/{command}"
        if os.path.exists(path) and os.access(path, os.X_OK):
            return True, f"{dir}/{command}"
        
    return False, None

def main():
    while True:

        sys.stdout.write("$ ")

        command = input()

        # exit
        if command == "exit":
            break

        # custom command
        custom_args = command.split(" ")
        executable, path = exists_and_executable(custom_args[0])
        if executable:
            subprocess.run(custom_args)
            continue
        else:
            # type
            valid_builtins = ["exit", "echo", "type", "pwd", "cd"]
            if command.startswith("type "):
                builtin = command.split(" ")
                if builtin[1] in valid_builtins:
                    print(f"{builtin[1]} is a shell builtin")
                    continue
                else:
                    executable, path = exists_and_executable(builtin[1])
                    if executable:
                        print(f"{builtin[1]} is {path}")
                        continue
                    if not executable:
                        print(f"{builtin[1]}: not found")
                        continue
            # cd
            if command.startswith("cd "):
                path = command.split("/")
                path = ''.join(path)
                if os.path.exists(path):
                    os.chdir(path)
                    continue
                else:
                    print(f"cd: {path}: No such file or directory")
                    continue
            
            # pwd
            if command.startswith("pwd"):
                print(os.getcwd())
                continue
            # echo
            if command.startswith("echo "):
                print(command[5:])
                continue
            else:
                print(f"{custom_args[0]}: command not found")
                continue

if __name__ == "__main__":
    main()

# cd codecrafters-shell-python/app