# -*- coding: utf-8 -*-
"""Mango-Leaf-Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nj8dIlhTQBzwTHZ1MdxLlYMQnLdz6EWr
"""

from google.colab import drive
drive.mount('/content/drive')

!ls /content/

import zipfile

dataset_path = "/content/drive/MyDrive/CSE465/Mango"  # Make sure this matches the exact file name

print("✅ Dataset extracted successfully!")

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Set directories
original_data_dir = "/content/drive/MyDrive/CSE465/Mango"  # Folder with original images
augmented_data_dir = "/content/augmented_dataset"  # Folder for augmented images
os.makedirs(augmented_data_dir, exist_ok=True)

# Create an ImageDataGenerator for augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Load original images and apply augmentation
batch_size = 32
num_augmented_images = 0

for class_name in os.listdir(original_data_dir):  # Loop through each category
    class_path = os.path.join(original_data_dir, class_name)
    save_path = os.path.join(augmented_data_dir, class_name)
    os.makedirs(save_path, exist_ok=True)

    for image in os.listdir(class_path):  # Loop through images
        img_path = os.path.join(class_path, image)
        img = tf.keras.preprocessing.image.load_img(img_path)
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = img_array.reshape((1,) + img_array.shape)

        # Generate 2 augmented images per original
        i = 0
        for batch in datagen.flow(img_array, batch_size=1, save_to_dir=save_path, save_prefix="aug", save_format="jpg"):
            i += 1
            num_augmented_images += 1
            if i >= 2:  # Change this number to control how many new images per original
                break

print(f"✅ Data augmentation completed! Added {num_augmented_images} images.")

!zip -r augmented_dataset.zip augmented_dataset

import os
import pandas as pd

# Construct a DataFrame with image paths and labels
image_paths = []
labels = []

base_dir = "/content/augmented_dataset"

for class_name in os.listdir(base_dir):
    class_path = os.path.join(base_dir, class_name)
    if os.path.isdir(class_path):
        for img in os.listdir(class_path):
            image_paths.append(os.path.join(class_path, img))
            labels.append(class_name)

df = pd.DataFrame({
    'image_path': image_paths,
    'label': labels
})

df['label_encoded'] = pd.Categorical(df['label']).codes
num_classes = df['label_encoded'].nunique()

import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

datagen = ImageDataGenerator(rescale=1./255)

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = []

for fold, (train_idx, val_idx) in enumerate(kfold.split(df['image_path'], df['label_encoded']), 1):
    print(f"\n🔁 Training Fold {fold}/5")

    train_df = df.iloc[train_idx]
    val_df = df.iloc[val_idx]

    train_gen = datagen.flow_from_dataframe(
        train_df,
        x_col='image_path',
        y_col='label',
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        shuffle=True
    )

    val_gen = datagen.flow_from_dataframe(
        val_df,
        x_col='image_path',
        y_col='label',
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        shuffle=False
    )

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(train_gen, validation_data=val_gen, epochs=5, verbose=1)

    # Predictions
    val_gen.reset()
    y_true = val_df['label_encoded'].values
    y_pred_probs = model.predict(val_gen, verbose=0)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # Metrics
    acc = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

    print(f"Fold {fold} - Acc: {acc:.4f}, Prec: {precision:.4f}, Rec: {recall:.4f}, F1: {f1:.4f}")

    results.append({
        'Fold': fold,
        'Accuracy': acc,
        'Precision': precision,
        'Recall': recall,
        'F1 Score': f1
    })

# Final results
results_df = pd.DataFrame(results)
print("\n📊 Final 5-Fold Results:\n")
print(results_df)

from tensorflow.keras.preprocessing import image

model.save('/content/final_model.h5')  # Save the trained model

# Load model and test on one image
loaded_model = tf.keras.models.load_model('/content/final_model.h5')

test_image_path = "/content/drive/MyDrive/CSE465/Mango/Anthracnose/20211008_124249 (Custom).jpg"
test_image = image.load_img(test_image_path, target_size=(224, 224))
test_image_array = image.img_to_array(test_image)
test_image_array = np.expand_dims(test_image_array, axis=0)
test_image_array /= 255.0

prediction = loaded_model.predict(test_image_array)
predicted_class = np.argmax(prediction, axis=1)

print(f"Predicted class: {predicted_class[0]}")

from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D

base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze base layers

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(num_classes, activation='softmax')(x)

resnet_model = Model(inputs=base_model.input, outputs=x)
resnet_model.compile(optimizer=Adam(learning_rate=0.001),
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])

resnet_model.summary()

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from google.colab import files
import pandas as pd

# Reuse y_true and y_pred from the last fold
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=pd.Categorical(df['label']).categories,
            yticklabels=pd.Categorical(df['label']).categories)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')

# Save the figure
plt.savefig("confusion_matrix.png", dpi=300, bbox_inches='tight')
plt.show()

# Download the saved image
files.download("confusion_matrix.png")







