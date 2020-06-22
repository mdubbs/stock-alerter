import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

twilio_sid    = os.getenv('SA_TWILIO_SID')
twilio_auth   = os.getenv('SA_TWILIO_AUTH_TOKEN')
twilio_from   = os.getenv('SA_TWILIO_FROM_NUMBER')
target_number = os.getenv('SA_TARGET_NUMBER')
target_url    = os.getenv('SA_TARGET_URL')
target_name   = os.getenv('SA_ITEM_NAME')

def send_text(number, message):
  client = Client(twilio_sid, twilio_auth)

  message = client.messages.create(
    body=message,
    from_=twilio_from,
    to=number
  )
  print(f"Sent SMS Alert: {message.sid}")

html_text = requests.get(target_url).text
soup = BeautifulSoup(html_text, 'html.parser')

attrs = {
  'data-hook': 'add-to-cart'
}
buttons = soup.find_all('button', attrs=attrs, limit=1)

item_name = target_name
for b in buttons:
  if b.string.lower() == 'out of stock':
    print(f"{item_name}\nStatus: {b.string}")
  else:
    print(f"{item_name}\nStatus: {b.string}")
    send_text(target_number, f"{b.string.upper()} - {item_name}")

