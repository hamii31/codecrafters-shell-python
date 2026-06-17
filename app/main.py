import sys


def main():
    while True:
        sys.stdout.write("$ ")

        command = input()

        # exit
        if command == "exit":
            break
        
        # echo
        if command.startswith("echo "):
            print(command[5:])
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
