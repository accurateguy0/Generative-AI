import requests
from bs4 import BeautifulSoup
import os
# Target Repository
repo_url = 'https://github.com/accurateguy0/Generative-AI'
base_raw_url = 'https://raw.githubusercontent.com'
# 1. Get the repository page
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(repo_url, headers=headers)
if response.status_code != 200:
    print(f"Failed to load page. Status: {response.status_code}")
    exit()
soup = BeautifulSoup(response.content, 'html.parser')
# 2. Find all file links
# GitHub links usually contain '/blob/' and represent files
links = soup.find_all('a')
pdf_links = []
print("Scanning for PDF files...")
for link in links:
    href = link.get('href')
    # Check if it is a file link (contains /blob/) and ends with .pdf
    if href and '/blob/' in href and href.endswith('.pdf'):
        pdf_links.append(href)
if not pdf_links:
    print("No PDF files found in the root of this repository.")
    # Debug: Print first 5 links to show what we CAN see
    print("Debug - First 5 links found on page:")
    for l in links[:5]:
        print(l.get('href'))
else:
    print(f"Found {len(pdf_links)} PDF(s). Downloading...")
    # 3. Download each file
    for href in pdf_links:
        # Convert GitHub "Blob" URL to "Raw" URL
        # From: /user/repo/blob/main/file.pdf
        # To:   https://raw.githubusercontent.com/user/repo/main/file.pdf
        download_url = base_raw_url + href.replace('/blob/', '/')    
        file_name = os.path.basename(href)  # Get 'report.pdf' from URL   
        print(f"Downloading {file_name} from {download_url}...")    
        file_resp = requests.get(download_url)    
        if file_resp.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(file_resp.content)
            print(" -> Saved!")
        else:
            print(f" -> Failed (Status {file_resp.status_code})")