import requests
from bs4 import BeautifulSoup


def beautiful_soup(url):
    """ Returns html from a website."""
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_all_breeds():
    """ Gets all breeds from akc home page and returns a dictionary with url."""
    url = "http://www.akc.org/dog-breeds/"
    breed_soup = beautiful_soup(url)
    breeds = breed_soup.findAll('option')
    breeds_info = {}

    for breed in breeds:
        breed_name = breed.get_text()
        if breed_name not in ['By Dog Group',
                              'Herding Group',
                              'Hound Group',
                              'Non Sporting Group',
                              'Sporting Group',
                              'Terrier Group',
                              'Toy Group',
                              'Working Group',
                              'FSS',
                              'Miscellaneous',
                              'By Dog Breed']:
            breed_url = url+breed_name.replace(' ', '-').lower()
            breeds_info[breed_name] = breed_url
            breeds_info['St. Bernard'] = 'http://www.akc.org/dog-breeds/st-bernard'

    return breeds_info


def get_characteristics(url):
    """Grabs all p info from html of the site, cleans up, and returns as a list."""
    soup = beautiful_soup(url)
    char_list = []
    for item in soup.findAll('p'):
        char_list.append(item.parent.get_text(strip=True))
    return char_list


def make_char_dict():
    """ Takes char_list from get_characteristics function and makes a dictionary."""
    char_dict = {}
    for breed, url in breeds_info.items():
        char_dict[breed] = get_characteristics(url)
    return char_dict


def make_breed_char_dict():
    """ Makes dictionary of each breed and all its characteristics. """
    # initializes breed_char_dict
    breed_char_dict = {}
    # adds each breed name in as a key, and an empty dictionary as a value
    for breed in breeds_info:
        breed_char_dict[breed] = {}

    for breed, chars in char_dict.items():
        # Fun Fact
        for char in chars:
            if 'Did you know?' in char:
                start = char.index('?') + 1
                breed_char_dict[breed]['Fun Fact'] = char[start:].replace('Read More', '')
        # History
        for char in chars:
            if 'History' in char[:10]:
                start = char.index('History') + len('History')
                year = char[start: start + 4]
                breed_char_dict[breed]['History'] = year + " - " + char[start + 4:].replace('Read More', '')
        # General Appearance
        for char in chars:
            if 'General Appearance' in char[:20]:
                start = char.index('General Appearance') + len('General Appearance')
                breed_char_dict[breed]['General Appearance'] = char[start:].replace('Read More', '')
        # Head
        for char in chars:
            if 'Head' in char[:6]:
                start = char.index('Head') + len('Head')
                breed_char_dict[breed]['Head'] = char[start:].replace('Read More', '')
        # Body
        for char in chars:
            if 'Body' in char[:6]:
                start = char.index('Body') + len('Body')
                breed_char_dict[breed]['Body'] = char[start:].replace('Read More', '')
        # Forequarters
        for char in chars:
            if 'Forequarters' in char[:15]:
                start = char.index('Forequarters') + len('Forequarters')
                breed_char_dict[breed]['Forequarters'] = char[start:].replace('Read More', '')
        # Hindquarters
        for char in chars:
            if 'Hindquarters' in char[:15]:
                start = char.index('Hindquarters') + len('Hindquarters')
                breed_char_dict[breed]['Hindquarters'] = char[start:].replace('Read More', '')
        # Grooming
        for char in chars:
            if '&Grooming' in char[:20]:
                start = char.index('&Grooming') + len('&Grooming')
                breed_char_dict[breed]['Grooming'] = char[start:].replace('Read More', '')
        # Coat
        for char in chars:
            if 'Coat' in char[:6] and 'Grooming' not in char[:20]:
                start = char.index('Coat') + len('Coat')
                breed_char_dict[breed]['Coat'] = char[start:].replace('Read More', '')
        # Nutrition & Feeding
        for char in chars:
            if 'Nutrition& Feeding' in char[:30]:
                start = char.index('Nutrition& Feeding') + len('Nutrition& Feeding')
                breed_char_dict[breed]['Nutrition & Feeding'] = char[start:].replace('Read More', '')
        # Exercise
        for char in chars:
            if 'Exercise' in char[:10]:
                start = char.index('Exercise') + len('Exercise')
                breed_char_dict[breed]['Exercise'] = char[start:].replace('Read More', '')
        # Health
        for char in chars:
            if 'Health' in char[:8]:
                start = char.index('Health') + len('Health')
                breed_char_dict[breed]['Health'] = char[start:].replace('Read More', '')

    return breed_char_dict


breeds_info = get_all_breeds()
char_dict = make_char_dict()
breed_char_dict = make_breed_char_dict()
