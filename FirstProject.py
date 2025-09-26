import os
import getpass
import socket
import argparse
from typing import Tuple, List, Optional

# --- КОНФИГУРАЦИЯ ---
class Configuration:
    """Хранит параметры конфигурации эмулятора."""
    def __init__(self, vfs_path: str, startup_script_path: Optional[str]):
        self.vfs_path = vfs_path
        self.startup_script_path = startup_script_path
        
    def debug_print(self):
        """Отладочный вывод всех заданных параметров (Требование 1)."""
        print("\n--- ОТЛАДОЧНЫЙ ВЫВОД ПАРАМЕТРОВ ---")
        print(f"VFS Path: {self.vfs_path}")
        print(f"Startup Script Path: {self.startup_script_path if self.startup_script_path else 'Не задан'}")
        print("----------------------------------\n")

# --- СЛУЖЕБНЫЕ ФУНКЦИИ ---

def get_prompt():
    """Формирует приглашение к вводу."""
    username = getpass.getuser()
    hostname = socket.gethostname()
    current_dir = "~" 
    return f"{username}@{hostname}:{current_dir}$ "

def parse_input(command_line: str) -> Tuple[Optional[str], List[str]]:
    """Парсер: разделяет строку на команду и аргументы по пробелам."""
    parts = command_line.strip().split()
    if not parts:
        return None, []
    
    command = parts[0]
    arguments = parts[1:]
    return command, arguments

def handle_command(command: Optional[str], arguments: List[str], is_script: bool = False) -> bool:
    """Обрабатывает команду. Возвращает True для продолжения, False для выхода."""
    
    # Обработка пустого ввода
    if not command:
        return True 
        
    # 1. Команды-заглушки ls и cd
    if command in ("ls", "cd"):
        source = "[Скрипт]" if is_script else "[REPL]"
        print(f"{source} Вызвана команда: {command}")
        print(f"Аргументы: {arguments if arguments else '(нет)'}")
        
    # 2. Команда exit
    elif command == "exit":
        print("Завершение работы эмулятора. Пока!")
        return False
        
    # 3. Обработка неизвестной команды
    else:
        # Для скрипта - пропускаем ошибочные строки (Требование 2)
        if is_script:
            print(f"[Скрипт] Ошибка: команда не найдена, пропускаем: {command}")
            # Возвращаем True, чтобы продолжить выполнение скрипта
            return True 
        else:
            # Для REPL - сообщаем об ошибке
            print(f"shell: команда не найдена: {command}")
        
    return True

# --- НОВАЯ ФУНКЦИЯ: ВЫПОЛНЕНИЕ СТАРТОВОГО СКРИПТА ---

def run_startup_script(config: Configuration):
    """Выполняет команды из стартового скрипта с пропуском ошибок (Требование 2)."""
    script_path = config.startup_script_path
    
    if not script_path:
        return

    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            print(f"\n--- ЗАПУСК СТАРТОВОГО СКРИПТА: {os.path.basename(script_path)} ---")
            
            for line_number, line in enumerate(f, 1):
                # Удаляем лишние пробелы и символы новой строки
                command_line = line.strip()
                
                # Пропускаем пустые строки
                if not command_line:
                    continue
                
                # Имитация диалога: отображение ввода (Требование 2)
                print(f"{get_prompt()}{command_line}")
                
                command, arguments = parse_input(command_line)
                
                # Выполнение команды. is_script=True включает логику пропуска ошибок.
                if command:
                    if not handle_command(command, arguments, is_script=True):
                        # Если команда 'exit' вызвана в скрипте
                        print("Прерывание из-за команды 'exit' в скрипте.")
                        return False # Сигнал о завершении работы эмулятора
                    
            print("--- СТАРТОВЫЙ СКРИПТ ЗАВЕРШЕН ---\n")

    except FileNotFoundError:
        print(f"Ошибка: Стартовый скрипт '{script_path}' не найден.")
    except Exception as e:
        print(f"Непредвиденная ошибка при выполнении скрипта: {e}")
        
    return True # Продолжаем работу эмулятора

# --- ОСНОВНАЯ ЛОГИКА ---

def parse_args():
    """Парсит аргументы командной строки (Требование 1)."""
    parser = argparse.ArgumentParser(description="Эмулятор языка оболочки ОС (Вариант 17)")
    
    # 1. Путь к VFS (обязательный)
    parser.add_argument(
        '--vfs-path', 
        type=str, 
        required=True, 
        help='Путь к физическому расположению VFS.'
    )
    
    # 2. Путь к стартовому скрипту (опциональный)
    parser.add_argument(
        '--script', 
        type=str, 
        default=None, 
        help='Путь к стартовому скрипту.'
    )
    
    args = parser.parse_args()
    return Configuration(args.vfs_path, args.script)

def repl(config: Configuration):
    """Основной цикл Read-Eval-Print-Loop."""
    
    should_continue = run_startup_script(config)
    if not should_continue:
        return

    running = True
    while running:
        try:
            command_line = input(get_prompt())
        except (EOFError, KeyboardInterrupt):
            print("\nЗавершение работы эмулятора. Пока!")
            break
            
        command, arguments = parse_input(command_line)
        
        # Выполнение команды. is_script=False для интерактивного режима.
        if command:
            running = handle_command(command, arguments, is_script=False)


if __name__ == "__main__":
    config = parse_args()
    
    print("--- Эмулятор языка оболочки ОС (Вариант 17, Этап 2: Конфигурация) ---")
    config.debug_print() # Отладочный вывод
    
    repl(config)