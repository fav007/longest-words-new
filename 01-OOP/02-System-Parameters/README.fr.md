# Paramètres système

Les scripts Python peuvent lire les arguments passés sur la ligne de commande. Cela peut s'avérer pratique lorsque vous souhaitez ajouter des options à votre script.

## Pour commencer

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 01-OOP/02-System-Parameters
code .
nosetests
pipenv run pylint calc.py
```

## Quelques mots sur `sys.argv`

Considérons le code suivant :

```python
# args.py
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
```

Vous pouvez le sauvegarder dans un fichier `args.py` et l'exécuter :

```bash
pipenv run python args.py arg1 arg2 arg3
# Nombre d'arguments : 4 arguments.
# Liste d'arguments : ['args.py', 'arg1', 'arg2', 'arg3']
```

[`sys.argv`](https://docs.python.org/3/library/sys.html#sys.argv) est une **liste** python contenant les arguments de ligne de commande passés à un script Python. `argv[0]` est toujours le nom du script.

## Exercice

Créons une calculatrice simple pour les **integers**. Voici comment elle doit fonctionner :

```bash
alias prp="pipenv run python"
prp calc.py 4 + 5
# => 9
prp calc.py 2 \* 6
# => 12
prp calc.py 3 - 9
# => -6
```

Ouvrez le fichier `calc.py` et implémentez ce comportement ! Vous trouverez une fonction `main` qui est exécutée automatiquement grâce à [cet idiome](https://docs.python.org/3/library/__main__.html).


## Aller plus loin

Si vous devez construire un outil CLI avec Python, pensez à l'intégration de la fonction [`argparse`](https://docs.python.org/3/library/argparse.html).

## (Optionnel) Arguments de ligne de commande dans PowerShell


Écrivons un autre [script PowerShell](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_scripts) en utilisant un argument passé sur la ligne de commande. Nous pouvons améliorer le script `hello.ps1` de l'exercice précédent avec quelque chose qui dira "Hello $SOMEONE", *someone* étant une variable passée sur la ligne de commande, comme ceci :

```bash
powershell -ExecutionPolicy bypass ./hello_name.ps1 -Name Boris
# => Hello Boris

powershell -ExecutionPolicy bypass ./hello_name.ps1 -Name Charlotte
# => Hello Charlotte

powershell -ExecutionPolicy bypass ./hello_name.ps1
# => Name parameter is required.
```

Ouvrez le fichier `hello_name.ps1` et essayez d'implémenter ce script de 2 lignes avec le mot clé `param`.

<details><summary markdown="span">Voir la solution
</summary>

```powershell
param($Name = $(throw "Name parameter is required."))
Write-Output "Hello $Name"
```

</details>
