from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import AzureOpenAI
import csv
import socket
import uvicorn  # Import uvicorn for running the server

# Get IP address
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Load CSV data
def load_data(file_path="data.csv"):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            headers = rows[0]
            data_string = ""
            for row in rows[1:]:
                row_data = {headers[i]: value for i, value in enumerate(row)}
                data_string += str(row_data) + "\n"
            return data_string
    except Exception as e:
        return f"Error loading data: {str(e)}"

# Initialize FastAPI app
app = FastAPI()

# OpenAI client
client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint="https://ai-aboubakrketoun6057ai192227861011.openai.azure.com/",
    api_key="DzeoBJP69Urru42XLlLdG3dwyOC4c2NmCZTVdx2OUMS0fYCwhwBhJQQJ99BDACHYHv6XJ3w3AAAAACOGjch8"
)

# Pydantic model for request body
class QueryRequest(BaseModel):
    query: str

# API endpoint
@app.post("/chat")
async def chat_with_bot(request: QueryRequest):
    try:
        data_context = load_data()
        response = client.chat.completions.create(
            model="databased-chatbot-o3-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Use the following data to answer the user's question:\n\n" + data_context},
                {"role": "user", "content": request.query}
            ],
            max_completion_tokens=500,
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

# Add a simple health check endpoint
@app.get("/")
def read_root():
    return {"status": "API is running"}

# Run the server if the file is executed directly
if __name__ == "__main__":
    ip = get_ip_address()
    print(f"Starting server on http://{ip}:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)