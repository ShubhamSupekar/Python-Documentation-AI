import requests
from bs4 import BeautifulSoup
import json
import re

# Function to clean the text
def clean_text(text):
    return (
        text.replace("Â", "")
            .replace("¶", "")# Remove special characters
            .replace("\n", " ")      # Replace newline characters with spaces
            .strip()                 # Remove leading/trailing spaces
            .replace("  ", " ")      # Replace multiple spaces with a single space
    )


def get_details(url):
    if url == "No link":
        return None,None,None,None
    
    url = "https://www.w3schools.com/python/"+url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    s = soup.find('div',class_ = 'w3-example')
    
    if s and s.find('p'):
        query = clean_text(s.find('p').text)
    else:
        query = None

    if s and s.find('div',class_='w3-code notranslate pythonHigh'):
        eg = s.find('div',class_='w3-code notranslate pythonHigh').text
    else:
        eg = None
    

    p = soup.find(class_='ws-table-all notranslate')
    if p:
        Parameter = clean_text(p.find_all('td')[0].text)
        Description = clean_text(p.find_all('td')[1].text)
    else:
        Parameter = None
        Description = None

    return query,eg,Parameter,Description

def createJason(data):
    json_object = json.dumps(data, indent=4)
    # Writing to sample.json
    with open("PythonDoc.json", "w") as outfile:
        outfile.write(json_object)


def main(urls):
    data = []

    for url in urls:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
                        
            # Find the table containing functions (by its class or structure)
            table = soup.find('table', class_='ws-table-all')  # Table with all functions
            
            # Check if table exists
            if table:
                # Find all rows in the table (skip the header row)
                rows = table.find_all('tr')[1:]  # Exclude the header row
                
                # Loop through each row
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) == 2:  # Ensure the row has two columns
                        function_name = clean_text(cols[0].get_text(strip=True))
                        
                        # Extract the link if available
                        link_tag = cols[0].find('a')
                        link = link_tag['href'] if link_tag else "No link"

                        query,eg,Parameter,eg_Description = get_details(link)
                            
                        
                        description = clean_text(cols[1].get_text(strip=True))
                        
                        # Append the cleaned data
                        data.append({
                            "function": function_name,
                            "link": link,
                            "description": description,
                            "query":query,
                            "eg":eg,
                            "Parameter":Parameter,
                            "eg_Description":eg_Description
                        })
            else:
                print("Table not found on the page.")
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        
        print("Done URL: ",url)
    
    # create a json file and load the data 
    createJason(data)
    

if __name__=="__main__":
    # # URL's of the webpage
    urls = ["https://www.w3schools.com/python/python_ref_functions.asp",
           "https://www.w3schools.com/python/python_ref_string.asp",
           "https://www.w3schools.com/python/python_ref_list.asp",
           "https://www.w3schools.com/python/python_ref_dictionary.asp",
           "https://www.w3schools.com/python/python_ref_tuple.asp",
           "https://www.w3schools.com/python/python_ref_set.asp",
           "https://www.w3schools.com/python/python_ref_file.asp",
           "https://www.w3schools.com/python/python_ref_keywords.asp",
           "https://www.w3schools.com/python/python_ref_exceptions.asp",
           "https://www.w3schools.com/python/python_ref_glossary.asp",
           "https://www.w3schools.com/python/module_random.asp",
           "https://www.w3schools.com/python/module_requests.asp",
           "https://www.w3schools.com/python/module_statistics.asp",
           "https://www.w3schools.com/python/module_math.asp",
           "https://www.w3schools.com/python/module_cmath.asp"]

    main(urls)