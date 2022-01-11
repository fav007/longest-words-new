# API Twitter - Jour 2

Dans ce défi, nous allons reprendre le travail commencé dans l'exercice **Twitter API** d'hier. Dans cet exercice, la base de données a été _simulée_ par une classe inventée `TweetRepository`.

## Configuration

Nous allons poursuivre la correction d'hier :
:point_right: [github.com/ssaunier/twitter-api](https://github.com/ssaunier/twitter-api)

```bash
cd ~/code/<user.github_nickname>
git clone git@github.com:ssaunier/twitter-api.git twitter-api-database
cd twitter-api-database
git remote rm origin
```

Allez sur [github.com/new](https://github.com/new) créez un repository _public_ sous votre compte _personnel_, nommez-le `twitter-api-database`.

```bash
git remote add origin git@github.com:<user.github_nickname>/twitter-api-database.git
git push -u origin master
```

Maintenant que vous avez le repository, vous devez créer le virtualenv et installer les packages :

```bash
pipenv install --dev
```

Assurez-vous que les tests passent :

```bash
nosetests
```

Assurez-vous que le serveur web peut être exécuté et affichez la documentation Swagger :

```bash
FLASK_ENV=development pipenv run flask run
```

:point_right: Allez sur [localhost:5000](http://localhost:5000/). Est-ce que tout va bien ?

## Configuration de SQLAlchemy

Comme dans l'exercice précédent, nous devons installer quelques outils :

```bash
pipenv install psycopg2-binary gunicorn python-dotenv
pipenv install flask-sqlalchemy flask-migrate
```

Nous devons configurer la base de données utilisée en utilisant une variable d'environnement, le plus simple est d'utiliser le package `python-dotenv` avec un fichier `.env` :

```bash
touch .env
echo ".env" >> .gitignore
```

Et ajoutez la variable `DATABASE_URL` :

```bash
# .env
DATABASE_URL="postgresql://postgres:<password_if_necessary>@localhost/twitter_api_flask"

# On OSX:
# DATABASE_URL="postgresql://localhost/twitter_api_flask"
```

Si vous obtenez un `sqlalchemy.exc.OperationalError`, vérifiez votre `DATABASE_URL`. Votre mot de passe ne doit pas contenir les symboles `<`, `>`.

```bash
# Exemple valide
DATABASE_URL="postgresql://postgres:root@localhost/twitter_api_flask"

# Exemple invalide
DATABASE_URL="postgresql://postgres:<root>@localhost/twitter_api_flask"
```

Nous devons maintenant créer un objet de configuration à passer à l'application Flask. Cela permettra de lier les variables d'environnement à la configuration actuelle de Flask / SQLAlchemy :

```bash
touch config.py
```

```python
import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
```

Maintenant, nous allons instancier une instance de `SQLAlchemy`, mais d'abord nous allons supprimer les faux repositories :

```bash
rm app/db.py
rm app/repositories.py
rm tests/test_repositories.py
```

Ouvrez le fichier `app/apis/tweets.py` et le fichier `tests/apis/test_tweet_views.py` et supprimez la ligne suivante dans les deux fichiers :

```python
from app.db import tweet_repository
```

C'est officiel, les tests sont maintenant cassés :scream : Mais le `flask run` fonctionne toujours :muscle : !
Continuons courageusement en instanciant notre session SQLAlchemy que nous utiliserons pour toutes les requêtes SQL (CRUD).

```python
# app/__init__.py
# pylint: disable=missing-docstring

# [...]
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)
    db.init_app(app)

    # [...]
```

### Modèle

Maintenant, il est temps de **convertir** notre modèle `Tweet` existant en un modèle SQLAlchemy approprié, et pas seulement une classe ordinaire. Ouvrez le fichier `app/models.py` et mettez-le à jour :

```python
# app/models.py
# pylint: disable=missing-docstring

from datetime import datetime

from app import db

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tweet #{self.id}>"
```

Nous pouvons également nous débarrasser des tests sur le modèle puisqu'il ne s'agit plus d'une classe normale. Nous faisons confiance à SQLAlchemy pour le comportement des colonnes, et comme nous n'avons pas de méthode d'instance ici, pas besoin de tests unitaires :

```bash
rm tests/test_models.py
```

### Configurer Alembic

Nous avons besoin d'une base de données locale pour notre application :

```bash
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask"

# MAC OS
# createdb twitter_api_flask
```

Ensuite, nous devons modifier le fichier `app/__init__.py` pour que le module `flask-migrate` puisse identifier les changements effectués dans les modèle de l'app Python afin de les retranscrire en tant que migration dans la db:


```python
# app/__init__.py
# [...]
from flask_migrate import Migrate

# After db.init_app(app)
migrate = Migrate(app, db)
# [...]
```

Maintenant nous pouvons utiliser Alembic (lancez `pipenv graph` pour voir où il en est) !

```bash
pipenv run flask db init
```

Cette commande a créé un dossier `migrations`, avec `versions` qui est vide dedans. Il est temps de lancer la première migration avec la création de la table `tweets` à partir de la classe `Tweet` de `app/models.py`.

```bash
pipenv run flask db migrate -m "Create tweets table"
```

Ouvrez le dossier `migrations/versions` : voyez-vous un premier fichier de migration ? Allez-y, ouvrez-le et lisez-le ! C'est un fichier que vous **pouvez** modifier si vous n'êtes pas satisfait de ce qui a été généré automatiquement. En fait, c'est quelque chose que l'outil vous dit :

```bash
# ### commands auto generated by Alembic - please adjust! ###
```

Lorsque vous êtes satisfait de la migration, il est temps de l'exécuter sur la base de données locale :

```bash
pipenv run flask db upgrade
```

Et c'est tout ! Il y a maintenant une table `tweets` dans la base de données locale `twitter_api_flask`. Elle est vide pour l'instant, mais elle existe bel et bien !

## Ajouter un premier tweet à partir de shell

Nous voulons aller voir le "manual testing route" pour mettre à jour le code du contrôleur de l'API en ajoutant manuellement un premier Tweet dans la base de données. Cela permettra de confirmer que tous nos efforts pour ajouter SQLAlchemy commencent à porter leurs fruits :

```bash
pipenv run flask shell
>>> from app import db
>>> from app.models import Tweet
>>> tweet = Tweet(text="Our first tweet!")
>>> db.session.add(tweet)
>>> db.session.commit()
# Did it work?
>>> db.session.query(Tweet).count()
>>> db.session.query(Tweet).all()
# Hooray!
```

## Mise à jour du code du contrôleur de l'API

Maintenant que les modèles ont été migrés d'une classe Python muette vers des modèles SQLAlchemy appropriés reposant sur une base de données Postgresql locale, nous voulons mettre à jour le code dans `app/apis/tweets.py` afin qu'il n'utilise plus le `tweet_repository`.

Nous n'utiliserons pas les tests ( obsolètes ) pour essayer de faire en sorte que notre serveur _fonctionne à nouveau_. Exécutez le serveur :

```bash
FLASK_ENV=development pipenv run flask run
```

:point_right: Allez sur [localhost:5000/tweets/1](http://localhost:5000/tweets/1). Faites le fonctionner et renvoyez un JSON contenant le premier tweet que nous avons créé dans le `flask shell`.

Regardez le message d'erreur dans le terminal et essayez de corriger le code _vous-mêmes_. Il y a seulement une ligne de code à ajouter (un `import`) et une autre à modifier. Vous pouvez le faire :muscle: !

<details><summary markdown='span'>Voir la solution
</summary>

```python
# app/apis/tweets.py
# Ajouter cette ligne en début de fichier
from app import db

# Dans `TweetResource#get` remplacer cette ligne:
#   tweet = tweet_repository.get(tweet_id))
# par:
tweet = db.session.query(Tweet).get(tweet_id)
```

Félicitations ! Le site [localhost:5000/tweets/1](http://localhost:5000/tweets/1) fonctionne maintenant !

</details>

Laissons seulement la route `GET /tweets/:id` fonctionner, sans toucher aux autres, et essayons de corriger les tests d'abord avant d'y revenir.

## Mettre à jour les tests

Ouvrez le fichier `tests/apis/test_tweet_views.py`. Avant de se lancer dans le remplacement du `tweet_repository` par un `db.session`, faisons une pause et réfléchissons à ce que nous faisons.

Que se passe-t-il si vous exécutez ce qui suit dans une de vos méthodes de test ?

```python
tweet = Tweet(text="A test tweet")
db.session.add(tweet)
db.session.commit()
```

C'est bien cela ! Il va **créer un enregistrement** dans la base de données. Ce qui signifie que si vous exécutez les tests 10 fois, il créera 10 enregistrements ! Ceci va polluer votre environnement de développement :disappointed_relieved:

La solution est :

- d'exécuter le test avec un _autre_ schéma de base de données.
- de vider le schéma (en supprimant toutes les tables/en les recréant) pour chaque exécution du test (même chaque méthode !).

Voici comment nous allons atteindre cet objectif. Tout d'abord, nous devons créer une nouvelle base de données en local :

```bash
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask_test"

# MAC OS
# createdb twitter_api_flask_test
```

Et puis nous pouvons mettre à jour notre classe `TestTweetViews` avec :

```python
# tests/apis/test_tweet_views.py

from flask_testing import TestCase
from app import create_app, db  # N'oubliez pas d'importer db
from app.models import Tweet

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # [...]
```

Maintenant, continuez et mettez à jour les quatre tests en remplaçant l'ancienne logique `tweet_repository` par celle de `db.session`. Une fois que vous avez terminé, retournez dans le fichier `app/apis/tweets.py` pour corriger le code de l'API également ! Vous pouvez le faire :muscle: !

Pour vérifier si vous progressez correctement, exécutez les tests :

```bash
nosetests
```

<details><summary markdown='span'>Voir la solution
</summary>

Voici le code mis à jour pour le scénario de test `TestTweetViews` :

```python
    # tests/apis/test_tweet_views.py
    # [...]

    def test_tweet_show(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])

    def test_tweet_create(self):
        response = self.client.post("/tweets", json={'text': 'New tweet!'})
        created_tweet = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(created_tweet["id"], 1)
        self.assertEqual(created_tweet["text"], "New tweet!")

    def test_tweet_update(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.patch("/tweets/1", json={'text': 'New text'})
        updated_tweet = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_tweet["id"], 1)
        self.assertEqual(updated_tweet["text"], "New text")

    def test_tweet_delete(self):
        first_tweet = Tweet(text="First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        self.client.delete("/tweets/1")
        self.assertIsNone(db.session.query(Tweet).get(1))
```

Et voici le code de `app/apis/tweets.py` où nous devons mettre à jour les occurrences de `tweet_repository` :

```python
# [...]

class TweetResource(Resource):
    @api.marshal_with(json_tweet)
    def get(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            return tweet

    @api.marshal_with(json_tweet, code=200)
    @api.expect(json_new_tweet, validate=True)
    def patch(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            tweet.text = api.payload["text"]
            db.session.commit()
            return tweet

    def delete(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            db.session.delete(tweet)
            db.session.commit()
            return None

@api.route('')
@api.response(422, 'Invalid tweet')
class TweetsResource(Resource):
    @api.marshal_with(json_tweet, code=201)
    @api.expect(json_new_tweet, validate=True)
    def post(self):
        text = api.payload["text"]
        if len(text) > 0:
            tweet = Tweet(text=text)
            db.session.add(tweet)
            db.session.commit()
            return tweet, 201
        else:
            return abort(422, "Tweet text can't be empty")
```

</details>

## Mettre en place Travis

La configuration de Travis pour un projet où vous avez une vraie base de données PostgreSQL n'est pas aussi triviale que pour un projet sans base de données. Voyons comment nous pouvons reprendre la **configuration de Travis** déjà évoquée :

```bash
touch .travis.yml
```

```yml
# .travis.yml

language: python
python: 3.8
cache: pip
dist: xenial
addons:
  postgresql: 10
install:
  - pip install pipenv
  - pipenv install --dev
before_script:
  - psql -c 'CREATE DATABASE twitter_api_flask_test;' -U postgres
env:
  - DATABASE_URL="postgresql://localhost/twitter_api_flask"
script:
  - pipenv run nosetests
```

Versionnez & poussez ce changement. Allez ensuite sur [github.com/marketplace/travis-ci](https://github.com/marketplace/travis-ci) pour ajouter `<github-nickname>/twitter-api-database` à votre plan Travis gratuit si ce n'est pas encore le cas.

## En savoir plus

### Liste des Tweets

Ajoutons un autre point d'entrée à notre API pour récupérer **tous les tweets** :

```bash
GET /tweets
```

Allez-y, vous pouvez utiliser le TDD !

## C'est terminé !

Sauvegardez votre avancement avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 04-Database/02-Twitter
touch DONE.md
git add DONE.md && git commit -m "04-Database/02-Twitter done"
git push origin master
```
