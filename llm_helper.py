from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
model_name = "llama-3.2-90b-text-preview"

model = ChatGroq(
    api_key = api_key,
    model_name = model_name
)

if __name__ == "__main__":
    
    response = model.invoke("who is Chatrapathi Sivaji ?")
    print(response.content)
