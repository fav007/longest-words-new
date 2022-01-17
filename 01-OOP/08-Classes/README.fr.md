# Classes

Python appartient à la famille des langages orientés objet. Dans OOP, le bloc de construction de base est une **Classe**. Les classes fournissent un moyen de regrouper les données et les fonctionnalités (ou le comportement). La création d'une nouvelle classe crée un nouveau **type** d'objet, permettant de créer de nouvelles **instances** de ce type. Chaque instance de classe peut avoir des **attributs** qui lui sont attachés pour maintenir son **état**. Les instances de classe peuvent également avoir des **méthodes** (définies par leur classe) pour modifier leur état.


Prenez le temps de lire [9.3 - A first look at classes](https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes) jusqu'à `9.4`.

## Pour commencer

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 01-OOP/08-Classes
code .
```

## Votre première classe

Ouvrez le fichier `vehicle.py` et implémentez une classe simple en suivant ces spécificités :

- Un véhicule a une marque et une couleur
- Un véhicule est démarré ou arrêté
- Un véhicule peut être démarré ou arrêté _via_ un appel

Pour vous aider dans cette tâche, nous avons mis en place quelques tests que vous pouvez exécuter :

```bash
nosetests
```

N'hésitez pas à ouvrir et **lire** le fichier de test dans `tests/test_vehicle.py` !
Il vous aidera à comprendre comment la classe `Vehicle` est appelée et ce que vous devez traduire en code.

💡 Si vous voulez utiliser le débogueur introduit précédemment avec `nosetests`, vous devez exécuter les tests avec [`--no-capture`](http://nose.readthedocs.io/en/latest/man.html#cmdoption-s)(raccourci : `-s`).

## (Optionnel) Classes PowerShell

Depuis sa création, PowerShell utilise le framework .Net, une plate-forme orientée objet, permettant au développeur d'accéder à une collection de types.

Depuis PowerShell 5.0, il existe une syntaxe formelle pour définir les classes et autres types définis par l'utilisateur. Elle se présente comme suit :

```powershell
# Définir la classe :
class Device {
    [string]$Brand # Une variable d'instance
}

# Créer une instance de la nouvelle classe `Device`.
$dev = [Device]::new()

# Et définir/appeler les variables d'instance :
$dev.Brand = "Microsoft"
$dev
```

La différence avec Python ici est que vous êtes invité à spécifier le type de chaque variable d'instance dans la définition de la classe (`[string]` pour la variable d'instance `$Brand`).

Vous pouvez lire [l'article complet de Microsoft Docs](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_classes) pour vous plonger dans les classes définies par l'utilisateur de PowerShell.
