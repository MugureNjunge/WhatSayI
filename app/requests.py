from app import app
import urllib.request,json
from app.models import User, Post, Quote

# quotes = quotes.quotes

base_url= 'http://quotes.stormconsultancy.co.uk/random.json'

def get_quotes():
  get_quotes_url = base_url.format()

  with urllib.request.urlopen(get_quotes_url) as url:
    get_quotes_data = url.read()
    get_quotes_response = json.loads(get_quotes_data)

    quotes_results = None

    if get_quotes_response['articles']:
      quotes_results_list = get_quotes_response['quotes']
      quotes_results = process_results(quotes_results_list)
  return quotes_results

def process_results(quotes_list):
  quotes_results = []
  for quotes_item in quotes_list:
    author = quotes_item.get("author")
    id = quotes_item.get("id")
    quote = quotes_item.get("quote")

    quotes_object = quote(author, id, quote)
    quotes_results.append(quotes_object)
  return quotes_results  