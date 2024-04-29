import os
import requests

# List of card names without 'S'
cards = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 'C1J', 'C2Q', 'C3K']

# List of suits including 'S'
suits = ['S', 'H', 'C', 'D']

# URL template
url_template = "http://www.marytcusack.com/maryc/decks/Images/Cards/Navigators/{}.jpg"

# Create folder if not exists
folder_path = './card_jpgs'
os.makedirs(folder_path, exist_ok=True)

# Download images
for card in cards:
    for suit in suits:
        card_name = suit + card
        url = url_template.format(card_name)
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder_path, f"{card_name}.jpg"), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {card_name}.jpg")
        else:
            print(f"Failed to download {card_name}.jpg")
