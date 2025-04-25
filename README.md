# 🌿 CSE465_Spring2025_Group-12

## 👤 Name: Imran Khan

### 📁 Model File
[Download model.h5](https://drive.google.com/file/d/1OoaAS1UWBsg_pyIuhQ5r-BnEfNLlkuu5/view?usp=sharing)

---

## 🔧 Contribution
| Your Name            | Contribution Description                                                  |
|----------------------|---------------------------------------------------------------------------|
| [Imran Khan]     | Completed the entire project individually — from data handling, model     |
|                      | design, training with 5-fold cross-validation, to evaluation and analysis. |


---

📥 Input Layer:
   - Shape: (224 x 224 x 3) RGB image

🔗 ResNet50 Backbone:
   - Pre-trained on ImageNet
   - Top layers removed (include_top=False)
   - All layers frozen (trainable=False)

🔄 Global Average Pooling:
   - Reduces feature map dimensions to 1D by averaging

🔢 Dense Layer:
   - 256 units
   - Activation: ReLU

🎯 Output Layer:
   - Number of units = Number of classes (auto from dataset)
   - Activation: Softmax (for multi-class classification)

---

![confusion_matrix](https://github.com/user-attachments/assets/f446ea6e-3aa1-4495-8e4a-0c47ff6165a7)


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
| 1    | 84.6%    | 86.5%     | 84.6%  | 84.5%    |
| 2    | 87.5%    | 88.4%     | 87.5%  | 87.5%    |
| 3    | 84.4%    | 85.2%     | 84.4%  | 84.4%    |
| 4    | 90.8%    | 91.1%     | 90.8%  | 90.6%    |
| 5    | 86.4%    | 86.5%     | 86.4%  | 86.4%    |

---

D)Final Project Execution Plan

1. **Preprocessing**: Finalize dataset and verify augmentation.
2. **Modeling**: Use a simple CNN initially, and apply **Transfer Learning with ResNet-50** on the full dataset using 5-fold cross-validation.
3. **Evaluation**: Store fold-wise performance and average results.
4. **Visualization**: Plot performance metrics, generate block diagram.
5. **Documentation**: Prepare `README.md`, final results, and slides/report.
6. **Submission**: Submit code, block diagram, and documentation on GitHub.


