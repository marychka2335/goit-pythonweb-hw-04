import os
import asyncio
from pathlib import Path
import shutil
import logging
from colorama import Fore, Style, init
import textwrap
import argparse

# Ініціалізуємо colorama
init(autoreset=True)

# Налаштування логування
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")

# Асинхронна функція для копіювання файлів за їх розширенням


async def copy_file(file_path, destination_dir):
    try:
        extension = file_path.suffix[1:].lower(
        ) if file_path.suffix else "unknown"
        target_dir = Path(destination_dir, extension)
        target_dir.mkdir(parents=True, exist_ok=True)
        destination = target_dir / file_path.name

        if destination.exists():
            print(
                Fore.YELLOW + f"Пропущено: Файл {file_path.name} вже існує у папці {target_dir}" + Style.RESET_ALL)
        else:
            # Асинхронне копіювання
            await asyncio.to_thread(shutil.copy2, file_path, destination)
            print(
                Fore.GREEN + f"Копіювання: {file_path} -> {destination}" + Style.RESET_ALL)
    except Exception as e:
        error_message = textwrap.fill(
            f"Помилка копіювання файлу {file_path}: {e}",
            width=100
        )
        logging.error(error_message)
        print(Fore.RED + error_message + Style.RESET_ALL)

# Асинхронна функція для рекурсивного читання папок


async def read_folder(source_dir, destination_dir):
    try:
        tasks = []
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root, file)
                tasks.append(copy_file(file_path, destination_dir))
        await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Помилка при обробці папки {source_dir}: {e}")
        print(
            Fore.RED + f"Помилка при обробці папки {source_dir}: {e}" + Style.RESET_ALL)

# Головна функція


def main():
    # Створення парсера аргументів командного рядка
    parser = argparse.ArgumentParser(
        description="Сортування файлів за розширеннями.")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки.")
    parser.add_argument("destination", type=str,
                        help="Шлях до цільової папки.")
    args = parser.parse_args()

    source_dir = args.source
    destination_dir = args.destination

    # Перевірка існування вихідної папки
    if not Path(source_dir).is_dir():
        print(Fore.RED + "Помилка: Вказана вихідна папка не існує або це не папка." + Style.RESET_ALL)
        return

    print(Fore.CYAN + "Розпочинається процес сортування..." + Style.RESET_ALL)
    asyncio.run(read_folder(source_dir, destination_dir))
    print(Fore.CYAN + "Сортування завершено." + Style.RESET_ALL)


if __name__ == "__main__":
    main()
