"""Лабораторная работа. Этап 1: REPL. Вариант 25. Эмулятор командной строки."""

import os
import getpass
import socket
import sys


def parse_and_expand(user_input):
    """Разбивает строку на команду и аргументы, а также заменяет $ПЕРЕМЕННЫЕ на их значения из ОС.

    Если строка пустая, возвращает пустую команду и пустой список.
    Для аргументов, начинающихся с $, отрезает знак доллара и ищет переменную в os.environ.
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


def run_repl():
    """Запускает главный интерактивный цикл программы эмулятора (CLI-интерфейс).

    Получает имя пользователя и хоста для вывода приглашения.
    Проверяет команду exit на избыток аргументов и завершает работу.
    Выводит информацию для заглушек ls и cd, проверяя cd на количество путей.
    Выводит ошибку 'command not found' в sys.stderr для всех остальных команд.
    Ловит Ctrl+C и Ctrl+D для корректного выхода из терминала.
    """
    username = getpass.getuser()
    hostname = socket.gethostname()

    while True:
        try:
            prompt = f"{username}@{hostname}:~$ "
            user_input = input(prompt).strip()

            if user_input == "":
                continue

            command, args = parse_and_expand(user_input)

            if command == "exit":
                if len(args) > 0:
                    print("exit: too many arguments", file=sys.stderr)
                else:
                    print("logout")
                    break

            elif command == "ls" or command == "cd":
                if command == "cd" and len(args) > 1:
                    print("cd: too many arguments", file=sys.stderr)
                else:
                    print(f"[заглушка] Вызвана команда: {command}")
                    print(f"[заглушка] Переданные аргументы: {args}")

            else:
                print(f"bash: {command}: command not found", file=sys.stderr)

        except (KeyboardInterrupt, EOFError):
            print("\nlogout")
            break


if __name__ == "__main__":
    run_repl()
