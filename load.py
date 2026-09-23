from langchain_community.document_loaders import TextLoader
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

loader = TextLoader("text.txt")
docs = loader.load()

# llm = ChatOllama(model="tinyllama")

llm = ChatGoogleGenerativeAI(model='gemini-3.1-flash-lite')

# Take question from user
question = input("Aks Any Questions → : ")

# Create prompt
prompt = PromptTemplate(
    template=
"""
Document:
{document}
Question:
{question}

"""
)

# Fill values in prompt

final_prompt = prompt.invoke({
"document": docs[0].page_content,
"question": question
})

# Get answer from LLM
result = llm.invoke(final_prompt)

print(result.content)
