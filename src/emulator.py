"""Лабораторная работа. Этап 1: REPL. Вариант 25. Эмулятор командной строки."""

import os
import getpass
import socket
import sys


def parse_and_expand(user_input):
    """Разбивает строку на команду и аргументы,
    а также заменяет $ПЕРЕМЕННЫЕ на их значения из ОС.

    Если строка пустая, возвращает пустую команду и пустой список.
    Для аргументов, начинающихся с $,
    отрезает знак доллара и ищет переменную в os.environ.
    """
    parts = user_input.split()
    if len(parts) == 0:
        return "", []

    command = parts[0]
    args = parts[1:]

    for i in range(len(args)):
        if args[i].startswith("$"):
            var_name = args[i][1:]
            args[i] = os.environ.get(var_name, "")

    return command, args


def handle_command(command, args):
    """Обрабатывает введенную команду и возвращает True,
    если нужно продолжить цикл, или False для выхода."""

    if command == "exit":
        if len(args) > 0:
            print("exit: too many arguments", file=sys.stderr)
            return True
        print("logout")
        return False

    if command in ("ls", "cd"):
        if command == "cd" and len(args) > 1:
            print("cd: too many arguments", file=sys.stderr)
        else:
            print(f"[user] Вызвана команда {command}")
            print(f"[user] Переданные аргументы {args}")
        return True

    print(f"system: {command}: command not found", file=sys.stderr)
    return True


def run_repl():
    """Запускает главный интерактивный цикл программы (CLI-интерфейс)."""
    username = getpass.getuser()
    hostname = socket.gethostname()

    while True:
        try:
            user_input = input(f"{username}@{hostname}:~$ ").strip()
            if not user_input:
                continue

            command, args = parse_and_expand(user_input)
            if not handle_command(command, args):
                break

        except (KeyboardInterrupt, EOFError):
            print("\nlogout")
            break


if __name__ == "__main__":
    run_repl()
