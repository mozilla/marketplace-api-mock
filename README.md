A mock API server for Firefox Marketplace frontend projects. This is primarily
used for continuous integration tests as well as offering a solution to offline
development. In other words, it allows frontend projects to not need an actual
installation of the backend.

- [Marketplace frontend documentation](https://marketplace-frontend.readthedocs.org)
- [Marketplace documentation](https://marketplace.readthedocs.org)
- [Marketplace API documentation](https://firefox-marketplace-api.readthedocs.org)


## Installation

### Foreword

A foreword, you may not need to install the Marketplace mock API yourself.
There is an instance already set up and hosted:

```
https://flue.paas.allizom.org/
```

Some reasons that you might want to actually install the Marketplace mock API:

* You're working on the API
* You have a spotty internet connection
* You're creating new features which use yet-to-be-built APIs

### Installation Process

The Marketplace mock API is powered by Python+Flask. To install the Marketplace
mock API:

```bash
curl -s https://raw.github.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL
source ~/.profile
mkvirtualenv --no-site-packages marketplace-mock-api
workon marketplace-mock-api
pip install -r requirements.txt
python main.py
```

This will install a Python virtualenv, Pip dependencies, and start a local
server at `0.0.0.0:5000`. The server also takes ```--host``` and ```--port```
arguments.


## Developing

Development tips and guidelines:

- Since our tests depend on the mock API, keep geenrated results predictable
  as to not have intermittent test failures.
- To add an endpoint, look into ```main.py``` to add a view that returns a
response.
- If you are generating a mock object, a good place to add that would be in
factory.py

### Throttling

If you wish to throttle the server to test something, an easy way is to put
a ```time.sleep(X)``` into the view in ```main.py```.


## Deploying an Update

Note that you must be added to the Marketplace Stackato group. File a bug with
ops (e.g., bugzilla.mozilla.org/show_bug.cgi?id=895478) to gain access.
To deploy an update to the Marketplace mock API that is running on
```https://flue.paas.allizom.org/```:

```bash
stackato group marketplace
stackato push --no-prompt
stackato start
```

If ```stackato push``` doesn't work, try ```stackato update```.
If you don't want the instance to go temporarily offline during the push:

```bash
stackato group marketplace
stackato update
```

You'll be asked to confirm the following:

```
Bind existing services to 'flue' ?  [yN]: N
Create services to bind to 'flue' ?  [yN]: N
```

Enter `N` (or hit enter) to proceed.

## Additional API

To facilitate testing, some slugs will tell the mock API to return
specially-altered objects that have some explicitly defined results.

- ```/app/developed/``` returns an app that the user is the developer of
- ```/app/free/``` returns a free app
- ```/app/packaged/``` returns a packaged app
- ```/app/paid/``` returns a premium app
- ```/app/upsell/``` returns an app with upsell information
- ```/apps/rating/can_rate/``` returns reviews with metadata that states the
  user is authorized to review the app
- ```/apps/rating/cant_rate/``` returns reviews with metadata that states the
  user is *not* authorized to review the app
- ```/apps/rating/has_rated/``` returns reviews with metadata that states the
  user has previously reviewed the app
