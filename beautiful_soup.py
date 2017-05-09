import requests
from bs4 import BeautifulSoup

breeds_info = {}

def beautiful_soup(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_all_breeds():
    url = "http://www.akc.org/dog-breeds/"
    breed_soup = beautiful_soup(url)
    breeds = breed_soup.findAll('option')
    group_soup = beautiful_soup("http://www.akc.org/dog-breeds/groups/herding/")

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
            breeds_info[breed_name] = {'url': breed_url}

get_all_breeds()

all_groups = ['Australian Cattle Dog', 'Australian Shepherd', 'Bearded Collie', 'Beauceron', 'Belgian Malinois', 'Belgian Sheepdog', 'Belgian Tervuren', 'Bergamasco', 'Berger Picard', 'Border Collie', 'Bouvier des Flandres', 'Briard', 'Canaan Dog', 'Cardigan Welsh Corgi', 'Collie', 'Entlebucher Mountain Dog', 'Finnish Lapphund', 'German Shepherd Dog', 'Icelandic Sheepdog', 'Miniature American Shepherd', 'Norwegian Buhund', 'Old English Sheepdog', 'Pembroke Welsh Corgi', 'Polish Lowland Sheepdog', 'Puli', 'Pumi', 'Pyrenean Shepherd', 'Shetland Sheepdog', 'Spanish Water Dog', 'Swedish Vallhund', 'Afghan Hound', 'American English Coonhound', 'American Foxhound', 'Basenji', 'Basset Hound', 'Beagle', 'Black and Tan Coonhound', 'Bloodhound', 'Bluetick Coonhound', 'Borzoi', "Cirneco dell'Etna", 'Dachshund', 'English Foxhound', 'Greyhound', 'Harrier', 'Ibizan Hound', 'Irish Wolfhound', 'Norwegian Elkhound', 'Otterhound', 'Petit Basset Griffon Vendeen', 'Pharaoh Hound', 'Plott', 'Portuguese Podengo Pequeno', 'Redbone Coonhound', 'Rhodesian Ridgeback', 'Saluki', 'Scottish Deerhound', 'Sloughi', 'Treeing Walker Coonhound', 'Whippet', 'American Eskimo Dog', 'Bichon Frise', 'Boston Terrier', 'Bulldog', 'Chinese Shar-Pei', 'Chow Chow', 'Coton de Tulear', 'Dalmatian', 'Finnish Spitz', 'French Bulldog', 'Keeshond', 'Lhasa Apso', 'Lowchen', 'Norwegian Lundehund', 'Poodle', 'Schipperke', 'Shiba Inu', 'Tibetan Spaniel', 'Tibetan Terrier', 'Xoloitzcuintli', 'Airedale Terrier', 'American Hairless Terrier', 'American Staffordshire Terrier', 'Australian Terrier', 'Bedlington Terrier', 'Border Terrier', 'Bull Terrier', 'Cairn Terrier', 'Cesky Terrier', 'Dandie Dinmont Terrier', 'Glen of Imaal Terrier', 'Irish Terrier', 'Kerry Blue Terrier', 'Lakeland Terrier', 'Manchester Terrier', 'Miniature Bull Terrier', 'Miniature Schnauzer', 'Norfolk Terrier', 'Norwich Terrier', 'Parson Russell Terrier', 'Rat Terrier', 'Russell Terrier', 'Scottish Terrier', 'Sealyham Terrier', 'Skye Terrier', 'Smooth Fox Terrier', 'Soft Coated Wheaten Terrier', 'Staffordshire Bull Terrier', 'Welsh Terrier', 'West Highland White Terrier', 'Wire Fox Terrier', 'Affenpinscher', 'Brussels Griffon', 'Cavalier King Charles Spaniel', 'Chihuahua', 'Chinese Crested', 'English Toy Spaniel', 'Havanese', 'Italian Greyhound', 'Japanese Chin', 'Maltese', 'Manchester Terrier', 'Miniature Pinscher', 'Papillon', 'Pekingese', 'Pomeranian', 'Poodle', 'Pug', 'Shih Tzu', 'Silky Terrier', 'Toy Fox Terrier', 'Yorkshire Terrier', 'Akita', 'Alaskan Malamute', 'Anatolian Shepherd Dog', 'Bernese Mountain Dog', 'Black Russian Terrier', 'Boerboel', 'Boxer', 'Bullmastiff', 'Cane Corso', 'Chinook', 'Doberman Pinscher', 'Dogue de Bordeaux', 'German Pinscher', 'Giant Schnauzer', 'Great Dane', 'Great Pyrenees', 'Greater Swiss Mountain Dog', 'Komondor', 'Kuvasz', 'Leonberger', 'Mastiff', 'Neapolitan Mastiff', 'Newfoundland', 'Portuguese Water Dog', 'Rottweiler', 'Samoyed', 'Siberian Husky', 'Standard Schnauzer', 'Tibetan Mastiff', 'St. Bernard', 'American Leopard Hound', 'Appenzeller Sennenhunde', 'Azawakh', 'Barbet', 'Basset Fauve de Bretagne', 'Belgian Laekenois', 'Biewer Terrier', 'Bolognese', 'Bracco Italiano', 'Braque du Bourbonnais', 'Brazue Francais Pyrenean', 'Broholmer', 'Catahoula Leopard Dog', 'Caucasian Shepherd Dog', 'Central Asian Shepherd Dog', 'Czechoslovakian Vlcak', 'Danish-Swedish Farmdog', 'Deutscher Wachtelhund', 'Dogo Argentino', 'Drentsche Patrijshond', 'Drever', 'Dutch Shepherd', 'Estrela Mountain Dog', 'Eurasier', 'French Spaniel', 'German Longhaired Pointer', 'German Spitz', 'Grand Basset Griffon Vendeen', 'Hamiltonstovare', 'Hokkaido', 'Hovawart', 'Jagdterrier', 'Jindo', 'Kai Ken', 'Karelian Bear Dog', 'Kishu Ken', 'Kromfohrlander', 'Lancashire Heeler', 'Mudi', 'Nederlandse Kooikerhondje', 'Norrbottenspets', 'Perro de Presa Canario', 'Peruvian Inca Orchid', 'Portuguese Pondengo', 'Portuguese Pointer', 'Portuguese Sheepdog', 'Pudelpointer', 'Pyrenean Mastiff', 'Rafeiro do Alentejo', 'Russian Toy', 'Russian Tsvetnaya Bolonka', 'Schapendoes', 'Shikoku', 'Slovensky Cuvac', 'Slovensky Kopov', 'Small Munsterlander Pointer', 'Spanish Mastiff', 'Stabyhoun', 'Swedish Lapphund', 'Teddy Roosevelt Terrier', 'Thai Ridgeback', 'Tornjak', 'Tosa', 'Transylvanian Hound', 'Treeing Tennessee Brindle', 'Working Kelpie']
