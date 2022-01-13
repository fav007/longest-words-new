# Twitter API - Containerization

The goal of this exercise is to continue the work on Wednesday's and Thursday's exercises: **Twitter API**.

We have already set up an web application and a database, and today we will focus on containerizing this stack locally, to be able to develop on it, and run our tests inside containers.

---

## 0. Setup

We're going to continue from yesterday's correction :
:point_right: [github.com/ssaunier/twitter-api](https://github.com/ssaunier/twitter-api)

Start from the following code (using the `docker` branch):

```bash
cd ~/code/<user.github_nickname>
git clone git@github.com:ssaunier/twitter-api.git twitter-api-docker
cd twitter-api-docker
git checkout docker  # get these branch before changing the remote
git remote rm origin
```

Go to [github.com/new](https://github.com/new) and create a _public_ repository under your _personal_ account, name it `twitter-api-docker`.

```bash
git remote add origin git@github.com:<user.github_nickname>/twitter-api-docker.git
git push -u origin docker
```

---

## 1. Sanity check - non-containerized stack (⏰ reminder of day 3 and 4)

The stack is not containerized yet. But let's make a sanity check to verify that everything is working. This also acts as a reminder of the two previous days on this challenge !

### 1.a. Install dependencies

:point_right: Use `pipenv` to install the dependencies locally, for the development environment!

<details><summary markdown='span'>View solution</summary>

```bash
pipenv install --dev
```

</details>

### 1.b. Run the test suite locally

:point_right: Make sure the tests are passing locally

<details><summary markdown='span'>View solution</summary>

```bash
nosetests
```

</details>

Does it work ? It should not ! Why ?
:point_right: Try to fix ! You have been through this yesterday already !

<details><summary markdown='span'>Hint</summary>

Yesterday, we used a `.env` file to configure the used Database with an environment variable.

</details>

<details><summary markdown='span'>View solution</summary>

Create a `.env` file:

```bash
touch .env
```

Reference the `DATABASE_URL` variable there:

```bash
# .env
DATABASE_URL="postgresql://postgres@localhost/twitter_api_flask"
```

You should still have the `twitter_api_flask` and `twitter_api_flask_test` databases on your laptop.
Now running your test suite `nosetests` should work !

Please note that if you deleted the **dev** and **test** databases yesterday, you would have to re-set them up !

Create the **dev** and **test** Postgres databases (remember that we have 2 separate database for our _development_ and _test_ environments ! We <b>really</b> want to distinguish them not to mix any data - which could lead to unwanted behavior !!

```bash
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask"
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask_test"
```

And now running your test suite `nosetests` should work !

</details>


### 1.c. Run the app

:point_right: Make sure the web server can be run

<details><summary markdown='span'>View solution</summary>

```bash
FLASK_ENV=development pipenv run flask run
```

</details>

:point_right: Visit the Swagger documentation page in your web browser.
:point_right: Visit the `/tweets` page as well. Is everything fine ?

<details><summary markdown='span'>View solution</summary>

Go to <a href="http://localhost:5000/">localhost:5000</a> and <a href="http://localhost:5000/tweets">localhost:5000/tweets</a>.


Note that if you deleted your dev database yesterday, you would have to run the migrations again:

```bash
pipenv run python manage.py db upgrade
```

</details>


Everything working ? 🎉 Perfect ! Now, let's adopt a new strategy, and do all of it in Docker containers:

- first for the _development_ environment (where we run the app),
- then for the _test_ environment (where we run the test suite).

---

## 2. Containerization - development environment

When containerizing our app, we generally do not use `pipenv` anymore. We prefer having the requirements listed in a static file (typically named `requirements.txt`) and use `pip` directly to install them. Why ?

- Because we do not need a virtual environment - docker is already, by design, a layer of virtualization
- And because it makes the docker image a bit lighter ! And in software development, lighter is better 🙂


We say "generally", because with Docker you can install and build pretty much anything, so we _could_ still use it. Here, we will use the common `requirements.txt` method.

:point_right: Upgrade your `pipenv` version :

```bash
pip install --upgrade pipenv
```

and double check their versions:

```bash
pipenv --version
```

It must look like `2020.x`. If not, please ask a TA.
Now that `pipenv` is up-to-date, we can safely lock the requirements in static text files.

:point_right: Run the following commands:

```bash
pipenv lock --requirements > requirements.txt
```

and

```bash
pipenv lock --requirements --dev > requirements-dev.txt
```

After running them, these files should have been created in your folder and filled in with python dependencies.

---

### 2.1 Dockerfile - Flask app

Let's first Dockerize our Flask app: build an image, run a container and check all is fine.

:point_right: Create an empty Dockerfile

```bash
touch Dockerfile
```

:point_right: Copy paste the following code in it, and save it

```dockerfile
FROM python:3.8-alpine as base

RUN apk update && apk add postgresql-dev gcc musl-dev
RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /code
COPY . /code

RUN pip install -r requirements-dev.txt

ENV DATABASE_URL postgres://localhost/twitter_api_flask
ENV FLASK_APP wsgi.py
ENV FLASK_ENV development

EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
```

Do you understand the instructions ? If we decompose them one by one, we see that:

* we start from the Python 3.8 image, and more specifically its `alpine` version. Alpine Linux is a Linux distribution known for its light weight, but still complete toolbox
* we install a few packages required for our image to build (among which `pip`)
* we create a workspace directory (in the containers that will be run) called `/code`
* we copy our local code folder into this container workspace directory
* we install the requirements (in development mode for this challenge)
* we setup some environment variables for the container to run properly
* we setup a command to be run when the container is run

🤔 Why do we have `--host 0.0.0.0` in the `CMD` instruction ?

<details><summary markdown='span'>View solution</summary>

We do not want to only bind to `localhost` interface as we did before: we bind to `0.0.0.0` so the container can be accessible from the outside (especially accessible from your docker host, which is your laptop !)

</details>


:point_right: Now, build this image and tag it as `twitter-api`

<details><summary markdown='span'>Hint</summary>

There is an example for building and tagging an image in the same command, in the previous exercise (`Docker-101`).

</details>

<details><summary markdown='span'>View solution</summary>

```bash
docker build -t twitter-api .
```

</details>

Done ? Perfect ! Now let's run a container from this image, and check that our application is working.
A few specs for this run:

* name it `twitter-api-docker`
* you need to map a host port to the container port of your application, in order to access it from your host: add the `-p 5000:5000` option to your command. This way, the app will run in the container on port 5000, and you will be able to access it on your host (your machine) on port 5000 as well.
* add the `--rm` option to your `docker run` command to automatically remove the container once it exits.

<details><summary markdown='span'>Hint</summary>

You need to use `docker run` with various options (the container name, a port mapping, the `--rm` flag, the name of the image). Check out `docker run --help` if needed !

</details>

<details><summary markdown='span'>View solution</summary>

```bash
docker run --name twitter-api -it -p 5000:5000 --rm twitter-api
```

</details>

You now have a container running.

:point_right: Let's check [localhost:5000](http://localhost:5000/) to see if it worked: is it fine ?

<details><summary markdown='span'>View solution</summary>

It should ! If not, double check the command you have run and if the problem still persists, please ask a TA !

</details>


:point_right: What happens with the `/tweets` endpoint now ? Why ?

<details><summary markdown='span'>Hint</summary>

Visit <a href="http://localhost:5000/tweets">localhost:5000/tweets</a> in your web browser.

</details>
<details><summary markdown='span'>View solution</summary>

When we hit this endpoint, it's crashing. Indeed, we are trying to make a call to our database, but it's not set up ! So our Flask app would not find its database ready for new connections, and it raises a `sqlalchemy.exc.OperationalError` exception.

So let's setup our database - and dockerize it at the same time to make the development and testing flow easier !

</details>

:point_right: Hit `CTRL-C` to stop your container (and also remove it - as you passed in the `--rm` flag in your `docker run` command !).

---

### 2.2 Containerize our database service

We need to add a DB and we will use `docker-compose` for this.
We have seen in lecture that `docker-compose` was used to define multiple services, and bring up the application stack with the `docker-compose up` command.

:point_right: Once again, let's start small, and create an empty `docker-compose.yml` file.

```bash
touch docker-compose.yml
```

:point_right: Copy and paste the following content in it: here we define a single service: `web`, for our Flask app. It is mostly based on the Dockerfile previously created, through the `build` keyword.

```yaml
version: '3.8'

services:
  web:
    build: .
    volumes:
      - .:/code
    ports:
      - 5000:5000
```

:point_right: Bring up the stack by running

```bash
docker-compose up
```

You will probably be asked to share some files with `docker-compose` (as it needs access to your application code to run it): click "accept".

:point_right: Browse to [localhost:5000](http://localhost:5000) and [localhost:5000/tweets](http://localhost:5000/tweets).

Yes, still the same errors as before when the app tries to reach the database ! Here, we have not changed much, as we only have one service (web) in our `docker-compose.yml` file, that relies on our previously defined `Dockerfile`.
So in a way, we have only changed - so far - the way to run our container ! But we will do more now ...

:point_right: You can now exit your container using `CTRL-C`


Remember that the idea is to add a database service to it. So let's add our Postgres database ! For this, we are going to do the following:

a. update our `Dockerfile` accordingly
b. adjust our `docker-compose.yml` to account for the database service


#### 2.2.a Update our existing Dockerfile
:point_right: Update your `Dockerfile` with the following:

```dockerfile
FROM python:3.8-alpine as base

RUN apk update && apk add postgresql-dev gcc musl-dev bash
RUN pip install --upgrade pip

WORKDIR /code
COPY . /code

RUN pip install -r requirements-dev.txt

EXPOSE 5000

ENV FLASK_APP wsgi.py
```

Note that we have simplified our `Dockerfile`:

- we removed some environment variables
- we remove the `CMD` instruction that the container should run

... but don't worry we are going to reference those in the `docker-compose.yml` file - they are not "gone" !

We also installed `bash` in our image, as we will need to run a script (maybe you noticed a `wait-for-it.sh` script in the repo: it's not an error, it's here on purpose. We will talk about it in the next paragraph).


#### 2.2.b Add a database service to our docker-compose.yml
:point_right: Update your `docker-compose.yml` file with the following:

```yaml
version: '3.8'

services:
  db:
    image: postgres:12-alpine
    container_name: db
    networks:
      - default
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_PASSWORD=password
  web:
    build: .
    container_name: web
    networks:
      - default
    depends_on:
      - db
    command: ["./wait-for-it.sh", "db:5432", "--", "flask", "run"]
    volumes:
      - .:/code
    ports:
      - 5000:5000
    environment:
      - DATABASE_URL=postgres://postgres:password@db:5432/twitter_api_flask
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_ENV=development

volumes:
  postgres_data:
```

The idea here it to migrate what is _configurable_ from the `Dockerfile` into the `docker-compose.yml`, and only keep what is static (such as packages, dependencies definition) in the `Dockerfile`.

We now have two services: `web` and `db`.

👀  Closer look on `db`:

* This service is based on the `postgres` image (accessible on the Docker Hub)
* We name the container that will be run `db` - for simplicity
* We specify environment variables - that we know is mandatory for the `postgres` image !
* Notice the `volumes` keyword ? In a few words - just to introduce the concept:
  * In order to be able to save (persist) data and also to share data between containers, Docker came up with the concept of **volumes**
  * Quite simply, volumes are directories (or files) that  live "outside" the container, on the host machine (in our case, your laptop)
  * From the container, the volume acts like a folder which you can use to store and retrieve data. It is simply a _mount point_ to a directory on the host
  * In other words: here the `/var/lib/postgresql/data/` directory from the `db` container "points towards" the `postgres_data` volume on your host. All the database data will end up in this volume
  * **But why ?** 🤔 Well if you stop and remove your container, you do not want its persistent data to be lost as well. So it is kept safe on the docker host, and you can re-attach the volume to any new container you would like to run !

👀  Closer look on `web`:

* This service is based on a custom image - instructed in our Dockerfile
* We name the container that will be run `web` - for simplicity
* It ["depends on"](https://docs.docker.com/compose/compose-file/#depends_on) the `db` service: services will be started in dependency order. We need our database (`db`) to be up and ready for new connections before running our Flask app (`web`) !
* In order to make sure our dependency container (that is, our database) is running, we need some kind of "control". It's the exact purpose of the `wait-for-it.sh` script ! You can read more [here](https://docs.docker.com/compose/startup-order/) if you are interested. The `web` container runs this script, that will **make it wait until the database is up and accepting connections**, before running the flask app (`command: ["./wait-for-it.sh", "db:5432", "--", "flask", "run"]`).


#### 2.2.c Initial operations

Let's perform a few initial steps to setup the containers and databases we will need:

:point_right: Make sure you have _"Unix line endings"_ for your `wait-for-it.sh` script: open it with **VS Code**, open the command pallette (CTRL+SHIFT+P) and type `Change All End Of Line Sequence`, then click on `CRLF`. This way, it will be correctly interpreted in your containers.

:point_right: Bring up the stack, running containers in the background, and re-building the image for `web` : ```docker-compose up -d --build``` 🛠

:point_right: Double check it actually launched your tech stack: run `docker ps` to see the containers running on your host.

<details><summary markdown='span'>View solution</summary>

You should see your `web` and `db` containers running.

</details>

:point_right: Let's create our databases for **development** and **testing** now:
* connect to the `db` container: `docker exec -it db psql -U postgres`
* create databases for development and test environments: in the `psql` prompt, type:
  * `CREATE DATABASE twitter_api_flask;`
  * `CREATE DATABASE twitter_api_flask_test;`
  * Exit the `psql` prompt: `\q` + **Enter**

:point_right: Eventually, run your migrations: ```docker-compose run web python manage.py db upgrade```

<details><summary markdown='span'>View solution</summary>

You should get an output like this:

```bash
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 3812f6776f12, Create tweets table
```

</details>

⚠️ Note that is not something that we necessarily automate for **development** and **test** environments as we want to be able to play with migrations manually. But for **CI** and **production**, these commands would be scripted to be run programmatically. You would not have to manually enter the command and run it !

Now our endpoints are fixed 🍾:

:point_right: Visit the [Swagger documentation](http://localhost:5000) and the [`/tweets` index](http://localhost:5000/tweets)

<details><summary markdown='span'>View solution</summary>

You should see: the Swagger documentation as usual for the first endpoint, and an empty list for the second endpoint (you do not have any data yet !)

</details>

Some details about what just happened:

* Calling `docker-compose up` will launch `db` and `web`
* `web` depends on `db` to be up and healthy. The `docker-compose up` commands make sure of it by running a control script: `wait-for-it.sh`
* once `db` is up and healthy, `web` can be run
* our database is secured by a user/password, that Flask knows (we pass it through the `DATABASE_URL` environment variable that you already know from yesterday)

⚠️ Note that we have **hard-coded** a dummy **database password** ("_password_") here. We would of course do better going live 💪 (such as using an environment variable, or a secret from a Vault). But remember that we are industrializing our stack progressively: of course all our iterations cannot perfect but we are aiming at something robust in the end !

---

### 2.3 Interact using data

#### 2.3.a Add data using Postman !

* Open your Postman app

* Create some data: make a `POST` request to `http://localhost:5000/tweets`, with a JSON body:

```json
{
    "text": "Hey this is a new tweet!"
}
```

* Create another tweet (use the text you want, and send the request)

#### 2.3.b Check your data using the API

Now that you have some data in your database, check the list of tweets through the [`GET /tweets` endpoint](http://localhost:5000/tweets). Note that you can do that in Postman (setting up the `GET` request yourself), or in your web browser ! It is exactly the same, both would hit your Flask API similarly !

#### 2.3.c Check your data using the database directly

Another way to see the data would be to connect to the **development** database directly.
That's convenient because you have a container for it.

:point_right: Similarly to what we did in the previous exercise, run:

```
docker exec -it db psql -U postgres twitter_api_flask
```

You will get a `psql` prompt where you can write SQL.

* 💡 **Tip** typing `\d+` and hitting **Enter** will show you the list of available tables in the database

<details><summary markdown='span'>View solution</summary>

You should get an output like this:

```bash
twitter_api_flask=# \d+
                             List of relations
 Schema |      Name       |   Type   |  Owner   |    Size    | Description
--------+-----------------+----------+----------+------------+-------------
 public | alembic_version | table    | postgres | 8192 bytes |
 public | tweets          | table    | postgres | 8192 bytes |
 public | tweets_id_seq   | sequence | postgres | 8192 bytes |
(3 rows)
```

</details>

* Running `SELECT * FROM tweets;` would display all your data

<details><summary markdown='span'>View solution</summary>

You should get an output like this - with your own tweets:

```bash
twitter_api_flask=# SELECT * FROM tweets;
 id |           text            |         created_at
----+---------------------------+----------------------------
  1 | this is a tweet !!!       | 2020-12-06 18:53:59.493008
  2 | this is another tweet !!! | 2020-12-06 18:54:15.282337
(2 rows)
```

</details>

* Exit the `psql` prompt: `\q` + **Enter**

---

## 3. Containerization - test environment

Let's adjust our `docker-compose.yml` so we have a command to test locally.
Add the following paragraph to it:

```yaml
version: '3.8'

services:
  ...

  web:
    ...

    environment:
      - DATABASE_URL=postgres://postgres:password@db:5432/twitter_api_flask
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_ENV=development

  test:
    build: .
    container_name: test
    depends_on:
      - db
    command: ["./wait-for-it.sh", "db:5432", "--", "nosetests", "-s", "--exe"]
    volumes:
      - .:/code
    environment:
      - DATABASE_URL=postgres://postgres:password@db:5432/twitter_api_flask
      - FLASK_ENV=test

volumes:
  postgres_data:
```

👉 Run `docker-compose up test` to launch the test suite locally.

Your tests should all pass:

<details><summary markdown='span'>View solution</summary>

You should get an output like this:

```bash
test    | wait-for-it.sh: waiting 15 seconds for db:5432
test    | wait-for-it.sh: db:5432 is available after 0 seconds
test    | .......
test    | ----------------------------------------------------------------------
test    | Ran 7 tests in 0.979s
test    |
test    | OK
test exited with code 0
```

</details>

* you have not changed any Python code, and it worked with the local setup at the beginning of the challenge
* so the only reason it could fail would be docker-based ! If you have an issue with your test suite, please ask a TA !


🎉 That's it for our local setup: we now have a standard way to **develop** our app and **run our test suite** on it.
It might not seem super useful but trust us: **it is** !
With this kind of setup:

* you will not have any compatibility issues
* you will be able to develop and test in a standardized way,
* you will be able to contribute with other developers on the exact same setup (that is now super easy to kick-off)

---

## I'm done! 🎉

Clean up your docker host by running ```docker-compose down -v``` to stop and remove the containers, and remove the volumes used above.

And that's it for this challenge ! Before you jump to the next challenge (`03-Background-Jobs`), let's mark your progress with the following:

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 05-Docker/02-Twitter-API
touch DONE.md
git add DONE.md && git commit -m "05-Docker/02-Twitter-API"
git push origin master
```
