#Location Share

Welcome to the documentation for location share!  In this documentation we'll be walking through the location share application and explaining it's features as well as work flows!

##Preamble 

The location share application (at least this version) was created by Eric Schles with direction from Chris Johnson, (CTO of crisis text line at the time of this writing).  The goal of this application is pretty simple - to make it easy to figure out where clients who may be in danger or a danger to themselves are at the time they start texting with crisis text line.  

At the present time getting your location from a mobile phone is hard.  However, browsers are reasonably good at tracking this.  Thus we are working off the assumption that browser GPS tracking will be sufficient to get a relatively close location to a client (the person texting crisis text line), who is in need.

##How location share was built - High Level

This version of the platform is built with three languages:

* Python (backend / middleware)
* Jinja2 templates (frontend)
* HTML (frontend)
* Javascript (frontend)
* Jquery (frontend/ middleware)

###Backend / Middleware

Within the Python context [Flask](http://flask.pocoo.org/) is being used, a powerful micro framework that scales reasonably easily.  It's worth noting that if this application is going to be extended and scaled up, it'd be worth looking at [blueprints](http://flask.pocoo.org/docs/0.11/blueprints/), a concept used to help keep code easy to understand within flask apps.  

In addition to using Flask, the application uses, [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/) (a general purpose ORM), [Flask-login](https://flask-login.readthedocs.io/en/latest/), [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) some great simple to use addons for the flask framework that give it a lot of extra power at minimal code cost.  

As for the backend - we are making use of postgres and postgresql.  There are numerous postgres resources on the internet, and people tend to have their own favorite resources for this wonderful database.  I'll include mine here but if you have your own, please feel free to use that instead:

* [some minimal documentation I maintain](https://github.com/EricSchles/postgres_flask_macosx)
* [postgres official docs](https://www.postgresql.org/docs/)
* [heroku postgres docs](https://devcenter.heroku.com/categories/heroku-postgres)

Feel free to use your own favorite resources!

###Frontend

Now that we've talked about all the backend technologies at a high level, let's dive into the frontend high level!  Flask applications come with a templating language called jinja that allow you to embed control-flow, variable assignment, looping, and evaluation of python statements, directly into your frontend code.  This application makes use of looping and evaluation on the frontend.  Additionally, this application makes use of standard HTML and client side javascript.  Additionally, JQuery is used to make some server side calls to send specific pices of information.

In order to understand how JQuery and flask interoperate, I'd check out this stackoverflow answer (it's the one I used):

[jquery & flask, first stackoverflow answer](http://stackoverflow.com/questions/29987323/how-do-i-send-data-from-js-to-python-with-flask)

In addition to that, I made use of the following resources to get the location information:

* [getting location information from the browser](https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/Using_geolocation)
* [w3schools tutorial on getting location information](http://www.w3schools.com/html/html5_geolocation.asp)

The last thing I did was make use of bootstrap to make things a little pretty.  I won't go into depth about that here, other than reference [bootstrap's documentation here](http://getbootstrap.com/)


##Diving in



