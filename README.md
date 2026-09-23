
# 📄 Document Q&A using LangChain & Google Gemini

Project Link → https://langchain-first-project-1.onrender.com/

A simple **AI-powered Document Question Answering application** built using **Flask, LangChain, and Google Gemini**.

Users can upload a `.txt` document and ask questions about its content. The application sends the document content and user's question to the Google Gemini model and returns an AI-generated answer based on the uploaded document.

---

## 🚀 Features

* 📄 Upload `.txt` documents
* 🤖 Ask questions about the uploaded document
* 🧠 Uses Google Gemini for AI responses
* 🔗 Uses LangChain for prompt management
* 🌐 Flask-based web application
* ⚡ Simple and clean web interface
* ☁️ Can be deployed on Render
* 🔐 API key stored securely using environment variables

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **LangChain**
* **Google Gemini**
* **python-dotenv**
* **Gunicorn**
* **HTML**
* **CSS**
* **JavaScript**

---

## 📁 Project Structure

```text
document-qa-project/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env
```

> ⚠️ Do not upload `.env` to GitHub because it contains your API key.

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/document-qa-project.git
```

Move into the project directory:

```bash
cd document-qa-project
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure Google Gemini API Key

Create a `.env` file in the project root directory:

```env
GOOGLE_API_KEY=your_google_api_key
```

Replace `your_google_api_key` with your actual Google Gemini API key.

> 🔒 Never commit your `.env` file to GitHub.

---

## ▶️ Run the Application

Run:

```bash
python app.py
```

The application will start on:

```text
http://127.0.0.1:5000
```

Open the URL in your browser.

---

## 📄 How to Use

### Step 1

Open the application in your browser.

### Step 2

Upload a `.txt` document.

### Step 3

Enter your question about the document.

For example:

```text
What is the main topic of this document?
```

### Step 4

Click the **Ask Question** button.

### Step 5

The application sends the document and question to Google Gemini and displays the answer.

---

## 🧠 How It Works

The application follows this basic workflow:

```text
User
  ↓
Upload TXT File
  ↓
Flask Application
  ↓
Read Document Content
  ↓
Create LangChain Prompt
  ↓
Google Gemini
  ↓
Generate Answer
  ↓
Display Answer
```

The document content and user's question are inserted into a prompt:

```text
Document Context:
{document}

User Question:
{question}

Answer:
```

The prompt is then sent to the Google Gemini model through LangChain.

---

## 📦 Requirements

The project uses the following Python packages:

```text
Flask
python-dotenv
langchain-core
langchain-google-genai
gunicorn
```

Install them using:

```bash
pip install -r requirements.txt
```

---

## 🌐 Deployment on Render

This application can be deployed on **Render**.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn --timeout 120 app:app
```

### Environment Variable

Add the following environment variable in Render:

```text
GOOGLE_API_KEY=your_google_api_key
```

Do not add the API key directly inside `app.py`.

---

## 🔐 Security

The Gemini API key should be stored in an environment variable.

Example:

```env
GOOGLE_API_KEY=your_google_api_key
```

The `.gitignore` file should contain:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
```

This prevents sensitive files and unnecessary Python files from being uploaded to GitHub.

---

## 🎯 Future Improvements

The project can be extended with:

* 📕 PDF document support
* 📘 DOCX document support
* 📊 CSV document support
* 📑 Multiple document uploads
* 🔍 Vector database integration
* 🧩 RAG (Retrieval-Augmented Generation)
* 💬 Chat history
* 📚 Document embeddings
* 🔐 User authentication
* 🎨 Improved UI
* ☁️ Cloud storage integration

---

## 👨‍💻 Author

**ReLearn Careers**

A practical AI project demonstrating document-based question answering using **Flask + LangChain + Google Gemini**.

---

## ⭐ Project Goal

The main goal of this project is to demonstrate how **Generative AI can be integrated with a web application** to allow users to interact with their own documents using natural language questions.
