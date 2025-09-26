#!/bin/bash
PYTHON_EXECUTABLE=python # Замените на python3, если необходимо
EMULATOR_SCRIPT=FirstProject.py

echo "--- Тест 1: Запуск только с обязательным VFS-path (Интерактивный режим) ---"
$PYTHON_EXECUTABLE $EMULATOR_SCRIPT --vfs-path /vfs/data

echo "--- Тест 2: Запуск со Стартовым скриптом (start.sh) ---"
# Примечание: Убедитесь, что файл start.sh существует в текущей директории
$PYTHON_EXECUTABLE $EMULATOR_SCRIPT --vfs-path /vfs/data --script start.sh

echo "--- Тест 3: Запуск с несуществующим VFS-path (VFS-path все равно принимается) ---"
$PYTHON_EXECUTABLE $EMULATOR_SCRIPT --vfs-path /invalid/path/to/vfs

echo "--- Тест 4: Запуск с несуществующим Скриптом (Вывод ошибки и переход в REPL) ---"
$PYTHON_EXECUTABLE $EMULATOR_SCRIPT --vfs-path /vfs/data --script non_existent_script.sh

echo "--- Тестирование завершено ---"