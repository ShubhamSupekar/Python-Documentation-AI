import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://docs.python.org/3/library/functions.html"

# Send HTTP request
response = requests.get(url)

# Parse the HTML
soup = BeautifulSoup(response.content, "html.parser")


# Function to clean the text
def clean_text(text):
    return (
        text.replace("Â", "")
            .replace("¶", "")# Remove special characters
            .replace("\n", " ")      # Replace newline characters with spaces
            .strip()                 # Remove leading/trailing spaces
            .replace("  ", " ")      # Replace multiple spaces with a single space
    )

# Extract function names and descriptions
functions = []
for dt, dd in zip(soup.find_all("dt"), soup.find_all("dd")):
    function_name = clean_text(dt.get_text(strip=True))
    description = clean_text(dd.get_text(strip=True))
    functions.append({"function": function_name, "description": description})

# Display the extracted data
print(functions[0])
print(f"\n{functions[1]}")
print(f"\n{functions[2]}")
