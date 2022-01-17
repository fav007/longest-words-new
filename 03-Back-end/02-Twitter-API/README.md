# Twitter API

Now that we have played a bit with Flask, it's time to start the exercises which will keep us busy for the next three days. The goal is to build a clone of the [Twitter API](https://developer.twitter.com/en/docs/api-reference-index) using Flask and different Flask plugins (like [these](https://github.com/humiaozuzu/awesome-flask)).

⚠️ In this exercise, we will implement some API endpoints with a big restriction: we don't have a relational database yet! This constraint will help you focus on the HTTP layer of the API, not on the information retrieval. To abstract the database, we will use the [data access object (DAO)](https://en.wikipedia.org/wiki/Data_access_object) pattern and tomorrow we will replace it with actual queries to the database.

## Getting started

Let's start a new Flask project:

```bash
cd ~/code/<user.github_nickname>
mkdir twitter-api && cd twitter-api
pipenv --python 3.8
pipenv install flask
touch wsgi.py
```

### Factory Pattern

In the previous example, we initialized the `Flask` application right in the `wsgi.py`. Doing so, `app` was a global variable. The problem with this approach is it makes it harder to test in isolation. The solution to this problem is to use [Application Factories](http://flask.pocoo.org/docs/patterns/appfactories/), a pattern which will turn useful to make our app more modular (i.e. with multiple "small" files rather than some "big" ones).

👉 Take some time to read [this page of the Flask documentation](http://flask.pocoo.org/docs/patterns/appfactories/)

Let's use this approach:

```bash
mkdir app             # This is our main application's package.
touch app/__init__.py # And open this file in VS Code
```

```python
# app/__init__.py
# pylint: disable=missing-docstring

from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return "Hello World!"

    return app
```

Then open the `./wsgi.py` file and import this new `create_app` to use it right away:

```python
# ./wsgi.py

from app import create_app

application = create_app()
if __name__ == '__main__':
    application.run(debug=True)
```

Go ahead and launch the app:

```bash
FLASK_ENV=development pipenv run flask run
```

The server should start. Open your browser and visit [`localhost:5000/hello`](http://localhost:5000/hello). You should see "Hello world!" as a text answer!

### Namespace

The code in `app/__init__.py` is a copy/paste from the previous exercise, we just took the code and put it into a `create_app` method, returning the instance of `Flask` created. We can do better!

We will use the [`flask-restx`](https://flask-restx.readthedocs.io/) package:

```bash
pipenv install flask-restx
```

Take some time to read the following article:

:point_right: [Quick Start](https://flask-restx.readthedocs.io/en/stable/quickstart.html)

We want to start on the right foot in term of scalability, again take some time to read this:

:point_right: [Scaling your project](https://flask-restx.readthedocs.io/en/stable/scaling.html)

```bash
mkdir app/apis
touch app/apis/tweets.py
```

```python
# app/apis/tweets.py
# pylint: disable=missing-docstring

from flask_restx import Namespace, Resource

api = Namespace("tweets")


@api.route("/hello")
class TweetResource(Resource):
    def get(self):
        return "Hello from the 'tweets' namespace!"
```

:bulb: By using to our "tweets" namespace `api = Namespace("tweets")`, our "hello" API route will become `/tweets/hello` instead of just `/hello`

:bulb: The `get` method defined above will be called when the server receives an HTTP GET request on `/tweets/hello`

We can now import our simple namespace into our main application, like this:

```python
# app/__init.py__
# pylint: disable=missing-docstring

from flask import Flask
from flask_restx import Api

def create_app():
    app = Flask(__name__)

    from .apis.tweets import api as tweets
    api = Api()
    api.add_namespace(tweets)
    api.init_app(app)

    app.config['ERROR_404_HELP'] = False
    return app
```

If you stopped your server, restart it with:

```bash
FLASK_ENV=development pipenv run flask run
```
Open your browser and visit [`localhost:5000/tweets/hello`](http://localhost:5000/tweets/hello). You should see "Hello from the 'tweets' namespace!" as a text answer!

💡 It's important to understand the `from .apis.tweets import api as tweets` line which happens before the namespace registering. The `from .apis.tweets` means that we look into the `apis/tweets.py` file from the **same** package as the local `__init__.py`. It's a shortcut for `from app.apis.tweets`. Then the `import api` means that we import the variable or method `api` defined in this `tweets.py` file (here it's a variable: an instance of `Namespace`). The `as tweets` just renames the `api` that we imported to `tweets`, for readability.

### Testing

Let's set up our app so that writing test is easy and TDD is possible:

```bash
pipenv install flask-testing nose --dev
```

Let's create our `tests` folders and a first file

```bash
mkdir tests
mkdir tests/apis
touch tests/apis/__init__.py
touch tests/apis/test_tweet_view.py
```

```python
# tests/apis/test_tweet_view.py
from flask_testing import TestCase
from app import create_app

class TestTweetView(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def test_tweet(self):
        response = self.client.get("/tweets/hello")
        text = response.data.decode()
        print(text)
        self.assertIn("Goodbye", text)
```

Open the terminal and run:

```bash
pipenv run nosetests -s tests/apis/test_tweet_view.py
```

The test should be red!

👉 How can you fix the test to make the command turn green?
👉 Do we need the `print()` statement in the test method? Why (not)?

### Deployment

We want to use Gunicorn and Heroku for production:

```bash
pipenv install gunicorn
echo "web: gunicorn wsgi --access-logfile=-" > Procfile
```

Finally let's set up git:

```bash
git init
git add .
git commit -m "New flask project boilerplate"
```

By that time, you should already have created 5 applications (which is the free limit).

So we need to `do to some cleaning`.
First we want to get application name in order to remove it :

```bash
heroku apps  # Display created apps
# === <your_mail> Apps
# <app_name_1> (eu)
# <app_name_2> (eu)
# <app_name_3> (eu)
# <app_name_4> (eu)
# <app_name_5> (eu)
```

Then we can remove it :
```bash
heroku apps:destroy <app_name_1>
# !    WARNING: This will delete <app_name_1> including all add-ons.
# !    To proceed, type <app_name_1> or re-run this command with
# !    --confirm <app_name_1>

<app_name_1>  # Type <app_name_1> and press <Enter>
# Destroying <app_name_1> (including all add-ons)... done
```

**Proceed to this operation each time needed.**

We can now create an app to be deployed on Heroku:

```bash
heroku create --region=eu
git push heroku master

heroku open # Check the app is actually running.
```

## First API endpoint - `/tweets/:id`

In the following section, we will implement the HTTP API serving a JSON of a single tweet.

### Model

Before rushing to the Flask namespace we need to create to serve an HTTP response,
we need a model to hold some data. We don't have a database (yet) so we will
create everything manually today.

Let's think about our `Tweet` and use TDD to implement this class. Have a look at
what [a Tweet is](https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-show-id#example-response) and you'll see that is quite complex.
Let's simplify by saying a tweet will hold some `text` and `created_at` date.

### TDD

Let's use TDD to implement this `Tweet` class with its two instance variables. We will write
the test first and then walk our way until the test turns green.

```bash
touch tests/test_models.py
```

```python
# tests/test_models.py
from unittest import TestCase
from app.models import Tweet  # We will code our `Tweet` class in `app/models.py`

class TestTweet(TestCase):
    def test_instance_variables(self):
        # Create an instance of the `Tweet` class with one argument
        tweet = Tweet("my first tweet")
        # Check that `text` holds the content of the tweet
        self.assertEqual(tweet.text, "my first tweet")
        # Check that when creating a new `Tweet` instance, its `created_at` date gets set
        self.assertIsNotNone(tweet.created_at)
        # Check that the tweet's id is not yet assigned when creating a Tweet in memory
        self.assertIsNone(tweet.id)
```

👉 Take some time to read the [26.4. `unittest`](https://docs.python.org/3/library/unittest.html) chapter.

OK, the test is written, let's run it! (it should not be green):

```bash
pipenv run nosetests tests/test_models.py
```

💡 _In the command above ☝️, we give the exact filename to run only this test file_

You should get something which looks like this:

```bash
======================================================================
1) ERROR: Failure: ModuleNotFoundError (No module named 'app.models')
----------------------------------------------------------------------
    # [...]
    tests/test_models.py line 2 in <module>
      from app.models import Tweet
   ModuleNotFoundError: No module named 'app.models'
```

:question: What's next? **Read the error message and try to fix it**

<details><summary markdown='span'>View solution
</summary>

You must create the `models.py` file so that this module is defined!

```bash
touch app/models.py
```
</details>

<br />

Run the tests again **until the error message changes**. You should get this one:

```bash
======================================================================
1) ERROR: Failure: ImportError (cannot import name 'Tweet')
----------------------------------------------------------------------
    # [...]
    tests/test_models.py line 2 in <module>
      from app.models import Tweet
   ImportError: cannot import name 'Tweet'
```

:question: What is the **minimum** code change you can do to fix this error?

<details><summary markdown='span'>View solution
</summary>

The error complains about the fact that `Tweet` is not defined. The minimum code
change we can do is to create an **empty** class:

```python
# app/models.py
class Tweet:
    pass
```
</details>

<br />

The next error should be:

```bash
======================================================================
1) ERROR: test_instance_variables (test_models.TestTweet)
----------------------------------------------------------------------
   Traceback (most recent call last):
    tests/test_models.py line 6 in test_instance_variables
      tweet = Tweet("my first tweet")
   TypeError: object() takes no parameters
```

:question: What is the **minimum** code change you can do to fix this error?

<details><summary markdown='span'>View solution
</summary>

Our `Tweet` class is empty and needs an [instance variable](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables) `text`:

```python
# app/models.py
# pylint: disable=missing-docstring

class Tweet:
    def __init__(self, text):
        self.text = text
```

</details>

<br />


The next two errors should complain about:

```bash
'Tweet' object has no attribute [...]
```

:question: How can we fix this last two errors and make the test pass?

<details><summary markdown='span'>View solution
</summary>

Our `Tweet` class is missing the `created_at` instance variable, automatically
set to [the current time](https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python).
It's also missing the `id` instance variable, set to `None` on instance creation.

```python
# app/models.py
# pylint: disable=missing-docstring

from datetime import datetime

class Tweet:
    def __init__(self, text):
        self.id = None
        self.text = text
        self.created_at = datetime.now()
```

</details>

<br />

✨ Congrats! You just implemented the `Tweet` class using TDD.

### Repository

We need a model to hold all instances of `Tweet` and assigned auto-incremented ids.
This class will be replaced in the next chapter by a proper [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping)
interacting with a relational database. Until then, we need to **fake** it.


**Specification**: The repository class will hold a list of tweets, empty at first,
but will `add` new tweets. When adding a new tweet, it will automatically assign
to it an auto-incremented id (starting at `1`). Last but not least, it should allow
to `get` a tweet based on its id.
The list of tweets will be hold in memory.

If we wanted to test the behaviour of our new class, here is what we could do (try to understand what it does and what cases we are testing):

💡 This is only informative, you don't need to copy-paste the test code

```python
# tests/test_repositories.py
from unittest import TestCase
from app.models import Tweet
from app.repositories import TweetRepository

class TestTweetRepository(TestCase):
    def test_instance_variables(self):
        repository = TweetRepository()
        self.assertEqual(len(repository.tweets), 0)

    def test_add_tweet(self):
        repository = TweetRepository()
        tweet = Tweet("a new tweet")
        repository.add(tweet)
        self.assertEqual(len(repository.tweets), 1)

    def test_auto_increment_of_ids(self):
        repository = TweetRepository()
        first_tweet = Tweet("a first tweet")
        repository.add(first_tweet)
        self.assertEqual(first_tweet.id, 1)
        second_tweet = Tweet("a second tweet")
        repository.add(second_tweet)
        self.assertEqual(second_tweet.id, 2)

    def test_get_tweet(self):
        repository = TweetRepository()
        tweet = Tweet("a new tweet")
        repository.add(tweet)
        self.assertEqual(tweet, repository.get(1))
        self.assertIsNone(repository.get(2))
```


Now let's create our `TweetRepository` class. Copy-paste this code in a new file `app/repositories.py`:

```python
# app/repositories.py
# pylint: disable=missing-docstring

class TweetRepository:
    def __init__(self):
        self.clear()

    def add(self, tweet):
        self.tweets.append(tweet)
        tweet.id = self.next_id
        self.next_id += 1

    def get(self, id):
      for tweet in self.tweets:
          if tweet.id == id:
              return tweet
      return None

    def clear(self):
      self.tweets = []
      self.next_id = 1
```

💡 See how the test file is way longer than the actual implementation?

💡 Our `TweetRepository` class is a _mock_, i.e. it mimics the behavior of another feature, relieving us from the need of another dependency. Here we mock a database layer by using a simple `tweets` list.

<br />

### Controller + Route

It's now time to add a new route to our app to serve our API endpoint.
Remember, we want to have this:

```bash
GET /tweets/1

=> a JSON of the given tweet
```

Let's write the test for our new route:

```python
# tests/apis/test_tweet_view.py

from flask_testing import TestCase
from app import create_app
from app.models import Tweet
from app.db import tweet_repository

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def setUp(self):
        tweet_repository.clear()

    def test_tweet_show(self):
        first_tweet = Tweet("First tweet")
        tweet_repository.add(first_tweet)
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])
```

💡 If you run the test, it will complain that `tweet_repository` does not exist.

```bash
pipenv run nosetests tests/apis/test_tweet_views.py
```

`tweet_repository` is our fake database. This is just an instance of `TweetRepository`. Create it:

```bash
touch app/db.py
```

```python
# app/db.py

from .repositories import TweetRepository

tweet_repository = TweetRepository()
```

Now, let's make the test pass! You can remove the `/hello` route by replacing the content of this file entirely:

```python
# app/apis/tweets.py
# pylint: disable=missing-docstring

from flask_restx import Namespace, Resource, fields
from app.db import tweet_repository

api = Namespace('tweets')

@api.route('/<int:id>')
@api.response(404, 'Tweet not found')
class TweetResource(Resource):
    def get(self, id):
        tweet = tweet_repository.get(id)
        if tweet is None:
            api.abort(404)
        else:
            return tweet
```

:question: Implement the rest of `app/apis/tweets.py` to make the test pass.

:bulb: **Hint**: you need to use the `api.model()` and `@api.marshal_with` described [in the doc](https://flask-restx.readthedocs.io/en/stable/quickstart.html#data-formatting) to overcome the following error:

```bash
TypeError: Object of type Tweet is not JSON serializable
```

Do you understand this error? If not, ask your buddy then ask a TA!

```bash
pipenv run nosetests tests/apis/test_tweet_views.py
```

:bulb: **Hint**: have a look at the [full example](https://flask-restx.readthedocs.io/en/stable/example.html) from the documentation!

<details><summary markdown='span'>View solution (Really try first 🙏)
</summary>

We will use the Flask-RESTX built-in serialization:

```python
# app/apis/tweets.py
# pylint: disable=missing-docstring

from flask_restx import Namespace, Resource, fields
from app.db import tweet_repository

api = Namespace('tweets')

tweet = api.model('Tweet', {
    'id': fields.Integer,
    'text': fields.String,
    'created_at': fields.DateTime
})

@api.route('/<int:id>')
@api.response(404, 'Tweet not found')
@api.param('id', 'The tweet unique identifier')
class TweetResource(Resource):
    @api.marshal_with(tweet)
    def get(self, id):
        tweet = tweet_repository.get(id)
        if tweet is None:
            api.abort(404)
        else:
            return tweet
```

</details>

<br />

### Running the server

Let's leave the tests for now (running `nosetests` should yield 6 passing tests) and launch the server:

```bash
FLASK_ENV=development pipenv run flask run
```

Now open your browser and go to [`localhost:5000/tweets/1`](http://localhost:5000/tweets/1).

:question: Read the error message and find which line of your code triggers it. Why?

<details><summary markdown='span'>View solution
</summary>

On line 8 of `app/api/tweets.py`, we retrieve a tweet with id == 1 **but** there is no tweet in the repository
yet! Then `tweet` is `None`, thus the error:

```bash
AttributeError: 'NoneType' object has no attribute 'id'
```

To solve this problem, we need to simulate a database with pre-existing tweets at server boot. We can do so with:

```python
# app/__init__.py
# pylint: disable=missing-docstring

from flask import Flask # This line already exists
from flask_restx import Api # This line already exists

from .db import tweet_repository
from .models import Tweet
tweet_repository.add(Tweet("a first tweet"))
tweet_repository.add(Tweet("a second tweet"))

def create_app():  # This line already exists
    # [...]
```

Try again [`localhost:5000/tweets/1`](http://localhost:5000/tweets/1). Do you get a nice JSON of your tweet? Hoorah!

</details>

:bulb: Don't forget to commit and deploy!

## Bonus

### Swagger documentation

The Flask-RESTx package comes with [swagger doc](https://flask-restx.readthedocs.io/en/stable/swagger.html) embeded. Run your server and access the root URL:

:point_right: [http://localhost:5000](http://localhost:5000)

Can you see the documentation? You can try your endpoints right within it!

### Going further

If you reached this part, you get the gist of building a RESTful API with Flask. It's time to practise!

- Implement the remaining endpoints to have a full `CRUD` RESTful API! Today we don't care about User Authorization for create, update & delete. [The doc is your friend](https://flask-restx.readthedocs.io/en/stable/)
- Use the GitHub flow for each new endpoint!
- Deploy often! Everytime you merge a branch with a new endpoint, `git push heroku master`!

Good luck 😉

## I'm done!

Before you jump to the next exercise, let's mark your progress with the following:

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 03-Back-end/02-Twitter-API
touch DONE.md
git add DONE.md && git commit -m "03-Back-end/02-Twitter-API done"
git push origin master
```
