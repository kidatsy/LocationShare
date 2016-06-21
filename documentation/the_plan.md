#Tracking location

##High level details

The goal of this application is to get the location of a user, that they opt into.  

Here is how things will go from a user perspective.

1. the user is passed a unique url
2. the user visits the url by openning a browser
3. the user clicks allow browser to share location

Here is how things will go from the developer perspective

1. a unique id is generated for every new session with a user
2. the unique id is passed to a function which generates a unique route
3. the unique route is served by a server with hotswaping
4. once the unique route has been visited and permission to share location has been given, the location and unique id
is passed to the database for storage, along with a timestamp of when the location was shared.
5. once the session is over the route is removed dynamically from the server

##Technologies used

For this application I'm going to make use of html5's geolocation service, flask, and and featherweight, to dynamically generate routes.

featherweight can be found here: https://github.com/EricSchles/featherweight_web_api

Work flow:

Hi risk conversation -> 

	- cc ids risk
	- supervisor takes over conversation

Investigation comences ->
	
(PSAP - public saftey answering point - 911 folks)
	- ask for address:
		-> yes - call PSAP
		-> no - silence - call presumed PSAP
	PSAP might not successfully yield something and no might yield something -> PSAP dispatches EMS

Work flow for supervisor:

1. pull up location share
2. get url to send to texter
3. long pull/socket events 
	- notifying: 1. the link has been openned
				 2. the location once sent

Deleting information should be done by supervisor if they click "close case"
Scrub information every 48 hours.

Other data:

- user agent string parsed - ip address
- we want browser information, ip address, (is this at home?  Or is this mobile?)

Serving things:

Beanstalk for serving!  RDS layer (implicitly)
Use environment variables for configuration with server side stuff.
Use a virtual env.

Chris will set up everything, just push and use environment variables for things.

realtime update for all the location information

delete anything older than 48 hours only

Frontend:

- bootstrap dashboard like
- user accounts
- no high level statistics

SMS features:

- because we are getting permission from the browser this is a different experience - Make sure to describe in the message what's happening in the link.


Stub:

<li class="list-group-item">latitude: {{ result.latitude }} </li>
<li class="list-group-item">longitude: {{ result.longitude }} </li>
<li class="list-group-item">timestamp: {{ result.timestamp }} </li>
<li class="list-group-item">unique id: {{ result.unique_id }} </li>


