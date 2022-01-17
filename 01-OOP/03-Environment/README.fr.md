# Environnement

Une autre façon de modifier le comportement d'un script Python (autre que les arguments de la ligne de commande) est d'utiliser les **variables d'environnement**.

## Pour commencer

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 01-OOP/03-Environment
code .
nosetests
pipenv run pylint flask_option.py
```

## Exercice

Ouvrez le fichier `flask_option.py` et implémentez la méthode `start`. Elle devrait retourner une `String` en fonction de la présence et de la valeur de la variable d'environnement `FLASK_ENV`.

Voici le comportement attendu :

```bash
FLASK_ENV=development pipenv run python flask_option.py
# => "Démarrage en mode développement..."

FLASK_ENV=production pipenv run python flask_option.py
# => "Démarrage en mode production..."

pipenv run python flask_option.py
# => "Démarrage en mode production..."
```

:bulb: **Tip**: Jetez un coup d'œil au module [`os`](https://docs.python.org/3/library/os.html).

## (Optionnel) Variables d'environnement dans PowerShell

Écrivons un troisième [programme Hello World](https://en.wikipedia.org/wiki/%22Hello,_World!%22_program) avec le comportement suivant :

```bash
THE_NAME=Boris powershell -ExecutionPolicy bypass ./hello_env.ps1
# => Hello Boris
```

Vous devriez être en mesure de comprendre comment mettre en œuvre ce script à 2 lignes à partir de la [documentation](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_environment_variables)

<details><summary markdown="span">Voir la solution
</summary>

```powershell
$name = (Get-Item -Path Env:THE_NAME).value
Write-Output "Hello $name"
```

</details>
