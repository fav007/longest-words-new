## Manipulation de String

La classe `String` est l'une des classes les plus utilisées de Python et des langages de programmation en général. De nombreuses méthodes intégrées existent déjà pour vous faciliter la vie et votre objectif dans ces exercices sera :

- D'apprendre à rechercher la bonne méthode dans la documentation Python.
- De vous familiariser avec l'utilisation de l'interpréteur Python pour expérimenter de nouvelles méthodes et se les approprier.

L'interpréteur Python fonctionne comme suit :

```bash
pipenv run python
```

1. Il lit l'expression écrite par l'utilisateur, qui peut être n'importe quelle expression python valide comme `"Hello"`, `2+2`, `"hello".upper()` ...
2. Il évalue le résultat de cette expression.
3. Il print ce résultat.
4. Il retourne au point 1, en attendant une nouvelle entrée de l'utilisateur.

Démarrez-le en tapant la commande "python" dans votre terminal.

* **Expérimentez les lignes suivantes** sur l'interpréteur Python :

```python
1 + 1
"A string object".lower()
"A string object".upper()
type(4)
```

## Pour commencer


```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 01-OOP/05-String-Manipulation
code .
nosetests
pipenv run pylint string_methods.py
```

En Python, tout (une String, un Integer un Float, une Liste...) est un objet. Nous pouvons appeler des méthodes sur ces objets. Ces méthodes sont appelées **méthodes d'instance** car elles ne peuvent être appelées que sur des instances de la classe. L'objet sur lequel nous appelons la méthode est appelé le **récepteur** (*receiver*).

## Exercice

Trouvez les bonnes méthodes Python de la [classe String](https://docs.python.org/3/library/stdtypes.html#string-methods) pour les insérer et faire passer les tests.

Pour coder, il faut être intelligent et savoir comment et où chercher l'information dont on a besoin ! Souvent, l'étape la plus difficile est de poser la bonne question à Google. Pour trouver les méthodes dont vous aurez besoin pour ce défi, utilisez :

* Google et [Stack Overflow](http://stackoverflow.com/)
* [La doc python](https://docs.python.org/3) si vous avez une idée approximative de la méthode que vous recherchez.

Lorsque vous pensez avoir trouvé la méthode que vous recherchez, et que vous pensez savoir comment l'utiliser, utilisez l'interpréteur Python pour tester cette méthode sur quelque chose ! L'expérimentation sur l'interpréteur Python est une étape cruciale pour les débutants.

## (Optionnel) Lectures complémentaires sur les Strings dans PowerShell

Comme tout langage de programmation, PowerShell offre au développeur un grand nombre d'outils pratiques intégrés à utiliser avec les Strings. [Cet article](https://4sysops.com/archives/strings-in-powershell-replace-compare-concatenate-split-substring/) est une bonne introduction à ces outils.
