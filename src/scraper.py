import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Define the URL you want to scrape from
url = 'https://www.diputados.gob.mx/LeyesBiblio/index.htm'

# Connect to the website and fetch the page content
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Initialize the BeautifulSoup object with the page content and parser
soup = BeautifulSoup(response.content, 'html.parser')

# Find all PDF links
# pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
pdf_links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]

folder_name = "TextDocuments"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Download and save each PDF
for link in pdf_links:
    filename = os.path.join(folder_name, os.path.basename(link))
    with requests.get(link, stream=True) as r:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

print(f"All PDFs downloaded to the '{folder_name}' folder!")