import sys
import subprocess
import shlex
import os

PATH=os.getenv("PATH")
HOME=os.getenv("HOME")

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

        args = shlex.split(command)
        if not args:
            continue

        cmd = args[0]

        # Execute builtins with priority
        if cmd == "exit":
            break

        if ">" in args or "1>" in args:
            redirect_token = ">" if ">" in args else "1>"
            redir_index = args.index(redirect_token)

            exec_command = args[:redir_index]
            file_path = args[redir_index + 1]
            try:
                result = subprocess.run(exec_command, capture_output=True, text=True)
            except (FileNotFoundError, subprocess.SubprocessError) as e:
                print(e)
                continue

            with open(file_path, "w") as file:
                file.write(result.stdout)

            if result.stderr:
                print(result.stderr, end="")

            continue

        if "2>" in args:
            redir_index = args.index("2>")
            
            exec_command = args[:redir_index]
            file_path = args[redir_index + 1]

            try:
                result = subprocess.run(exec_command, capture_output=True, text=True)
            except (FileNotFoundError, subprocess.SubprocessError) as e:
                print(e)
                continue

            with open(file_path, "w") as file:
                file.write(result.stderr)

            if result.stdout:
                print(result.stdout, end="")

            continue

        if ">>" in args or "1>>" in args:
            redirect_token = ">>" if ">>" in args else "1>>"
            redir_index = args.index(redirect_token)
        
            exec_command = args[:redir_index]
            file_path = args[redir_index + 1]
            try:
                result = subprocess.run(exec_command, capture_output=True, text=True)
            except (FileNotFoundError, subprocess.SubprocessError) as e:
                print(e)
                continue
        
            with open(file_path, "a") as file:
                file.write(result.stdout)
        
            if result.stderr:
                print(result.stderr, end="")
        
            continue



        if cmd == "echo":
            print(" ".join(args[1:]))
            continue

        if cmd == "type":
            valid_builtins = ["exit", "echo", "type", "pwd", "cd"]
            target = args[1]
            if target in valid_builtins:
                print(f"{target} is a shell builtin")
            else:
                executable, path = exists_and_executable(target)
                if executable:
                    print(f"{target} is {path}")
                else:
                    print(f"{target}: not found")
            continue

        if cmd == "pwd":
            print(os.getcwd())
            continue

        if cmd == "cd":
            path = args[1]
            if path == "~":
                os.chdir(HOME)
            elif os.path.exists(path):
                os.chdir(path)
            else:
                print(f"cd: {path}: No such file or directory")
            continue

        # then check for custom execs
        executable, path = exists_and_executable(cmd)
        if executable:
            subprocess.run(args)
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    main()