import os
import sys
import unittest

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../src",
        )
    )
)

from src.emulator import handle_command, parse_and_expand

class TestEmulator(unittest.TestCase):
    """Тестирование чистой логики эмулятора."""

    def test_empty_input(self):
        """Проверка пустой строки."""
        cmd, args = parse_and_expand("")
        self.assertEqual(cmd, "")
        self.assertEqual(args, [])

    def test_simple_command(self):
        """Проверка парсинга команды."""
        cmd, args = parse_and_expand("ls -la")
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, ["-la"])

    def test_env_expansion(self):
        """Проверка раскрытия переменных."""
        os.environ["TEST_VAR"] = "success"
        cmd, args = parse_and_expand("echo $TEST_VAR")
        self.assertEqual(args, ["success"])

    def test_exit_success(self):
        """Проверка успешного выхода."""
        status, out, err = handle_command("exit", [])
        self.assertFalse(status)
        self.assertEqual(out, "logout")
        self.assertEqual(err, "")

    def test_exit_with_args(self):
        """Проверка exit с ошибкой аргументов."""
        status, out, err = handle_command(
            "exit",
            ["extra"],
        )
        self.assertTrue(status)
        self.assertEqual(err, "exit: too many arguments")

    def test_unknown_command(self):
        """Проверка неизвестной команды."""
        status, out, err = handle_command(
            "invalid",
            [],
        )
        self.assertTrue(status)
        self.assertIn("command not found", err)


if __name__ == "__main__":
    unittest.main()
