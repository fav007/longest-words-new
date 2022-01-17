# Programme d'arrière-plan

Pour cet exercice, nous n'utiliserons **pas** Docker et nous travaillerons sur des programmes en arrière-plan sur notre **structure locale** (comme nous l'avons fait les jours précédents). En effet, il est plus facile de traiter ce sujet sans la complexité de la conteneurisation dans un premier temps.

---

Lors de la création d'une API, il arrive que le traitement à effectuer dans le contrôleur recevant une requête HTTP prenne beaucoup de temps (plus d'une seconde). Il peut s'agir de l'envoi d'un courrier électronique (SMTP est un protocole lent), de la mise à jour de nombreux enregistrements dans la base de données, de l'appel d'une autre API qui peut mettre un certain temps à répondre, etc.

Nous utiliserons le projet [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) qui fournit une **file de tâches distribuées** pour exécuter ces tâches en arrière-plan. Voici un diagramme de séquence de ce que nous voulons faire :

![](https://res.cloudinary.com/wagon/image/upload/v1560714606/celery_thtll5.png)

Essayons de mettre cela en place dans notre application Flask.

## Configuration

Une fois encore, nous pouvons utiliser notre application produit pour tester le paquet `celery` :

```bash
cd ~/code/<user.github_nickname>/flask-with-sqlalchemy
```

Assurez-vous que votre `git status` est propre et n'oubliez pas de travailler dans une branche ! N'hésitez pas à demander de l'aide à un TA.

```bash
# Assurez-vous que `git status` est propre.
git checkout master
git checkout -b celery
```

Avant de vous lancer dans le code, veuillez lire l'[Introduction à Celery](http://docs.celeryproject.org/en/latest/getting-started/introduction.html) de la documentation pour avoir un aperçu de ce qu'est Celery et de son fonctionnement.

### Redis

Nous utiliserons [**Redis**](https://redis.io/) pour le back-end de Celery. Il s'agit d'un service externe qui est nécessaire et qui sera installé à côté du service Postgresql.

<details><summary markdown='span'><b>Installer et démarrer Redis sous Windows</b> - cliquez sur la flèche</summary>

Veuillez <a href="https://github.com/MicrosoftArchive/redis/releases">télécharger</a> le dernier Redis compilé pour Windows (recherchez le fichier `.zip`). Extrayez l'archive téléchargée dans `C:\Users\Le Wagon\code\redis`.

Vous êtes maintenant prêt à démarrer le serveur Redis en arrière-plan. Ouvrez un autre onglet du Terminal et exécutez :

```bash
cd ~/code/redis
./redis-server.exe
```

</details>

<details><summary markdown='span'><b>Installer et démarrer Redis sur MacOS</b> - cliquez sur la flèche</summary>

Nous utilisons `brew` comme gestionnaire de paquets, et nous vous conseillons de faire de même.

* Si vous n'avez pas encore `brew`, téléchargez-le en exécutant :

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

* Ensuite, vous pouvez installer redis

```bash
brew install redis
```

* Et lancez-le dans une fenêtre de terminal séparée (ou tab : `ctrl+T` dans votre terminal) :

```bash
redis-server
```
</details>

### Celery

Maintenant que le service Redis fonctionne en arrière-plan, nous pouvons passer au code. Tout d'abord, installez Celery et sa dépendance Redis :

```bash
pipenv install celery[redis]
```

Ouvrez le fichier `.env` et ajoutez une nouvelle variable d'environnement :

```bash
# .env
REDIS_URL="redis://localhost:6379"  # Nouvelle ligne !
```

Nous devons également préparer la configuration de l'application avec deux nouvelles variables pour les backends Celery Broker et Result. Nous utiliserons `REDIS_URL` pour les deux :

```python
# config.py
import os

class Config(object):
    # [...]
    CELERY_RESULT_BACKEND = os.environ['REDIS_URL']  # Nouvelle ligne !
    CELERY_BROKER_URL = os.environ['REDIS_URL']  # Nouvelle ligne !
```

Ensuite, en suivant l'article de la [documentation Flask sur Celery](http://flask.pocoo.org/docs/1.0/patterns/celery/), nous découvrons que nous devons créer une méthode **factory** pour Celery.

```bash
touch tasks.py
```

```python
# tasks.py
# pylint: disable=missing-docstring

from celery import Celery
from wsgi import app

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)
```

Nous venons de créer le boilerplate pour exécuter le service Celery. Aucune tâche d'arrière-plan n'a encore été définie. Néanmoins, nous pouvons lancer le service pour nous assurer que tout fonctionne correctement :

```bash
pipenv run celery -A tasks.celery worker --loglevel=INFO --pool=solo
```

Vous devriez voir quelque chose de ce genre :

```
[2019-04-04 15:42:38,497: INFO/MainProcess] Connected to redis://localhost:6379//
[2019-04-04 15:42:38,508: INFO/MainProcess] mingle: searching for neighbors
[2019-04-04 15:42:39,529: INFO/MainProcess] mingle: all alone
[2019-04-04 15:42:39,543: INFO/MainProcess] celery@Macbook ready.
```

Si non, vérifiez que le serveur Redis fonctionne ! Si vous n'arrivez pas à le faire fonctionner, demandez à votre buddy ou à un TA !

## Ajout d'une toute première tâche

Vous pouvez maintenant arrêter le processus Celery en pressant `Ctrl` + `C` deux fois.

Il est temps d'ajouter une première tâche. Retournez dans VS Code dans le fichier `tasks.py` et au bas de ce fichier, définissez une fonction. Cette fonction doit être une tâche longue puisqu'elle va être exécutée par le programme (worker). Pour en simuler une, nous pouvons utiliser [`time.sleep()`](https://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python).

Nous allons accompagner cette tâche avec `@celery.task()` pour que le processus Celery en soit conscient.

```python
# tasks.py

# [...]

@celery.task()
def very_slow_add(a, b):
    import time
    time.sleep(3)
    return a + b
```

Nous venons d'implémenter une méthode `very_slow_add(a, b)`. Testons-la !

Relancez le programme Celery avec :

```bash
pipenv run celery -A tasks.celery worker --loglevel=INFO --pool=solo
```

Ouvrez une autre fenêtre de terminal et lancez un Flask Shell :

```bash
pipenv run flask shell
```

Et maintenant nous allons **mettre en file d'attente** notre programme d'arrère-plan !

```python
from tasks import very_slow_add
job = very_slow_add.delay(5, 7)
response = job.wait()
```

La `réponse` devrait prendre exactement 3 secondes. Regardez les registres du programme Celery, vous devriez voir le programme être mis en file d'attente, être traité, et ensuite retourner un résultat !

```bash
[... INFO/MainProcess] Received task: tasks.very_slow_add[7da941c2-...]
[... INFO/ForkPoolWorker-2] Task tasks.very_slow_add[7da941c2-...] succeeded in 3.00225233499998s: 12
```

Voilà, c'est fait ! Vous savez maintenant comment créer des fonctions qui seront exécutées par Celery en tant que tâches, et les mettre en file d'attente ! Vous pouvez les ajouter au fichier `wsgi.py` dans la méthode qui reçoit les requêtes HTTP pour votre API. Elles ne bloqueront pas l'exécution du déroulement et garderont vos points d'entrée API rapides :

```python
# wsgi.py

# [...]
from schemas import many_product_schema

@app.route(f'{BASE_URL}/products', methods=['GET'])
def get_many_product():
    from tasks import very_slow_add
    very_slow_add.delay(1, 2) # Cela pousse une tâche vers Celery et ne bloque pas.

    products = db.session.query(Product).all() # SQLAlchemy request => 'SELECT * FROM products'
    return many_product_schema.jsonify(products), 200

```

Sortez de votre précédent `flask shell` en tapant `quit()` ou `exit()` puis en appuyant sur la touche `<ENTER>`.
Ensuite, lancez le serveur Flask :

```bash
FLASK_ENV=development pipenv run flask run
```

Allez sur [`http://localhost:5000/api/v1/products`](http://localhost:5000/api/v1/products) et regardez les registres de Celery. Pouvez-vous voir que le programme est mis en file d'attente sans ralentir votre point d'entrée API ?

## Déploiement

Nous avons presque terminé avec Celery, un dernier point que nous devons couvrir est le **déploiement**. Cela peut devenir un peu confus, récapitulons ce dont nous avons besoin :

1. Nous avons besoin que Redis soit opérationnel sur l'hôte (donc nous en avons besoin aussi sur Heroku !)
2. Nous avons besoin d'exécuter le `celery` dans un processus séparé (même chose pour Heroku !)
3. Nous devons configurer l'application avec des variables d'environnement pour que Celery trouve Redis.

Pour le point `1.`, nous devons ajouter une **extension** (add-on) sur notre application Heroku. Nous allons utiliser [Heroku Redis](https://elements.heroku.com/addons/heroku-redis) qui est gratuit jusqu'à 25M, assez pour bricoler.


Afin d'utiliser Heroku Redis, Heroku vous demande de `vérifier votre compte` en `entrant une carte de crédit` comme mentionné [ici](https://devcenter.heroku.com/articles/account-verification#how-to-verify-your-heroku-account).
Pas de panique, **vous ne serez pas débité**.
Nous allons `supprimer votre carte de crédit` de votre compte Heroku `ensemble à la fin de cet exercice`.

```bash
heroku addons:create heroku-redis:hobby-dev
```

Cela résoudra automatiquement le point `3.`, ce que nous pouvons vérifier avec :

```bash
heroku config
```

Pouvez-vous voir le `REDIS_URL` sur Heroku ?

Pour résoudre le point `2.`, nous devons mettre à jour le `Procfile` avec une **nouvelle ligne** :

```yaml
# Procfile

[...]

worker: celery -A tasks.celery worker --loglevel=INFO
```

Le Procfile aura maintenant 3 lignes :

- une ligne `web` pour lancer l'application flask
- une ligne `release` pour mettre automatiquement à jour la base de données à chaque déploiement
- une ligne `worker` pour lancer Celery !

Il est maintenant temps de pousser notre branche sur Heroku :

```bash
git add .
git commit -m "Ajout de Celery et configuration de Heroku"
git push heroku celery:master
```

Par défaut, Heroku démarre seulement un [dyno](https://www.heroku.com/dynos) pour le processus `web`. Nous devons lui dire de démarrer également un processus `worker` :

```bash
heroku ps:scale worker=1 web=1
```

Vous pouvez vérifier que cela a été activé sur votre [tableau de bord Heroku](https://dashboard.heroku.com/apps) en `sélectionnant votre application`. Vous devriez voir quelque chose de ce genre :

![](https://res.cloudinary.com/wagon/image/upload/v1560714714/heroku_celery_nr43t1.png)

Observons notre application dans la nature.

```bash
heroku open
```

Lancez ensuite la commande suivante pour observer le journal (logs) de production :

```bash
heroku logs --tail
```

Et allez dans `/api/v1/produits`. Observez votre registre. Pouvez-vous voir la tâche mise en file d'attente et le résultat en cours de traitement ? Excellent travail :clap: !

## Retirer votre carte de crédit de Heroku

Il est maintenant temps de `supprimer votre carte de crédit` de votre compte Heroku !

Affichez vos applications afin de `supprimer la dernière application` (**qui utilise 2 dynos**) :

```bash
heroku apps  # Afficher les applications créées
# === <your_mail> Apps
# <app_name_1> (eu)
# <app_name_2> (eu)
# <app_name_3> (eu)
# <app_name_4> (eu)
# <app_name_5> (eu)
```

Une fois que vous avez reconnu la `dernière`, utilisez son nom pour la `supprimer` :

```bash
heroku apps:destroy <nom_derniere_application>
# !    WARNING: This will delete <nom_derniere_application> including all add-ons.
# !    To proceed, type <nom_derniere_application> or re-run this command with
# !    --confirm <nom_derniere_application>

<nom_derniere_application>  # Type <nom_derniere_application> and press <Enter>
# Destroying <nom_derniere_application> (including all add-ons)... done
```

Si vous ne vous souvenez pas du nom de votre dernière application, allez sur votre [tableau de bord Heroku](https://dashboard.heroku.com/apps) et cliquez sur chaque application pour trouver `l'application avec 2 dyno` (avec un `celery worker`).

Ou vous pouvez simplement `supprimer toutes vos applications`.

Il suffit d'aller [ici](https://dashboard.heroku.com/account/billing) et de cliquer sur le bouton rouge `Supprimer la carte de crédit`.
