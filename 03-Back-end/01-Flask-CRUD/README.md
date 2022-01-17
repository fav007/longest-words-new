# Flask CRUD

![](http://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png)

[Flask](http://flask.palletsprojects.com/en/1.1.x/) is a **microframework** for Python to quickly build a web application.

In this exercise, we will quickly go over every important features of Flask.

## Getting started

You will work in a dedicated repository to apply the best practices covered in the previous lecture.

```bash
cd ~/code/<user.github_nickname>
mkdir flask-101 && cd $_
pipenv --python 3.8
pipenv install flask gunicorn
touch wsgi.py
code . # Open VS Code in the current folder.
```

Curious what packages Flask is relying on? Run this in your terminal:

```bash
pipenv graph
```

Neat, isn't it?

### Flask Boilerplate

In your `wsgi.py` file, copy paste the following boilerplate:

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"
```

What does this code do?

1. First we imported the Flask class. An instance of this class will be our Web application.
1. Next we create an instance of this class. The first argument is the name of the application’s module or package.
1. We then use the `route()` decorator to tell Flask what URL should trigger our function.
1. The function is given a name which is also used to generate URLs for that particular function, and returns the message we want to display in the user’s browser.

### Development run

Go back to your terminal and run:

```bash
FLASK_ENV=development pipenv run flask run
```

The server should start. Open your browser and visit [`localhost:5000`](http://localhost:5000). You should see "Hello world!" as a text answer!

Try to edit the code and reload the page in the browser. 💡 What is happenning?

### Production run

In production, we don't want to use the default Flask server, optimized for development, but something like [Gunicorn](http://gunicorn.org/), already installed in the `Pipfile` thanks to a previous command.

The production server will run this code:

```bash
# Ctrl-C to kill the previous server
pipenv run gunicorn wsgi:app --access-logfile=-
```

:bulb: If you launch this on Windows, it will fail as gunicorn does not support (yet?) Windows:

- [github.com/benoitc/gunicorn/issues/524](https://github.com/benoitc/gunicorn/issues/524)
- [stackoverflow.com/questions/11087682/does-gunicorn-run-on-windows](https://stackoverflow.com/questions/11087682/does-gunicorn-run-on-windows) (they talk about [`waitress`](https://docs.pylonsproject.org/projects/waitress))

## Heroku

Let's try to deploy this application to Heroku:

```bash
touch Procfile
```

```bash
# Procfile
web: gunicorn --workers=1 wsgi:app --access-logfile=-
```

```bash
git init
git add .
git commit -m "First deployment of Flask boilerplate"

heroku create --region=eu
git push heroku master

heroku ps                  # Do you have a free dyno up running `gunicorn`?

heroku open                # Do you get an "Hello world" in the browser?
heroku logs -n 1000 --tail # Check the access logs are coming up. Reload the browser.
```

## JSON

Right now, our app returns some plain text. Today's goal is to build a REST API.

👉 Add a `/api/v1/products` route which will return **a JSON array**:

```python
PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv' },
}
```

:bulb: **Tip**: Have a look at [`jsonify`](http://flask.pocoo.org/docs/api/#flask.json.jsonify)

To test your code, open the browser and go to [`localhost:5000/api/v1/products`](http://localhost:5000/api/v1/products).

:bulb: **Tip**: Install the [JSONView Chrome extension](https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc) to have a better visualisation of JSON HTTP responses.


Commit and push your code to Heroku:
```bash
git add .
git commit -m "Adding /api/v1/products endpoint"

git push heroku master

heroku ps

heroku open
heroku logs -n 1000 --tail
```

Check the new `/api/v1/products` endpoint works in **production**.

## Testing

Testing our APIs will be mandatory. Whether we use strict TDD or not during the development process, at some point the application should have tests exercising every endpoint.

We are using an external module called [`Flask Testing`](https://pythonhosted.org/Flask-Testing/).

![](https://pythonhosted.org/Flask-Testing/_static/flask-testing.png)

```bash
pipenv install flask-testing nose --dev
```

Now let's create the `tests` directory and a first test file. This test file is about **views**, which is the closest component to the HTTP response in a MVC framework (more on that later):

```bash
mkdir tests
touch tests/test_views.py
```

Open the file in VS Code, read and copy-paste this.

```python
# tests/test_views.py
from flask_testing import TestCase
from wsgi import app

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_read_many_products(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.
```

Then open the terminal and run:

```bash
nosetests -s
```

👉 Your test should be failing. How do you fix the code in `wsgi.py` to make the test green?

(`-s` flag is useful to actually view your `print()` statements, or use `pdb`).

<details><summary markdown='span'>View solution
</summary>

Just add a third element to the `PRODUCTS` dict!
```python
PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv'},
    3: { 'id': 3, 'name': 'Le Wagon'},
}
```

</details>

## CRUD

Congratulations :tada: ! You wrote the first route of the RESTful API. Now it's time to implement the four other endpoints to properly implement CRUD on the `product` resource.

Practice the **GitHub Flow** with four feature branches (one per `CRUD` acronym letter), and push to `heroku` after each Pull Request merge!

### Read

First add a test for the `GET /api/v1/products/:id` route. Then implement it. This route retrieves a single `product` and serve a JSON representation of it (Status code: `200`). `:id` represents the dynamic part of the url asking our api. Here are some request urls examples matched by our url route: `/api/v1/products/3`, `/api/v1/products/1`, etc.
If the `:id` does not match any known `product` id in the fake `PRODUCTS` database, then return a [`404`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404).
Add a separate test case for this.

:bulb: **Tip**: Have a look at the [Variable Rules](http://flask.pocoo.org/docs/1.0/quickstart/#variable-rules) in the Flask documentation.

### Delete

Add a test for the `DELETE /api/v1/products/:id` route. This route will **remove** a single `product` from the fake `PRODUCTS` database. Return an empty response with status code [`204`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204).

:bulb: **Tip**: Have a look at how Flask defines an [HTTP Method](http://flask.pocoo.org/docs/quickstart/#http-methods) for a given route.

:bulb: **Tip**: If you want to TDD this method you will have a hard time as the Database is simulated in a constant list. Go ahead and only write the code in wsgi.py, we will cover later how to isolate the test environment and use a proper Database setup for that. This remark will be the same for the next two sections "Create" & "Update".

### Create

Start by adding a test for the `POST /api/v1/products` route. This route will **create** a new `product` in the fake `PRODUCTS` database and return the JSON representation of the newly created resource (Status code: [`201`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201))

:bulb: **Tip** You may need to use the [`Request.get_json`](http://flask.pocoo.org/docs/1.0/api/#flask.Request.get_json) method.

```python
from flask import request

request.get_json()
```

:bulb: **Tip** You might need to introduce a way to generate auto-incremented ids:

```python
import itertools

# [...]

START_INDEX = len(PRODUCTS) + 1
IDENTIFIER_GENERATOR = itertools.count(START_INDEX)

# Here is how to use it :
print(next(IDENTIFIER_GENERATOR))
```

:bulb: **Tip** To send a POST request **in your tests**, you can use the following method:

```python
response = self.client.post("/api/v1/products", json={'name': 'HistoVec'})
```

:bulb: **Tip** Here is a payload you can use in Postman to test this route:

```
{
    "name": "HistoVec"
}
```

Don't forget to select "Raw" and "JSON" to automatically add a `Content-Type: application/json` header. Without this header, your `request.get_json()` call will ignore the payload, as mentioned in the [`Request.get_json documentation`](http://flask.pocoo.org/docs/1.0/api/#flask.Request.get_json)

![](https://res.cloudinary.com/wagon/image/upload/v1560715014/postman-workelo_ztvqyf.png)

### Update

Finally, add a test for the `PATCH /api/v1/products/:id` route which will **update** an existing `product` (based on its id). Return a `204` when completed, or `422` if there is a validation error (needs a separate test case, validation error could be that supplied product name is _empty_)

### Solutions

:warning: **Please read the solutions only once you have tried implementing all the tests and HTTP methods!**

<details><summary markdown="span">View tests
</summary>

```python
# tests/test_views.py
from flask_testing import TestCase
from wsgi import app

class TestViews(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_read_many_products(self):
        response = self.client.get("/api/v1/products")
        products = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 2) # 2 is not a mistake here.

    def test_read_one_products(self):
        response = self.client.get("/api/v1/products/1")
        product = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(product, dict)
        self.assertEqual(product['name'], 'Skello')

    def test_read_one_product_not_found(self):
        response = self.client.get("/api/v1/products/20")
        product = response.json
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(product)

    def test_delete_product(self):
        delete_response = self.client.delete("/api/v1/products/3")
        deleted_product = delete_response.json
        self.assertEqual(delete_response.status_code, 204)
        self.assertIsNone(deleted_product)

        read_one_response = self.client.get("/api/v1/products/3")
        read_one_product = read_one_response.json
        self.assertEqual(read_one_response.status_code, 404)
        self.assertIsNone(read_one_product)

    def test_delete_product_not_found(self):
        response = self.client.delete("/api/v1/products/20")
        product = response.json
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(product)

    def test_create_product(self):
        response = self.client.post("/api/v1/products", json={'name': 'Netflix'})
        product = response.json
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(product, dict)
        self.assertEqual(product['name'], 'Netflix')

    def test_create_product_validation_error(self):
        response_1 = self.client.post("/api/v1/products", json={'name': 2})
        product_1 = response_1.json
        self.assertEqual(response_1.status_code, 422)
        self.assertIsNone(product_1)

        response_2 = self.client.post("/api/v1/products", json={'name': ''})
        product_2 = response_2.json
        self.assertEqual(response_2.status_code, 422)
        self.assertIsNone(product_2)

    def test_create_product_bad_request(self):
        response_1 = self.client.post("/api/v1/products", json={'other': 2})
        product_1 = response_1.json
        self.assertEqual(response_1.status_code, 400)
        self.assertIsNone(product_1)

        response_2 = self.client.post("/api/v1/products", json={'other': 'what'})
        product_2 = response_2.json
        self.assertEqual(response_2.status_code, 400)
        self.assertIsNone(product_2)

        response_3 = self.client.post("/api/v1/products")
        product_3 = response_3.json
        self.assertEqual(response_3.status_code, 400)
        self.assertIsNone(product_3)

    def test_update_product(self):
        update_response = self.client.patch("/api/v1/products/1", json={'name': 'Netlify'})
        update_product = update_response.json
        self.assertEqual(update_response.status_code, 204)
        self.assertIsNone(update_product)

        read_response = self.client.get("/api/v1/products/1")
        product = read_response.json
        self.assertEqual(read_response.status_code, 200)
        self.assertIsInstance(product, dict)
        self.assertEqual(product['name'], 'Netlify')

    def test_update_product_not_found(self):
        response = self.client.patch("/api/v1/products/20", json={'name': 'Doctolib'})
        product = response.json
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(product)

    def test_update_product_validation_error(self):
        response_1 = self.client.patch("/api/v1/products/1", json={'name': 2})
        product_1 = response_1.json
        self.assertEqual(response_1.status_code, 422)
        self.assertIsNone(product_1)

        response_2 = self.client.patch("/api/v1/products/1", json={'name': ''})
        product_2 = response_2.json
        self.assertEqual(response_2.status_code, 422)
        self.assertIsNone(product_2)

    def test_update_product_bad_request(self):
        response_1 = self.client.patch("/api/v1/products/1", json={'other': 'what'})
        product_1 = response_1.json
        self.assertEqual(response_1.status_code, 400)
        self.assertIsNone(product_1)

        response_2 = self.client.patch("/api/v1/products/1")
        product_2 = response_2.json
        self.assertEqual(response_2.status_code, 400)
        self.assertIsNone(product_2)
```

</details>
<details><summary markdown="span">View wsgi.py
</summary>

```python
# wsgi.py
# pylint: disable=missing-docstring
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

import itertools

from flask import Flask, jsonify, abort, request
app = Flask(__name__)

# Prefix api path using a version number is really important to manage future breaking evolutions
# This way, we can continue to offer the old service using /v1 url and offer the new one using /v2
# We will remove /v1 api (and related code) when all our users will use /v2 url.
BASE_URL = '/api/v1'

# Remember this is only a really simple database simulation.
# This data is only persisted in RAM : if you restart your server, modifications are lost.
# Don't worry about this, our goal for today is to understand REST api, not to really persist data.
PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv' },
    3: { 'id': 3, 'name': 'Le Wagon'},
}

