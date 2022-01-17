# Jenkins

Dans l'exercice précédent d'**Intégration Continue**, nous avons vu comment utiliser le fournisseur de cloud [Travis CI](https://travis-ci.com/) pour mettre rapidement en place une "ferme d'exploitation" pour notre repository GitHub. L'intégration étroite entre GitHub et Travis CI, combinée à l'utilisation des fonctionnalités OAuth de GitHub, permet à tout développeur d'être opérationnel en quelques minutes. La partie la plus délicate de cette installation est toujours d'obtenir la bonne configuration du fichier `.travis.yml`.

Dans cet exercice, nous allons remplacer Travis CI par **Jenkins**.

## Contexte

[Jenkins](https://jenkins.io/) est un serveur d'automatisation _open-source_ développé en java. Il s'agit d'un système basé sur un serveur qui tourne dans des conteneurs de servlets tels qu'Apache Tomcat. Publié sous la licence MIT, Jenkins est un logiciel libre.

Jenkins a été publié pour la première fois en **2011** et est largement utilisé par des entreprises du monde entier. Les entreprises qui ne veulent pas faire confiance au fournisseur de cloud Travis CI se tournent vers Jenkins et hébergent ce logiciel sur leurs propres serveurs. Pour cet exercice, Le Wagon fournit une instance de Jenkins hébergée sur AWS EC2. De retour dans votre entreprise, vous pourrez peut-être utiliser les instances de Jenkins fournies par vos équipes informatiques si de telles instances existent.

## Partir de zéro

Créons un nouveau projet simple à configurer en Intégration Continue avec Jenkins.

```bash
cd ~/code/<user.github_nickname>
mkdir morse
cd morse

pipenv --python 3.8
pipenv install nose pylint --dev
```

Créons les fichiers pour notre projet :

```bash
touch morse.py
mkdir tests
touch tests/test_morse.py
```

Écrivons une classe vide pour notre package principal `morse.py` :

```python
# morse.py
# pylint: disable=missing-docstring

def decode(message):
    pass # TODO: implémentez le comportement !
```

Notre objectif est de coder un **décodeur** de [code Morse](https://en.wikipedia.org/wiki/Morse_code) qui se comporte comme ceci :

```python
sentence = decode(".- .-.. .-.. / -.-- --- ..- / -. . . -.. / .. ... / -.-. --- -.. .")
# => ALL YOU NEED IS CODE
```

Nous voulons utiliser Jenkins, donc nous avons besoin de tests ! Écrivons quelques tests unitaires pour la méthode `decode()` :

```python
# tests/test_morse.py
import unittest
from morse import decode

class TestMorse(unittest.TestCase):
    def test_empty_message(self):
        self.assertEqual(decode(""), "")

    def test_a(self):
        self.assertEqual(decode(".-"), "A")

    def test_b(self):
        self.assertEqual(decode("-..."), "B")

    def test_c(self):
        self.assertEqual(decode("-.-."), "C")

    def test_d(self):
        self.assertEqual(decode("-.."), "D")

    def test_e(self):
        self.assertEqual(decode("."), "E")

    def test_f(self):
        self.assertEqual(decode("..-."), "F")

    def test_g(self):
        self.assertEqual(decode("--."), "G")

    def test_h(self):
        self.assertEqual(decode("...."), "H")

    def test_i(self):
        self.assertEqual(decode(".."), "I")

    def test_j(self):
        self.assertEqual(decode(".---"), "J")

    def test_k(self):
        self.assertEqual(decode("-.-"), "K")

    def test_l(self):
        self.assertEqual(decode(".-.."), "L")

    def test_m(self):
        self.assertEqual(decode("--"), "M")

    def test_n(self):
        self.assertEqual(decode("-."), "N")

    def test_o(self):
        self.assertEqual(decode("---"), "O")

    def test_p(self):
        self.assertEqual(decode(".--."), "P")

    def test_q(self):
        self.assertEqual(decode("--.-"), "Q")

    def test_r(self):
        self.assertEqual(decode(".-."), "R")

    def test_s(self):
        self.assertEqual(decode("..."), "S")

    def test_t(self):
        self.assertEqual(decode("-"), "T")

    def test_u(self):
        self.assertEqual(decode("..-"), "U")

    def test_v(self):
        self.assertEqual(decode("...-"), "V")

    def test_w(self):
        self.assertEqual(decode(".--"), "W")

    def test_x(self):
        self.assertEqual(decode("-..-"), "X")

    def test_y(self):
        self.assertEqual(decode("-.--"), "Y")

    def test_z(self):
        self.assertEqual(decode("--.."), "Z")

    def test_sos(self):
        self.assertEqual(decode("... --- ..."), "SOS")

    # NOTE: nous ajouterons plus tard un test pour les *phrases*
```

Dans votre terminal, exécutez les tests :

```bash
nosetests
```

Vous devriez obtenir 28 tests défaillants ! Super, nous avons l'étape "rouge" du TDD. Procédons à la configuration de Jenkins avant de faire passer les tests au vert.

Avant de faire cela, nous avons besoin que notre projet soit pushé sur GitHub :

```bash
git init
git add .
git commit -m "Morse code. Failing tests. Pending Jenkins configuration"
```

Allez sur [github.com/new](https://github.com/new) et créez un repository `morse`. Poussez votre code :

```bash
git remote add origin git@github.com:<user.github_nickname>/morse.git
git push origin master
```

## Configuration de Jenkins

Allez sur [jenkins.lewagon.com](http://jenkins.lewagon.com) et connectez-vous avec votre compte GitHub. Si tout se passe bien, vous devriez arriver sur l'écran de connexion suivant.

![](https://res.cloudinary.com/wagon/image/upload/v1560714819/jenkins-after-login_rmgpbu.png)

Cliquez sur "New item" pour créer une nouvelle configuration.

![](https://res.cloudinary.com/wagon/image/upload/v1560714835/jenkins-create-project_ktaqas.png)

Vous devriez arriver sur cet écran :

![](https://res.cloudinary.com/wagon/image/upload/v1560714745/jenkins-add-1_tgeslg.png)

Une fois que "GitHub" a été sélectionné comme source, les choses se compliquent. L'idée est que nous allons fournir un moyen pour Jenkins de :

1. Téléchargez la source depuis GitHub. Pour un repository public, cela peut sembler évident puisque le code est open-source, donc pas besoin d'authentification, n'est-ce pas ? Eh bien, c'est vrai, mais il faudrait supprimer le deuxième élément :
1. Définir le statut de chaque versionnage de chaque branche et de chaque Pull Request, ce qui permet aux développeurs d'être au courant des failles directement depuis GitHub

![](https://res.cloudinary.com/wagon/image/upload/v1560714760/jenkins-add-2_tz9oso.png)

Sélectionnez le projet pour stocker les informations d'identification (et non une configuration globale de Jenkins). Une fenêtre pop-in vous demandant un nom d'utilisateur et un mot de passe s'affichera. **Ne mettez pas votre mot de passe** ici. Allez sur [github.com/settings/tokens](https://github.com/settings/tokens) pour en générer un nouveau.

Vous devez disposer des autorisations suivantes :

- `repo:status`
- `public_repo`
- `read:org`
- `user:email`

![](https://res.cloudinary.com/wagon/image/upload/v1560714771/jenkins-add-3_ebbb5l.png)

![](https://res.cloudinary.com/wagon/image/upload/v1560714784/jenkins-add-4_e7rqs7.png)

Enregistrez la configuration de vos informations d'identification, ce qui fermera la fenêtre. Il est maintenant temps de sélectionner le bon repository GitHub comme source.

![](https://res.cloudinary.com/wagon/image/upload/v1560714797/jenkins-add-5_dtqxan.png)

Enfin, il devrait scanner votre repository à la recherche de branches. Pour chaque branche, il cherchera un `Jenkinsfile`, qu'il ne trouvera pas.

![](https://res.cloudinary.com/wagon/image/upload/v1560714808/jenkins-add-6_yacmsb.png)

### Jenkinsfile

Ajoutons un `Jenkinsfile` à notre projet pour indiquer à Jenkins comment le construire. C'est l'équivalent du fichier `.travis.yml` que nous avions précédemment.

```bash
touch Jenkinsfile
```

Ouvrez ce fichier dans VS Code et copiez-collez la configuration suivante :

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.8'
        }
    }
    environment {
        HOME = "${env.WORKSPACE}"
    }
    stages {
        stage('build') {
            steps {
                sh 'pip install pipenv --user'
                sh '~/.local/bin/pipenv install --dev'
            }
        }
        stage('test') {
            steps {
                sh '~/.local/bin/pipenv run nosetests'
            }
        }
    }
}
```

Comparez ceci au `.travis.yml` que vous aviez dans l'exercice précédent. Quelles sont les similitudes ? Quelles sont les différences ? Discutez-en avec votre buddy.

Avant de versionner et de pousser, nous devons établir le lien entre GitHub et Jenkins en configurant un webhook sur le repository. Allez à l'adresse suivante :

```
https://github.com/<user.github_nickname>/morse/settings/hooks
```

Et cliquez sur le bouton en haut à droite "Add webhook".

Entrez l'URL suivante dans le champ `Payload URL` :
```
http://jenkins.lewagon.com/jenkins/github-webhook/
```

Vous voulez ajouter un Webhook pour les événements suivants :

- Pull Requests
- Pushes

Cela devrait ressembler à ça :

![](https://res.cloudinary.com/wagon/image/upload/v1560714654/github-add-webhook_mtor6z.png)

Cliquez sur le bouton en bas à gauche "Add webhook".
Et voilà ! GitHub signalera à Jenkins chaque fois que vous pousserez ou ouvrirez une Pull Request.

Alors poussons !

```bash
git add Jenkinsfile
git commit -m "Adding Jenkinsfile"
git push origin master
```

Allez sur Jenkins et regardez une compilation **#1** commencer, finir et être **rouge**.

![](https://res.cloudinary.com/wagon/image/upload/v1560714848/jenkins-first-build-red-1_tjtpjz.png)

![](https://res.cloudinary.com/wagon/image/upload/v1560714884/jenkins-first-build-red-2_dkamdz.png)

![](https://res.cloudinary.com/wagon/image/upload/v1560714895/jenkins-first-build-red-3_vxygvy.png)

### Faire passer le projet de Jenkins au vert (bleu)

Jenkins utilise un cercle bleu :large_blue_circle : pour représenter un build réussi et un cercle rouge :red_circle : pour un build échoué. En ce moment, notre branche `master` est rouge sur Jenkins. Nous devons la corriger !

Prenez le temps d'implémenter la fonction `decode(self, message)` dans `morse.py`. Pour exécuter les tests, vous pouvez lancer localement :

```bash
nosetests
```

Coincé ? Demande à ton buddy ! Toujours coincé ? Demande à un TA !

<details><summary markdown='span'>Voir la solution
</summary>

```python
# pylint: disable=missing-docstring

ALPHABET = {
    '.-':   'A',
    '-...': 'B',
    '-.-.': 'C',
    '-..':  'D',
    '.':    'E',
    '..-.': 'F',
    '--.':  'G',
    '....': 'H',
    '..':   'I',
    '.---': 'J',
    '-.-':  'K',
    '.-..': 'L',
    '--':   'M',
    '-.':   'N',
    '---':  'O',
    '.--.': 'P',
    '--.-': 'Q',
    '.-.':  'R',
    '...':  'S',
    '-':    'T',
    '..-':  'U',
    '...-': 'V',
    '.--':  'W',
    '-..-': 'X',
    '-.--': 'Y',
    '--..': 'Z'
}

def decode(message):
    if message == "":
        return ""

    symbols = message.split(" ")
    letters = [ALPHABET[s] for s in symbols]
    return ''.join(letters)
```
</details>

Une fois que votre test est passé localement, il est temps de versionner et de pousser :

```bash
git add morse.py
git commit -m "100% passing tests for one-word Morse decoder"
git push origin master
```

Retournez sur Jenkins, et regardez votre build s'exécuter.

![](https://res.cloudinary.com/wagon/image/upload/v1560714907/jenkins-second-build-green_rb7mxy.png)

Hourra ! Jenkins passe maintenant.

### L'utilisation de Jenkins dans une Pull Request

L'implémentation de notre méthode `decode()` ne prend en charge que les phrases d'un seul mot. Nous n'analysons pas encore le séparateur de mots ` / `. Faisons-le dans une **branche** !


```bash
git checkout -b multi-word-decode
```

Ouvrez le fichier `tests/test_morse.py` et ajoutez le test suivant en bas :

```bash
    def test_whole_sentence(self):
        message = decode(".- .-.. .-.. / -.-- --- ..- / -. . . -.. / .. ... / -.-. --- -.. .")
        self.assertEqual(message, "ALL YOU NEED IS CODE")
```

Retournez au terminal et exécutez les tests :

```bash
pipenv run nosetests
```

Vous devriez avoir 29 tests en exécution et un en échec :

```bash
.........................E...
======================================================================
ERROR: test_whole_sentence (test_morse.TestMorse)
----------------------------------------------------------------------
Traceback (most recent call last):
[...]
----------------------------------------------------------------------
Ran 29 tests in 0.013s

FAILED (errors=1)
```

Avant d'essayer de faire passer ce test au vert en implémentant la fonctionnalité dans le fichier `morse.py`, nous allons versionner et pousser cette branche :

```bash
git add tests/test_morse.py
git commit -m "Adding a multi-word test. Red for now"
git push origin multi-word-decode
```

Retournez sur Jenkins, dans votre projet (ne restez pas dans la branche `master`). L'URL devrait ressembler à quelque chose comme ceci :

```
http://jenkins.lewagon.com/jenkins/me/my-views/view/all/job/<user.github_nickname>-morse/
```

Vous avez maintenant 2 branches ! Et vous pouvez voir que la branche `multi-word-decode` est en fait rouge.

**À votre tour** ! Essayez de passer cette branche au vert en implémentant la fonctionnalité. Si vous êtes bloqué, parlez-en à votre camarade. Demandez de l'aide à un TA.

<details><summary markdown='span'>Voir la solution
</summary>

```python
    # [...]

    def decode(message):
        if message == "":
            return ""

        words = message.split(" / ")
        decoded_words = [decode_word(word) for word in words]
        return ' '.join(decoded_words)

    def decode_word(word):
        symbols = word.split(" ")
        letters = [ALPHABET[s] for s in symbols]
        return ''.join(letters)
```

</details>

Vous pouvez versionner et pousser votre travail sur votre branche :

```bash
git add morse.py
git commit -m "Implement multi-word decoding. All green!"
git push origin multi-word-decode
```

Vous voulez fusionner le `multi-word-decode` (`HEAD`) dans `master` (branche de base). Allez sur GitHub et cliquez sur le bouton "New pull request". Créez la Pull Request et profitez de l'intégration entre Jenkins et GitHub, grâce au webhook **et** à votre token d'accès personnel.

Allez-y et mergez la branche. Retournez sur Jenkins, vous devriez voir `master` compilé une fois de plus (car la fusion d'une branche sur GitHub crée en fait un versionnage supplémentaire, un merge de versionnage). Vous pouvez le voir ici :

```
https://github.com/<user.github_nickname>/morse/network
```

![](https://res.cloudinary.com/wagon/image/upload/v1560714675/github-morse-network_jesjkb.png)

## Conclusion

Comme pour Travis CI, l'ajout de tests à un repository et le couplage de GitHub avec Jenkins permettent au développeur d'avoir l'esprit tranquille lorsqu'il ajoute du code, de vérifier les éventuelles régressions, et d'exercer l'ensemble des tests à _chaque_ versionnage !

Gardez à l'esprit qu'en fonction de votre projet, le `Jenkinsfile` variera. Pour cet exercice, nous utilisons un **Agent Docker** exécuté par Jenkins, avec `pipenv` pour installer les dépendances du `Pipfile` et `nose` comme lanceur de tests. D'autres projets pourraient utiliser une distribution Python comme [Anaconda](https://www.anaconda.com/) et [`tox`](https://tox.readthedocs.io/en/latest/) en tant que gestionnaire de virtualenv / lanceur de tests. Parlez-en avec votre équipe !

## C'est terminé !

Avant de passer à l'exercice suivant, sauvegardez votre avancement avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 02-Best-Practices/05-Optional-Jenkins
touch DONE.md
git add DONE.md && git commit -m "02-Best-Practices/05-Optional-Jenkins done"
git push origin master
```
