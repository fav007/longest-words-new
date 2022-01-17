# Valideur Sudoku

Félicitations pour avoir atteint cet exercice ! Nous allons implémenter un valideur de Sudoku. Son but est simple : déterminer si la grille de Sudoku **9x9** est valide !

![](https://res.cloudinary.com/wagon/image/upload/v1560713910/sudoku_szhhdf.png)

## Règles

Un sudoku est valide si et seulement si :

- Une ligne doit contenir tous les chiffres de `1` à `9`.
- Une colonne doit contenir tous les chiffres de `1` à `9`.
- Chacun des neuf petits carrés 3x3 doit contenir les chiffres de `1` à `9`.

## Pour commencer

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 01-OOP/09-Optional-Sudoku
code .
```

## Modèle de données

Une grille de Sudoku sera représentée par une liste de listes Python :

```python
grid = [
    [7,8,4,  1,5,9,  3,2,6],
    [5,3,9,  6,7,2,  8,4,1],
    [6,1,2,  4,3,8,  7,5,9],

    [9,2,8,  7,1,5,  4,6,3],
    [3,5,7,  8,4,6,  1,9,2],
    [4,6,1,  9,2,3,  5,8,7],

    [8,7,6,  3,9,4,  2,1,5],
    [2,4,3,  5,6,1,  9,7,8],
    [1,9,5,  2,8,7,  6,3,4]
]
```

Avec cette structure à l'esprit, vous pouvez accéder à une cellule de la ligne `i` et de la colonne `j` avec l'instruction suivante :

```python
grid[i][j]
```

💡 Rappelez-vous que les index des listes python commencent à **`0`**, donc les valeurs `i` et `j` sont comprises entre `0` et `8`.

## Exercice

Ouvrez le fichier `sudoku.py` et implémentez la méthode d'instance `is_valid()` de la classe `SudokuSolver`. Pour vérifier si votre code fonctionne, vous pouvez exécuter les tests avec :

```bash
nosetests
```

## C'est fait ?

Nous allons bientôt commencer un livecode avec toute la classe. Vous pouvez pratiquer vos compétences en Python sur Codewars (connectez-vous avec GitHub !) avec les Kata suivants :

- [Snake and Ladders](https://www.codewars.com/kata/snakes-and-ladders-1/train/python)
- [Decode the morse code](https://www.codewars.com/kata/decode-the-morse-code/train/python)
- [Escape the mines!](https://www.codewars.com/kata/escape-the-mines/train/python)
