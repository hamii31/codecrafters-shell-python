import sys
import subprocess
import shlex
import os
import readline

PATH=os.getenv("PATH")
HOME=os.getenv("HOME")
VALID_BUILTINS = ["exit", "echo", "type", "pwd", "cd"]

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

def display_matches(substitution, matches, longest_match_len):
    print()
    print("  ".join(sorted(matches)))

    sys.stdout.write("$ " + readline.get_line_buffer())
    sys.stdout.flush()

def completer(text, state):
    # builtin execs
    matches = [b + " " for b in VALID_BUILTINS if b.startswith(text)]

    # custom execs
    if not matches:
        for directory in PATH.split(":"):
            try:
                entries = os.listdir(directory)
            except (FileNotFoundError, NotADirectoryError, PermissionError):
                continue
            
            for name in entries:
                if name.startswith(text) and name not in VALID_BUILTINS:
                    full_path = os.path.join(directory, name)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        matches.append(name + " ")
    # files
    if not matches:
        current_directory = os.getcwd()
        try:
            entries = os.listdir(current_directory)
        except (FileNotFoundError, NotADirectoryError, PermissionError):
            return
                
        for name in entries:
            if name.startswith(text):
                full_path = os.path.join(directory, name)
                if os.path.isfile(full_path):
                    matches.append(name + " ")

    if state < len(matches):
        return matches[state]
    return None

def main():

    while True:
        sys.stdout.write("$ ")

        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
        readline.set_completion_display_matches_hook(display_matches)

        command = input()

        args = shlex.split(command)
        if not args:
            continue

        cmd = args[0]

        # Execute builtins with priority
        if cmd == "exit":
            break

        if (">" in args or "1>" in args) or (">>" in args or "1>>" in args):
            redirect_token = next((i for i in args if i in (">", "1>", ">>", "1>>")), None)
            
            mode = "w"
            if redirect_token == ">>" or redirect_token == "1>>":
                mode = "a"

            redir_index = args.index(redirect_token)

            exec_command = args[:redir_index]
            file_path = args[redir_index + 1]
            try:
                result = subprocess.run(exec_command, capture_output=True, text=True)
            except (FileNotFoundError, subprocess.SubprocessError) as e:
                print(e)
                continue

            with open(file_path, mode) as file:
                file.write(result.stdout)

            if result.stderr:
                print(result.stderr, end="")

            continue

        if "2>" in args or "2>>" in args:
            redirect_token = "2>" if "2>" in args else "2>>"
            mode = "w"
            
            if redirect_token == "2>>":
                mode = "a"

            redir_index = args.index(redirect_token)

            exec_command = args[:redir_index]
            file_path = args[redir_index + 1]

            try:
                result = subprocess.run(exec_command, capture_output=True, text=True)
            except (FileNotFoundError, subprocess.SubprocessError) as e:
                print(e)
                continue

            with open(file_path, mode) as file:
                file.write(result.stderr)

            if result.stdout:
                print(result.stdout, end="")

            continue

        if cmd == "echo":
            print(" ".join(args[1:]))
            continue

        if cmd == "type":
            target = args[1]
            if target in VALID_BUILTINS:
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