import sys
import os
PATH=os.environ.get("PATH")

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
                # Go through PATH
                path_dirs = PATH.split(":")
                for dir in path_dirs:
                    path = f"{dir}/{builtin[1]}"
                    if os.path.exists(path) and os.access(path, os.X_OK):
                        print(f"{builtin[1]} is {dir}/{builtin[1]}")
                        break
                    else:
                        (f"{builtin[1]}: command not found")

        # echo
        elif command.startswith("echo "):
            print(command[5:])
        else:
            print(f"{command}: command not found")
        




if __name__ == "__main__":
    main()