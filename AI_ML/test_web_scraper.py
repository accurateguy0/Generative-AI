import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO  # <--- 1. Import this to fix the warning

url = 'https://en.wikipedia.org/wiki/Cloud-computing_comparison'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("Requesting page...")
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error: Access denied with status code {response.status_code}")
else:
    print("Success! Parsing HTML...")

    # Optional: Verify title manually
    soup = BeautifulSoup(response.content, 'html.parser')
    if soup.title:
        print("Page Title: " + soup.title.text)

    try:
        # 2. Fix the Warning: Wrap the text in StringIO
        html_data = StringIO(response.text)
        
        # 3. Read the tables
        tables = pd.read_html(html_data)
        
        print(f"Found {len(tables)} tables.")

        if len(tables) > 0:
            # Table 0 is usually the "General" comparison table
            df = tables[0] 
            print("\nPreview of extracted data:")
            print(df.head())

            df.to_csv('cloud_comparison.csv', index=False)
            print("\nSaved to cloud_comparison.csv")
        else:
            print("No tables found.")
            
    except Exception as e:
        print(f"Error parsing tables: {e}")
