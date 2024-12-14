import requests
from bs4 import BeautifulSoup
import json

# URL of the webpage to scrape
url = "https://docs.python.org/3.12/whatsnew/index.html"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the webpage content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all div elements with the class "toctree-wrapper compound"
    target_divs = soup.find_all("div", class_="toctree-wrapper compound")
    
    # Create a dictionary to store the version-to-URL mapping
    version_url_map = {}
    
    for div in target_divs:
        # Find all top-level <li> elements in the <ul>
        top_level_items = div.find_all("li", class_="toctree-l1")
        for item in top_level_items:
            # Get the Python version (text from the <a> tag)
            version_link = item.find("a")
            if version_link:
                python_version = version_link.get_text(strip=True)
                nested_ul = item.find("ul")  # Find the nested <ul> for this Python version
                
                # Collect all URLs from the nested <ul>
                urls = []
                if nested_ul:
                    urls = [li.find("a")["href"] for li in nested_ul.find_all("li") if li.find("a")]
                
                # Add to the map
                version_url_map[python_version] = urls
    
    # Specify the key to remove
    key_to_remove = "Changelog"

    # Check if the key exists in the dictionary
    if key_to_remove in version_url_map:
        del version_url_map[key_to_remove]  # Use 'del' to remove the key

    # Alternatively, you can use .pop() to remove and retrieve the value
    # removed_value = version_url_map.pop(key_to_remove, None)

    # Convert to JSON and print after removal
    result_json = json.dumps(version_url_map, indent=4)
    # Specify the filename
    filename = "python_versions.json"

    # Save the dictionary as a JSON file
    with open(filename, "w") as json_file:
        json.dump(version_url_map, json_file, indent=4)

    print(f"JSON data has been saved to {filename}")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
