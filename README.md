# Adventure Planner
Adventure Planner helps users plan their next adventure. Yelp and Google Maps API are implemented to allow users to search any city and have the option to choose top sights (Sightseeing/tourist attraction), museums, nature, night life, or restaurants. Users can interact with a map of the sights to plan their adventure. Once explored, the user can make a profile to save their sights to a trip they create, which are stored in a PostgreSQL database. Users can also make a to-do list for each trip, check it off when they are done with the task, delete a trip or sight, and the status is dynamically updated via AJAX.

<img src="/static/_readme-img/homepage.jpg">

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

Search for any city and choose top sights, museums, nature, night life, or restaurants. User account registration not required. <br>
<img src="/static/_readme-img/search.gif">

Once registered and logged in, user can add/delete an adventure to their profile
<img src="/static/_readme-img/profile.gif">