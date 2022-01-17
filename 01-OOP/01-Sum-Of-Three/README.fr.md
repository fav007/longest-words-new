# Somme de trois

Commençons par un exercice très simple pour comprendre comment ces exercices vont fonctionner.

## Pour commencer

```bash
cd ~/code/<user.github_nickname>/reboot-python
git pull upstream master # Récupérer la dernière version de l'exercice

cd 01-OOP/01-Sum-Of-Three
code . # Ouvrez le dossier dans VS Code
```

## Procédure

Votre but est d'implémenter la méthode `sum3` dans le fichier `sum_of_three.py`. Avant d'essayer de le faire, exécutez les **tests** que nous avons préparés :

```bash
nosetests
```

Vous devriez obtenir trois tests qui échouent. Lisez l'erreur (en particulier le `AssertionError`) pour comprendre ce qui ne va pas et essayez d'implémenter la méthode `sum3`. Lorsque vous avez terminé, exécutez à nouveau la commande ci-dessus.

Répétez jusqu'à ce que tous les tests soient réussis (i.e. `0 FAILED`)

Vérifiez ensuite votre style avec :

```bash
pipenv run pylint sum_of_three.py
```

Si vous obtenez des erreurs de style, corrigez-les, sauvegardez et exécutez à nouveau la commande ci-dessus.

## Conclusion

Le but de cet exercice était de vous montrer comment exécuter les tests pour évaluer automatiquement votre code (à la fois le style et le contenu) et de vous initier à cette boucle de rétroaction.

## (Optionnel) PowerShell

Si vous travaillez dans un environnement Windows, il vous sera utile d'apprendre [**Powershell**](https://docs.microsoft.com/powershell/), et vous pouvez également l'utiliser sur macOS et Linux.

Écrivons notre tout premier script PowerShell. Ouvrez le fichier `hello.ps1` dans VS Code et copiez-collez l'instruction suivante [`Write-Output`](https://docs.microsoft.com/powershell/module/microsoft.powershell.utility/write-output) :

```powershell
Write-Output "Hello World"
```

Ensuite, vous pouvez exécuter le script depuis Git Bash avec :

```bash
powershell -ExecutionPolicy bypass ./hello.ps1
```

Vous devriez obtenir un `Hello World` ! Si ce n'est pas le cas, demandez à un TA.

Vous n'avez peut-être pas les droits d'administration sur l'ordinateur sur lequel vous travaillez, c'est pourquoi l'indicateur `-ExecutionPolicy bypass` est nécessaire. Sur un ordinateur où vous êtes administrateur, vous pouvez configurer la politique en `RemoteSigned` en [lisant la documentation](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-6). Cela remplacera une clé de registre (*Registry Key*).