# This is a simple naive way to generate consecutive id (like a database will do)
START_INDEX = len(PRODUCTS) + 1
IDENTIFIER_GENERATOR = itertools.count(START_INDEX)


@app.route(f'{BASE_URL}/products', methods=['GET'])
def read_many_products():
    products = list(PRODUCTS.values())

    # Returns a tuple corresponding to flask.Response constructor arguments
    # Cf: https://flask.palletsprojects.com/en/1.1.x/api/?highlight=response#flask.Response
    # By default, 2nd argument is 200 (but we want to be explicit while learning concepts)
    return jsonify(products), 200  # OK


@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['GET'])
def read_one_product(product_id):
    product = PRODUCTS.get(product_id)

    if product is None:
        abort(404)

    return jsonify(product), 200  # OK


@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['DELETE'])
def delete_one_product(product_id):
    product = PRODUCTS.pop(product_id, None)

    if product is None:
        abort(404)  # No product of product_id found is a Not Found Error

    # If 204, 1st argument (body) is ignored
    # We can put anything we want in 1st argument (but we want to be explicit to make our code more maintenable)
    # '' or None are common used values to explicit this case
    #
    # Delete action (DELETE method) no need to return the entity since we removed this entity
    return '', 204  # No Content


# No product_id in create (POST method) url since it is the database which implements the id counter
# If api consumers could choose an id, it would lead to many erros :
#  - race condition for a given id choosed by many users
#  - how to know which is is not used for now
#  - database can optimize ids management because they know the way they are created
@app.route(f'{BASE_URL}/products', methods=['POST'])
def create_one_product():
    data = request.get_json()

    if data is None:
        abort(400)  # Missing needed field(s) is a Bad Request Error

    name = data.get('name')

    if name is None:
        abort(400)  # Missing needed field is a Bad Request Error

    if name == '' or not isinstance(name, str):
        abort(422)  # Bad format for needed field is a Unprocessable Entity Error

    next_id = next(IDENTIFIER_GENERATOR)
    PRODUCTS[next_id] = {'id' : next_id , 'name' : name }

    # We need to return the entire entity to comunicate the new id to the api consumer
    # This way, he can act on this resource using his id.
    #
    # We could simply return the id, but it's not in the REST spirit
    # => Don't forget : /<entity>/<entity_id> represents an entire entity
    return jsonify(PRODUCTS[next_id]), 201  # Created


