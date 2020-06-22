import os
import requests
import time
import random
import logging
from bs4 import BeautifulSoup
from twilio.rest import Client

logging.basicConfig(
  filename='stock_alerter.log',
  format='%(asctime)s - %(levelname)s - %(message)s',
  level=logging.INFO,
  datefmt='%d-%b-%y %H:%M:%S'
  )

REQUIRED_ENV_VARS = [
  'SA_TWILIO_SID',
  'SA_TWILIO_AUTH_TOKEN',
  'SA_TWILIO_FROM_NUMBER',
  'SA_TARGET_NUMBER',
  'SA_TARGET_URL',
  'SA_ITEM_NAME'
  ]

for var in REQUIRED_ENV_VARS:
  if var not in os.environ:
    raise EnvironmentError(f"Failed because {var} is not set.")

twilio_sid    = os.getenv('SA_TWILIO_SID')
twilio_auth   = os.getenv('SA_TWILIO_AUTH_TOKEN')
twilio_from   = os.getenv('SA_TWILIO_FROM_NUMBER')
target_number = os.getenv('SA_TARGET_NUMBER')
target_url    = os.getenv('SA_TARGET_URL')
target_name   = os.getenv('SA_ITEM_NAME')

def send_text(number, message):
  client = Client(twilio_sid, twilio_auth)

  message = client.messages.create(
    body  = message,
    from_ = twilio_from,
    to    = number
  )
  logging.info(f"Sent SMS Alert: {message.sid}")

# randomly sleep before execution to look like less of a bot
n = round(random.uniform(5.0, 50.5), 2)
logging.info(f"Sleeping for {n} seconds...")
time.sleep(n)

logging.info("Executing stock check...")
html_text = requests.get(target_url).text
soup = BeautifulSoup(html_text, 'html.parser')

attrs = {
  'data-hook': 'add-to-cart'
}
buttons = soup.find_all('button', attrs=attrs, limit=1)

item_name = target_name
for b in buttons:
  if b.string.lower() == 'out of stock':
    logging.info(f"{item_name} - Status: {b.string}")
  else:
    logging.info(f"{item_name} - Status: {b.string}")
    send_text(target_number, f"{b.string.upper()} - {item_name}")

