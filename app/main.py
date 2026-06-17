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
            print(builitin[1])
            if builitin[1] in valid_builitins:
                print(f"{builitin[1]} is a shell builtin")
            else:
                print(f"{builitin[1]}: not found")


if __name__ == "__main__":
    main()