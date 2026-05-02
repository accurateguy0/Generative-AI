import os
from google import genai
from dotenv import load_dotenv # Import the loader


load_dotenv() 

# os.getenv will be able to find the key
G_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=G_KEY)

print("Listing models available to your key:")
try:
    for m in client.models.list():
        print(f" - {m.name}")
except Exception as e:
    print(f"Error: {e}")