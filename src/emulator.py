import argparse
import getpass
import json
import os
import socket
import sys

VFS = {}
CURRENT_DIR = ["root"]


def parse_and_expand(user_input):
    """Разбивает строку на команду и аргументы,

    а также заменяет $ПЕРЕМЕННЫЕ на их значения.
    """
    expanded = os.path.expandvars(user_input)
    parts = expanded.split()
    if len(parts) == 0:
        return "", []
    return parts, parts[1:]


def get_dir_node(path_list):
    """Возвращает узел VFS по заданному пути."""
    node = VFS
    for part in path_list:
        if part in node and "children" in node[part]:
            node = node[part]["children"]
        else:
            return None
    return node


def cmd_ls():
    """Выводит список файлов и папок в текущей директории."""
    node = get_dir_node(CURRENT_DIR)
    if node is None:
        return ""
    return "  ".join(sorted(node.keys()))


def cmd_cd(args):
    """Меняет текущую рабочую директорию эмулятора."""
    if not args:
        return ""
    target = args
    if target == "/":
        CURRENT_DIR[:] = ["root"]
        return ""
    parts = [p for p in target.split("/") if p and p != "."]
    new_dir = list(CURRENT_DIR)
    for p in parts:
        if p == "..":
            if len(new_dir) > 1:
                new_dir.pop()
        else:
            new_dir.append(p)
    if get_dir_node(new_dir) is None:
        return f"cd: {target}: No such directory"
    CURRENT_DIR[:] = new_dir
    return ""


def handle_command(command, args):
    """Маршрутизирует вызовы команд."""
    if command == "exit":
        if len(args) > 0:
            return True, "", "exit: too many arguments"
        return False, "logout", ""
    if command == "ls":
        return True, cmd_ls(), ""
    if command == "cd":
        err = cmd_cd(args)
        return True, "", err
    return True, "", f"system: {command}: command not found"


def execute_line(user_input, prompt):
    """Имитирует диалог и выполняет одну строку."""
    print(f"{prompt}{user_input}")
    cleaned = user_input.strip()
    if not cleaned:
        return True
    cmd, args = parse_and_expand(cleaned)
    status, out, err = handle_command(cmd, args)
    if out:
        print(out)
    if err:
        print(err, file=sys.stderr)
    return status


def run_script(script_path, prompt):
    """Последовательно выполняет строки скрипта."""
    if not os.path.exists(script_path):
        print(f"Ошибка: Скрипт не найден!", file=sys.stderr)
        return
    print(f"\n--- Запуск скрипта: {script_path} ---")
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            for line in f:
                content = line.rstrip("\r\n")
                if not content:
                    continue
                if not execute_line(content, prompt):
                    break
    except Exception as e:
        print(f"Ошибка чтения: {e}", file=sys.stderr)
    print("--- Завершение работы скрипта ---\n")


def load_vfs(vfs_path):
    """Загружает VFS из JSON файла в память."""
    global VFS
    if not os.path.exists(vfs_path):
        print("Ошибка загрузки VFS: файл не найден", file=sys.stderr)
        sys.exit(1)
    try:
        with open(vfs_path, "r", encoding="utf-8") as f:
            VFS = json.load(f)
    except (json.JSONDecodeError, TypeError):
        print("Ошибка загрузки VFS: неверный формат", file=sys.stderr)
        sys.exit(1)


def run_repl():
    """Запускает главный цикл или скрипт."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs")
    parser.add_argument("--script")
    args = parser.parse_args()
    if not args.vfs:
        print("Ошибка: Передайте параметр --vfs", file=sys.stderr)
        sys.exit(1)
    load_vfs(args.vfs)
    username = getpass.getuser()
    hostname = socket.gethostname()
    prompt = f"{username}@{hostname}:~$ "
    if args.script:
        run_script(args.script, prompt)
        return
    while True:
        try:
            user_input = input(prompt)
            if not execute_line(user_input, prompt):
                break
        except (KeyboardInterrupt, EOFError):
            print("\nlogout")
            break


if __name__ == "__main__":
    run_repl()
