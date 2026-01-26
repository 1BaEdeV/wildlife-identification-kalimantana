import streamlit as st
import io
import os
from PIL import Image
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
import faiss
import sqlite3
import json

# Загрузка основной модели
def load_model():
    model = keras.models.load_model(r'E:\ULTIMATE_PROJECT\wildlife-identification-kamchatka\models\monkey_classifier.h5')
    return model

# Загрузка FAISS и SQLite
def load_vector_db():
    index = faiss.read_index(r'E:\ULTIMATE_PROJECT\wildlife-identification-kamchatka\db\faiss_index.bin')
    conn = sqlite3.connect(r'E:\ULTIMATE_PROJECT\wildlife-identification-kamchatka\db\database.db')
    conn.row_factory = sqlite3.Row
    
    return index, conn

# Извлечение эмбеддинга для поиска похожих
def extract_embedding_for_search(img):
    # Та же модель EfficientNet, что и для создания базы
    from tensorflow.keras.applications import EfficientNetB0
    model = EfficientNetB0(
        weights='imagenet',
        include_top=False,
        pooling='avg'
    )
    
    img_array = preprocess_image(img)
    embedding = model.predict(img_array, verbose=0)[0]
    return embedding

# Поиск похожих изображений
def find_similar_images(query_embedding, index, conn, top_k=3):
    # Поиск в FAISS
    distances, indices = index.search(np.array([query_embedding]).astype('float32'), top_k)
    # Получение информации из SQLite
    similar_images = []
    cursor = conn.cursor()
    
    for idx, distance in zip(indices[0], distances[0]):
        cursor.execute('SELECT filename, filepath, species FROM monkey_images WHERE faiss_index = ?', (int(idx),))
        row = cursor.fetchone() 
        if row:
            # Конвертирирование расстояния в схожесть (0-1)
            similarity = 1.0 / (1.0 + distance)
            similar_images.append({
                'path': row['filepath'],
                'species': row['species'],
                'similarity': float(similarity)
            })
    return similar_images

def preprocess_image(img):
    img = img.resize((224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)
    x = preprocess_input(x)
    return x

def load_image():
    uploaded_file = st.file_uploader(label = "Upload a photo of a monkey", type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data, caption="Загруженное изображение", width=300)
        return Image.open(io.BytesIO(image_data))
    else:
        return None


model = load_model()
index, conn = load_vector_db()
class_names = ['Cephalopachus bancanus','Hylobates albibarbis','Hylobates funereus' ,'Macaca fascicularis' ,'Macaca nemestrina' ,'Nasalis larvatus' ,'Nycticebus menagensis' ,'Pongo pygmaeus' ,'Presbytis hosei' ,'Presbytis rubicunda' ,'Trachypithecus cristatus']
st.title("Bornean Ape Classifier")
img = load_image()
result = st.button("Classify and Find Similar")

if result and img:
    x = preprocess_image(img)
    pred = model.predict(x, verbose=0)
    class_idx = np.argmax(pred[0])
    conf = pred[0][class_idx]
    
    st.write("## Classification Result")
    st.write(f"**Your Monkey is:** {class_names[class_idx]}")
    st.write(f"**Confidence:** {conf:.2%}")
    

    st.write("## Similar Images")
    # Извлечение эмбеддингов для поиска
    query_embedding = extract_embedding_for_search(img)
    # Поиск похожих
    similar_images = find_similar_images(query_embedding, index, conn, top_k=3)
    if similar_images:
        # Показываем похожие изображения в колонках
        cols = st.columns(3)
        for i, sim_img in enumerate(similar_images):
            with cols[i]:
                if os.path.exists(sim_img['path']):
                    # Загружаем и показываем изображение
                    sim_image = Image.open(sim_img['path'])
                    st.image(sim_image, width=200)
                else:
                    st.write(f"Image not found")
    else:
        st.write("No similar images found in database")
        
elif result and not img:
    st.write("Please upload an image first!")
    
# Закрываем соединение при завершении
conn.close()