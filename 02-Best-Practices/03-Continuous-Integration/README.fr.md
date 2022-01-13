# Intégration Continue

Avoir des tests sur un repository vous donne un avantage considérable : vous pouvez mettre en place une [**Intégration continue**](https://en.wikipedia.org/wiki/Continuous_integration). La section _Best Practices_ de cet article Wikipedia vaut la peine d'être lue.

Le but de cet exercice est de lier notre logiciel de contrôle de version avec un moteur de production. L'idée est d'exécuter un moteur de production à chaque fois qu'un versionnage est envoyé à l'outil de contrôle de version. Quelle que soit la branche, un processus de production est déclenché pour donner un retour aux développeurs sur ce versionnage, si il est _vert_ ou _rouge_ (ce qui signifie que les tests passent / que la production peut être terminée).

## Outils

Comme pour les logiciels de contrôle de version, il existe de nombreux outils permettant de réaliser de l'intégration continue :

- [Jenkins](https://jenkins.io/), le logiciel de CI le plus populaire (vous devez l'installer)
- [Github Actions](https://github.com/features/actions), l'outil de Github pour mettre en place des workflows et du CI/CD
- [Travis](https://travis-ci.com/), le service de CI **cloud** le plus populaire
- [Beaucoup d'autres](https://en.wikipedia.org/wiki/Comparison_of_continuous_integration_software)

Pour garder cet exercice simple, nous utiliserons Github Actions, car c'est l'outil directement intégré dans GitHub (et vous verrez que c'est important) sans aucun effort de configuration de la part du développeur. De plus, il est **gratuit** pour les repositories publics de GitHub !

## Mise en place

Nous allons déployer le repository que vous avez créé dans l'exercice 02-TDD. D'abord, créez un repository vide `longest-word` dans votre compte Github. Après cela, vous pouvez pousser vos changements :

```bash
cd ~/code/<user.github_nickname>/longest-word

git init
git add .
git commit -m "Game development with TDD"

git remote add origin git@github.com:<user.github_nickname>/longest-word.git

git push origin master
```


## Workflow CI

Vous devez maintenant écrire un script de configuration pour le CI (Intégration Continue). Ces outils sont _génériques_, ils peuvent construire des programmes dans de nombreux langages, avec de nombreux frameworks. Nous devons être spécifiques et expliquer à Githun Actions que notre projet est un projet Python 3, que nous utilisons `pipenv` pour gérer les dépendances externes et que nous utilisons `nosetests` pour exécuter les tests.

Pour se faire, Github va lire le fichier `.python-ci.yml` situé dans votre dossier `.github/workflows` :

```bash
mkdir -p .github/workflows
touch .github/workflows/.python-ci.yml
```

```yml
# .python-ci.yml

name: basic CI
on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: "3.8"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pipenv
        pipenv install --dev
    - name: Test with nose
      run: |
        pipenv run nosetests
```

Enregistrez ce fichier dans Sublime Text, et effectuez un versionnage :

```bash
git add .github/workflows/python-ci.yml
git commit -m "Configure Github Actions CI to run nosetests"
```

Génial ! Avant de pousser, allez sur cette page :

[github.com/<user.github_nickname>/longest-word/commits/master](https://github.com/<user.github_nickname>/longest-word/commits/master)

Vous devriez avoir un versionnage. Maintenant retournez dans le terminal :

```bash
git push origin master
```

:warning: Ne passe PAS l'option `--force` lorsque tu pousses ton code avec git car cela empêchera sûrement Travis de détecter tes changements.

Quand le push est terminé, retournez à la page, et **rechargez** la. Vous devriez voir le versionnage avec un cercle jaune, puis une coche verte ! Ceci est l'intégration entre GitHub et Github Actions. Elle s'exécutera à chaque fois que vous enverrez des versionnages à GitHub.

## Intégration Continue & Pull Request

Améliorons notre jeu avec une validation plus précise. Actuellement, vous pouvez gagner avec le scénario suivant :

```
Grid: KWIENFUQW
My proposition: FEUN
```

```python
new_game = Game()
new_game.grid = list('KWIENFUQW')
new_game.is_valid('FEUN')
# => true
```

Bien sûr, c'est syntaxiquement valide (chaque lettre de `FEUN` peut être trouvée dans la grille), mais ce n'est pas un mot anglais valide du dictionnaire !

Travaillons sur ce point dans une nouvelle branche de fonctionnalité :

```bash
git checkout -b dictionary-api
```

Comme nous suivons le paradigme TDD, nous devons ajouter un test :

```python
# tests/test_game.py
# [...]
    def test_unknown_word_is_invalid(self):
      new_game = Game()
      new_game.grid = list('KWIENFUQW') # Forcer la grille à un scénario de test :
      self.assertIs(new_game.is_valid('FEUN'), False)
```

Nous pouvons versionner dès maintenant :

```bash
git add test_game.py
git commit -m "TDD: Check that attempt exists in the English dictionary"
git push origin dictionary-api
```

Maintenant, ouvrons une Pull Request sur GitHub pour cette branche. Vous trouverez peut-être que c'est un peu tôt, mais c'est quelque chose qui est en fait encouragé par le [flow GitHub](http://scottchacon.com/2011/08/31/github-flow.html) :

Si vous êtes bloqué dans le développement de votre fonctionnalité ou de votre branche et que vous avez besoin d'aide ou de conseils, ou si vous êtes un développeur et que vous avez besoin d'un designer pour revoir votre travail (ou vice versa), ou même si vous avez peu ou pas de code mais quelques captures d'écran ou des idées générales, vous ouvrez une pull request.

Au Wagon, les développeurs ouvrent des Pull Request très tôt pour leurs branches de fonctionnalités afin de montrer à leurs coéquipiers ce qu'ils font et de solliciter des retours très tôt. Pas besoin d'attendre que le code soit complet pour ouvrir une Pull Request ! Voici une capture d'écran de notre application principale, le préfixe `[WIP]` est utilisé dans les titres des Pull Request pour montrer que la branche n'est pas encore prête à être fusionnée :

![](https://res.cloudinary.com/wagon/image/upload/v1560714921/kitt-wip-prs_obp6e7.png)

Revenons à notre Pull Request. Si vous scrollez un peu en dessous de la description de la PR et de la liste des versionnages, vous verrez l'intégration avec Github Actions :

![](img/github_actions_picture.png)

Cette fonctionnalité est vraiment importante. Vous avez un retour direct, et directement dans GitHub, sur l'état de la construction de votre branche. Bien sûr, ici nous _voulons_ avoir une branche rouge car nous avons ajouté un test mais n'avons pas encore implémenté le comportement. Néanmoins, vous pouvez imaginer que quelqu'un qui push du code et oublie d'exécuter les tests localement sur sa machine sera averti directement sur GitHub qu'il a cassé quelque chose dans le code.

---

Revenons à l'implémentation de notre fonctionnalité. Nous voulons faire passer le test suivant :

```python
pipenv run nosetests tests/test_game.py:TestGame.test_unknown_word_is_invalid
# Vous voyez que nous n'exécutons qu'*un* seul test et pas toute la série ?
```

❓ Voici quelques conseils pour implémenter cette fonctionnalité :

- Vous pouvez utiliser la solution simple du Wagon. [Dictionary API](https://wagon-dictionary.herokuapp.com/)
- Vous pouvez `pipenv install requests` pour faire des [requêtes HTTP](http://docs.python-requests.org/en/master/) à cette API.

<details><summary markdown='span'>Voir la solution
</summary>

Nous pouvons implémenter une méthode privée `__check_dictionary` pour exécuter un appel API.

```python
# game.py
# [...]
import requests

class Game:
    # [...]

    def is_valid(self, word):
        # [...]

        return self.__check_dictionary(word)


    @staticmethod
    def __check_dictionary(word):
        response = requests.get(f"https://wagon-dictionary.herokuapp.com/{word}")
        json_response = response.json()
        return json_response['found']
```

</details>

<br>

N'oubliez pas d'exécuter les tests localement jusqu'à ce que vous ayez 5 tests réussis. Lorsque vous avez terminé, il est temps d'observer le résultat sur GitHub / Github Actions!

```bash
git add .
git commit -m "Feature complete: Dictionary check of attempt"
git push origin dictionary-api
```

Retournez à votre page Pull Request, vous devriez voir les icônes passer de croix rouges à points jaunes. Cela signifie que Github Actions est en train de compiler le code avec le dernier versionnage. Attendez quelques secondes, et il devrait mettre à jour le statut. Voici ce que vous devriez voir :

![](https://res.cloudinary.com/wagon/image/upload/v1560714701/github-travis-passing_vppc1l.png)

Beau travail 🎉 ! Invitez votre buddy en tant que collaborateur de repo pour revoir le code de la Pull Request et le **merger**.

## Conclusion

L'ajout de tests dans un repository et coupler GitHub avec un service comme Github Actions permet au développeur d'avoir l'esprit tranquille lorsqu'il ajoute du code, de vérifier les éventuelles régressions, et d'exercer l'ensemble des tests à _chaque_ versionnage !

Avant de d'avancer plus loin dans le DevOps avec le prochain exercice sur le déploiement continu, quelques derniers conseils :

- Faites en sortes que les différences entre les Pull Request soient les plus minimes possible. Une bonne taille est de **moins de 100 lignes** de différence (onglet `Files changed` de la Pull Request).
- Gardez une pull request centrée sur une _simple_ fonctionnalité. Ajoutez au moins un test pour chaque Pull Request
- Avant de demander une révision, relisez votre code dans l'onglet `Files changed`. Voir le code sous cet angle (dans un navigateur web sous un format différent) vous aidera à repérer les problèmes de style, les possibilités de refactorisation, etc. que vous ne pouviez pas voir directement dans votre éditeur de texte.
- Enfin, vos pairs GitHub ont rédigé un excellent article sur [la manière d'écrire correctement](https://blog.github.com/2015-01-21-how-to-write-the-perfect-pull-request/) dans une Pull Request (à la fois pour la personne évaluée et pour l'évaluateur).

## C'est terminé !

Avant de passer à l'exercice suivant, sauvegardez votre avancement avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 02-Best-Practices/03-Continuous-Integration
touch DONE.md
git add DONE.md && git commit -m "02-Best-Practices/03-Continuous-Integration done"
git push origin master
```
