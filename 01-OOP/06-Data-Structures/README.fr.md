# Structures de données

Dans cet exercice, nous allons couvrir les structures de données intégrées les plus utiles.
Avant de plonger dans le code, prenez le temps de lire ce qui suit :

- [Listes](https://docs.python.org/3.8/tutorial/introduction.html#lists), appelées _array_ dans d'autres langages
- [En savoir plus sur les listes](https://docs.python.org/3.8/tutorial/datastructures.html#more-on-lists)
- [Comprehensions des listes](https://docs.python.org/3.8/tutorial/datastructures.html#list-comprehensions)
- [Tuples](https://docs.python.org/3.8/tutorial/datastructures.html#tuples-and-sequences)
- [Dictionnaires](https://docs.python.org/3.8/tutorial/datastructures.html#dictionaries), appelés _hash_ ou _hashmap_ dans d'autres langages
- [Techniques de boucles](https://docs.python.org/3.8/tutorial/datastructures.html#looping-techniques) avec le mot clé `for`

Vous avez tout lu ? C'est parti pour le codage !

## Pour commencer

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 01-OOP/06-Data-Structures
code .
```

## Exercice

### Devises

Construisons un convertisseur de devises dans le fichier `currencies.py`. Dans cet exercice, nous allons manipuler des listes, des dictionnaires et des Tuples.

1. Créez un nouveau dictionnaire constant `RATES` en haut de `currencies.py`. Les clés seront des Strings de 6 lettres comme `"USDEUR"`, `"GBPEUR"`, `"CHFEUR"`, et les valeurs, leur taux stocké comme un simple [`Float` Python](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex). Vous pouvez trouver ces informations sur [Google](https://www.google.com/search?q=USDEUR)
2. Implémentez la méthode `convert(amount, currency)`. Le premier paramètre est un **Tuple** de deux éléments : un Float et une devise (par exemple, `(100, "USD")`). Le second paramètre est une `String`, la devise dans laquelle vous voulez convertir le montant.
3. Pour simplifier, nous considérerons les montants comme des centimes et le résultat sera _arrondi_.
4. Lorsqu'elle est appelée avec un taux inconnu (par exemple, `"RMBEUR"`), la méthode `convert` doit retourner `None`.


Exécutez les tests avec :

```bash
nosetests
```

Vous remarquerez peut-être que certains tests échouent. Mettez à jour vos taux avec les valeurs suivantes car les résultats ont été codés en dur dans les tests :

- `USDEUR`: `0.85`
- `GBPEUR`: `1.13`
- `CHFEUR`: `0.86`

Enfin, vérifiez votre style avec:

```bash
pipenv run pylint currencies.py
```

## (Optionnel) Structures de données dans PowerShell

PowerShell est livré avec les éléments suivants :

- [Arrays](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_arrays) (équivalent des `listes` en Python)
- [Hash Tables](https://docs.microsoft.com/powershell/module/microsoft.powershell.core/about/about_hash_tables) (équivalent des `Dictionnaires` dans Python)

Maintenant, essayez d'implémenter un script qui se comporte comme les exemples suivants

```bash
powershell -ExecutionPolicy bypass ./convertor.ps1
# => Le montant est requis.

powershell -ExecutionPolicy bypass ./convertor.ps1 -Amount 12.4
# => La devise de destination est obligatoire.

powershell -ExecutionPolicy bypass ./convertor.ps1 -Amount 12.4 -Currency AAA
# => Désolé, la devise AAA n'est pas encore prise en charge

powershell -ExecutionPolicy bypass ./convertor.ps1 -Amount 12.4 -Currency GBP
# => 12.4 EUR => 14.012 GBP
```

Vous aurez peut-être besoin d'utiliser [`Hashtable.ContainsKey(key)`](https://docs.microsoft.com/dotnet/api/system.collections.hashtable.containskey).

<details><summary markdown="span">Voir la solution
</summary>

```powershell
param(
  [double]$Amount = $(throw "Amount is required."),
  [string]$Currency = $(throw "Destination currency is required.")
)

$rates = @{
  USDEUR = 0.85;
  GBPEUR = 1.13;
  CHFEUR = 0.86
}

$key = $Currency + "EUR"

if ($rates.ContainsKey($key)) {
  $result = ($Amount * $rates[$key])
  Write-Output "$Amount EUR => $result $Currency"
} else {
  Write-Error "Sorry, currency $Currency is not yet supported"
}
```

</details>
