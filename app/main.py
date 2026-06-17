import sys
import os


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
                print(os.path.exists(f"/usr/{builtin[1]}"))
                print(os.path.exists(f"/local/{builtin[1]}"))
                print(os.path.exists(f"/bin/{builtin[1]}"))
        # echo
        elif command.startswith("echo "):
            print(command[5:])
        else:
            print(f"{command}: command not found")
        




if __name__ == "__main__":
    main()