import pytesseract
import cv2
import re
from pymongo import MongoClient

def extract_menu_items(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Unable to load image.")
        return []

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Extract text using Tesseract
    text = pytesseract.image_to_string(gray)

    # Split the text into lines
    lines = text.split("\n")

    # Initialize an empty list to store menu items
    menu_items = []

    # Define a regular expression to match prices
    price_pattern = re.compile(r'\d+(\.\d{1,2})?')

    # Iterate over the lines
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Split the line into words
        words = line.split()

        # Check if the line contains both an item and a price
        if len(words) < 2:
            continue

        # Check if the last word is numeric (likely a price)
        if price_pattern.match(words[-1]):

            item = " ".join(words[:-1])
            price = words[-1]

            menu_items.append({"item": item, "price": price})

    return menu_items

def store_menu_items(menu_items):
    client = MongoClient('mongodb+srv://admin:1234@cluster0.8t9vy4b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')  # Update with your MongoDB connection string
    db = client['Menu']
    collection = db['Data'] 

    result = collection.insert_many(menu_items)
    print(f"{len(result.inserted_ids)} menu items inserted successfully.")


image_paths = ["./Images/menu1.png", "./Images/menu2.png", "./Images/menu3.png", "./Images/menu4.png", "./Images/menu5.png"]

print("Menu items extracted successfully.")

for image_path in image_paths:
    menu_items = extract_menu_items(image_path)

    if menu_items:
        
        for item in menu_items:
            print(f"Item: {item['item']}, Price: {item['price']}")
        store_menu_items(menu_items)
    else:
        print("No menu items extracted.")

