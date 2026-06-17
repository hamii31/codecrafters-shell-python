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

        # type
        valid_builitins = ["exit", "echo", "type"]
        if command.startswith("type "):
            builitin = command.split(" ")
            if builitin in valid_builitins:
                print(f"{builitin} is a shell builtin")
            else:
                print(f"{builitin}: not found")


if __name__ == "__main__":
    main()
