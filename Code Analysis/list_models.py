from google import genai
import os

G_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=G_KEY)

print("Listing models available to your key:")
try:
    # In the new SDK, we just list them directly
    for m in client.models.list():
        print(f" - {m.name}")
except Exception as e:
    print(f"Error: {e}")
