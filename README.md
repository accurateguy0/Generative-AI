# 🤖 Generative AI & Machine Learning Research Hub

This repository is a centralized laboratory for Generative AI, Deep Learning, and Automated Data Governance. It contains end-to-end pipelines ranging from medical imaging classifiers to LangChain-based code analysis agents.

## 🚀 Project Portfolio

### 🩺 [Medical Computer Vision](https://www.google.com/url?sa=E&q=./Medical_Computer_Vision)

A specialized deep learning project focused on hematology analysis.

- **Dataset:** Utilizes the **BloodMNIST** dataset (bloodmnist.npz).
    
- **Architecture:** Features ResNet-based architectures defined in src/architecture.py.
    
- **Training:** Interactive experiments documented in Jupyter Notebooks.
    
- **Inference:** Production-ready scripts for testing against real-world blood smear samples.
    

### 🧠 [Code Analysis](https://www.google.com/url?sa=E&q=./Code%20Analysis)

Automating the understanding of software logic using Large Language Models (LLMs).

- **Agentic Workflows:** Employs **LangChain agents** to analyze codebases.
    
- **Automation:** Includes custom workflows for model listing and data ingestion.
    

### 🛡️ [Data Classification & Governance](https://www.google.com/url?sa=E&q=./Data_Classification)

Focuses on the ethical and secure handling of data in the AI era.

- **Governance Bot:** An automated tool for enforcing data policy.
    
- **PII Masking:** Demonstrates data privacy through masked customer datasets (customer_data_MASKED.csv).
    
- **Classification:** Scripts to categorize data for compliance and security.
    

### ☁️ [Cloud AI](https://www.google.com/url?sa=E&q=./Cloud_AI)

Integration of AI services within cloud environments.

- **Architecture:** Modular structure for deploying AI logic to cloud endpoints.
    
- **Privacy:** Implementation of data masking for cloud-based processing.
    

### 🧪 [AI & ML Toolbox](https://www.google.com/url?sa=E&q=./AI_ML)

A collection of utility scripts for the standard ML lifecycle.

- **Preprocessing:** Robust data cleaning and preparation scripts.
    
- **Web Scraping:** Automated tools for gathering training data from the web.
    
- **Deployment:** Includes Dockerfile and app.py for containerized application hosting.
    

---

## 🛠️ Tech Stack

- **Deep Learning:** PyTorch, Torchvision (ResNet), MedMNIST.
    
- **LLM Frameworks:** LangChain, OpenAI/Open-Source Model APIs.
    
- **Data Science:** Pandas, NumPy, Scikit-learn.
    
- **DevOps:** Docker, Virtual Environments (venv).
    
- **Languages:** Python 3.x.
    

---

## ⚙️ Installation & Setup

### 1. Using Virtual Environments

It is recommended to use the provided venv structure:

codeBash

```
# Activate the environment
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Using Docker

To ensure a consistent environment across all modules:

codeBash

```
docker build -t gen-ai-hub .
docker run -it gen-ai-hub
```

---

## 📊 Key Notebooks

- **training_experiment.ipynb:** The primary research document for the Medical CV project, containing loss curves, accuracy metrics, and model checkpoints (resnet_blood_best.pth).
    

---

## ⚖️ Ethics & Governance

This repository includes a **Governance Bot** and **Data Classification** logic to emphasize the importance of AI safety, PII protection, and responsible AI development. All customer data samples included are masked and dummy-generated for testing purposes.
