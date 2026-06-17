import sys


def main():
    while True:
        sys.stdout.write("$ ")

        command = input()

        # type
        valid_builitins = ["exit", "echo", "type"]
        if command.startswith("type "):
            builitin = command.split(" ")
            if builitin[1] in valid_builitins:
                print(f"{builitin[1]} is a shell builtin")
            else:
                print(f"{builitin[1]}: not found")
                # echo
        elif command.startswith("echo "):
            print(command[5:])
        else:
            print(f"{command}: command not found")

        # exit
        if command == "exit":
            break
        




if __name__ == "__main__":
    main()