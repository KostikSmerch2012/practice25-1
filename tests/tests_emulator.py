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

import emulator


class TestEmulatorStage3(unittest.TestCase):
    """Тестирование функционала VFS на Этапе 3."""

    def setUp(self):
        """Инициализация тестовой VFS в памяти перед тестом."""
        emulator.VFS = {
            "root": {
                "type": "dir",
                "children": {
                    "test.txt": {"type": "file"},
                    "subdir": {
                        "type": "dir",
                        "children": {},
                    },
                },
            }
        }
        emulator.CURRENT_DIR = ["root"]

    def test_ls_root(self):
        """Проверка вывода команды ls."""
        res = emulator.cmd_ls()
        self.assertIn("test.txt", res)
        self.assertIn("subdir", res)

    def test_cd_valid(self):
        """Проверка успешной смены директории."""
        err = emulator.cmd_cd(["subdir"])
        self.assertEqual(err, "")
        self.assertEqual(
            emulator.CURRENT_DIR,
            ["root", "subdir"],
        )

    def test_cd_invalid(self):
        """Проверка cd в несуществующую директорию."""
        err = emulator.cmd_cd(["wrong_dir"])
        self.assertIn("No such directory", err)


if __name__ == "__main__":
    unittest.main()
