# Medical_Computer_Vision
Deep Learning project for medical image classification using the BloodMNIST dataset. Features a custom CNN (MedNet) and Transfer Learning with ResNet18 in PyTorch.
# Medical Computer Vision - BloodMNIST Classification

## 🔬 Project Overview
This project focuses on identifying different types of blood cells using Deep Learning. I've implemented two different approaches to compare their performance:
1. **MedNet**: A custom-built Convolutional Neural Network (CNN).
2. **ResNet18**: Using Transfer Learning with pre-trained weights for higher accuracy.

## 📊 Dataset
The project uses the **BloodMNIST** dataset (part of MedMNIST), which contains 17,092 images of 8 types of blood cells. 

## 🛠 Tech Stack
- **Framework**: PyTorch
- **Models**: CNN (MedNet), ResNet18
- **Tools**: Matplotlib, NumPy, MedMNIST API
- **Environment**: Linux (Kali/Ubuntu), Jupyter Notebook

## 📁 Project Structure
- `notebooks/`: Training experiments and data visualization.
- `src/`: Core architecture and helper scripts.
- `models/`: Saved model weights (.pth files).
- `inference_samples/`: Test images for real-world predictions.
