# Эмулятор командной строки UNIX-подобной ОС

## 1. Общее описание
Проект представляет собой эмулятор командной строки
UNIX-подобной ОС для практических работ по дисциплине
«Конфигурационное управление» (Вариант №25). На
Этапе 3 реализовано подключение виртуальной файловой
системы (VFS), которая полностью загружается из
JSON-файла и обрабатывается внутри оперативной памяти.

## 2. Описание функций и настроек
- **Архитектура:** код использует docstring вместо
  строковых комментариев. Все операции с файлами
  производятся исключительно в памяти.
- **Основные функции:**
  * `parse_and_expand` — парсинг ввода и раскрытие
    переменных окружения реальной ОС.
  * `load_vfs` — чтение JSON-структуры файловой
    системы и обработка ошибок формата/доступа.
  * `get_dir_node` — поиск узла VFS по пути.
  * `run_script` — выполнение стартовых сценариев.
- **Команды:** `exit` (выход), `ls` (вывод списка
  файлов текущей VFS папки), `cd` (смена каталога
  внутри VFS пространства).

## 3. Сборка и запуск
- **Требования:** Python 3.8+, модули `os`, `sys`,
  `getpass`, `socket`, `json`, `argparse`.
- **Запуск со стартовым скриптом:**
  ```bash
  python3 src/emulator.py \
    --vfs "vfs_deep.json" \
    --script "start_vfs.txt"
  ```
- **Запуск интерактивного режима (REPL):**
  ```bash
  python3 src/emulator.py --vfs "vfs_deep.json"
  ```
- **Тесты:** `python3 -m unittest discover -s tests`

## 4. Примеры использования
Пример навигации по виртуальной JSON-системе:
```text
talgat@MacBook-Pro-Talgat.local:~\$ ls
level1
talgat@MacBook-Pro-Talgat.local:~\$ cd level1
talgat@MacBook-Pro-Talgat.local:~\$ ls
level2
talgat@MacBook-Pro-Talgat.local:~\$ cd level2
talgat@MacBook-Pro-Talgat.local:~\$ ls
level3.txt
talgat@MacBook-Pro-Talgat.local:~\$ exit
logout
```
