import requests
import json
from bs4 import BeautifulSoup
import html 
bot_token = '6312354572:AAEVL8qY06V7xcMj-EVL6zSoetezuBk4tmY'
bot_chat_id = '-1001775234264'
def button():
    button_text = "ይጫኑ"
    button_data = "films"

    reply_markup = {
        "inline_keyboard": [[{"text": button_text, "callback_data": button_data}]]
    }

    # Send the button message to the channel
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": bot_chat_id,
        "text": "የዕለቱን የፊልም መርሐግብር ለማወቅ ከታች ያለውን ቁልፍ ይጫኑ",
        "reply_markup": json.dumps(reply_markup)  # Convert the reply_markup to JSON format
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Button message sent successfully")
    else:
        print("Failed to send button message")
def button_click(update):
    query_data = update['callback_query']['data']
    if query_data == 'films':
        # Send the the data in films when the  button is clicked
        films(update['callback_query']['message']['chat']['id'])
def films(chat_id):#scrap the data
    url = 'http://www.alemcinema.com/'
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = soup.find_all("div",attrs={"id":"fh5co-board"})
        if response.status_code == 200:                       
            for card in titles:
                title_tag2 = card.find("div",attrs={"class":"item"})
                title2 = title_tag2.text.strip("ስለፊልሙ አስተያየቶን ይስጡ") if title_tag2 else "Title not found" 
                image_tag = card.find("img")
                image_url = image_tag["src"] if image_tag and "src" in image_tag.attrs else "Image URL not found"      
                message = f"ርዕስ  :\n{title2}"                     
                url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"          # url for photo
                data = {
                            "chat_id": bot_chat_id,
                            "photo": image_url,
                            "caption": message,
                            "parse_mode": "HTML",  # Set parse mode to HTML to interpret the message as HTML
                        }
                        # Send the message to the Telegram channel
                response = requests.post(url, json=data)
            if response.status_code == 200:
                            print("Message sent successfully")
            else:
                            print("Failed to send message")
    if response.status_code == 200:
        print("films successfully")
    else:
        print("Failed to send films")
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    params = {}
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get updates")
        return None
if __name__ == "__main__":
    button()
    offset = None
    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates.get("result", []):
                button_click(update)
                offset = update["update_id"] + 1
