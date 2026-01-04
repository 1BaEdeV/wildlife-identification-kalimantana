import os
from pathlib import Path
import sys

def count_folder_contents(target_folder):
    """
    Подсчитывает содержимое всех папок в указанной директории
    """
    if not os.path.exists(target_folder):
        print(f"Ошибка: Папка '{target_folder}' не существует!")
        return
    
    if not os.path.isdir(target_folder):
        print(f"Ошибка: '{target_folder}' не является папкой!")
        return
    
    print(f"Анализ папки: {target_folder}")
    print("=" * 50)
    
    total_folders = 0
    total_files = 0
    total_size = 0
    
    # Проходим по всем элементам в целевой папке
    for item in os.listdir(target_folder):
        item_path = os.path.join(target_folder, item)
        
        if os.path.isdir(item_path):
            folder_files = 0
            folder_size = 0
            
            # Рекурсивно подсчитываем файлы в подпапке
            for root, dirs, files in os.walk(item_path):
                folder_files += len(files)
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        folder_size += os.path.getsize(file_path)
                    except:
                        pass
            
            total_folders += 1
            total_files += folder_files
            total_size += folder_size
            
            # Конвертируем размер в читаемый формат
            if folder_size < 1024:
                size_str = f"{folder_size} Б"
            elif folder_size < 1024**2:
                size_str = f"{folder_size/1024:.2f} КБ"
            elif folder_size < 1024**3:
                size_str = f"{folder_size/(1024**2):.2f} МБ"
            else:
                size_str = f"{folder_size/(1024**3):.2f} ГБ"
            
            print(f"📁 {item}:")
            print(f"   Файлов: {folder_files}")
            print(f"   Размер: {size_str}")
            print()
    
    # Итоговая статистика
    print("=" * 50)
    print(f"ИТОГО:")
    print(f"Папок: {total_folders}")
    print(f"Всего файлов: {total_files}")
    
    # Конвертируем общий размер
    if total_size < 1024:
        total_size_str = f"{total_size} Б"
    elif total_size < 1024**2:
        total_size_str = f"{total_size/1024:.2f} КБ"
    elif total_size < 1024**3:
        total_size_str = f"{total_size/(1024**2):.2f} МБ"
    else:
        total_size_str = f"{total_size/(1024**3):.2f} ГБ"
    
    print(f"Общий размер: {total_size_str}")

if __name__ == "__main__":
    # Укажите путь к вашей специальной папке
    special_folder = "./inat_from_csv"
    
    # Или используйте аргумент командной строки
    if len(sys.argv) > 1:
        special_folder = sys.argv[1]
    
    count_folder_contents(special_folder)