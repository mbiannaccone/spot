import requests
from bs4 import BeautifulSoup


def beautiful_soup(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_all_breeds():
    url = "http://www.akc.org/dog-breeds/"
    soup = beautiful_soup(url)
    dogs = soup.findAll('option')

    dogs_dict = {}

    for dog in dogs:
        dog_name = dog.get_text()
        if dog_name not in ['By Dog Group',
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
            dog_url = url+dog_name.replace(' ', '-').lower()
            dogs_dict[dog_name] = dog_url

