# API Twitter - Containerisation

Le but de cet exercice est de poursuivre le travail des exercices des jours 3 et 4 : **API Twitter**.

Nous avons déjà mis en place une application web et une base de données, et aujourd'hui nous allons nous concentrer sur la conteneurisation de ces éléments localement, pour pouvoir développer par dessus, et exécuter nos tests à l'intérieur des conteneurs.

---

## 0. Configuration

Nous allons continuer à partir de la correction d'hier :
:point_right: [github.com/ssaunier/twitter-api](https://github.com/ssaunier/twitter-api)

Commencez par le code suivant (en utilisant la branche `docker`) :

```bash
cd ~/code/<user.github_nickname>
git clone git@github.com:ssaunier/twitter-api.git twitter-api-docker
cd twitter-api-docker
git checkout docker  # récupérer cette branche avant de changer la version distante
git remote rm origin
```

Allez sur [github.com/new](https://github.com/new) et créez un repository _public_ sur votre compte _personnel_, nommez-le `twitter-api-docker`.

```bash
git remote add origin git@github.com:<user.github_nickname>/twitter-api-docker.git
git push -u origin docker
```

---

## 1. Contrôle - ensemble d'applications non conteneurisée (⏰ rappel des jours 3 et 4).

Cet ensemble d'applications n'est pas encore conteneurisé. Mais faisons un contrôle pour vérifier que tout fonctionne. Cela sert également de rappel des deux jours précédents cet exercice !

### 1.a. Installer les dépendances

:point_right: Utilisez `pipenv` pour installer les dépendances localement, pour l'environnement de développement !

<details><summary markdown='span'>Voir la solution</summary>

```bash
pipenv install --dev
```
</details>


Nous allons également installer `python-dotenv` qui nous permet de charger les variables d'environnement que nous allons disposer dans le fichier `.env` :
```bash
pipenv install python-dotenv
```
</details>

### 1.b. Exécuter la suite de tests localement

:point_right: Assurez-vous que les tests passent localement

<details><summary markdown='span'>Voir la solution</summary>

```bash
nosetests
```

</details>

Est-ce que ça marche ? Ça ne devrait pas ! Pourquoi ?
:point_right: Essayez de réparer ça ! Vous êtes déjà passé par là hier !

<details><summary markdown='span'>Indice</summary>

Hier, nous avons utilisé un fichier `.env` pour configurer la base de données utilisée avec une variable d'environnement.

</details>

<details><summary markdown='span'>Voir la solution</summary>

Créez un fichier `.env` :

```bash
touch .env
```

Indiquez la variable `DATABASE_URL` :

```bash
# .env
DATABASE_URL="postgresql://postgres@localhost/twitter_api_flask"
```

Vous devriez toujours avoir les bases de données `twitter_api_flask` et `twitter_api_flask_test` sur votre ordinateur portable.
Maintenant, l'exécution de votre suite de tests `nosetests` devrait fonctionner !

Veuillez noter que si vous avez supprimé les bases de données **dev** et **test** hier, vous devrez les réinstaller !

Créer les bases de données Postgres **dev** et **test** (rappelez-vous que nous avons 2 bases de données distinctes pour nos environnements _developpement_ et _test_ ! Nous voulons <b>vraiment</b> les distinguer pour ne pas mélanger les données - ce qui pourrait conduire à un comportement indésirable !!

```bash
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask"
winpty psql -U postgres -c "CREATE DATABASE twitter_api_flask_test"
```

Et maintenant l'exécution de votre suite de tests `nosetests` devrait fonctionner !

</details>


### 1.c. Lancez l'application

:point_right: Assurez-vous que le serveur web peut être exécuté

<details><summary markdown='span'>Voir la solution</summary>

```bash
FLASK_ENV=development pipenv run flask run
```

</details>

:point_right: Visitez la page de documentation Swagger dans votre navigateur Web.
:point_right: Visitez également la page `/tweets`. Est-ce que tout va bien ?

<details><summary markdown='span'>Voir la solution</summary>

Allez sur<a href="http://localhost:5000/">localhost:5000</a> et <a href="http://localhost:5000/tweets">localhost:5000/tweets</a>.


Notez que si vous avez supprimé votre base de données dev hier, vous devrez exécuter à nouveau les migrations :

```bash
pipenv run python manage.py db upgrade
```

</details>


Tout fonctionne ? 🎉 Parfait ! Maintenant, adoptons une nouvelle stratégie, et faisons tout cela dans des conteneurs Docker :

- d'abord pour l'environnement _development_ (où nous exécutons l'application),
- puis pour l'environnement _test_ (où nous exécutons la suite de tests).

---

## 2. Conteneurisation - environnement de développement

Lorsque nous conteneurisons notre application, nous n'utilisons généralement plus `pipenv`. Nous préférons avoir les configurations listées dans un fichier statique (typiquement nommé `requirements.txt`) et utiliser `pip` directement pour les installer. Pourquoi ?

- Parce que nous n'avons pas besoin d'un environnement virtuel - docker est déjà, par conception, une couche de virtualisation
- Et parce que cela rend l'image docker un peu plus légère ! Et dans le développement de logiciels, plus léger c'est mieux 🙂


Nous disons " généralement ", car avec Docker, vous pouvez installer et construire à peu près n'importe quoi, donc nous _pourrions_ toujours l'utiliser. Ici, nous allons utiliser la méthode commune `requirements.txt`.

:point_right: Mettez à jour votre version de `pipenv`. :

```bash
pip install --upgrade pipenv
```

et vérifier leurs versions :

```bash
pipenv --version
```

Il doit ressembler à `2020.x`. Si ce n'est pas le cas, demandez à un TA.
Maintenant que `pipenv` est à jour, nous pouvons sauvegarder en toute sécurité les configurations dans des fichiers texte statiques.

:point_right: Exécutez les commandes suivantes :

```bash
pipenv lock --requirements > requirements.txt
```

et

```bash
pipenv lock --requirements --dev > requirements-dev.txt
```

Après les avoir exécutés, ces fichiers devraient avoir été créés dans votre dossier et remplis de dépendances python.

---

### 2.1 Dockerfile - Application Flask

Commençons par Dockeriser notre application Flask : construire une image, exécuter un conteneur et vérifier que tout va bien.

:point_right: Créer un Dockerfile vide

```bash
touch Dockerfile
```

:point_right: Copiez-collez le code suivant dans celui-ci, et sauvegardez-le

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

Comprenez-vous les instructions ? Si nous les décomposons une par une, nous voyons que :

* nous partons de l'image de Python 3.8, et plus particulièrement de sa version `alpine`. Alpine Linux est une solution Linux connue pour sa panoplie d'outils légère, et complète.
* Nous installons quelques paquets nécessaires à la construction de notre image (dont `pip`).
* Nous créons un répertoire de travail (dans les conteneurs qui seront exécutés) appelé `/code`.
* Nous copions notre dossier de code local dans le répertoire de l'espace de travail du conteneur.
* nous installons les configurations requises (en mode développement pour cet exercice)
* nous configurons quelques variables d'environnement pour que le conteneur fonctionne correctement
* Nous configurons une commande à exécuter lorsque le conteneur est lancé.

🤔 Pourquoi avons-nous `--host 0.0.0.0` dans l'instruction `CMD` ?

<details><summary markdown='span'>Voir la solution</summary>

Nous ne voulons pas seulement nous lier à l'interface `localhost` comme nous le faisions avant : nous nous lions à `0.0.0.0` pour que le conteneur soit accessible de l'extérieur (surtout accessible depuis votre hôte docker, qui est votre ordinateur portable !)

</details>


:point_right: Maintenant, construisez cette image et identifiez-la comme `twitter-api`.

<details><summary markdown='span'>Indice</summary>

Il y a un exemple pour construire et baliser une image dans la même commande, dans l'exercice précédent (`Docker-101`).

</details>

<details><summary markdown='span'>Voir la solution</summary>

```bash
docker build -t twitter-api .
```

</details>

C'est fait ? Parfait ! Maintenant, exécutons un conteneur à partir de cette image, et vérifions que notre application fonctionne.
Quelques spécifications pour cette exécution :

* nommez-la `twitter-api-docker`.
* vous devez attribuer un port hôte au port du conteneur de votre application, afin d'y accéder depuis votre hôte : ajoutez l'option `-p 5000:5000` à votre commande. De cette façon, l'application sera exécutée dans le conteneur sur le port 5000, et vous serez en mesure d'y accéder sur votre hôte (votre machine) sur le port 5000 également.
* ajoutez l'option `--rm` à votre commande `docker run` pour supprimer automatiquement le conteneur une fois qu'il aura terminé.

<details><summary markdown='span'>Indice</summary>

Vous devez utiliser `docker run` avec diverses options (le nom du conteneur, une attribution de port, l'indicateur `--rm`, le nom de l'image). Consultez `docker run --help` si nécessaire !

</details>

<details><summary markdown='span'>Voir la solution</summary>

```bash
docker run --name twitter-api -it -p 5000:5000 --rm twitter-api
```

</details>

Vous avez maintenant un conteneur en cours d'exécution.

:point_right: Vérifions [localhost:5000](http://localhost:5000/) pour voir si cela a fonctionné : est-ce que ça va ?

<details><summary markdown='span'>Voir la solution</summary>

Ça devrait ! Si ce n'est pas le cas, vérifiez la commande que vous avez exécutée et si le problème persiste, demandez à un TA !

</details>


:point_right: Que se passe-t-il avec le point d'entrée `/tweets` maintenant ? Pourquoi ?

<details><summary markdown='span'>Indice</summary>

Allez sur <a href="http://localhost:5000/tweets">localhost:5000/tweets</a> dans votre navigateur.

</details>
<details><summary markdown='span'>Voir la solution</summary>

Lorsque nous atteignons ce point d'entrée, il y a un problème. En effet, nous essayons de faire un appel à notre base de données, mais elle n'est pas configurée ! Donc notre application Flask ne trouve pas sa base de données prête pour de nouvelles connexions, et elle renvoie une erreur `sqlalchemy.exc.OperationalError`.

Nous allons donc configurer notre base de données - et la dockeriser en même temps pour faciliter le flux de développement et de test !

</details>

:point_right: Appuyez sur `CTRL-C` pour arrêter votre conteneur (et aussi le supprimer - puisque vous avez passé l'indicateur `--rm` dans votre commande `docker run` !)

---

### 2.2 Conteneuriser notre service de base de données

Nous devons ajouter une base de données et nous allons utiliser `docker-compose` pour cela.
Nous avons vu dans le cours que `docker-compose` était utilisé pour définir de multiples services, et faire apparaître l'ensemble d'applications avec la commande `docker-compose up`.


:point_right: Encore une fois, commençons petit, et créons un fichier vide `docker-compose.yml`.

```bash
touch docker-compose.yml
```

:point_right: Copiez et collez le contenu suivant dedans : ici nous définissons un seul service : `web`, pour notre application Flask. Il est principalement basé sur le Dockerfile créé précédemment, via le mot-clé `build`.

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

:point_right: Assembler l'ensemble d'applications en exécutant :

```bash
docker-compose up
```

Il vous sera probablement demandé de partager certains fichiers avec `docker-compose` (car il a besoin d'accéder au code de votre application pour l'exécuter) : cliquez sur "accepter".

:point_right: Allez sur [localhost:5000](http://localhost:5000) et [localhost:5000/tweets](http://localhost:5000/tweets).

Oui, toujours les mêmes erreurs que précédemment lorsque l'application essaie d'atteindre la base de données ! Ici, nous n'avons pas changé grand chose, car nous n'avons qu'un seul service (web) dans notre fichier `docker-compose.yml`, qui repose sur notre `Dockerfile` défini précédemment.
Donc, d'une certaine manière, nous n'avons changé - jusqu'à présent - que la façon de faire fonctionner notre conteneur ! Mais nous allons faire plus maintenant ...

:point_right: Vous pouvez maintenant quitter votre conteneur en utilisant `CTRL-C`


Rappelez-vous que l'idée est d'y ajouter un service de base de données. Ajoutons donc notre base de données Postgres ! Pour cela, nous allons faire ce qui suit :

a. mettre à jour notre `Dockerfile` en conséquence
b. ajuster notre `docker-compose.yml` pour prendre en compte le service de base de données


#### 2.2.a Mise à jour de notre Dockerfile existant
:point_right: Mettez à jour votre `Dockerfile` avec ce qui suit :

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

Notez que nous avons simplifié notre `Dockerfile` :

- nous avons supprimé certaines variables d'environnement
- nous supprimons l'instruction `CMD` que le conteneur doit exécuter

... mais ne vous inquiétez pas, nous allons les utiliser dans le fichier `docker-compose.yml` - elles n'ont pas "disparu" !

Nous avons également installé `bash` dans notre image, car nous aurons besoin de lancer un script (peut-être avez-vous remarqué un script `wait-for-it.sh` dans le repo : ce n'est pas une erreur, il est là exprès. Nous en parlerons dans le prochain paragraphe).


#### 2.2.b Ajouter un service de base de données à notre docker-compose.yml
:point_right: Mettez à jour votre fichier `docker-compose.yml` avec ce qui suit :

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

L'idée ici est de migrer ce qui est _configurable_ du `Dockerfile` vers le `docker-compose.yml`, et de ne garder que ce qui est statique (comme les paquets, la définition des dépendances) dans le `Dockerfile`.

Nous avons maintenant deux services : `web` et `db`.

👀 Regardons de plus près le `db` :

* Ce service est basé sur l'image `postgres` (accessible sur le Docker Hub)
* Nous nommons le conteneur qui sera exécuté `db` - pour plus de simplicité.
* Nous spécifions des variables d'environnement - que nous savons être obligatoires pour l'image `postgres` !
* Remarquez le mot-clé `volumes` ? En quelques mots - juste pour présenter le concept :
  * Afin de pouvoir sauvegarder ( faire persister ) des données et aussi de partager des données entre conteneurs, Docker a créé le concept de **volumes**.
  * Les volumes sont tout simplement des répertoires (ou des fichiers) qui vivent "à l'extérieur" du conteneur, sur la machine hôte (dans notre cas, votre ordinateur portable).
  * Depuis le conteneur, le volume agit comme un dossier que vous pouvez utiliser pour stocker et récupérer des données. Il s'agit simplement d'un _point de fixation_ vers un répertoire sur l'hôte.
  * En d'autres termes : ici le répertoire `/var/lib/postgresql/data/` du conteneur `db` "pointe vers" le volume `postgres_data` sur votre hôte. Toutes les données de la base de données se retrouveront dans ce volume.
  * **Mais pourquoi ?** 🤔 Eh bien si vous arrêtez et supprimez votre conteneur, vous ne voulez pas que ses données persistantes soient également perdues. Elles sont donc conservées en sécurité sur l'hôte docker, et vous pouvez rattacher le volume à tout nouveau conteneur que vous souhaitez exécuter !

👀 Regardons de plus près le `web` :

* Ce service est basé sur une image personnalisée - renseignée dans notre Dockerfile
* Nous nommons le conteneur qui sera lancé `web` - pour plus de simplicité.
* Il ["dépend du"](https://docs.docker.com/compose/compose-file/#depends_on) service `db` : les services seront démarrés dans l'ordre des dépendances. Nous avons besoin que notre base de données (`db`) soit opérationnelle et prête pour de nouvelles connexions avant de lancer notre application Flask (`web`) !
* Afin de s'assurer que notre conteneur de dépendances (c'est-à-dire notre base de données) fonctionne, nous avons besoin d'une sorte de "contrôle". C'est le but exact du script `wait-for-it.sh` ! Vous pouvez en lire plus [ici](https://docs.docker.com/compose/startup-order/) si vous êtes intéressés. Le conteneur `web` exécute ce script, qui **lui fera attendre que la base de données soit opérationnelle et accepte les connexions**, avant de lancer l'application flask (`command : ["./wait-for-it.sh", "db:5432", "--", "flask", "run"]`).

#### 2.2.c Opérations initiales

Effectuons quelques opérations initiales pour configurer les conteneurs et les bases de données dont nous aurons besoin :

:point_right: Assurez-vous d'avoir des _"terminaisons de ligne Unix"_ pour votre script `wait-for-it.sh` : ouvrez-le avec **Sublime Text**, et cliquez sur `View` > `Line Endings` > `Unix`, puis enregistrez-le ⚠️. De cette façon, il sera correctement interprété dans vos conteneurs.

:point_right: Assemblez les applications, exécutez les conteneurs en arrière-plan, et recompilez l'image pour `web` : ``docker-compose up -d --build`` 🛠

:point_right: Vérifiez qu'il a bien lancé votre ensemble d'applications technologique : exécutez `docker ps` pour voir les conteneurs qui sont exécutés sur votre hôte.

<details><summary markdown='span'>Voir la solution</summary>

Vous devriez voir vos conteneurs `web` et `db` fonctionner.

</details>

:point_right: Créons maintenant nos bases de données pour le **développement** et les **tests** :
* connectez-vous au conteneur `db` :
```bash
docker exec -it db psql -U postgres
```
* créez des bases de données pour les environnements de développement et de test : dans l'invite `psql`, tapez :
  * `CREATE DATABASE twitter_api_flask;`
  * `CREATE DATABASE twitter_api_flask_test;`
  * Quittez l'invite `psql` : `\q` + **Entrer**

:point_right: Finalement, exécutez vos migrations: ```docker-compose run web python manage.py db upgrade```

<details><summary markdown='span'>Voir la solution</summary>

Vous devriez obtenir un résultat comme celui-ci :

```bash
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 3812f6776f12, Create tweets table
```

</details>

⚠️ Notez que ce n'est pas quelque chose que nous automatisons nécessairement pour les environnements de **développement** et de **test** car nous voulons pouvoir jouer avec les migrations manuellement. Mais pour le **CI** et la **production**, ces commandes seraient scriptées pour être exécutées de manière programmée. Vous n'auriez pas à saisir manuellement la commande et à l'exécuter !

Maintenant, nos points d'entrée sont fixés 🍾 :

:point_right: Consultez la [documentation Swagger](http://localhost:5000) et l'index [`/tweets`] (http://localhost:5000/tweets).

<details><summary markdown='span'>Voir la solution</summary>

Vous devriez voir : la documentation Swagger comme d'habitude pour le premier point d'entrée, et une liste vide pour le second point d'entrée (vous n'avez pas encore de données !).

</details>

Quelques détails sur ce qui vient de se passer :

* Appeler `docker-compose up` lancera `db` et `web`.
* `web` dépend de `db` qui doit être opérationnel et en bonne santé. Les commandes `docker-compose up` s'en assurent en exécutant un script de contrôle : `wait-for-it.sh`
* une fois que `db` est opérationnel et sain, `web` peut être lancé.
* notre base de données est sécurisée par un utilisateur/mot de passe, que Flask connaît (nous le passons par la variable d'environnement `DATABASE_URL` que vous connaissez déjà depuis hier)

⚠️ Notez que nous avons **hard-codé** un mot de passe fictif **de la base de données** ("_password_") ici. Nous ferions bien sûr mieux de passer en direct 💪 (en utilisant par exemple une variable d'environnement, ou la clé d'un coffre-fort). Mais n'oubliez pas que nous industrialisons notre ensemble d'applications progressivement : bien sûr, toutes nos évolutions ne peuvent pas être parfaites, mais nous visons quelque chose de robuste au final !

---

### 2.3 Interagir en utilisant des données

#### 2.3.a Ajouter des données en utilisant Postman !

* Ouvrez votre application Postman

* Créez des données : faites une requête `POST` vers `http://localhost:5000/tweets`, avec un corps JSON :

```json
{
    "text": "Hey, c'est un nouveau tweet!"
}
```

* Créez un autre tweet (utilisez le texte que vous voulez, et envoyez la demande)

#### 2.3.b Vérifiez vos données en utilisant l'API

Maintenant que vous avez des données dans votre base de données, vérifiez la liste des tweets via le [point d'entrée `GET /tweets`](http://localhost:5000/tweets). Notez que vous pouvez faire cela dans Postman (en configurant vous-même la requête `GET`), ou dans votre navigateur web ! C'est exactement la même chose, les deux utiliseront votre API Flask de la même manière !

#### 2.3.c Vérifier vos données en utilisant directement la base de données

Une autre façon de voir les données serait de se connecter directement à la base de données **de développement**.
C'est pratique car vous avez un conteneur pour cela.

:point_right: Comme nous l'avons fait dans l'exercice précédent, exécutez :

```
docker exec -it db psql -U postgres twitter_api_flask
```

Vous obtiendrez une invite `psql` où vous pourrez écrire du SQL.

* 💡 **Astuce** En tapant ``d+` et en appuyant sur **Entrer**, vous obtiendrez la liste des tables disponibles dans la base de données.

<details><summary markdown='span'>Voir la solution</summary>

Vous devriez obtenir un résultat comme celui-ci :

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

* L'exécution de `SELECT * FROM tweets;` affichera toutes vos données.

<details><summary markdown='span'>Voir la solution</summary>

Vous devriez obtenir un résultat comme celui-ci - avec vos propres tweets :

```bash
twitter_api_flask=# SELECT * FROM tweets;
 id |           text            |         created_at
----+---------------------------+----------------------------
  1 | this is a tweet !!!       | 2020-12-06 18:53:59.493008
  2 | this is another tweet !!! | 2020-12-06 18:54:15.282337
(2 rows)
```

</details>

* Quittez l'invite `psql` : `\q` + **Entrer**

---

## 3. Containerisation - environnement de test

Ajustons notre `docker-compose.yml` pour avoir une commande à tester localement.
Ajoutez-y le paragraphe suivant :

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

👉 Exécutez `docker-compose up test` pour lancer la suite de tests localement.

Vos tests devraient tous passer :

<details><summary markdown='span'>Voir la solution</summary>

Vous devriez obtenir un résultat comme celui-ci :

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

* vous n'avez pas changé de code Python, et cela a fonctionné avec la configuration locale au début de l'exercice
* donc la seule raison pour laquelle il pourrait échouer serait basée sur docker ! Si vous avez un problème avec votre suite de test, veuillez demander à un TA !


🎉 C'est tout pour notre configuration locale : nous avons maintenant un moyen standard de **développer** notre application et d'**exécuter notre suite de tests** sur celle-ci.
Cela peut ne pas sembler très utile mais croyez-nous : **ça l'est** !
Avec ce type de configuration :

* vous n'aurez aucun problème de compatibilité
* vous serez en mesure de développer et de tester de manière standardisée
* vous pourrez contribuer avec d'autres développeurs sur la même configuration (qui est maintenant très facile à lancer).

---

## J'ai fini! 🎉

Nettoyez votre hôte docker en exécutant ``docker-compose down -v`` pour arrêter et supprimer les conteneurs, et supprimer les volumes utilisés ci-dessus.

Et c'est tout pour cet exercice ! Avant de passer au prochain exercice (`03-Background-Jobs`), sauvergardez vos progrès avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 05-Docker/02-Twitter-API
touch DONE.md
git add DONE.md && git commit -m "05-Docker/02-Twitter-API"
git push origin master
```
