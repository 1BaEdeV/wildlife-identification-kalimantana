import shutil
import os
import random
import yaml

# Загружаем параметры из params.yaml
with open('params.yaml') as f:
    params = yaml.safe_load(f)

N = params['prepare']['samples_per_class']
initialdir = params['prepare']['source_path']
targetdir = "training_dataset"


script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
targetdir = os.path.join(project_root, "training_dataset")

# Очищаем старую папку
if os.path.exists(targetdir):
    shutil.rmtree(targetdir)
os.makedirs(targetdir)

# Ваш код копирования (немного адаптированный)
for class_name in os.listdir(initialdir):
    class_path = os.path.join(initialdir, class_name)
    if not os.path.isdir(class_path):
        continue
    
    target_class_dir = os.path.join(targetdir, class_name)
    os.makedirs(target_class_dir, exist_ok=True)
    
    photos_dir = os.path.join(class_path, "all_photos")
    if not os.path.exists(photos_dir):
        print(f" Нет папки all_photos в {class_name}")
        continue
    
    all_photos = [f for f in os.listdir(photos_dir) 
                  if os.path.isfile(os.path.join(photos_dir, f))]
    
    if len(all_photos) < N:
        selected_photos = all_photos
        print(f" В классе {class_name} только {len(all_photos)} фото")
    else:
        selected_photos = random.sample(all_photos, N)
    
    for photo in selected_photos:
        src_path = os.path.join(photos_dir, photo)
        dst_path = os.path.join(target_class_dir, photo)
        shutil.copy2(src_path, dst_path)
    
    print(f" {class_name}: {len(selected_photos)} фото")
