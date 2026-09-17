# 🧠 Alzheimer AI — Alzheimer Disease Detection

An AI-powered research and educational application for classifying brain MRI images into four Alzheimer's disease-related categories using a fine-tuned EfficientNetB0 deep learning model.

## 🚀 Features

- 🔐 Login authentication
- 🧠 Brain MRI image upload and preview
- 🤖 EfficientNetB0 transfer learning + fine-tuning
- 📊 Four-class MRI classification
- 📈 Prediction confidence and class probabilities
- 💾 SQLite prediction history
- 📊 Prediction analytics
- 🎨 Streamlit web interface
- ⚠️ Research and educational disclaimer

## 🏗️ Model

The project uses **EfficientNetB0** with ImageNet pretrained weights.

### Training Configuration

- Input Size: `224 × 224 × 3`
- Optimizer: Adam
- Data Augmentation:
  - Random Horizontal Flip
  - Random Rotation
  - Random Zoom
  - Random Contrast
- Transfer Learning
- Fine-tuning
- Class Weighting

## 📚 Classes

The model predicts four classes:

1. `MildDemented`
2. `ModerateDemented`
3. `NonDemented`
4. `VeryMildDemented`

## 📊 Dataset

Total images: **44,000**

| Class | Images |
|---|---:|
| MildDemented | 10,000 |
| ModerateDemented | 10,000 |
| NonDemented | 12,800 |
| VeryMildDemented | 11,200 |
| **Total** | **44,000** |

### Dataset Split

- Training: 30,800
- Validation: 6,600
- Testing: 6,600

## 📈 Model Performance

Final EfficientNetB0 test accuracy:

### **74.91%**

| Class | Precision | Recall | F1-Score |
|---|---:|---:|---:|
| MildDemented | 73.65% | 71.73% | 72.68% |
| ModerateDemented | 98.10% | 100.00% | 99.04% |
| NonDemented | 67.60% | 78.23% | 72.53% |
| VeryMildDemented | 62.39% | 51.55% | 56.45% |

## 🖥️ Application

### Dashboard

Displays:

- Total predictions
- AI model
- Number of classes
- System status
- Model information

### Alzheimer Detection

Users can:

1. Upload a brain MRI
2. Preview the MRI
3. Analyze the image
4. Get predicted class
5. View confidence
6. View class probabilities
7. Save prediction to database

### Prediction History

Stores:

- Image name
- Prediction
- Confidence
- Date and time

### Analytics

Displays:

- Total analyses
- Prediction distribution
- Class-wise prediction counts
- Percentages

## 📁 Project Structure

```text
Alzheimer-Disease-Detection/
│
├── app.py
├── config.py
├── database.py
├── model.py
├── utils.py
├── requirements.txt
├── .gitignore
│
├── model/
│   └── alzheimer_efficientnet_best.keras
│
├── data/
│   └── alzheimer.db
│
├── notebooks/
│   └── Alzheimer_Detection.ipynb
│
└── dataset/
    ├── MildDemented/
    ├── ModerateDemented/
    ├── NonDemented/
    └── VeryMildDemented/