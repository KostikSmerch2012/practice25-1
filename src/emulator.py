import argparse
import getpass
import os
import socket
import sys


def parse_and_expand(user_input):
    """Разбивает строку на команду и аргументы,

    а также заменяет $ПЕРЕМЕННЫЕ на их значения.
    """
    expanded = os.path.expandvars(user_input)
    parts = expanded.split()
    if len(parts) == 0:
        return "", []
    return parts[0], parts[1:]


def handle_command(command, args):
    """Обрабатывает команду.

    Возвращает (bool_продолжать, str_вывод, str_ошибка).
    """
    if command == "exit":
        if len(args) > 0:
            return True, "", "exit: too many arguments"
        return False, "logout", ""

    if command in ("ls", "cd"):
        out = (
            f"[user] Вызвана команда {command}\n"
            f"[user] Аргументы {args}"
        )
        return True, out, ""

    err = f"system: {command}: command not found"
    return True, "", err


def execute_line(user_input, prompt):
    """Имитирует диалог и выполняет одну строку.

    Возвращает True, если цикл продолжается.
    """
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
        print(
            f"Ошибка: Скрипт не найден!",
            file=sys.stderr,
        )
        return

    print(f"\n--- Запуск скрипта: {script_path} ---")
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                content = line.rstrip("\r\n")
                if not content:
                    continue
                if not execute_line(content, prompt):
                    break
    except Exception as e:
        print(f"Ошибка чтения: {e}", file=sys.stderr)
    print("--- Завершение работы скрипта ---\n")


def print_debug(args):
    """Выводит отладочную информацию."""
    print("=== ОТЛАДОЧНЫЙ ВЫВОД ПАРАМЕТРОВ ===")
    print(f"Путь к VFS: {args.vfs}")
    script_info = args.script if args.script else "Нет"
    print(f"Стартовый скрипт: {script_info}")
    print("===================================\n")


def run_repl():
    """Запускает главный цикл или скрипт."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs")
    parser.add_argument("--script")
    args = parser.parse_args()

    if not args.vfs:
        print(
            "Ошибка: Передайте параметр --vfs",
            file=sys.stderr,
        )
        sys.exit(1)

    print_debug(args)
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
