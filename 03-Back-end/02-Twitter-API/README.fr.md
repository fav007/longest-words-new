# API Twitter

Maintenant que nous avons joué un peu avec Flask, il est temps de commencer les exercices qui nous occuperont pendant les trois prochains jours. L'objectif est de construire un clone de l'[API Twitter](https://developer.twitter.com/en/docs/api-reference-index) en utilisant Flask et différents modules externes Flask (comme [ceux-ci](https://github.com/humiaozuzu/awesome-flask)).

⚠️ Dans cet exercice, nous allons implémenter quelques points d'entrée (endpoints) d'API avec une grosse contrainte : nous n'avons pas encore de base de données relationnelle ! Cette contrainte vous aidera à vous concentrer sur la couche HTTP de l'API, et non sur la récupération des informations. Pour faire abstraction de la base de données, nous utiliserons le modèle [data access object (DAO)](https://en.wikipedia.org/wiki/Data_access_object) et demain, nous le remplacerons par des requêtes réelles vers la base de données.

## Pour commencer

Commençons un nouveau projet Flask :

```bash
cd ~/code/<user.github_nickname>
mkdir twitter-api && cd twitter-api
pipenv --python 3.8
pipenv install flask
touch wsgi.py
```

### Modèle d'usine (Factory Pattern)

Dans l'exemple précédent, nous avons initialisé l'application `Flask` directement dans le fichier `wsgi.py`. En faisant cela, `app` était une variable globale. Le problème avec cette approche est qu'il est plus difficile de tester en isolant. La solution à ce problème est d'utiliser [Application Factories](http://flask.pocoo.org/docs/patterns/appfactories/), un modèle qui s'avérera utile pour rendre notre application plus modulable (c'est-à-dire avec plusieurs "petits" fichiers plutôt que quelques "gros").

👉 Prenez le temps de lire [cette page de la documentation de Flask](http://flask.pocoo.org/docs/patterns/appfactories/)

Utilisons cette approche :

```bash
mkdir app             # Il s'agit du dossier de notre application principale.
touch app/__init__.py # Et ouvrez ce fichier dans VS Code
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

Ensuite, ouvrez le fichier `./wsgi.py` et importez cette nouvelle `create_app` pour l'utiliser immédiatement :

```python
# ./wsgi.py

from app import create_app

application = create_app()
if __name__ == '__main__':
    application.run(debug=True)
```

Allez-y et lancez l'application :

```bash
FLASK_ENV=development pipenv run flask run
```

Le serveur devrait démarrer. Ouvrez votre navigateur et visitez [`localhost:5000/hello`](http://localhost:5000/hello). Vous devriez voir s'afficher "Hello world !" !

### Espace de noms (Namespace)

Le code dans `app/__init__.py` est un copier/coller de l'exercice précédent, nous avons juste pris le code et l'avons mis dans une méthode `create_app`, retournant l'instance de `Flask` créée. Nous pouvons faire mieux !

Nous utiliserons le paquet [`flask-restx`](https://flask-restx.readthedocs.io/) :

```bash
pipenv install flask-restx
```

Prenez le temps de lire l'article suivant :

:point_right: [Démarrage rapide](https://flask-restx.readthedocs.io/en/stable/quickstart.html)

Nous voulons commencer du bon pied en termes de possibilités d'évolution, prenez le temps de lire ce qui suit :

:point_right: [Faire évoluer votre projet](https://flask-restx.readthedocs.io/en/stable/scaling.html)

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

:bulb: En utilisant notre espace de noms "tweets" `api = Namespace("tweets")`, notre route API "hello" deviendra `/tweets/hello` au lieu de simplement `/hello`.

:bulb: La méthode `get` définie ci-dessus sera appelée lorsque le serveur recevra une requête HTTP GET sur `/tweets/hello`.

Nous pouvons maintenant importer notre espace de noms simple dans notre application principale, comme ceci :

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

Si vous avez arrêté votre serveur, redémarrez-le avec :

```bash
FLASK_ENV=development pipenv run flask run
```
Ouvrez votre navigateur et visitez [`localhost:5000/tweets/hello`](http://localhost:5000/tweets/hello). Vous devriez voir s'afficher "Hello from the 'tweets' namespace !" !

💡 Il est important de comprendre la ligne `from .apis.tweets import api as tweets` qui se trouve avant l'enregistrement de l'espace de nom. Le `from .apis.tweets` signifie que nous regardons dans le fichier `apis/tweets.py` du **même** dossier que le `__init__.py` local. C'est un raccourci pour `from app.apis.tweets`. Ensuite, le `import api` signifie que nous importons la variable ou la méthode `api` définie dans ce fichier `tweets.py` (ici c'est une variable : une instance de `Namespace`). Le `as tweets` renomme simplement l'`api` que nous avons importé en `tweets`, pour plus de lisibilité.

### Tests

Configurons notre application de manière à ce que l'écriture de tests soit facile et que le TDD soit possible :

```bash
pipenv install flask-testing nose --dev
```

Créons nos dossiers `tests` et un premier fichier

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

Ouvrez le terminal et exécutez :

```bash
pipenv run nosetests -s tests/apis/test_tweet_view.py
```

Le test doit être rouge !

👉 Comment corriger le test pour que la commande devienne verte ?
👉 Avons-nous besoin de l'instruction `print()` dans la méthode de test ? Pourquoi (non) ?

### Déploiement

Nous voulons utiliser Gunicorn et Heroku pour la production :

```bash
pipenv install gunicorn
echo "web: gunicorn wsgi --access-logfile=-" > Procfile
```

Enfin, nous allons configurer git :

```bash
git init
git add .
git commit -m "Nouveau projet Flask"
```

À ce moment-là, vous devriez déjà avoir créé 5 applications (ce qui est la limite gratuite).

Nous devons donc `faire un peu de nettoyage`.
Tout d'abord, nous voulons obtenir le nom de l'application afin de la supprimer :

```bash
heroku apps  # Affiche les applications créées
# === <votre_mail> Apps
# <app_name_1> (eu)
# <app_name_2> (eu)
# <app_name_3> (eu)
# <app_name_4> (eu)
# <app_name_5> (eu)
```

Alors nous pouvons la supprimer :
```bash
heroku apps:destroy <app_name_1>
# !    WARNING: This will delete <app_name_1> including all add-ons.
# !    To proceed, type <app_name_1> or re-run this command with
# !    --confirm <app_name_1>

<app_name_1>  # Tapez <nom_app_1> et appuyez sur <Entrée>.
# Destroying <app_name_1> (including all add-ons)... done
```

**Procédez à cette opération chaque fois que nécessaire**

Nous pouvons maintenant créer une application qui sera déployée sur Heroku :

```bash
heroku create --region=eu
git push heroku master

heroku open # Vérifier que l'application fonctionne bien.
```

## Premier point d'entrée de l'API - `/tweets/:id`

Dans la section suivante, nous allons implémenter l'API HTTP servant un JSON d'un seul tweet.

### Modèle

Avant de se précipiter dans l'espace de noms Flask, nous devons créer pour servir une réponse HTTP, nous avons besoin d'un modèle pour contenir des données. Nous n'avons pas (encore) de base de données, donc nous allons créer tout manuellement aujourd'hui.

Pensons à notre `Tweet` et utilisons le TDD pour implémenter cette classe. Jetez un coup d'oeil à ce qu'est [un Tweet](https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-statuses-show-id#example-response) et vous verrez que c'est assez complexe.
Simplifions en disant qu'un tweet contient un `text` et une date `created_at`.

### TDD

Utilisons le TDD pour implémenter cette classe `Tweet` avec ses deux variables d'instance. Nous allons d'abord écrire le test en premier et ensuite nous avancerons jusqu'à ce que le test devienne vert.

```bash
touch tests/test_models.py
```

```python
# tests/test_models.py
from unittest import TestCase
from app.models import Tweet  # Nous allons coder notre classe `Tweet` dans `app/models.py`.

class TestTweet(TestCase):
    def test_instance_variables(self):
        # Créer une instance de la classe `Tweet` avec un argument
        tweet = Tweet("my first tweet")
        # Vérifiez que `text` contient le contenu du tweet.
        self.assertEqual(tweet.text, "my first tweet")
        # Vérifiez que lors de la création d'une nouvelle instance de `Tweet`, sa date `created_at` est définie.
        self.assertIsNotNone(tweet.created_at)
        # Vérifier que l'id du tweet n'est pas encore attribué lors de la création d'un tweet en mémoire.
        self.assertIsNone(tweet.id)
```

👉 Prenez le temps de lire le chapitre [26.4. `unittest`](https://docs.python.org/3/library/unittest.html).

OK, le test est écrit, exécutons-le ! (il ne doit pas être vert) :

```bash
pipenv run nosetests tests/test_models.py
```

💡 _Dans la commande ci-dessus ☝️, on donne le nom exact du fichier pour n'exécuter que ce fichier de test_.

Vous devriez obtenir quelque chose qui ressemble à ceci :

```bash
======================================================================
1) ERROR: Failure: ModuleNotFoundError (No module named 'app.models')
----------------------------------------------------------------------
    # [...]
    tests/test_models.py line 2 in <module>
      from app.models import Tweet
   ModuleNotFoundError: No module named 'app.models'
```

:question: Quelle est la prochaine étape ? **Lisez le message d'erreur et essayez de le corriger**.

<details><summary markdown='span'>Voir la solution
</summary>

Vous devez créer le fichier `models.py` pour que ce module soit défini !

```bash
touch app/models.py
```
</details>

<br />

Exécutez à nouveau les tests **jusqu'à ce que le message d'erreur change**. Vous devriez obtenir celui-ci :

```bash
======================================================================
1) ERROR: Failure: ImportError (cannot import name 'Tweet')
----------------------------------------------------------------------
    # [...]
    tests/test_models.py line 2 in <module>
      from app.models import Tweet
   ImportError: cannot import name 'Tweet'
```

:question: Quel est le changement de code **minimal** que vous pouvez faire pour corriger cette erreur ?

<details><summary markdown='span'>Voir la solution
</summary>

L'erreur dit que `Tweet` n'est pas défini. La modification du code
que nous pouvons faire est de créer une classe **vide** :

```python
# app/models.py
class Tweet:
    pass
```
</details>

<br />

La prochaine erreur devrait être :

```bash
======================================================================
1) ERROR: test_instance_variables (test_models.TestTweet)
----------------------------------------------------------------------
   Traceback (most recent call last):
    tests/test_models.py line 6 in test_instance_variables
      tweet = Tweet("my first tweet")
   TypeError: object() takes no parameters
```

:question: Quel est le changement de code **minimal** que vous pouvez faire pour corriger cette erreur ?

<details><summary markdown='span'>Voir la solution
</summary>

Notre classe `Tweet` est vide et a besoin d'une [variable d'instance](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables) `text`:

```python
# app/models.py
# pylint: disable=missing-docstring

class Tweet:
    def __init__(self, text):
        self.text = text
```

</details>

<br />


Les deux erreurs suivantes devraient se produire :

```bash
'Tweet' object has no attribute [...]
```

:question: Comment pouvons-nous corriger ces deux dernières erreurs et faire passer le test ?

<details><summary markdown='span'>Voir la solution
</summary>

Il manque à notre classe `Tweet` la variable d'instance `created_at`,
automatiquement définie à [l'heure actuelle](https://stackoverflow.com/questions/415511/how-to-get-current-time-in-python).
Il lui manque également la variable d'instance `id`, définie comme `None` lors de la création de l'instance.

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

✨ Félicitations ! Vous venez d'implémenter la classe `Tweet` en utilisant le TDD.

### Repository

Nous avons besoin d'un modèle pour contenir toutes les instances de `Tweet` et les id auto-incrémentés assignés.
Cette classe sera remplacée dans le prochain chapitre par un véritable [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping)
qui interagit avec une base de données relationnelle. En attendant, nous avons besoin d'en **créer un faux**.

**Spécification** : La classe *repository* contiendra une liste de tweets, vide au début,
mais va `ajouter` de nouveaux tweets. Lors de l'ajout d'un nouveau tweet, elle lui attribuera
automatiquement un id auto-incrémenté (en commençant par `1`). Enfin, il devrait permettre
`d'obtenir` un tweet basé sur son id.
La liste des tweets sera conservée en mémoire.


Si nous voulions tester le comportement de notre nouvelle classe, voici ce que nous pourrions faire (essayez de comprendre ce qu'elle fait et quels cas nous testons) :

💡 Ceci est seulement informatif, vous n'avez pas besoin de copier-coller le code de test.

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


Maintenant, nous allons créer notre classe `TweetRepository`. Copiez-collez ce code dans un nouveau fichier `app/repositories.py` :

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

💡 Vous voyez comment le fichier de test est beaucoup plus long que l'implémentation réelle ?

💡 Notre classe `TweetRepository` est une _simulation_, c'est-à-dire qu'elle imite le comportement d'une autre fonctionnalité, nous soulageant de la nécessité d'une autre dépendance. Ici, nous simulons une couche de base de données en utilisant une simple liste de `tweets`.

<br />

### Controller + Route

Il est maintenant temps d'ajouter une nouvelle route à notre application pour servir notre point d'entrée API.
Rappelez-vous, nous voulons avoir ceci :

```bash
GET /tweets/1

=> un JSON du tweet abtenu
```

Écrivons le test pour notre nouvelle route :

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

💡 Si vous exécutez le test, il se dira que `tweet_repository` n'existe pas.

```bash
pipenv run nosetests tests/apis/test_tweet_views.py
```

`tweet_repository` est notre fausse base de données. C'est juste une instance de `TweetRepository`. Créez-la :

```bash
touch app/db.py
```

```python
# app/db.py

from .repositories import TweetRepository

tweet_repository = TweetRepository()
```

Maintenant, faisons en sorte que le test passe ! Vous pouvez supprimer la route `/hello` en remplaçant entièrement le contenu de ce fichier :

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

:question: Implémentez le reste de `app/apis/tweets.py` pour que le test passe.

:bulb: **Astuce**: vous devez utiliser le `api.model()` et `@api.marshal_with` décrit [dans le document](https://flask-restx.readthedocs.io/en/stable/quickstart.html#data-formatting) pour contourner l'erreur suivante :

```bash
TypeError: Object of type Tweet is not JSON serializable
```

Comprenez-vous cette erreur ? Si ce n'est pas le cas, demandez à votre buddy puis à un TA !

```bash
pipenv run nosetests tests/apis/test_tweet_views.py
```

:bulb: **Astuce**: Jetez un coup d'œil à l'[exemple complet](https://flask-restx.readthedocs.io/en/stable/example.html) de la documentation !

<details><summary markdown='span'>Voir la solution (Essayez vraiment d'abord 🙏)
</summary>

Nous allons utiliser la sérialisation intégrée de Flask-RESTX :

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

### Exécution du serveur

Laissons les tests pour le moment (l'exécution de `nosetests` devrait donner 6 tests réussis) et lançons le serveur :

```bash
FLASK_ENV=development pipenv run flask run
```

Ouvrez maintenant votre navigateur et allez sur [`localhost:5000/tweets/1`](http://localhost:5000/tweets/1).

:question: Lisez le message d'erreur et trouvez quelle ligne de votre code le déclenche. Pourquoi ?

<details><summary markdown='span'>Voir la solution
</summary>

A la ligne 8 de `app/api/tweets.py`, nous récupérons un tweet avec id == 1 **mais** il n'y a pas de tweet dans le référentiel
encore ! Alors `tweet` est `None`, d'où l'erreur :

```bash
AttributeError: 'NoneType' object has no attribute 'id'
```

Pour résoudre ce problème, nous devons simuler une base de données avec des tweets préexistants au démarrage du serveur. Nous pouvons le faire avec :

```python
# app/__init__.py
# pylint: disable=missing-docstring

from flask import Flask # Cette ligne existe déjà
from flask_restx import Api # Cette ligne existe déjà

from .db import tweet_repository
from .models import Tweet
tweet_repository.add(Tweet("a first tweet"))
tweet_repository.add(Tweet("a second tweet"))

def create_app():  # Cette ligne existe déjà
    # [...]
```

Essayez à nouveau [`localhost:5000/tweets/1`](http://localhost:5000/tweets/1). Vous obtenez un joli JSON de votre tweet ? Hourra !

</details>

:bulb: N'oubliez pas de versionner et de déployer !

## Bonus

### Documentation sur Swagger

Le paquet Flask-RESTx est livré avec [swagger doc](https://flask-restx.readthedocs.io/en/stable/swagger.html) intégré. Exécutez votre serveur et accédez à l'URL racine :

:point_right: [http://localhost:5000](http://localhost:5000)

Vous pouvez voir la documentation ? Vous pouvez essayer vos points d'entrée directement dans celle-ci !

### Pour aller plus loin

Si vous avez atteint cette partie, vous avez compris l'essentiel de la construction d'une API RESTful avec Flask. Il est temps de s'exercer !

- Implémentez les autres points d'entrée pour avoir une API RESTful `CRUD` complète ! Aujourd'hui, nous ne nous soucions pas de l'autorisation de l'utilisateur pour la création, la mise à jour et la suppression. [Le document est votre ami](https://flask-restx.readthedocs.io/en/stable/)
- Utilisez le flux GitHub pour chaque nouveau point d'entrée !
- Déployez souvent ! Chaque fois que vous intégrez une branche avec un nouveau point d'entrée, `git push heroku master`

Bonne chance 😉

## J'ai fini!

Avant de passer à l'exercice suivant, indiquons vos progrès avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 03-Back-end/02-Twitter-API
touch DONE.md
git add DONE.md && git commit -m "03-Back-end/02-Twitter-API terminé"
git push origin master
```
