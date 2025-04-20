# 🌿 CSE465_Spring2025_Group-12

## 👤 Name: Imran Khan

### 📁 Model File
[Download model.h5](https://drive.google.com/file/d/1OoaAS1UWBsg_pyIuhQ5r-BnEfNLlkuu5/view?usp=sharing)

---

## 🔧 Contribution
- ✅ Data Augmentation  
- ✅ Model Testing

---

## 🧪 Data Augmentation Details

Applied using `ImageDataGenerator` from TensorFlow. These techniques were used to increase dataset diversity and improve model generalization:

| Technique              | Description |
|------------------------|-------------|
| **Rotation** (`rotation_range=20`) | Randomly rotates images within ±20°, helping generalize to leaf orientation. |
| **Width Shift** (`width_shift_range=0.2`) | Horizontally shifts image up to 20% of total width. |
| **Height Shift** (`height_shift_range=0.2`) | Vertically shifts image up to 20% of total height. |
| **Shear** (`shear_range=0.2`) | Applies shear transformations to simulate geometric distortions. |
| **Zoom** (`zoom_range=0.2`) | Random zoom in/out by 20%, allowing varied views of leaves. |
| **Horizontal Flip** (`horizontal_flip=True`) | Flips images horizontally, aiding generalization. |
| **Fill Mode** (`fill_mode='nearest'`) | Fills missing pixels using nearest neighbor values. |

---

## 📊 Model Performance (5-Fold Cross Validation)

| Fold | Accuracy | Precision | Recall | F1 Score |
|------|----------|-----------|--------|----------|
| 1    | 66.8%    | 69.9%     | 66.8%  | 64.6%    |
| 2    | 77.6%    | 82.2%     | 77.6%  | 78.1%    |
| 3    | 77.3%    | 77.6%     | 77.3%  | 77.2%    |
| 4    | 84.1%    | 84.1%     | 84.1%  | 84.0%    |
| 5    | 81.4%    | 82.4%     | 81.4%  | 81.2%    |

---

✅ **Note**: Model performance improved significantly across folds due to effective augmentation and consistent testing procedures.


