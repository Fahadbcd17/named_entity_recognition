# 🔍 Named Entity Recognition **(NER)** Web Application

## Professional Training - YN3012170034 (Intermediate Level)
## Mid-term Assignment
## Student: FAHAD

### 📘 Overview

This project is a Gradio-based web application that performs Named Entity Recognition (NER) using a pre-trained BERT model.
Users can input any text, and the system automatically detects:

**👤 Persons (PER)**

**🏢 Organizations (ORG)**

**📍 Locations (LOC)**

**📌 Miscellaneous entities (MISC)**

The app highlights detected entities and displays them in an organized and readable format.

This project fulfills the requirements for the Mid-term Assignment of Professional Training - YN3012170034.


### 🚀 Features

✔ Built with Python

✔ Uses HuggingFace Transformers

✔ Interactive UI using Gradio

✔ Real-time entity detection

✔ Text highlighting with color-coded labels

✔ Clean and modular code

✔ Examples included for quick testing


### 🛠 Technology Stack

Python 3

Gradio

Transformers (HuggingFace)

PyTorch

Regular Expressions (re)



### 📁 Project Structure
│── app.py                Main application
│── requirements.txt      Project dependencies
│── README.md             Documentation
└── .venv/                Python virtual environment


# 📦 Installation & Setup
### 1️⃣ Clone the Project
git clone [https://github.com/Fahadbcd17/named_entity_recognition]
cd <named_entity_recognition/>

### 2️⃣ Create Virtual Environment (.venv)
python3 -m venv .venv

#### Ubuntu / Linux / macOS
source .venv/bin/activate

#### Windows (PowerShell)
.\.venv\Scripts\activate

### 3️⃣ Install Dependencies
pip3 install -r requirements.txt

### 4️⃣ Run the App
python3 app.py

You will see a Gradio link such as: ***Running on http://127.0.0.1:7860***