#!/bin/bash
echo "=== ТЕСТ 1: Минимальная VFS ==="
python3 src/emulator.py --vfs "vfs_min.json" --script "start_vfs.txt"

echo "=== ТЕСТ 2: Глубокая VFS (3 уровня) ==="
python3 src/emulator.py --vfs "vfs_deep.json" --script "start_vfs.txt"

echo "=== ТЕСТ 3: Ошибка загрузки (неверный формат) ==="
echo "not a json" > broken.json
python3 src/emulator.py --vfs "broken.json"
