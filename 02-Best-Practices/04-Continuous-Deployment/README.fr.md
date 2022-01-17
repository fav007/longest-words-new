# Déploiement Continu

Le graal du DevOps que les équipes veulent atteindre est le **Déploiement Continu**. L'idée est de configurer votre environnement d'hébergement de telle sorte que chaque changement dans `master` qui donne lieu à un build vert sur le moteur de production _puisse être_ et _sera_ pushé en production dès que possible.

Dans cet exercice, nous allons mettre en place un [**PaaS**](https://en.wikipedia.org/wiki/Platform_as_a_service) pour héberger notre jeu de mots le plus long.

## Serveur HTTP

Avant de pousser notre code chez un hébergeur, nous aimerions pouvoir interagir avec lui. La façon la plus simple de le faire est d'encapsuler le jeu autour d'un petit serveur HTTP.

Nous allons construire une page simple qui affichera la grille aléatoire. En dessous de cette grille, un formulaire avec un champ input pour taper un mot, et un bouton submit.

En cliquant sur le bouton, le formulaire sera envoyé et la page sera rechargée pour afficher les résultats.

![](https://res.cloudinary.com/wagon/image/upload/v1560714935/longest-word-mockup_mwtd3d.png)

Retournez à votre code, et créez une branche pour commencer à travailler sur cette fonctionnalité.

```bash
cd ~/code/<user.github_nickname>/longest-word

git status # Est-ce que c'est vide ?
git checkout master
git pull origin master
git branch -d dictionary-api
git checkout -b http-server
```

Nous allons utiliser [Flask](http://flask.pocoo.org/), un micro-framework permettant de créer rapidement des applications web.

```bash
pipenv install flask
touch wsgi.py
code .
```

Ouvrez le fichier `wsgi.py` et copiez-collez le code suivant :

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello world!"
```

Vous pouvez commencer cette application Flask très basique avec :

```bash
FLASK_ENV=development pipenv run flask run
```

Ouvrez votre navigateur et allez sur [localhost:5000](http://localhost:5000/). Est-ce que cela fonctionne, est-ce que vous obtenez "Hello World" comme réponse texte du serveur ? Si ce n'est pas le cas, appelez un professeur.

Le but de cet exercice n'est pas d'implémenter une petite application, nous parlerons de Flask en détail dans le cours de demain. Alors construisons ensemble notre application :

```bash
mkdir static
touch static/style.css
mkdir templates
touch templates/home.html
```

Nous venons de créer une feuille de style CSS et le template HTML pour la page d'accueil. Ajoutons la logique métier dans `wsgi.py` :

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, render_template
from game import Game

app = Flask(__name__)

@app.route('/')
def home():
    game = Game()
    return render_template('home.html', grid=game.grid)
```

Dans le code ci-dessus, nous initialisons une nouvelle instance de `Game` pour générer une grille. Nous passons cette grille comme variable locale au modèle `home.html`, afin de pouvoir l'utiliser dans la vue.
Comme la logique de `Game` ne s'occupe que des lettres majuscules, nous avons décidé de forcer le contenu de `<input name="word">` en majuscules en utilisant du JavaScript.
Ajoutons ce code dans `templates/home.html` :

```html
<!-- templates/home.html -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf8" />
    <title>Longest Word</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <h1>Longest Word</h1>
    <div>
      {% for letter in grid %}
        <span class="letter">{{ letter }}</span>
      {% endfor %}
    </div>
    <form action="/check" id="form" method="post">
      <input type="hidden" name="grid" value="{{ ''.join(grid) }}">
      <input type="text" name="word" onkeyup="this.value = this.value.toUpperCase();">
      <button>Check!</button>
    </form>
  </body>
</html>
```

Nous vous donnons également quelques lignes de CSS à ajouter dans `static/style.css` :

```css
/* static/style.css */
body {
  font-family: sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
.letter {
  border: 1px solid #999;
  padding: 8px 6px;
  width: 24px;
  display: inline-block;
  text-align: center;
  background-color: #333;
  color: #eee;
}
#form, #results {
  margin: 1em 0;
}
.valid {
  color: green;
}
.invalid {
  color: red;
}
```

Ouf ! Maintenant essayons ceci, allez dans votre navigateur et rechargez la page. Pouvez-vous voir la grille avec un formulaire ? C'est génial !

Si vous essayez de jouer, vous obtiendrez une erreur. C'est parce que nous n'avons pas encore implémenté le endpoint `/check` (celui où le formulaire est soumis).
Faisons-le :

```python
# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, render_template, request

# [...]

@app.route('/check', methods=["POST"])
def check():
    game = Game()
    game.grid = list(request.form['grid'])
    word = request.form['word']
    is_valid = game.is_valid(word)
    return render_template('check.html', is_valid=is_valid, grid=game.grid, word=word)
```

L'idée est de récupérer la grille (en tant que champ caché) et le mot (celui que vous avez tapé dans l'input) de la requête précédente, puis créons une instance de `Game` et vérifions si le mot est valide. Nous renvoyons ces informations à la vue `check.html` qui sera utilisée pour afficher les résultats.

💡 Nous devons en fait passer la grille dans la requête `POST` car HTTP est **sans état**.

```bash
touch templates/check.html
```

```html
<!-- templates/check.html -->
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf8" />
    <title>Longest Word</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  </head>
  <body>
    <h1>Longest Word</h1>
    <h2>Result</h2>
    <div>
      {% for letter in grid %}
        <span class="letter">{{ letter }}</span>
      {% endfor %}
    </div>
    <div id="results">
      Your word: <strong>{{ word }}</strong>.
      {% if is_valid %}
        <span class="valid">Congrats, it's valid!</span>
      {% else %}
        <span class="invalid">Sorry, it's invalid...</span>
      {% endif %}
    </div>
    <div>
      <a href="/">New game</a>
    </div>
  </body>
</html>
```

Voilà, c'est fait ! Votre application devrait fonctionner correctement. Il est temps de versionner, pousser et _ouvrir une Pull Request_ sur GitHub :

```bash
git add .
git commit -m "Small web app wrapper around the Game"
git push origin http-server
# rendez-vous sur github.com pour ouvrir une Pull Request !
```

## Installation de Heroku

Avant de pouvoir déployer notre petite application web, nous devons créer un compte Heroku. Si vous en avez déjà un, vous pouvez l'utiliser. Sinon, [inscrivez-vous](https://signup.heroku.com/) (c'est gratuit pour essayer). Mettez une adresse e-mail à laquelle vous pouvez accéder facilement car vous devrez cliquer sur un lien de confirmation.

Une fois votre compte créé, si vous n'avez pas encore installé l'outil de ligne de commande d'Heroku, il est temps de le faire!  Allez sur [cette page Heroku Dev Center](https://devcenter.heroku.com/articles/getting-started-with-python#set-up), téléchargez le CLI et installez-le. Ne laissez pas l'option `Git` cochée dans les composants à installer car vous l'avez déjà ! Laissez les options `Heroku CLI` et `Set PATH...` cochées.

Ouvrez Git Bash et connectez-vous :

```bash
heroku update
heroku login
```

S'il y a un problème, vous pouvez [avoir besoin d'utiliser `winpty`](https://github.com/heroku/cli/issues/84)

Nous pouvons maintenant préparer notre application à être exécutée sur Heroku. Il ne manque qu'une petite chose : nous devons indiquer à Heroku comment **démarrer** notre application. Pour ce faire, nous devons créer un fichier spécial :

```bash
git status # Est-ce que c'est vide ?
git checkout master
git pull origin master

# Travaillons sur `master` pour ce cas précis, pas sur une branche.
touch Procfile
```

Et mettez ce qui suit dans le `Procfile` :

```bash
# Procfile
web: gunicorn wsgi:app
```

Nous ne pouvons pas utiliser la commande normale `flask run` en production, nous devons utiliser [`gunicorn`](https://devcenter.heroku.com/articles/python-gunicorn) qui doit encore être ajouté au `Pipfile` :

```bash
pipenv install gunicorn
git add .
git commit -m "Add Procfile to prepare Heroku deployment"
git push origin master
```

Notre application est maintenant prête à être déployée sur Heroku. Tout d'abord, nous devons créer une application distante qui approvisionnera un [dyno](https://www.heroku.com/dynos) dans le cloud.

```bash
heroku create --region=eu # Nous voulons utiliser le datacenter de l'UE pour être plus proche de nous.
git remote -v
# Vous voyez ? Il n'y a pas que `origin` comme remote maintenant !
git push heroku master # C'est d'ailleurs la commande de déploiement !

# Une fois que notre application est déployée, nous pouvons l'ouvrir sur Chrome avec :
heroku open
```

Tout va bien ? Si non, vous pouvez débugger la production avec `heroku logs --tail` et bien sûr demander à un TA.

## Déploiement continu

Nous y sommes presque. Voici un rapide récapitulatif :

1. Notre code est sur GitHub
1. Nous avons mis en place l'Intégration Continue grâce à Github Actions
1. Chaque versionnage (dans `master` ou une branche de fonctionnalité) déclenche une compilation de Github Actions
1. Le statut d'une Pull Request est mis à jour par Github Actions et donne le contexte à l'examinateur.
1. Nous devons toujours **manuellement** exécuter la commande `git push heroku master` pour déployer

Automatisons cette dernière partie et atteignons le Graal !

Allez sur [dashboard.heroku.com](https://dashboard.heroku.com). Cliquez sur votre application hébergeant `longest-word`.

 Allez sur l'onglet `Deploy` (le troisième). Si vous scrollez vers le bas, vous verrez une section "Deployment method". Cliquez sur `GitHub`. Scrollez vers le bas et cliquez sur le bouton violet `Connect to GitHub`.

 Vous pourrez alors sélectionner le repository `longest-word` et le **connecter** à cette application Heroku.

 Après cette étape, si vous descendez encore un peu, vous trouverez la section `Automatic deploys`. C'est là que vous pourrez cocher la case `Wait for CI to pass before deploy`, sélectionnez `master` (par défaut) dans la liste déroulante, et cliquer sur le bouton noir **Enable Automatic Deploys**.

 Voilà, c'est fait ! Mais est-ce que ça marche vraiment ?

 ---

 Testons !

 Faisons un changement très simple. Nous allons mettre à jour la couleur de fond des lettres de la grille.

```bash
git checkout -b yellow-letter
```

```css
/* static/style.css */
/* [...] */
.letter {
  /* [...] */
  background-color: #FFEB3B;
  color: #666;
}
```

Vous pouvez tester localement avec `FLASK_ENV=development pipenv run flask run`. Si les changements CSS ne sont pas pris en compte, faites un[force-refresh](https://superuser.com/a/89811).

La couleur vous convient ? Vous pouvez versionner :

```bash
git add static/style.css
git commit -m "Change letter grid background-color to yellow"
git push origin yellow-letter
```

Allez sur github.com, créez une Pull Request et attendez que Github Actions la passe au vert.

Pendant que Github Actions travaille, ouvrez un autre onglet Chrome et retournez sur [dashboard.heroku.com](https://dashboard.heroku.com), puis sélectionnez votre projet `longest-word`.
Regardez l'onglet `Activity` (le 5ème) de votre application Heroku pour visualiser votre flux d'activité. Laissez cet onglet ouvert.

Revenez sur la Pull Request, et dès qu'elle est verte, mergez-la vers `master`. Retournez sur l'onglet Heroku, et attendez ~1 minute (dans GitHub vous pouvez jeter un coup d'oeil à la page `Commits` et voir que le dernier merge de versionnage est en train d'être testé par Github Actions, grâce au petit point orange).

Avez-vous réussi ? Avez-vous pu obtenir une compilation/un déploiement automatique sur Heroku grâce à un feu vert de Github Actions sur le nouveau merge de versionnage GitHub sur `master` ?

👏 👏 👏

## En savoir plus

Ce type de développement avec de petites branches de fonctionnalités qui sont automatiquement déployées en production dès qu'elles sont mergées sur master peut ne pas fonctionner pour des fonctionnalités importantes qui nécessitent plusieurs étapes, plusieurs pull request, etc. Vous ne voulez pas garder une branche de fonctionnalité ouverte pendant des semaines car la Pull Request serait horrible à relire, et la merger sur `master` serait un cauchemar. Nous encourageons toujours les petites pull requests, mais nous cachons la fonctionnalité en cours de développement derrière un [**feature toggle**](https://en.wikipedia.org/wiki/Feature_toggle).

## (Optionnel) Score & Session

Si vous avez terminé tous les exercices du jour, revenez au sudoku facultatif d'hier si vous ne l'avez pas terminé (ou aux exercices précédents).

Si vous l'avez déjà terminé, jetez un coup d'œil à la [documentation Flask](http://flask.pocoo.org/). Nous aborderons Flask dans le cours de demain, en attendant, vous pouvez essayer d'implémenter une fonctionnalité dans le jeu du "mot le plus long" : un **score** global ! L'idée est que chaque fois qu'un utilisateur trouve un mot valide, vous incrémentez le score (1 point par lettre). Comme HTTP est sans état, vous devez utiliser l'extension Flask [Flask-Session](https://flask-session.readthedocs.io/en/latest/) pour gérer le concept de **session** (avec `SESSION_TYPE='filesystem'`).

## C'est terminé !

Avant de passer à l'exercice suivant, sauvegardez votre avancement avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 02-Best-Practices/04-Continuous-Deployment
touch DONE.md
git add DONE.md && git commit -m "02-Best-Practices/04-Continuous-Deployment done"
git push origin master
```

