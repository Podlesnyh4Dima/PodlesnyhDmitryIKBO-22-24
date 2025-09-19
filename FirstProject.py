import os
import shlex
import socket

def repl_emulator():
    try:
        # Получение имени пользователя и имени хоста
        username = os.getlogin()
        hostname = socket.gethostname()
    except (OSError, ImportError, socket.error):
        # Если не удалось получить, используем заглушки
        username = "user"
        hostname = "localhost"

    while True:
        # Формирование приглашения к вводу
        prompt = f"{username}@{hostname}:~$ "
        try:
            user_input = input(prompt)
            # Разделение ввода на команду и аргументы
            parts = shlex.split(user_input)
            if not parts:
                continue

            command = parts[0]
            args = parts[1:]

            # Обработка команд
            if command == "ls":
                print(f"Команда: {command}")
                print(f"Аргументы: {args}")
            elif command == "cd":
                print(f"Команда: {command}")
                print(f"Аргументы: {args}")
            elif command == "exit":
                print("Выход из эмулятора.")
                break
            else:
                print(f"Ошибка: Команда '{command}' не найдена.")

        except EOFError:
            print("\nВыход из эмулятора.")
            break
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    repl_emulator()