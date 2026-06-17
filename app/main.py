import sys
import os


def main():
    while True:
        PATH="/usr/bin:/usr/local/bin:$PATH"

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
                path_dirs = PATH.split("/")
                for dir in path_dirs:
                    if os.path.exists(f"{dir}/{builtin[1]}"):
                        print(f"{builtin[1]} is {dir}/{builtin[1]}")

        # echo
        elif command.startswith("echo "):
            print(command[5:])
        else:
            print(f"{command}: command not found")
        




if __name__ == "__main__":
    main()