import requests
from bs4 import BeautifulSoup
import json
import os

# URL of the page to scrape
url = 'https://www.zabihah.com/search?k=Halal&l=21114'

# Send a GET request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Page fetched successfully")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    exit()

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all <div> elements with id='header'
bodies = soup.find_all('div', id='header')

# List to store store information
store_info = []

# Iterate through each body
for body in bodies:
    # Find all elements with class 'titleBS' for store names
    names = body.find_all('div', class_='titleBS')
    # Find all elements with class 'tinyLink' for addresses
    addresses = body.find_all('div', class_='tinyLink')
    # Find all elements with id 'alertBox2' for categories
    categories = body.find_all('div', id='alertBox2')
    # Find all elements with class 'badge_score' for ratings
    ratings = body.find_all('div', id='badge_score')
    # Find all elements with class 'badge_review' for number of reviews
    reviews = body.find_all('div', id='badge_review')

    # Loop through names and addresses, and collect data
    for i in range(len(names)):
        store = names[i]
        address = addresses[i]
        
        link = store.find('a')  # Find the <a> tag within each store
        if link:
            store_name = link.get_text(strip=True)  # Get the text of the <a> tag
            store_address = address.get_text(strip=True)  # Get the address text
            
            # Collect store categorys
            store_category_list = []
            if i < len(categories):
                category_div = categories[i]
                category_items = category_div.find_all('div')  # Assuming categories are in nested divs
                store_category_list.extend([t.get_text(strip=True) for t in category_items])
            
            # Get rating and review, defaulting if not available
            rating = ratings[i].get_text(strip=True) if i < len(ratings) else "NR"
            rating_output = f"{rating}/5.0" if rating != "NR" else "NR"
            review = reviews[i].get_text(strip=True) if i < len(reviews) else "No reviews available"
            review_output = f"{review} reviews" if review != "No reviews available" else "No reviews available"
            # Create a dictionary for the store information
            store_info.append({
                'Name': store_name,
                'Address': store_address,
                'Category': ', '.join(store_category_list) if store_category_list else "No categorys available",
                'Rating': rating_output,
                'Reviews': review_output
            })

# Create the output directory if it doesn't exist
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Store the information in a dictionary with the description as a list
data_with_description = {
    "description": [
        "This JSON file contains store information for halal businesses, including names, addresses, categories, ratings, and reviews.",
        "",
        "Example Entries:",
        "Name: 'Halal Meat Market'",
        "Address: '123 Main Street, City, State'",
        "Category: 'Butcher, Grocery'",
        "Rating: '4.5/5.0'",
        "Reviews: '15 reviews'",
        "",
        "Name: 'Halal Express Deli'",
        "Address: '456 Elm Street, City, State'",
        "Category: 'Restaurant, Deli'",
        "Rating: '4.0/5.0'",
        "Reviews: '5 reviews'"
    ],
    "store_info": store_info  # Use the actual scraped store information here
}

# Write the data with description to a JSON file
output_file_path = os.path.join(output_dir, 'store_information.json')
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_with_description, json_file, ensure_ascii=False, indent=4)

print(f"Store information with description has been written to {output_file_path}")
