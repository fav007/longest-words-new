# Développements Pilotés par les Tests

Le développement piloté par les tests (alias **TDD** Test Driven Development) est un processus de développement logiciel qui s'appuie sur la répétition d'un cycle de développement très court : red-green-refactor. L'idée de ce processus est de transformer une fonctionnalité du code en un ou deux cas de test spécifiques, d'exécuter ces tests pour s'assurer qu'ils sont rouges (red), puis d'implémenter le code pour rendre ces tests verts (green). Une troisième étape consiste à refactoriser le code tout en gardant les tests verts.

![](https://res.cloudinary.com/wagon/image/upload/v1560715040/tdd_y0eq2v.png)

Le modèle de test recommandé est en quatre phases et est décrit dans cet [article de blog de Thoughtbot](https://robots.thoughtbot.com/four-phase-test)

## Le mot le plus long

Pratiquons le TDD avec un jeu simple que nous utiliserons jusqu'à la fin de la journée. Nous allons mettre en œuvre "Le mot le plus long", un jeu où, à partir d'une liste de neuf lettres, vous devez trouver le plus long mot anglais possible formé par ces lettres.

Exemple :

```
Grid: OQUWRBAZE
Longest word: BAROQUE
```

Le mot [`baroque`](https://en.wiktionary.org/wiki/baroque) est valide car il existe dans le dictionnaire anglais (même si son origine est française 🇫🇷 😋).

Notez que le mot [`bower`](https://en.wiktionary.org/wiki/bower) est également valide. Le but ici n'est **pas** d'écrire un code qui trouve le mot le plus long, mais d'analyser la tentative du joueur humain et de juger si ce mot est valide ou non par rapport à la grille donnée !

### Une première approche

Nous devons **décomposer** le problème en petits morceaux. Nous devons également trouver le bon niveau de **modélisation** par rapport au paradigme Orienté Objet.

Dans le paradigme TDD, une question que nous nous posons toujours est :

> Comment puis-je le tester ?

Se poser cette question signifie que vous devez considérer votre code comme une boîte noire. Il prendra certains paramètres en entrée et vous observerez la sortie, en la comparant à un résultat attendu.

❓ Prenez quelques minutes pour réfléchir aux **deux fonctions principales** de notre jeu.

<details><summary markdown="span">Voir la solution
</summary>

Nous avons besoin d'une première fonction pour construire une grille de neuf lettres aléatoires :

```python
def random_grid():
    pass
```

Nous avons aussi besoin d'une autre fonction qui, à partir d'une grille de neuf lettres, indique si un mot est valide :

```python
def is_valid(word, grid):
    pass
```

</details>

<br>

❓ Comment pouvons-nous utiliser le paradigme Orienté Objet sur ce problème ? Encore une fois, prenez le temps d'y réfléchir.

<details><summary markdown='span'>Voir la solution
</summary>

Nous pouvons créer une classe `Game` qui aura le modèle suivant :

1. Générer et maintenir une liste aléatoire de 9 lettres
1. Testez la validité d'un mot par rapport à cette grille

</details>

<br>

### Démarrer le projet en TDD

Maintenant que nous avons une meilleure idée de l'objet que nous voulons construire, nous pouvons commencer à écrire un test. Tout d'abord, créons un nouveau projet Python :

```bash
cd ~/code/<user.github_nickname>
mkdir longest-word && cd $_
pipenv --python 3.8
pipenv install nose pylint --dev
pipenv install --pre --dev astroid # Fix for https://github.com/PyCQA/pylint/issues/2241

touch game.py
mkdir tests
touch tests/test_game.py

code .
```

Créons notre classe de test, héritant de [`unittest.TestCase`](https://docs.python.org/3.8/library/unittest.html#basic-example)

```python
# tests/test_game.py
import unittest
import string
from game import Game

class TestGame(unittest.TestCase):
    def test_game_initialization(self):
        new_game = Game()
        grid = new_game.grid
        self.assertIsInstance(grid, list)
        self.assertEqual(len(grid), 9)
        for letter in grid:
            self.assertIn(letter, string.ascii_uppercase)

```

Lisez ce code. Si vous avez _des_ questions à son sujet, demandez à un professeur. Vous pouvez copier/coller ce code dans `tests/test_game.py`.

Maintenant, il est temps de l'exécuter pour s'assurer que ces tests **échouent** :

```bash
nosetests
```

Et ensuite ? Maintenant, vous devez **lire le message d'erreur**, et essayer de le **corriger**, seulement celui-ci (n'anticipez pas). Faisons le premier ensemble :

```bash
E
======================================================================
ERROR: Failure: ImportError (cannot import name 'Game' from 'game' (/Users/seb/code/ssaunier/longest-word/game.py))
----------------------------------------------------------------------
Traceback (most recent call last):
  # [...]
  File ".../longest-word/tests/test_game.py", line 2, in <module>
    from game import Game
ImportError: cannot import name 'Game' from 'game' (.../longest-word/game.py)

----------------------------------------------------------------------
Ran 1 test in 0.004s

FAILED (errors=1)
```

Le message d'erreur est donc `ImportError : cannot import name 'Game' from 'game'`. Il ne trouve pas le type `Game`.

❓ Comment pouvons-nous le résoudre ?

<details><summary markdown='span'>Voir la solution
</summary>

Nous devons créer une classe `Game` dans le fichier `./game.py` :

```python
# game.py
# pylint: disable=missing-docstring

class Game:
    pass
```

</details>

<br>

Exécutons à nouveau les tests :

```bash
nosetests
```

Nous obtenons ce message d'erreur :

```
E
======================================================================
ERROR: test_game_initialization (test_game.TestGame)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../longest-word/tests/test_game.py", line 7, in test_game_initialization
    grid = new_game.grid
AttributeError: 'Game' object has no attribute 'grid'

----------------------------------------------------------------------
Ran 1 test in 0.004s

FAILED (errors=1)
```

🎉 NOUS PROGESSONS !!! Nous avons un **nouveau** message d'erreur : `AttributeError: 'Game' object has no attribute 'grid'`.

![](https://res.cloudinary.com/wagon/image/upload/v1560715000/new-error_pvqomj.jpg)

### A votre tour !

Vous avez compris cette boucle de rétroaction rapide ? Nous exécutons le test, nous obtenons un message d'erreur, nous trouvons un moyen de le corriger, nous exécutons à nouveau le test et nous passons à un nouveau message d'erreur !

❓ Essayez d'implémenter le code de la classe `Game` pour faire passer ce test. Ne regardez pas encore la solution, essayez d'appliquer le TDD sur ce problème !

💡 Vous pouvez utiliser `print()` ou `import pdb; pdb.set_trace()`en association avec `nosetests -s`.

<details><summary markdown='span'>Voir la solution
</summary>

Une des implémentations possibles est :

```python
# game.py
# pylint: disable=missing-docstring

import string
import random

class Game:
    def __init__(self):
        self.grid = []
        for _ in range(9):
            self.grid.append(random.choice(string.ascii_uppercase))
```

</details>

<br>

## Vérifier la validité d'un mot

Passons à la deuxième méthode de notre classe `Game`.

Nous utilisons le **TDD**, ce qui signifie que nous devons écrire le test **en premier**. Pour le premier test, nous vous avons donné le code.

❓ C'est à votre tour d'implémenter un test pour cette nouvelle méthode `is_valid(self, word)` ! Vous voyez, nous vous avons déjà donné la [signature](https://en.wikipedia.org/wiki/Type_signature#Method_signature) de la méthode...

<details><summary markdown='span'>Voir la solution
</summary>

Une implémentation possible de ce test serait :

```python
# tests/test_game.py

# [...]

    def test_empty_word_is_invalid(self):
        new_game = Game()
        self.assertIs(new_game.is_valid(''), False)

    def test_is_valid(self):
        new_game = Game()
        new_game.grid = list('KWEUEAKRZ') # Forcer la grille à un scénario de test :
        self.assertIs(new_game.is_valid('EUREKA'), True)
        self.assertEqual(new_game.grid, list('KWEUEAKRZ')) # S'assurer que la grille n'a pas été modifiée

    def test_is_invalid(self):
        new_game = Game()
        new_game.grid = list('KWEUEAKRZ') # Forcer la grille à un scénario de test :
        self.assertIs(new_game.is_valid('SANDWICH'), False)
        self.assertEqual(new_game.grid, list('KWEUEAKRZ')) # S'assurer que la grille n'a pas été modifiée
```
</details>

<br>

Exécutez les tests pour vous assurer qu'ils ne passent pas :

```bash
nosetests
```

❓ C'est à votre tour ! Mettez à jour l'implémentation de `game.py` pour que les tests passent !

<details><summary markdown='span'>Voir la solution
</summary>

Une implémentation possible est :

```python
# game.py

# [...]

    def is_valid(self, word):
        if not word:
            return False
        letters = self.grid.copy() # Consume letters from the grid
        for letter in word:
            if letter in letters:
                letters.remove(letter)
            else:
                return False
        return True
```

</details>

<br>


## Style

Assurez-vous de rendre `pylint` content :

```bash
pipenv run pylint game.py
```

Vous pouvez désactiver ces règles :

```python
# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
```

## C'est terminé !

Avant de passer à l'exercice suivant, sauvegardez votre avancement avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 02-Best-Practices/02-TDD
touch DONE.md
git add DONE.md && git commit -m "02-Best-Practices/02-TDD done"
git push origin master
```
