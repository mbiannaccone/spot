# Spot

Spot is an online marketplace for dog breeders and buyers to connect. Users can search for dog breeds by characteristics (web-scraped from www.akc.org). Users can also search for dog breeders in their area (fake breeder data used for the purposes of this project). On a breeder's homepage, users can find information about the breeder, including location, litters, dogs, events, and a blog.
Spot is a project I completed in 4 weeks during my software engineering fellowship at Hackbright.

Deployed on AWS: [www.spot-spot.com](http://www.spot-spot.com/)

# Contents
* [Technologies Used](#technologiesused)
* [Data Modeling](#data)
* [Features](#features)
* [Installation](#install)
* [About the Author](#author)


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

REGISTER/LOGIN: Users can login/register by clicking on the drop-down on the right-hand side of the navbar.

<kbd>![navbar](/static/img/readme/navbar-login-register.png)</kbd>

BREED SEARCH: From the landing page users can search for a breed that fits their needs, using criteria from the American Kennel Club's website. The criteria are size, energy level, group, a list of traits ('good with kids', 'apartment dog', etc), and a keyword. 

<kbd>![breed-search1](/static/img/readme/breed-search.png)</kbd>

An algorithm sorts the results based on relevance

<kbd>![breed-search2](/static/img/readme/breed-search2.png)</kbd>

From there the user can go to a breed's home page for more information and read through the breed standards and information that was web-scraped from the American Kennel Club's website.

<kbd>![breed1](/static/img/readme/breed1.png)</kbd>
<kbd>![breed2](/static/img/readme/breed2.png)</kbd>

BREEDER SEARCH: It's easy to jump over to the breeder data from here using the "find a breeder" search button on the left side. That will pull up all the breeders of this breed and place them on a Google Map (using the Google Maps API). It also calculates the distance between the user and each of the breeders, and ranks them according to proximity. 

Note: the user can also get to this same place from the homepage, by using the breeder search box on the right side.

<kbd>![breeder-search1](/static/img/readme/breeder-search.png)</kbd>


<kbd>![breeder-search1](/static/img/readme/breeder-search1.png)</kbd>

On a breeder's page, the user can find a host of information - photos, location, litters, dogs, awards, events, and a blog. 

<kbd>![breeder1](/static/img/readme/breeder1.png)</kbd>

You can also navigate to further pages for individuals components - for example one of the breeder's litters:

<kbd>![litter](/static/img/readme/litter.png)</kbd>

If the user decides they like this breeder, they can 'spot' it using the green paw in the corner of the breeder's photo gallery. Then, when the user navigates to their homepage they can see all the breeders (and breeds) that they've spotted, and any relevant information (litters, event) that might interest them. 

<kbd>![homepage](/static/img/readme/homepage.png)</kbd>

Also on the user's homepage is a dynamic form where the user can update their
information. When the user clicks submit, it sends an AJAX call to the database
to update the information (after the user verifies their password).

<kbd>![user](/static/img/readme/user-info.png)

## <a name="install"></a>Installation

To install Spot:

Install PostgreSQL (Mac OSX)

Clone or fork this repo:

```
https://github.com/mbestwick/spot
```

Create and activate a virtual environment inside your Spot directory:

```
virtualenv env
source env/bin/activate
```

Install the dependencies:

```
pip install -r requirements.txt
```

Set up the database:

```
createdb spot
psql spot < dogs.sql
```

Run the server:

```
python server.py
```

You can now navigate to 'localhost:5000/' to access and enjoy Spot!

## <a name="author"></a>About the Author

Hello! My name is [Michela Bestwick](https://www.linkedin.com/in/michela-bestwick/) and I am a software engineer. I grew up in the bay area and graduated from UCLA in 2012 with a B.S. in Mathematics. For five years I worked as a consultant at Triage Consulting Group, where I analyzed complex healthcare data sets (using SQL) and managed large databases. My love for data and problem solving led me to software engineering. I attended Hackbright Academy, a 12-week intensive software engineering fellowship for women, and graduated in June 2017. I am currently seeking full-time employment as a software developer in the San Francisco Bay Area. Feel free to email michelabestwick@gmail.com if you'd like to discuss my project or future employment. Thanks!

