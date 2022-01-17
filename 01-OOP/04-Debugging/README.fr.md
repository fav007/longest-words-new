# Débogage

Le débogage est le processus consistant à _trouver_ et _résoudre_ les problèmes dans votre code. Comme le dit Wikipedia, le débogage est une tactique :

> [...] qui peut impliquer le débogage **interactif**, l'analyse du flux de contrôle, les tests unitaires, les tests d'intégration, l'analyse des fichiers *log*, le monitoring au niveau de l'application ou du système, les vidages de mémoire et le profilage.

Dans cet exercice, nous allons nous concentrer sur le débogage interactif et l'analyse du flux de contrôle, les bases du débogage.

## Pour commencer

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 01-OOP/04-Debugging
code .
```

## Le Débogueur Python

Une des grandes qualités de Python est qu'il est livré avec un débogueur inclus, prêt à l'emploi ! La documentation contient un [article détaillé sur le module `pdb`](https://docs.python.org/3/library/pdb.html) auquel vous devriez jeter un coup d'oeil.

Allons tout de suite au fond des choses. Dans ce dossier d'exercice, vous trouverez un `hello.py` qui contient un programme. Ce programme a un bug, utilisons le débogueur Python pour le trouver !

```bash
pipenv run python hello.py john lennon
```

Quel est le problème avec ce programme ? Essayons de déboguer ce problème ! Il semble qu'il y ait un problème avec la création du nom complet concaténé. Essayons de déboguer ça. Insérez la ligne suivante juste après le `def full_name` :

```python
def full_name(first_name, last_name):
    import pdb; pdb.set_trace()
    # [... le reste de la fonction]
```

Retournez dans le terminal et exécutez à nouveau la commande :

```bash
pipenv run python hello.py john lennon
```

Le programme **s'arrêtera** à la ligne où vous avez inséré le `pdb.set_trace()` :

```bash
> [...]/reboot-python/01-OOP/04-Debugging/hello.py(6)full_name()
-> name = f"{first_name.capitalize()}{last_name.capitalize()}"
(Pdb)
```

Il est temps de jouer avec le débogueur. De là, vous pouvez faire deux choses :

1. Contrôler le flux du programme, en indiquant au débogueur d'exécuter la ligne suivante, d'entrer dans une fonction ou d'en sortir.
2. Jetez un coup d'oeil à la mémoire actuelle, c'est-à-dire à ce qui est stocké dans les variables à cet instant. Le programme est arrêté afin que vous puissiez examiner de plus près ses composants internes.

Tapez ceci:

```bash
(Pdb) sys.argv
# => ['hello.py', 'john', 'lennon']
```

Vous voyez comment cela fonctionne ? Vous venez de demander au débogueur d'appeler le tableau `sys.argv` et de regarder ce qui est stocké dans ce tableau.

Notre problème est qu'il manque un espace entre `John` et `Lennon`. Nous aimerions donc jeter un coup d'oeil à la variable locale `name`. Tapons :

```bash
(Pdb) name
# => *** NameError: name 'name' is not defined
```

Pourquoi avons-nous ce `NameError` ? Où sommes-nous arrêtés ? Pour vérifier à quelle ligne le programme est arrêté, vous pouvez taper :

```bash
(Pdb) ll
# 4     def full_name(first_name, last_name):
# 5         import pdb; pdb.set_trace()
# 6  ->     name = f"{first_name.capitalize()}{last_name.capitalize()}"
# 7         return name
```

Le programme s'est arrêté **avant** la ligne indiquée par la petite flèche `->`. Cela signifie que la variable `name` n'a **pas encore été assignée**, donc nous obtenons l'erreur "`name` is not defined". OK, tout est clair maintenant !

Nous sommes à l'intérieur d'une fonction. Quelque chose d'utile est d'afficher la liste des arguments de la fonction courante :

```bash
(Pdb) args
# first_name = 'john'
# last_name = 'lennon'
```

Que pouvons-nous faire maintenant ? Nous pouvons demander au débogueur d'exécuter la ligne suivante avec :

```bash
(Pdb) next
```

Voilà, le débogueur a avancé d'une ligne et l'a exécutée. Vous pouvez voir où le programme s'arrête maintenant avec :

```bash
(Pdb) ll
```

Vous voyez comment la petite flèche `->` a avancé ? Maintenant nous pouvons vérifier ce qu'il y a dans la variable `name` :

```bash
(Pdb) name
# => 'JohnLennon'
```

C'est fait ! Nous avons identifié la ligne coupable ! Il manque un espace dans l'interpolation.

Vous pouvez laisser le programme s'exécuter jusqu'au prochain point d'arrêt (ou jusqu'à la fin) avec :

```bash
(Pdb) continue
```

Corrigez la méthode `full_name` dans `hello.py`, et exécutez à nouveau le programme. N'oubliez pas d'enlever la ligne du débogueur ! C'est quelque chose que l'on oublie facilement et que l'on ajoute à un commit. Certaines équipes pourraient vouloir ajouter un [pre-commit hook](http://blog.keul.it/2013/11/no-more-pdbsettrace-committed-git-pre.html) pour éviter que cela ne se produise.

## Aller plus loin

La section précédente portait sur la compréhension des commandes de base du débogueur. Vous pouvez l'imaginer comme un lecteur DVD avec les boutons suivants :

- Pause (`pdb.set_trace()` dans le code source)
- Next frame (`next`)
- Play (`continue`)

Il existe [beaucoup d'autres commandes de débogage](https://docs.python.org/3/library/pdb.html#debugger-commands) comme `step` ou `return`.

## (Optionnel) Débogage dans PowerShell

Windows est livré avec **PowerShell ISE**, un programme interactif permettant de déboguer vos scripts. Allez-y et [lisez l'article](https://docs.microsoft.com/powershell/scripting/components/ise/how-to-debug-scripts-in-windows-powershell-ise) sur Microsoft Docs.
