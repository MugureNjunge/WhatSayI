from .models import Quote
import urllib.request, json

randomUrl = "http://quotes.stormconsultancy.co.uk/random.json"

def getRandom():
    with urllib.request.urlopen(randomUrl) as url:
        quote_details_data = url.read()
        quote_details_response = json.loads(quote_details_data)
        quote_object = None

        if quote_details_response:
            author = quote_details_response.get('author')
            quote = quote_details_response.get('quote')
            quote_object = Quote(author, quote)
            return quote_object


popularUrl = "http://quotes.stormconsultancy.co.uk/popular.json"
def getPopular():
     with urllib.request.urlopen('popularUrl') as url:
        quote_details_data = url.read()
        quote_details_response = json.loads(quote_details_data)
        quote_object = None

        if quote_details_response:
            author = quote_details_response.get('author')
            quote = quote_details_response.get('quote')
            quote_object = Quote(author, quote)
            return quote_object