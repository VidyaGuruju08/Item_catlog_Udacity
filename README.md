# ITEM CATALOG

## Aim of the Application ##
This is an application that provides a list of items within a variety of categories as well as provides a user registration and authentication system. Authentication is provided via OAuth and all data is stored within a PostgreSQL database. Authenticated users will have the ability to post, edit, and delete their own items. This Restful web application uses the Python framework Flask along with third-party OAuth authentication.

## Tools and Frameworks ##
This web application was built with HTML5, CSS, Vagrant, Flask, SQLAlchemy, Google Oauth2 & APIs.

## Prerequisites ##
Requires Python, pip, and you will need git  to be installed.


## Steps to run this application ##

-> Have Vagrant and Virtual Box installed on your machine.
-> Unzip the file and put the contents in the vagrant directory.
-> Launch the Vagrant box (VM).
	 $ vagrant up 
	 $ vagrant ssh 
-> To Initialize Database and To initialize the SQLite database 
	 $ python database.py 
-> To load the initial sporting categories
	$ python Clotsofmenu.py
	Now categories and some items belong to that category are added.
-> To start the application or to run the project on the server
	$ python Cproject.py
-> The web app will be running on your localhost at port 5001 ( http://localhost:5001/ )
-> Open the above mentioned link to use the web app.
-> You can only view the catalog without signing in.
-> To create, update and delete the items in the catlog, sign in using Google+.
-> To login using Google+
	http://localhost:5001/login to login to the app
-> To Use Google Authentication Services
	We will need a client_secret.json file.
We can create an application to use Google's OAuth service at https://console.developers.google.com.
After creating and downloading client_secret.json file, move it to the directory where it is accessible to the project file.
Adding, editing, and deleting items requires the user to log in. Logins are handled by Google OAuth.
Users can see all items but can only edit and delete their own items.



