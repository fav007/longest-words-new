# SQLAlchemy

Avant de retourner sur le repository `twitter-api` d'hier, créons une toute nouvelle application Flask (sans le factory pattern `create_app`).

Voici la liste de ce que nous allons installer au cours de cet exercice :

 :bulb: _**ne les installez pas tout de suite**, nous le ferons progressivement_

- [psycopg2](http://initd.org/psycopg/) qui nous permettra d'utiliser PostgreSQL
- [SQLAlchemy](https://www.sqlalchemy.org/) comme ORM en plus de PostgreSQL
- [Alembic](http://alembic.zzzcomputing.com/) pour gérer les migrations de schéma avec le paquet [`Flask-Migrate`](http://flask-migrate.readthedocs.io/).
- Nous allons déployer notre application avec Heroku

## PostgreSQL

:warning: **N'installez pas Postgres si vous utilisez un ordinateur du Wagon**. Il devrait être déjà installé. Si ce n'est pas le cas, installez-le.

Vous pouvez maintenant vous rendre sur [postgresql.org/download/windows/](https://www.postgresql.org/download/windows/) et `télécharger` le programme d'installation de `PostgreSQL 10+`.

Exécutez-le. Il installera :

- le serveur PostgreSQL
- pgAdmin 4, un client GUI très utile pour exécuter des requêtes et administrer le serveur
- Les outils de ligne de commande qui seront utiles pour installer le paquet `psycopg2`

L'assistant d'installation vous demandera un mot de passe superadmin. Mettez quelque chose dont vous pouvez vous souvenir facilement (généralement `root`).

Vous devriez laisser le port à la valeur suggérée par défaut (`5432`), et choisir `Anglais, États-Unis` comme locale par défaut.

Une fois l'installation terminée, `stack-builder` s'ouvrira. Il suffit `d'annuler`. Nous n'avons pas besoin d'installer d'autres outils postgreSQL.

## Pour commencer

Créons un nouveau repository à partir de zéro (c'est le moment d'installer toutes nos dépendances) :

```bash
cd ~/code/<user.github_nickname>
mkdir flask-with-sqlalchemy
cd flask-with-sqlalchemy
git init
pipenv --python 3.8
pipenv install flask psycopg2-binary gunicorn flask-sqlalchemy flask-migrate python-dotenv
pipenv install pylint --dev
```

```bash
touch wsgi.py
code . # Ouvrir VS Code dans le dossier actuel
```

### Flask Boilerplate

Dans votre fichier `wsgi.py`, copiez-collez le boilerplate suivant :

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask
app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200
```

Vérifiez que votre application commence par :

```bash
FLASK_ENV=development pipenv run flask run
```

Et allez sur [`localhost:5000/hello`](http://localhost:5000/hello)

Nous allons devoir manipuler des variables d'environnement pour configurer l'accès à la base de données.

```bash
touch .env
echo ".env" >> .gitignore # Vous ne voulez pas versionner vos variables d'environnement !
```

Essayons cela tout de suite. Ouvrez le fichier `.env` dans VS Code et ajoutez une variable d'environnement fictive :

```bash
# .env
DUMMY="dummy"
```

Ouvrez le fichier `wsgi.py` et insérez au début du fichier le code suivant :

```bash
import os
import logging
logging.warn(os.environ["DUMMY"])

# [...]
```

Arrêtez et redémarrez le serveur :

```bash
FLASK_ENV=development pipenv run flask run
```

Vous devriez voir ça :

```bash
Loading .env environment variables...
# [...]
WARNING:root:dummy
```

Vous voyez ? Il remplit automatiquement le `os.environ` avec le contenu du fichier `.env`!

Vous pouvez maintenant `supprimer ces 3 lignes`, vous n'en avez plus besoin :

```bash
import os
import logging
logging.warn(os.environ["DUMMY"])

# [...]
```

## La classe `Config`

Pour préparer un déploiement sur Heroku, nous allons indiquer à l'application Flask comment se connecter à la base de données **via une variable d'environnement `DATABASE_URL`**. Nous pouvons encapsuler ce comportement dans un fichier spécifique :

```bash
touch config.py
```

```python
# config.py
# pylint: disable=missing-docstring

import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # L'appel de replace() permet de s'assurer que l'URI commence par 'postgresql://' et non par 'postgres://' comme c'était le cas auparavant (il s'agit d'un hack de rétrocompatibilité).
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"].replace("postgres://", "postgresql://", 1)
```

Une fois que nous avons ce fichier, nous pouvons **lier** l'application Flask à SQLAlchemy.
A ce stade, voici le `contenu complet` de votre fichier `wsgi.py` :

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World!", 200
```

## `DATABASE_URL`

La variable d'environnement `DATABASE_URL` est la base de la configuration de SQLAlchemy. C'est là que vous mettez toutes les informations nécessaires au code python pour se connecter au serveur de base de données.


Complétons le fichier `.env`!
`Supprimez` la variable `DUMMY`.
En développement, nous utiliserons cette url de base de données :

```bash
# .env
DATABASE_URL="postgresql://postgres:<password_if_necessary>@localhost/flask_db"
```

Si vous obtenez un `sqlalchemy.exc.OperationalError`, vérifiez votre `DATABASE_URL`. Votre mot de passe ne doit pas contenir les symboles `<`, `>`.

```bash
# Exemple valide
DATABASE_URL="postgresql://postgres:root@localhost/flask_db"

# Exemple invalide
DATABASE_URL="postgresql://postgres:<root>@localhost/flask_db"
```

Cela signifie que nous utilisons le serveur PostgreSQL que nous avons installé plus tôt ainsi que la base de données `flask_db`. Base de données que nous devons d'ailleurs créer!

Pour la première commande, utilisez votre `numéro de version postgreSQL` selon l'installateur que vous avez choisi (généralement `10` sur les ordinateurs du Wagon, `12` pour une nouvelle installation).

```bash
echo 'PATH="/c/Program Files/PostgreSQL/<YOUR_POSTGRESQL_VERSION>/bin":$PATH' >> ~/.profile
winpty psql -U postgres -c "CREATE DATABASE flask_db"
```

## Ajout du **premier** modèle

Créez un nouveau fichier `models.py` :

```bash
touch models.py
```

```python
# models.py
# pylint: disable=missing-docstring

from wsgi import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id)
```

Une fois le premier modèle créé, nous pouvons l'inclure dans le fichier principal :

```python
# wsgi.py
# [...] After `db = SQLAlchemy(app)`
from models import Product
```

Nous allons maintenant configurer Alembic pour générer notre première migration et mettre à jour la base de données pour **créer** la table `products`.

Ajoutez dans `wsgi.py` le code suivant:

```python
# wsgi.py
from flask_migrate import Migrate
# [...] After `from models import Product`

migrate = Migrate(app, db)
```

Ceci nous permet de créer un dossier de migration et d'initialiser les fichiers d'Alembic :

```bash
pipenv run flask db init
```

Ensuite, nous pouvons exécuter une migration pour capturer l'état du fichier `models.py` :

```bash
pipenv run flask db migrate -m "create products"
```

Ouvrez le fichier dans `./migrations/versions` et lisez la méthode auto-générée `upgrade()`. Avez-vous vu comment elle crée les deux colonnes `id` et `name` ?

Pour appliquer cette migration à la base de données, exécutez ceci :

```bash
pipenv run flask db upgrade
```

Pour vérifier manuellement que le schéma contient maintenant une table `product`, reconnectez-vous à la base de données PostgreSQL :

```bash
winpty psql -U postgres -d flask_db
flask_db#= \dt
# Vous devriez voir deux tables : `products` et `alembic_version` !
flask_db#= \d products
# Vous devriez voir les deux colonnes de la table `product` : `id` et `name`
flask_db#= \q
```

Vous voyez comme c'est facile ?

## Mettre à jour un modèle

Alembic (le package derrière `manage.py db`) se démarque lorsque nous mettons à jour un modèle. Il va automatiquement générer une nouvelle migration avec la "différence" dans la définition du modèle.

```python
# models.py
# pylint: disable=missing-docstring

class Product(db.Model):
    # [...]
    description = db.Column(db.Text())
```

Retournez dans le terminal et exécutez la commande `migrate` :

```bash
pipenv run flask db migrate -m "add description to products"
```

Que s'est-il passé dans `migrations/versions` ?
Lisez ce nouveau fichier et exécutez ensuite la commande `upgrade` :

```bash
pipenv run flask db upgrade
```

Vous pouvez vérifier que cela a fonctionné avec :

```bash
winpty psql -U postgres -d flask_db
flask_db#= \d products
# Vous devriez maintenant voir trois colonnes dans ce tableau
flask_db#= \q
```

## Insertion d'un enregistrement

Notre schéma de base de données est prêt. Nous avons utilisé la ligne de commande `psql` pour le consulter. Nous pouvons maintenant utiliser pgAdmin 4 pour rechercher des enregistrements dans la base de données. Lancez pgAdmin à partir du menu Démarrer de Windows. Il devrait ouvrir `localhost:53042` dans Chrome. Dans l'arborescence, allez dans `Servers` > `PostgreSQL 10` > `Databases` > `flask_db` > `Schemas` > `public` > `Tables` > `products` et faites un clic droit dessus : `View/Edit Data` > `All rows`. Il va générer la requête SQL `SELECT` pour vous. Cliquez sur le bouton avec un petit tonnerre ⚡️ (ou play ▶️) pour exécuter la requête. Il ne devrait y avoir _aucun_ enregistrement.

Insérons deux produits dans la base de données ! Nous pouvons utiliser la [fonction shell de flask](http://flask.pocoo.org/docs/1.0/cli/#open-a-shell).

```bash
pipenv run flask shell
>>> from models import Product
>>> from wsgi import db
>>> skello = Product()
>>> skello.name = "Skello"
>>> socialive = Product()
>>> socialive.name = "Socialive.tv"
>>> db.session.add(skello)
>>> db.session.add(socialive)
>>> db.session.commit()
>>> quit()
```

Retournez dans pgAdmin 4 dans Chrome et cliquez à nouveau sur le bouton tonnerre ⚡ (ou play ▶️). Hourra ! Vous avez maintenant deux enregistrements dans la base de données !


## À propos des modèles, des migrations et des versionnages

Puisque nos `modèles` génèrent des tables dans la base de données, ils sont `fortement corrélés` à nos `schémas de base de données`.
C'est pour cette raison que, à chaque création/mise à jour de modèle, nous devons `versionner` le code de nos `modèles` et de nos `migrations` générées ensemble afin d'assurer l'`atomicité` de notre logique fonctionnelle.
`Demandez à un TA` si cela n'est pas clair pour vous, ce point est `très important`.


## Création de notre premier point d'accès à l'API

Nous allons coder le point de terminaison `/products`, listant _tous_ les produits (ici nous ne paginons pas).

Hier, nous avons utilisé une fausse base de données et n'avons pas eu de problème avec `jsonify`. Maintenant que nous récupérons des données depuis la base de données et que nous utilisons des sous-classes `db.Model`, nous allons avoir des problèmes de **sérialisation**. Pour les anticiper, nous devons introduire un autre package : [`marshmallow`](https://marshmallow.readthedocs.io/)

```bash
pipenv install flask-marshmallow marshmallow-sqlalchemy
```

Nous pouvons maintenant instancier l'application `Marshmallow` (`faites attention` aux lignes `NEW LINE` et à leur position) :

```python
# wsgi.py
# pylint: disable=missing-docstring

# [ all previous imports ...
#   from flask import Flask, abort, request
#   from config import Config
#   app = Flask(__name__)
#   app.config.from_object(Config)
# ]

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow  # NEW LINE (L'ordre est important ici !)
db = SQLAlchemy(app)
ma = Marshmallow(app)  # NEW LINE


# [Product model import]

# [ 'hello' route definition ]
```

Nous devons également définir un schéma de sérialisation pour les modèles pour lesquels nous attendons une réponse sous le format JSON via nos points de terminaison d'API :

```bash
touch schemas.py
```

```python
# schemas.py
# pylint: disable=missing-docstring

from wsgi import ma
from models import Product

class ProductSchema(ma.Schema):
    class Meta:
        model = Product
        fields = ('id', 'name') # Ce sont les champs que nous voulons dans le JSON !

one_product_schema = ProductSchema()
many_product_schema = ProductSchema(many=True)
```

Maintenant que nous avons nos schémas, nous pouvons les utiliser et implémenter notre point de terminaison pour l'API !

```python
# wsgi.py
# pylint: disable=missing-docstring

BASE_URL = '/api/v1'

# [all previous imports... ending with Product model import]

from schemas import many_product_schema

# ['hello' route definition]

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200
```

Et ça devrait être bon ! Lancez votre serveur et allez sur `localhost:5000/api/v1/products`. Vous devriez voir les deux produits dans la base de données sous le format JSON !

## Déploiement sur Heroku

Il est temps de pousser notre fantastique code en production. Nous allons créer une nouvelle application Heroku, mais avant cela, nous devons configurer le `Procfile`. Avec SQLAlchemy, il y a un léger changement :

1. Nous devons indiquer à Heroku que nous avons besoin d'une base de données PostgreSQL
1. Nous avons besoin qu'Heroku exécute `pipenv run flask db upgrade` à chaque déploiement pour garder le schéma de la base de données de production en synchronisation avec le code !

```bash
touch Procfile
```

```bash
# Procfile

web: gunicorn wsgi:app --access-logfile=-
```

Déployons :

```bash
git add .
git commit -m "First Deployment to Heroku"

heroku create --region=eu
git push heroku master
```

Une fois de plus, vous pouvez profiter de la **magie** de Heroku ! Avec les 3 lignes suivantes, vous pouvez déployer votre base de donnée en production :

```bash
heroku config:get DATABASE_URL
heroku addons:create heroku-postgresql:hobby-dev
heroku run flask db upgrade
```

Ouvrez votre application !

```bash
heroku open
```

:question: Vous devriez obtenir le `Hello world` sur la page d'accueil. Allez sur `/api/v1/products`. Combien de produits voyez-vous ? Pourquoi est-ce différent de `localhost` ?

<details><summary markdown='span'>Voir la solution
</summary>

La base de données de production et la base de données locale (de développement) ne sont **pas les mêmes** !

Pour ajouter des produits à la base de données de production, vous pouvez utiliser le shell Flask, en vous connectant à distance au dyno Heroku (_comme avec SSH_) :

```bash
heroku run flask shell

>>> from models import Product
>>> from wsgi import db
>>> skello = Product()
>>> skello.name = "Skello"
>>> db.session.add(skello)
>>> db.session.commit()
>>> quit()
```

Maintenant, rechargez la page. Vous voyez, le nouveau produit a été ajouté !

</details>

## À votre tour !

Nous avons établi l'architecture de base de Flask en utilisant SQLAlchemy et un package de sérialisation pour obtenir des JSON de ces modèles. Vous devez maintenant implémenter ce qui suit :

- `READ` : Le point de terminaison pour lister **un seul produit** à partir de son id.
- `CREATE` : Le point de terminaison pour créer un nouveau produit à partir du corps de la requête `POST`
- `DELETE` : Le point de terminaison pour supprimer un produit d'une base de données
- `UPDATE` : Le point de terminaison pour mettre à jour un produit existant à partir du corps de la requête `PATCH` et de son id dans l'URL.

Ces liens de documentation devraient vous aider :

- [SQLAlchemy - `Query.get()`](http://docs.sqlalchemy.org/en/latest/orm/query.html#sqlalchemy.orm.query.Query.get)
- [SQLAlchemy - Adding and Updating Objects](http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#adding-and-updating-objects)

## C'est terminé !

Avant de passer à l'exercice suivant, sauvegardez votre avancement avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 04-Database/01-SQLAlchemy
touch DONE.md
git add DONE.md && git commit -m "04-Database/01-SQLAlchemy done"
git push origin master
```
