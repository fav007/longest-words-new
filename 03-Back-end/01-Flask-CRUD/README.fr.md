# CRUD Flask

![](http://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png)

[Flask](http://flask.palletsprojects.com/en/1.1.x/) est un **micro cadre d'application** pour Python permettant de construire rapidement une application web.

Dans cet exercice, nous allons passer rapidement en revue toutes les fonctionnalités importantes de Flask.

## Pour commencer

Vous travaillerez dans un repository dédié pour appliquer les bonnes pratiques abordées dans le cours précédent.

```bash
cd ~/code/<user.github_nickname>
mkdir flask-101 && cd $_
pipenv --python 3.8
pipenv install flask gunicorn
touch wsgi.py
code . # Ouvrez VS Code dans le dossier actuel.
```

Vous êtes curieux de savoir sur quels paquets Flask s'appuie ? Exécutez ceci dans votre terminal :

```bash
pipenv graph
```

Super, n'est-ce pas ?

### Boilerplate Flask

Dans votre fichier `wsgi.py`, copiez-collez le modèle suivant :

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"
```

Que fait ce code ?

1. D'abord nous avons importé la classe Flask. Une instance de cette classe sera notre application Web.
1. Ensuite, nous créons une instance de cette classe. Le premier argument est le nom du module ou du paquet de l'application.
1. Nous utilisons ensuite le décorateur `route()` pour indiquer à Flask quelle URL doit déclencher notre fonction.
1. La fonction reçoit un nom qui est également utilisé pour générer des URLs pour cette fonction particulière, et retourne le message que nous voulons afficher dans le navigateur de l'utilisateur.


### Poursuite du développement

Retournez à votre terminal et exécutez :

```bash
FLASK_ENV=development pipenv run flask run
```

Le serveur devrait démarrer. Ouvrez votre navigateur et aller sur [`localhost:5000`](http://localhost:5000). Vous devriez voir "Hello world !" comme réponse textuelle !

Essayez de modifier le code et de recharger la page dans le navigateur. 💡 Que se passe-t-il ?

### Phase de production

En production, nous ne voulons pas utiliser le serveur Flask par défaut, optimisé pour le développement, mais quelque chose comme [Gunicorn](http://gunicorn.org/), déjà installé dans le `Pipfile` grâce à une commande précédente.

Le serveur de production exécutera ce code :

```bash
# Ctrl-C pour arrêter le serveur précédent
pipenv run gunicorn wsgi:app --access-logfile=-
```

:bulb: Si vous le lancez sous Windows, il échouera car gunicorn ne prend pas (encore ?) en charge Windows :

- [github.com/benoitc/gunicorn/issues/524](https://github.com/benoitc/gunicorn/issues/524)
- [stackoverflow.com/questions/11087682/does-gunicorn-run-on-windows](https://stackoverflow.com/questions/11087682/does-gunicorn-run-on-windows) (ils parlent de [`waitress`](https://docs.pylonsproject.org/projects/waitress))

## Heroku

Essayons de déployer cette application sur Heroku :

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
git commit -m "Premier déploiement du boilerplate Flask"

heroku create --region=eu
git push heroku master

heroku ps                  # Vous avez un dyno `gunicorn` gratuit en service?

heroku open                # Obtenez-vous un "Hello world" dans le navigateur ?
heroku logs -n 1000 --tail # Vérifiez que le journal (logs) s'affiche. Rechargez le navigateur.
```

## JSON

Pour l'instant, notre application renvoie du texte brut. L'objectif d'aujourd'hui est de construire une API REST.

👉 Ajouter une route `/api/v1/produits` qui retournera **un tableau JSON** :

```python
PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv' },
}
```

:bulb: **Conseil** : Jetez un coup d'oeil à [`jsonify`](http://flask.pocoo.org/docs/api/#flask.json.jsonify)

Pour tester votre code, ouvrez le navigateur et allez à l'adresse suivante [`localhost:5000/api/v1/products`](http://localhost:5000/api/v1/products).

:bulb: **Conseil** : Installer l'[extension Chrome JSONView](https://chrome.google.com/webstore/detail/jsonview/chklaanhfefbnpoihckbnefhakgolnmc) pour avoir une meilleure visualisation des réponses HTTP JSON.


Versionnez et poussez votre code sur Heroku:
```bash
git add .
git commit -m "Adding /api/v1/products endpoint"

git push heroku master

heroku ps

heroku open
heroku logs -n 1000 --tail
```

Vérifiez que le nouveau point d'entrée (endpoint) `/api/v1/produits` fonctionne en **production**.

## Tests

Tester nos API sera obligatoire. Que nous utilisions ou non le TDD strict pendant le processus de développement, à un moment donné, l'application devrait avoir des tests pour chaque point d'entrée.

Nous utilisons un module externe appelé [`Flask Testing`](https://pythonhosted.org/Flask-Testing/).

![](https://pythonhosted.org/Flask-Testing/_static/flask-testing.png)

```bash
pipenv install flask-testing nose --dev
```

Maintenant, créons le répertoire `tests` et un premier fichier de test. Ce fichier de test concerne les **vues**, qui est le composant le plus proche de la réponse HTTP dans un cadre d'application MVC (nous y reviendrons plus tard) :

```bash
mkdir tests
touch tests/test_views.py
```

Ouvrez le fichier dans VS Code, lisez et copiez-collez ceci.

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

Ensuite, ouvrez le terminal et exécutez :

```bash
nosetests -s
```

👉 Votre test devrait échouer. Comment corrigez-vous le code dans `wsgi.py` pour que le test passe au vert ?

(`-s` est utile pour visualiser vos instructions `print()` ou pour utiliser `pdb`.

<details><summary markdown='span'>Voir la solution
</summary>

Il suffit d'ajouter un troisième élément au dictionnaire `PRODUCTS` !
```python
PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv'},
    3: { 'id': 3, 'name': 'Le Wagon'},
}
```

</details>

## CRUD

Félicitations :tada: ! Vous avez écrit la première route de l'API RESTful. Maintenant, il est temps d'implémenter les quatre autres points d'entrées pour implémenter correctement le CRUD sur la ressource `product`.

Pratiquez le **GitHub Flow** avec quatre branches de fonctionnalités (une par lettre de l'acronyme `CRUD`), et poussez vers `heroku` après chaque intégration de Pull Request !

### Read

Ajoutez d'abord un test pour la route `GET /api/v1/products/:id`. Ensuite, implémentez-le. Cette route récupère un seul `produit` et renvoie une représentation JSON de celui-ci (Code d'état : `200`). `:id` représente la partie dynamique de l'url faisant appel à notre api. Voici quelques exemples d'urls de requête correspondantes à notre route url : `/api/v1/products/3`, `/api/v1/products/1`, etc.

Si `:id` ne correspond à aucun id de `produit` connu dans la fausse base de données `PRODUCTS`, renvoyer un [`404`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404).
Ajoutez un scénario de test séparé pour cela.

:bulb: **Conseil** : Jetez un coup d'œil aux [Règles de Variable](http://flask.pocoo.org/docs/1.0/quickstart/#variable-rules) dans la documentation Flask.

### Delete

Ajout d'un test pour la route `DELETE /api/v1/products/:id`. Cette route va **supprimer** un seul `produit` de la fausse base de données `PRODUCTS`. Le test renvoie une réponse vide avec le code d'état [`204`] (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204).

:bulb: **Tip** : Regardez comment Flask définit une [méthode HTTP] (http://flask.pocoo.org/docs/quickstart/#http-methods) pour une route donnée.

:bulb: **Tip** : Si vous voulez faire du TDD avec cette méthode, vous aurez du mal car la base de données est simulée dans une liste constante. Allez-y et écrivez seulement le code dans wsgi.py, nous verrons plus tard comment isoler l'environnement de test et utiliser une configuration de base de données appropriée pour cela. Cette remarque sera la même pour les deux prochaines sections "Create" & "Update".

### Create

Commencez par ajouter un test pour la route `POST /api/v1/products`. Cette route **créera** un nouveau `produit` dans la fausse base de données `PRODUCTS` et renverra la représentation JSON de la ressource nouvellement créée (Status code : [`201`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201))

:bulb: **Conseil** Vous devrez peut-être utiliser la méthode [`Request.get_json`](http://flask.pocoo.org/docs/1.0/api/#flask.Request.get_json).

```python
from flask import request

request.get_json()
```

:bulb: **Conseil** Vous devrez peut-être trouver un moyen de générer des id auto-incrémentés :

```python
import itertools

# [...]

START_INDEX = len(PRODUCTS) + 1
IDENTIFIER_GENERATOR = itertools.count(START_INDEX)

# Voici comment l'utiliser :
print(next(IDENTIFIER_GENERATOR))
```

:bulb: **Conseil** Pour envoyer une requête POST **dans vos tests**, vous pouvez utiliser la méthode suivante :

```python
response = self.client.post("/api/v1/products", json={'name': 'HistoVec'})
```

:bulb: **Conseil** Voici une charge utile que vous pouvez utiliser dans Postman pour tester cette route :

```
{
    "name": "HistoVec"
}
```

N'oubliez pas de sélectionner "Raw" et "JSON" pour ajouter automatiquement un en-tête `Content-Type : application/json`. Sans cet en-tête, votre appel `request.get_json()` ignorera les données contenues dans le corps de la requête (body payload), comme indiqué dans la [documentation `Request.get_json`](http://flask.pocoo.org/docs/1.0/api/#flask.Request.get_json).

![](https://res.cloudinary.com/wagon/image/upload/v1560715014/postman-workelo_ztvqyf.png)

### Update

Enfin, ajoutez un test pour la route `PATCH /api/v1/products/:id` qui va **mettre à jour** un `produit` existant (basé sur son id). Il renvoie un `204` lorsqu'il est terminé, ou un `422` s'il y a une erreur de validation (il faut un cas de test séparé, l'erreur de validation pourrait être que le nom du produit fourni est _vide_).

### Solutions

:warning: **Veuillez ne lire les solutions qu'une fois que vous aurez essayé de mettre en œuvre tous les tests et toutes les méthodes HTTP**.

<details><summary markdown="span">Voir les tests
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
<details><summary markdown="span">Voir wsgi.py
</summary>

```python
# wsgi.py
# pylint: disable=missing-docstring
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods

import itertools

from flask import Flask, jsonify, abort, request
app = Flask(__name__)


# Préfixer le chemin de l'api en utilisant un numéro de version est vraiment important pour gérer les futures évolutions.
# De cette façon, nous pouvons continuer à proposer l'ancien service en utilisant l'url /v1 et proposer le nouveau service en utilisant /v2.
# Nous supprimerons l'api /v1 (et le code associé) lorsque tous nos utilisateurs utiliseront l'url /v2.
BASE_URL = '/api/v1'

# N'oubliez pas qu'il ne s'agit que d'une simulation de base de données très simple.
# Ces données ne sont conservées que dans la RAM : si vous redémarrez votre serveur, les modifications sont perdues.
# Ne vous inquiétez pas pour cela, notre but aujourd'hui est de comprendre l'API REST, pas de vraiment stocker des données.
PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv' },
    3: { 'id': 3, 'name': 'Le Wagon'},
}

# C'est une façon simple et naïve de générer des id consécutifs (comme le ferait une base de données).
START_INDEX = len(PRODUCTS) + 1
IDENTIFIER_GENERATOR = itertools.count(START_INDEX)


@app.route(f'{BASE_URL}/products', methods=['GET'])
def read_many_products():
    products = list(PRODUCTS.values())

   # Retourne un tuple correspondant aux arguments du constructeur flask.Response
    # Cf : https://flask.palletsprojects.com/en/1.1.x/api/?highlight=response#flask.Response
    # Par défaut, le second argument est 200 (mais nous voulons être explicites lors de l'apprentissage des concepts).
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
        abort(404)  # Aucun produit de product_id trouvé est une Erreur Non Trouvée (Not Found Error)

    # Si l'erreur est "204", le 1er argument (body) est ignoré
    # Nous pouvons mettre ce que nous voulons dans le premier argument (mais nous voulons être explicites pour rendre notre code plus maintenable).
    # '' ou None sont des valeurs couramment utilisées pour expliciter ce cas.
    #
    # L'action de suppression (méthode DELETE) n'a pas besoin de retourner l'entité puisque nous avons supprimé cette entité.
    return '', 204  # Pas de contenu


# Pas de product_id dans l'url de création (méthode POST) puisque c'est la base de données qui implémente le compteur d'id.
# Si les utilisateurs de l'api pouvaient choisir un id, cela conduirait à de nombreuses erreurs :
# - problème de compétition pour un id donné choisi par de nombreux utilisateurs.
# Comment savoir quel est l'id qui n'est pas utilisé pour le moment ?
# La base de données peut optimiser la gestion des id car elle sait comment ils sont créés.
@app.route(f'{BASE_URL}/products', methods=['POST'])
def create_one_product():
    data = request.get_json()

    if data is None:
        abort(400)  # L'absence de champ(s) nécessaire(s) est une Erreur de Requête Erronée (Bad Request Error)

    name = data.get('name')

    if name is None:
        abort(400)  # L'absence de champ nécessaire est une Erreur de Requête Erronée

    if name == '' or not isinstance(name, str):
        abort(422)  # Un mauvais format pour le champ requis est une Erreur d'Entité Non Traitable (Unprocessable Entity Error).

    next_id = next(IDENTIFIER_GENERATOR)
    PRODUCTS[next_id] = {'id' : next_id , 'name' : name }

    # Nous devons renvoyer l'entité entière pour communiquer le nouvel id à l'utilisateur de l'API.
    # De cette façon, il peut agir sur cette ressource en utilisant son id.
    #
    # Nous pourrions simplement retourner l'id, mais ce n'est pas dans l'esprit REST.
    # # N'oubliez pas : /<entity>/<entity_id> représente une entité entière.
    return jsonify(PRODUCTS[next_id]), 201  # Créé


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

    # Action de mise à jour (méthode UPDATE) pas besoin de retourner l'entité puisque nous savons ce que nous avons modifié.
    return '', 204
```

</details>

## (Optionnel) Client API REST PowerShell

Servons-nous de Powershell pour **utiliser** cette API. Gardez un onglet avec l'API en cours d'exécution afin que nous puissions exécuter des requêtes sur celle-ci :

```bash
cd ~/code/<user.github_nickname>/flask-101
FLASK_ENV=development pipenv run flask run
```

Puis ouvrez une nouvelle fenêtre de terminal. Créons un fichier script PowerShell :

```bash
cd ~/code/<user.github_nickname>/flask-101
touch consumer.ps1

# Pour exécuter le script :
powershell -ExecutionPolicy bypass ./consumer.ps1
```

Ouvrez votre fichier `consumer.ps1` dans VS Code. Nous voulons que vous implémentiez une fonction `Get-Products` pour que le code suivant interroge l'API et affiche tous les produits.

:bulb: Astuce : vous pourriez avoir besoin de la fonction [`Invoke-RestMethod`](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-6) !

```powershell
Write-Output "# Afficher tous les produits"
Get-Products | Write-Output
```

<details><summary markdown="span">Voir la solution
</summary>

```powershell
function Get-Products {
  return Invoke-RestMethod "$BASE_URL/products"
}
```

</details>

Allez-y et implémentez quatre autres méthodes utilisant l'API REST pour que le scénario suivant se déroule :

```powershell
Write-Output "# Afficher tous les produits"
Get-Products | Write-Output

Write-Output "-----------------------"

Write-Output "# Afficher un produit"
Get-Product -Id 1 | Write-Output

Write-Output "-----------------------"

Write-Output "# Mettre à jour le nom du produit 1"
Update-Product -Id 1 -Name "Skello v$(Get-Random)"
Get-Product -Id 1 | Write-Output

Write-Output "-----------------------"

Write-Output "# Ajout d'un produit"
New-Product -Name "Basecamp"

Write-Output "-----------------------"

Write-Output "# Afficher à nouveau tous les produits"
$products = Get-Products
$products | Write-Output

Write-Output "-----------------------"

$lastId = $products[-1].id
Write-Output "# Suppression du produit avec id $lastId"
Remove-Product $lastId
Write-Output "C'est fait"

Write-Output "-----------------------"

Write-Output "# Afficher tous les produits une dernière fois"
$products = Get-Products
$products | Write-Output
```


<details><summary markdown='span'>Voir la solution pour `Get-Product`
</summary>

```powershell
function Get-Product {
  param($Id)
  return Invoke-RestMethod "$BASE_URL/products/$id"
}
```

</details>

<details><summary markdown='span'>Voir la solution pour`New-Product`
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

<details><summary markdown='span'>Voir la solution pour `Update-Product`
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

<details><summary markdown='span'>Voir la solution pour `Remove-Product`
</summary>

```powershell
function Remove-Product {
  param($Id)
  return Invoke-RestMethod -Method 'DELETE' "$BASE_URL/products/$id"
}
```

</details>

## J'ai fini!

Avant de passer à l'exercice suivant, indiquons vos progrès avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 03-Back-end/01-Flask-CRUD
touch DONE.md
git add DONE.md && git commit -m "03-Back-end/01-Flask-CRUD terminé"
git push origin master
```
