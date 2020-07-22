import urllib.request, json

QUOTE_API = 'http://quotes.stormconsultancy.co.uk/random.json'

def get_quotes():

    with urllib.request.urlopen(QUOTE_API) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        quotes_dict = {}

        if get_quotes_response:
            quotes_dict['author']  = get_quotes_response['author']
            quotes_dict['quote']= get_quotes_response['quote']

    return quotes_dict