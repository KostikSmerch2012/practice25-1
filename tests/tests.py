import unittest
import os
import sys

from src import emulator

# Добавляем директорию src в путь поиска модулей, чтобы импортировать функцию
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.emulator import parse_and_expand

class TestEmulatorParser(unittest.TestCase):
    def test_empty_input(self):
        """Проверка обработки пустой строки."""
        cmd, args = parse_and_expand("")
        self.assertEqual(cmd, "")
        self.assertEqual(args, [])

    def test_simple_command(self):
        """Проверка обычного разделения команды и аргументов."""
        cmd, args = parse_and_expand("ls -la /home")
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, ["-la", "/home"])

    def test_environment_expansion(self):
        """Проверка подстановки существующих переменных окружения."""
        os.environ["TEST_VAR"] = "success"
        cmd, args = parse_and_expand("echo $TEST_VAR")
        self.assertEqual(args, ["success"])

if __name__ == "__main__":
    unittest.main()
