# Adventure Planner
Adventure Planner helps users plan their next adventure. Yelp and Google Maps API are implemented to allow users to search any city and have the option to choose top sights (Sightseeing/tourist attraction), museums, nature, night life, or restaurants. Users can interact with a map of the sights to plan their adventure. Once explored, the user can make a profile to save their sights to a trip they create, which are stored in a PostgreSQL database. Users can also make a to-do list for each trip, check it off when they are done with the task, delete a trip or sight, and the status is dynamically updated via AJAX.

<img src="/static/_readme-img/homepage.JPG">

## Table of Contents

* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [Looking Ahead](#future)

## <a name="tech-stack"></a>Tech Stack

__Frontend:__ JavaScript (AJAX, JSON), HTML, CSS, jQuery, Bootstrap, Jinja <br>
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy<br>
__APIs:__ Yelp, Google Maps <br>

## <a name="features"></a> Features

Search for any city and choose top sights, museums, nature, night life, or restaurants. User account registration not required. <br><br>
<img src="/static/_readme-img/search.gif">

Once registered and logged in, user can add/delete an adventure to their profile<br><br>
<img src="/static/_readme-img/profile.gif">

While logged in, user can add any sight to a trip of their choice and view the sights <br><br>
<img src="/static/_readme-img/addsight.gif">

User can add to a to-do list and check it off when the are done with the task and also delete a sight <br><br>
<img src="/static/_readme-img/todo.gif">

## <a name="installation"></a>Setup/Installation

Requirements:

- PostgreSQL
- Python 2.7
- Yelp API keys

To have this app running on your local computer, please follow the below steps:

Clone repository:
```
$ git clone https://github.com/tuongviatruong/Adventure-project.git
```
Create a virtual environment:
```
$ virtualenv env
```
Activate the virtual environment:
```
$ source env/bin/activate
```
Install dependencies:
```
(env) $ pip install -r requirements.txt
```
Get your own secret keys for [Yelp](https://www.yelp.com/developers/documentation/v3/authentication). Save them to a file `secrets.sh`. Your file should look something like this:
```
export CLIENT_ID="abc"
export YELP_API_KEY="abc"
```
Load secret info into the environment:
```
(env) $ source secrets.sh
```
Create database 'trips'.
```
(env) $ createdb trips
```
Create your database tables.
```
(env) $ python -i model.py
Connected to DB.
>>> db.create_all()

```
Run the app from the command line.
```
(env) $ python server.py
```

## <a name='future'></a> Looking Ahead
* Add more testing
* Add a map of the sights user added and get directions
* Ability to organize trips by days
