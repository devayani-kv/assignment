import requests
from lxml import html
from bs4 import BeautifulSoup

#subject = 'norway'


def get_location_description(location):

    '''Function makes an API call to the wikipedia API
    
    Args:
        location: location for which you want the description'''

    url = 'https://en.wikipedia.org/w/api.php'
    params = {
                'action': 'parse',
                'page': location,
                'format': 'json',
                'prop':'text',
                'redirects':''
            }

    response = requests.get(url, params=params)
    #print('RESPONSE ###########################################################')
    #print(response)
    data = response.json()
    #print()
    #print(data)
    raw_html = data['parse']['text']['*']
    soup = BeautifulSoup(raw_html,'html.parser')
    soup.find_all('p')
    text = ''

    for p in soup.find_all('p'):
        text += p.text
    return text

#text = get_location_description('Norway')
#print(text)
#print('Text length: ', len(text))