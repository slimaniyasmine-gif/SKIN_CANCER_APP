# 🌑 Skin Cancer Detection Clinic - Midnight Luxury Edition

![Skin Cancer Detection](https://img.shields.io/badge/Status-Premium-gold?style=for-the-badge)
![Flask](https://img.shields.io/badge/Backend-Flask-lightgrey?style=for-the-badge&logo=flask)
![TensorFlow](https://img.shields.io/badge/AI-TensorFlow-orange?style=for-the-badge&logo=tensorflow)
![MySQL](https://img.shields.io/badge/Database-MySQL-blue?style=for-the-badge&logo=mysql)

A sophisticated, AI-powered diagnostic application designed for dermatologists and clinical environments. This application combines state-of-the-art computer vision with a premium "Midnight Luxury" aesthetic to provide a seamless and professional medical experience.

## ✨ Key Features

- **AI-Powered Analysis**: Utilizes a VGG16-based deep learning model to analyze skin lesions with high precision.
- **Midnight Luxury UI**: A premium dark-themed interface featuring glassmorphism, sophisticated typography, and smooth micro-animations.
- **Patient Management**: Secure registry for managing patient records and diagnostic history.
- **Real-time Diagnostics**: Immediate feedback and classification of skin images.
- **Secure Authentication**: Robust login system for clinical staff.

## 🛠️ Technology Stack

- **Backend**: Python / Flask
- **Machine Learning**: TensorFlow / Keras (VGG16 Model)
- **Database**: MySQL
- **Frontend**: Vanilla CSS (Premium Custom Design System), HTML5, JavaScript
- **Storage**: Git LFS (Large File Storage) for AI models

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- MySQL Server
- Git & Git LFS

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/slimaniyasmine-gif/SKIN_CANCER_APP.git
   cd SKIN_CANCER_APP
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**:
   - Create a MySQL database named `skin_cancer_db`.
   - Update the `.env` file with your credentials (see `.env.example`).
   - Run the initialization script:
     ```bash
     python init_db.py
     ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

## 🧠 Model Information

The application uses a pre-trained **VGG16** model fine-tuned for skin cancer classification. Due to its size (136MB), it is tracked via **Git LFS**. Ensure you have Git LFS installed to pull the model weights correctly.

## 🎨 Design Philosophy

The "Midnight Luxury" aesthetic is designed to evoke a sense of professional calm and medical excellence. By using deep indigo and obsidian tones paired with gold accents and soft glassmorphism, the application provides a high-end experience that respects the clinical nature of the work while offering modern usability.

---
Developed with ❤️ by [slimaniyasmine-gif](https://github.com/slimaniyasmine-gif)