@app.route(f'{BASE_URL}/products/<int:product_id>', methods=['PATCH'])
def update_one_product(product_id):
    data = request.get_json()
    if data is None:
        abort(400)

    name = data.get('name')

    if name is None:
        abort(400)

    if name == '' or not isinstance(name, str):
        abort(422)

    product = PRODUCTS.get(product_id)

    if product is None:
        abort(404)

    PRODUCTS[product_id]['name'] = name

    # Update action (UPDATE method) no need to return the entity since we know what we modified
    return '', 204
```

</details>

## (Optional) PowerShell REST API Client

Let's use Powershell to **consume** this API. Keep a tab with the API running so that we can run queries against it:

```bash
cd ~/code/<user.github_nickname>/flask-101
FLASK_ENV=development pipenv run flask run
```

Then open a new terminal window. Let's create a PowerShell script file:

```bash
cd ~/code/<user.github_nickname>/flask-101
touch consumer.ps1

# To run the script:
powershell -ExecutionPolicy bypass ./consumer.ps1
```

Open your `consumer.ps1` file in VS Code. We want you to implement a function `Get-Products` so that the following code queries the API and prints all the products.

:bulb: Hint: you might need the [`Invoke-RestMethod`](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-6) function!

```powershell
Write-Output "# Printing all products"
Get-Products | Write-Output
```

<details><summary markdown="span">View solution
</summary>

```powershell
function Get-Products {
  return Invoke-RestMethod "$BASE_URL/products"
}
```

</details>

Go ahead and implement four other method consuming the REST API so that the following scenario goes through:

```powershell
Write-Output "# Printing all products"
Get-Products | Write-Output

