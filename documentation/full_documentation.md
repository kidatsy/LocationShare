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

###Python/Flask

Throughout this guide I will assume you understand the Python programming language.  Familiarity with Flask will not be assumed and I will make every attempt to explain Flask.  If you don't know Python, no worries!  It's very easy to learn.  Here are some resources I've found useful for getting up to speed quickly:

* [Learn Python the Hard Way](http://learnpythonthehardway.org/book/)
* [MIT's gentle introduction](http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2011/)
* [MIT's computer science intro class in Python](http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/)
* [Python - from first principals to Graphs](http://interactivepython.org/runestone/static/pythonds/index.html)

There are also more than a few resources other than this that are great, but those are my personal favorites.  From this point forward I will assume you know how python works!

Okay, so now that we have that out of the way, let's install flask and get a first example out of the way, so you can get started with understanding flask.  The next thing you'll need is pip (the python package manager).  You can get it [here](https://pip.pypa.io/en/stable/installing/).  After you have pip installed, go ahead and open a terminal and type:

`pip install flask`

At this point you should have flask installed.  If for some reason that failed you might be able to get it from another source like `brew` on mac os x, or `apt-get` on ubuntu.  If you're on windows, you can use [this site](http://www.lfd.uci.edu/~gohlke/pythonlibs/).  But for reasons of personal sanity, I highly recommend a linux based system for any and all development work in Python.  It's honestly just easier.  

Once you have flask and pip installed you'll be ready to copy paste the following one page application into a file called `app.py`:

```
from flask import Flask

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
	return "Hello world!"

app.run(debug=True)
```

once you have this code copy/pasted into `app.py` you can go ahead and run:

`python app.py`

This should start a local server.  Now you can go to [http://localhost:5000/](http://localhost:5000/) and you should see a browser window that says "Hello world!".  

There is actually quiet a bit going on here!  First we are creating our application - `app` from a `Flask` object, which we initialize from the current namespace.  Then we decorate methods to control how our different routes get called.  The idea of decoration in Python is a little bit tricky to understand, so let's break it down:

A decorator method is one that takes in a function and then augments the input to the function or output from the function in some way (or both).  In this case the route method, which operates within the `app` object context, augments the function by assigning it's output to the relative route passed into the `route` method.  

A second optional argument is the type of RESTful operations this route supports - in our case, "GET" and "POST", which means you can send data to this route and get data from this route, respectively.  Technically "POST" should only be included for methods that either get further information to display to the user, like on a click event or if the method is submitting form data to the server, but we include it here for purely illustrative purposes.  

The next thing to understand is the `app.run`.  This runs the flask server.  In our fully fledged application we won't be making use of the `app.run` method and will instead use gunicorn - a multithreaded server that performs much better than flask's builtin server.  However, for local testing `app.run` is fine.  

Now that we have a general sense of the basics of a flask route, let's go through and look at our routes.  By convention all flask routes should be stored in `views.py`.  At scale there should really be multiple view files, each with their own blueprint.  But this will do for the size and scale of the current version of the application.  

At this point it might be a good idea to clone the repository:  

`git clone https://github.com/CrisisTextLine/LocationShare.git`

Here's the directory structure the of the application:

```
location_share/
	requirements.txt
	runtime.txt
	.gitignore
	Procfile
	auto_delete_database.py
	manage.py
	run.py
	migrations/
	app/
		__init__.py
		models.py
		views.py <---
		static/
			map.jpg
		templates/
			map.html
			login.html
			get_location.html
			map_view.html
			show_db.html
```

Okay let's zero in on views.py:

Imports:

```
from app import app
from app.models import *
from app import db
from app import login_manager
import random
from datetime import datetime, timedelta
import json
from flask import request, render_template, url_for,redirect,session,g
import flask_login as flask_login
```

Notice that we import the other pieces of our flask application from the top level flask directory, that's why we do `from app.models import *` - here app refers to the `app/` directory and `models` refers to `models.py` in the `app/` directory.  You may notice that we also have three objects that we import from the `app/` directory:

* `app` - the app object 
* `db` - the database object
* `login_manager` - the application by which we access user state

In order to understand where these objects are coming from we'll need to dig into `__init__.py`.  The `__init__.py` file acts as an initializer for everything available to a python package.  We might want to think of this as the why python packages store global state.  Let's take a look at our `__init__.py` file:

```
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import flask_login as flask_login
import os

username,password = "eric_schles","1234"
app = Flask(__name__)
#if on localhost: app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://"+username+":"+password+"@localhost/location_share"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.secret_key = 'super secret string'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from app import views,models
```

Some of this should look familiar from our toy application (defined above).  The first line:

`app = Flask(__name__)` is exaclty the same and defines the flask object we will use to initialize our routes.  It defines the context with which our flask application run and gives us a whole bunch of context specific state.  

Our username and password - defined here:

`username,password = "eric_schles","1234"` only works when we are working in our application locally, so there's no harm in leaving it hardcoded.  We make use of this username and password here:

```#if on localhost: app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://"+username+":"+password+"@localhost/location_share"```

If we are working locally, this should be:

`app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://"+username+":"+password+"@localhost/location_share"`

and then we'd comment out the following line:

```#If we are working on the server: app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]```

`app.secret_key = 'super secret string'` - this sets up the secret_key for our application - this is important for flask-login, somehow.  I couldn't figure out how this actually affects things.  But best to chance this to something actually secret on the server, because some how it interacts with flask-login.  

Here we set up the database object:

`db = SQLAlchemy(app)` - SQLAlchemy takes in the application context and creates a database context - db - a database object which we will use to interact with our database.

Here we set up the migration context for local migrations to our database:

`migrate = Migrate(app,db)` - Migrate takes in the application context and creates a migration context - migrate - a migration object which we will use to create and rollback migrations for our database.

Here we setup the manager and add the migration command so we can migrate our database:

`manager = Manager(app)` - Manager takes in the application context and creates the manager context - manager - a manager object which we will use to create and rollback migrations for our database.
`manager.add_command('db', MigrateCommand)`  - here we add the migrate command so that we can actually use the migrations.  

So a natural question is - why did we need the migrate object if we use the manager to actually do the migrations?  Honest answer, I don't know.  I looked over the Flask-migrate documentation but I couldn't figure out why I need this object since I don't think it ever get's used.  But since this is going to be global to the application, there is probably some internal code that makes use of this context that we just aren't seeing.  

Here we set up our login manager:

`login_manager = flask_login.LoginManager()` - here we create our login manager object.
`login_manager.init_app(app)` - here we take in the application context and initializes a `login_manager` context with the app context.

Finally, we import the views and models:

`from app import views,models` - it feels a bit odd to do this, but here app refers to `app/` directory, not the `app` object.  More or less we are bringing views and models into the application context.  The flask documentation has a better explanation for this, but it feels a bit awkward and strange, so I don't tend to dig too deep into it.  

Now that we understand where all our global objects are coming, let's see how they are used in our `views.py`, the meat of our application:

###Understanding Login

```
#These routes are for logging in and out
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form['email']
    password = request.form['pw']
    user = User.query.filter_by(email=email).first()
    if user:
        if user.password == password:
            flask_login.login_user(user,force=True)
            flask_login.current_user = user
            return redirect(url_for('show_db'))
    return 'Bad login'

@app.before_request
def before_request():
    g.user = flask_login.current_user
    
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'
```

The login route is the first page that users see.  It should look like this:

![](login_screen.png)


The login function get's the login information via `request` which comes with flask.  If you are wondering how to import request:

`from flask import request`.  

`request` is one of the most powerful objects in the flask framework - it treats form data as part of a dictionary - so you can get any form data, via the input field's name attribute.  So for example, to get the email from the form we simply do:

`email = request.form['email']`

We'll make use of the information we get from the email field to get all the user information:

`user = User.query.filter_by(email=email).first()`.  We'll use this to ensure that the email address and password we have on file were correctly input:

```
password = request.form['pw']
if user:
        if user.password == password:
```

Once we have the password verified we log them in:

```
flask_login.login_user(user,force=True)
flask_login.current_user = user
return redirect(url_for('show_db'))
```

This is one of the best parts about flask login - you can login user's intuitively with a single method call:

`flask_login.login_user(user,force=True)`.

Once we've logged in the user we redirect to the route, show_db - this is the name of the function in our views.  We'll need to make sure, when writing new function that the method exists in our view context, before (in our case meaning in the `views.py` file), before we write any redirect's for it.  

Now to see the real power of the Flask-login, let's look at the url we get redirected to after login, show_db:

```
@app.route("/show_db",methods=["GET","POST"])
@flask_login.login_required
def show_db():
    locations = [to_geojson([elem.latitude,elem.longitude]) for elem in Clients.query.all() if elem.latitude != '' and elem.longitude != '']
    return render_template("show_db.html",results=Clients.query.all(),locations=json.dumps(locations))
```

This may seem like a pretty simple method (and it should), but it's super powerful!  Note first that we have a second decorator after `@app.route` - `@flask_login.login_required`.  This is all we need to ensure that our user logged in before they were able to see this route!  Otherwise users are met with a user unauthorized screen and won't be able to see any information!  Pretty awesome, huh?

Our `show_db` route, get's all our users, in this case defined as clients, from the parlenance of social workers, and get's all our geographical data, from users who have provided that information to us.  This will be shown as follows:

![](show_db.png)

As you can see, we can see all the information about our users and we can see this information geographically, via a map (below the user data).  This is where the user - client information goes and the location information goes, respectively.

Now let's dig into the `show_db.html` file to understand how flask-templates get rendered and to see some javascript in action!

```
<!-- ..snipped from show_db.html.. -->

<div class="container">
  <h2>User Information</h2>
  <p>Use the unique id to interact with a user - deleting them</p>
  <table class="table">
    <thead>
      <tr>
        <th>Unique ID</th>
        <th>URL</th>
        <th>latitude</th>
        <th>longitude</th>
        <th>timestamp</th>
        <th>link clicked</th>
        <th>map view</th>
      </tr>
    </thead>
    <tbody>
      {% for result in results %}
        <tr>
          <td>{{result.unique_id}}</td>
          <td>{{result.url}}</td>
          <td>{{result.latitude}}</td>
          <td>{{result.longitude}}</td>
          <td>{{result.timestamp}}</td>
          <td>{{result.link_clicked}}</td>
          <td><a href="/map_view/{{result.unique_id}}">map view</a></td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</div>
```

I won't be going through all the html code, because 1 - I'm assuming you understand HTML and 2 - that'd just be really hard to follow.  

So let's zero in on our evaluated code, specfically the for-loop:

```
   {% for result in results %}
        <tr>
          <td>{{result.unique_id}}</td>
          <td>{{result.url}}</td>
          <td>{{result.latitude}}</td>
          <td>{{result.longitude}}</td>
          <td>{{result.timestamp}}</td>
          <td>{{result.link_clicked}}</td>
          <td><a href="/map_view/{{result.unique_id}}">map view</a></td>
        </tr>
      {% endfor %}
```

This code makes use of `{%` and `%}` to start and end our for-loop statement.  Inside of the for loop, each element of our database object is evaluated to it's string equivalent, for example - `{{result.unique_id}}`, which is then displayed to the user.  It's important to note that you can evaluate this information even inside of strings as seen through this:  `<a href="/map_view/{{result.unique_id}}">`.  Also note that we need to end our for loop with:

`{% endfor %}`.

So what's the general rule?  For control flow we use `{%` and  `%}`.  For evaluation of objects we use `{{` and `}}`.  So to do a computation and display it as a string use: `{{` and `}}`.  I guess a better rule of thumb is, anything you want the user to see makes use of: `{{` and `}}`.  

Now let's understand our Javascript functions:

```
<script>

function Main(){
  pingServer();
  loadMap(); 
}

function pingServer(){
	var one_second = 1000;
	var one_minute = 60*one_second;
	var two_minutes = 2*one_minute;
	setTimeout(function(){
   		window.location.reload(1);
	}, one_minute);
}

function loadMap(){
  var locations = JSON.parse({{locations|tojson}});
  L.mapbox.accessToken = 'pk.eyJ1IjoiZXJpY3NjaGxlcyIsImEiOiI5Zjk4MjVkZTZlMjAwM2I3OTY2OTI4MTJmODVkN2Q3MCJ9.1gRox8Gx76YqrBJiCsxLLQ';  
  var map = L.mapbox.map('map', 'mapbox.streets')
  .setView([locations[0]["geometry"]["coordinates"][1],locations[0]["geometry"]["coordinates"][0]],11)
  .featureLayer.setGeoJSON(locations);
}

function getURL(){
  $.get( "/send_url",function(data){
     document.getElementById("new_url").innerHTML=$.parseJSON(data)["url"];
  })
}

function deleteAll(){
  $.post("/delete_all_users");
}

</script>
```

The pingServer method reloads our page, displaying any new information from the database - here we reload once a minute.  

The loadMap function gets all our information from the flask-server on reload or load, as well and displays it to the user.  Notice that loadMap expects [GeoJson](http://geojson.org/).  Our getURL function, which we use here:

![](get_url.png)

(A button found in our admin controls section in /show_db)

This makes use of JQuery's simple syntax to make a get request and then pass the generated url to our front end.  For more information on this please check out:

* [jquery & flask, first stackoverflow answer](http://stackoverflow.com/questions/29987323/how-do-i-send-data-from-js-to-python-with-flask)

And last but not least, if you want to delete all users older than 48 hours ago, you can use the `deleteAll` method, which is activated by this button:

![](delete_all.png)

Everything else should be pretty straight forward and therefore won't be covered here.  If needed, please feel free to contact Eric Schles @ ericschles@gmail.com if you feel this section is missing something or for further questions. 

