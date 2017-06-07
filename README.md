# Spot

Spot is an online marketplace for dog breeders and buyers to connect. Users can search for dog breeds by characteristics (web-scraped from www.akc.org). Users can also search for dog breeders in their area (fake breeder data used for the purposes of this project). On a breeder's homepage, users can find information about the breeder, including location, litters, dogs, events, and a blog.
Spot is a project I completed in 4 weeks during my software engineering fellowship at Hackbright. 

# Contents
* [Technologies](#technologies)
* [Data Modeling](#data)
* [Features](#features)
* [Installation](#install)


## <a name="technologiesused"></a>Technologies Used

* Python
* JavaScript/jQuery
* JSON/AJAX
* Flask
* PostgreSQL
* SQLAlchemy
* BeautifulSoup
* Jinja2
* HTML/CSS
* Bootstrap
* Google Maps API

## <a name="data"></a>Data Modeling

My favorite part of this project was designing the database structure. Knowing that dog breeders need to present a lot of data to their buyers, I really thought through what pieces of information to include and how they would need to be related to each other. Below is in image of the structure I built out before writing any code - 22 tables with lots of fun relationships between them!
<kbd>![Database Structure](/static/img/database_structure.png)</kbd>

The most challenging part of this project was web-scraping the breed information/standards from The American Kennel Club's website (www.akc.org). The breeds' html pages were all set up slightly differently, so I was unable to web-scrape them all at the same time. I clustered the breeds based on html setup-similarities and then web-scraped in groups. It was difficult - but in the end very fun and rewarding.

The breeder data provided in this repo is all fake data that was randomly generated.

## <a name="features"></a>Features

Users can search for a breed that fits their needs, using criteria from the American Kennel Club's website. The criteria are size, energy level, group, a list of traits ('good with kids', 'apartment dog', etc), and a keyword. 

<kbd>![breed1](/static/img/readme/breed-search.png)</kbd>

An algorithm sorts the results based on relevance, and from there the user can go to a breed's home page for more information.