Write-Output "-----------------------"

Write-Output "# Printing one product"
Get-Product -Id 1 | Write-Output

Write-Output "-----------------------"

Write-Output "# Update product 1's name"
Update-Product -Id 1 -Name "Skello v$(Get-Random)"
Get-Product -Id 1 | Write-Output

Write-Output "-----------------------"

Write-Output "# Adding a product"
New-Product -Name "Basecamp"

Write-Output "-----------------------"

Write-Output "# Printing all products once again"
$products = Get-Products
$products | Write-Output

Write-Output "-----------------------"

$lastId = $products[-1].id
Write-Output "# Removing product with id $lastId"
Remove-Product $lastId
Write-Output "Done"

Write-Output "-----------------------"

Write-Output "# Printing all products once last time"
$products = Get-Products
$products | Write-Output
```


<details><summary markdown='span'>View solution for `Get-Product`
</summary>

```powershell
function Get-Product {
  param($Id)
  return Invoke-RestMethod "$BASE_URL/products/$id"
}
```

</details>

<details><summary markdown='span'>View solution for `New-Product`
</summary>

```powershell
function New-Product {
  param($Name)
  $body = @{name=$Name} | ConvertTo-Json
  $uri = "$BASE_URL/products"
  return Invoke-RestMethod -Method 'POST' -Uri $uri -Body $body -ContentType "application/json"
}
```

</details>

<details><summary markdown='span'>View solution for `Update-Product`
</summary>

```powershell
function Update-Product {
  param($Id, $Name)
  $body = @{name=$Name} | ConvertTo-Json
  $uri = "$BASE_URL/products/$id"
  return Invoke-RestMethod -Method 'PATCH' -Uri $uri -Body $body -ContentType "application/json"
}
```

</details>

<details><summary markdown='span'>View solution for `Remove-Product`
</summary>

```powershell
function Remove-Product {
  param($Id)
  return Invoke-RestMethod -Method 'DELETE' "$BASE_URL/products/$id"
}
```

</details>

## I'm done!

Before you jump to the next exercise, let's mark your progress with the following:

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 03-Back-end/01-Flask-CRUD
touch DONE.md
git add DONE.md && git commit -m "03-Back-end/01-Flask-CRUD done"
git push origin master
```
