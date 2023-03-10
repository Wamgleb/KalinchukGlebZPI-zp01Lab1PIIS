# -*- coding: utf-8 -*-
"""Lab1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oTFKu0mKI4Z_bx2mwVb1wtC4YCci3PSE
"""

# Імпорт бібліотек та класів
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
import matplotlib.pyplot as plt
from google.colab import files

# Підготовка датасетів від Microsoft
train, _ = tfds.load('cats_vs_dogs', split=['train[:100%]'], with_info=True, as_supervised=True)

# Функція для зміни розміру зображення. Вона потрібна для уніфікації зобаражень
# Також це пришвидчить час обробки нейромережею фото 
SIZE = (224, 224)

def resize_image(img, label):
	img = tf.cast(img, tf.float32)
	img = tf.image.resize(img, SIZE)
	img /= 255.0
	return img, label

# Зменшуемо усі зображення з датасету
train_resized = train[0].map(resize_image)
train_batches = train_resized.shuffle(1000).batch(16)

# Створюжмо основний слой моделі
base_layers = tf.keras.applications.MobileNetV2(input_shape=(SIZE[0], SIZE[1], 3), include_top=False)

# Створення моделі нейромержі
model = tf.keras.Sequential([
	base_layers,
	GlobalAveragePooling2D(),
	Dropout(0.2),
	Dense(1)
])
model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

# Навчання
model.fit(train_batches, epochs=1)

# Функція для завантаження зображень
x = files.upload()

for i in x:
  my_input = [].append(i)
  print(my_input)

# тут ми вказуємо назві завантажених фото 
images = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg"]

# Перетворюємо усі зображення и визначаємо об'єкт на фото
for i in images:
	img = load_img(i)
	img_array = img_to_array(img)
	img_resized, _ = resize_image(img_array, _)
	img_expended = np.expand_dims(img_resized, axis=0)
	prediction = model.predict(img_expended)
	plt.figure()
	plt.imshow(img)
	label = 'Dog' if prediction > 10 else 'Cat'
	plt.title('{}'.format(label))