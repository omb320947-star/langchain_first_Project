import os
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

prompt_template = PromptTemplate(
    template="""You are a helpful assistant. Answer the user's question based strictly on the provided document context.

Document Context:
{document}

User Question:
{question}

Answer:"""
)

def extract_text_content(content):
    """Recursively extracts text from string, dict, list, or AIMessage formats."""
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        if 'text' in content:
            return content['text']
        elif 'content' in content:
            return extract_text_content(content['content'])
    elif isinstance(content, list):
        text_parts = []
        for item in content:
            extracted = extract_text_content(item)
            if extracted:
                text_parts.append(extracted)
        return "\n".join(text_parts)
    elif hasattr(content, 'content'):
        return extract_text_content(content.content)
    return str(content)


# Inline HTML + CSS + JS Template
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DocuQuery AI</title>
    <style>
        :root {
            --bg-color: #f4f6f9;
            --card-bg: #ffffff;
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --border: #e5e7eb;
            --accent-bg: #f8fafc;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 750px;
            background: var(--card-bg);
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid var(--border);
        }

        h1 {
            font-size: 1.75rem;
            margin-bottom: 6px;
            color: var(--text-main);
            text-align: center;
            font-weight: 700;
        }

        p.subtitle {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-bottom: 24px;
        }

        .section {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            font-size: 0.875rem;
            color: var(--text-main);
        }

        .file-upload-box {
            border: 2px dashed var(--border);
            padding: 24px;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            transition: border-color 0.2s, background-color 0.2s;
            background: var(--accent-bg);
        }

        .file-upload-box:hover {
            border-color: var(--primary);
            background: #eef2ff;
        }

        input[type="file"] {
            display: none;
        }

        .file-name-display {
            margin-top: 8px;
            font-size: 0.85rem;
            color: var(--primary);
            font-weight: 600;
        }

        textarea {
            width: 100%;
            height: 110px;
            background-color: #ffffff;
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-main);
            padding: 12px;
            font-size: 0.95rem;
            resize: vertical;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
        }

        button {
            width: 100%;
            padding: 12px;
            background-color: var(--primary);
            color: #ffffff;
            border: none;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        button:hover {
            background-color: var(--primary-hover);
        }

        button:disabled {
            background-color: #9ca3af;
            cursor: not-allowed;
        }

        .response-box {
            margin-top: 24px;
            padding: 20px;
            background: var(--accent-bg);
            border-radius: 8px;
            border: 1px solid var(--border);
            display: none;
        }

        .response-box h3 {
            font-size: 0.95rem;
            color: var(--primary);
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .response-content {
            font-size: 0.95rem;
            line-height: 1.6;
            white-space: pre-wrap;
            color: var(--text-main);
        }

        .loader {
            display: none;
            text-align: center;
            margin-top: 16px;
            font-size: 0.9rem;
            color: var(--primary);
            font-weight: 500;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Document Q&A Assistant</h1>
    <p class="subtitle">Upload a text file and get instant answers powered by Gemini</p>

    <form id="qaForm">
        <div class="section">
            <label>Upload Document (.txt)</label>
            <div class="file-upload-box" onclick="document.getElementById('fileInput').click()">
                <span id="uploadText" style="color: var(--text-muted); font-weight: 500;">Click to select or drag .txt file here</span>
                <input type="file" id="fileInput" name="file" accept=".txt" required onchange="handleFileChange(this)">
                <div class="file-name-display" id="fileName"></div>
            </div>
        </div>

        <div class="section">
            <label for="question">Your Question</label>
            <textarea id="question" name="question" placeholder="Ask anything about the uploaded document..." required></textarea>
        </div>

        <button type="submit" id="submitBtn">Ask Assistant</button>
    </form>

    <div class="loader" id="loader">Analyzing document...</div>

    <div class="response-box" id="responseBox">
        <h3>Answer</h3>
        <div class="response-content" id="responseContent"></div>
    </div>
</div>

<script>
    function handleFileChange(input) {
        const fileNameDisplay = document.getElementById('fileName');
        const uploadText = document.getElementById('uploadText');
        if (input.files && input.files[0]) {
            fileNameDisplay.textContent = `Selected File: ${input.files[0].name}`;
            uploadText.textContent = "Click to change file";
        }
    }

    document.getElementById('qaForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const fileInput = document.getElementById('fileInput');
        const questionInput = document.getElementById('question');
        const submitBtn = document.getElementById('submitBtn');
        const loader = document.getElementById('loader');
        const responseBox = document.getElementById('responseBox');
        const responseContent = document.getElementById('responseContent');

        if (!fileInput.files[0]) {
            alert('Please select a .txt file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        formData.append('question', questionInput.value);

        submitBtn.disabled = true;
        loader.style.display = 'block';
        responseBox.style.display = 'none';

        try {
            const response = await fetch('/query', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                responseContent.textContent = data.answer;
                responseBox.style.display = 'block';
            } else {
                alert(data.error || 'An error occurred.');
            }
        } catch (err) {
            alert('Error connecting to the server.');
        } finally {
            submitBtn.disabled = false;
            loader.style.display = 'none';
        }
    });
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT)

@app.route('/query', methods=['POST'])
def query_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    question = request.form.get('question', '')

    if file.filename == '' or not file.filename.endswith('.txt'):
        return jsonify({'error': 'Please upload a valid .txt file'}), 400

    if not question.strip():
        return jsonify({'error': 'Question cannot be empty'}), 400

    try:
        document_content = file.read().decode('utf-8')

        final_prompt = prompt_template.invoke({
            "document": document_content,
            "question": question
        })

        result = llm.invoke(final_prompt)

        # Parse text from structured content response block
        clean_text = extract_text_content(result)

        return jsonify({'answer': clean_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
