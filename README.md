# Gradescope API
This is an initial attempt at reverse engineering gradescope to allow for automated submission and controlling other
behaviour in an automated way as there is no official gradescope API.

Some initial endpoint info was [gotten from this MIT paper](https://courses.csail.mit.edu/6.857/2016/files/20.pdf).

## Design Philosophy
This is _not_ an API wrapper in reality, and more of a scraping tool. Therefore a lot is done to minimize the 
ammount of requests done. As such we do expensive things like loading rosters lazily but all at once. This means
we keep a lot of data locally (which is a space cost) but that allows us to not make network calls as often and lets
us update the local copy alongside posts.

## Design Structure
The primary structure used to interact with gradescope is the `session`. This is equivalent to going to the website
and hitting `Log In` and will give you access to the things you can access through the website normally.

### Sessions
```
session = GSConnection()
```
This creates a session but does not do any login work. This leaves the connection in an inactive state. In order
to activate it you can call the following:
```
session.login('my@email.com', 'my_password')
```

