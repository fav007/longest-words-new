# GitHub Flow

Commençons la journée en suivant le **GitHub flow** du tout début jusqu'au déploiement. Nous allons déployer une page HTML très simple pour nous concentrer sur l'apprentissage de `git` et GitHub plutôt que sur le code Python.

## Un peu de lecture

En 2011, Scott Chacon, l'un des premiers fondateurs de GitHub, a écrit un [article de blog](http://scottchacon.com/2011/08/31/github-flow.html) où il a présenté pour la première fois le concept de flow Github. Historiquement, il voulait quelque chose de plus simple qu'une autre méthodologie connue nommée [_git flow_](https://nvie.com/posts/a-successful-git-branching-model/) (ce n'est pas la même chose !).

GitHub a mis en place un [joli petit guide](https://guides.github.com/introduction/flow/) que vous pourriez lire.

## Pour commencer

Avant de faire notre premier versionnage, nous devons créer un repository GitHub !

1. Connectez-vous à GitHub
1. Allez sur [github.com/new](https://github.com/new) et créez un repository _public_  sur votre compte _personnel_ , nommez-le `github-flow`.
1. Allez dans votre terminal et créez un nouveau repository local. Ajoutez GitHub comme `origin` remote :

```bash
mkdir -p ~/code/<user.github_nickname>/github-flow && cd $_

git init
touch README.md
touch index.html
git add .
git commit -m "Initialize repository"

git remote add origin git@github.com:<user.github_nickname>/github-flow.git

git push origin master
```

Allez sur [github.com](https://github.com) et rafraîchissez la page de votre repository. Vous devriez voir le versionnage et les deux fichiers !

## Votre première Pull Request

Commençons à travailler sur ce repository. Avant de toucher au code, nous devons créer une **branche de fonctionnalité** (branche feature). Notre objectif ici est d'ajouter un squelette HTML de base au projet. Allons y :

```bash
git checkout -b html-skeleton
```

Ces commandes _créent_ la branche et _s'y connectent_. Vous pouvez voir que l'invite de commande Git Bash est mise à jour et n'affiche plus `master`. Vous êtes donc prêt à coder dans cette branche !

```bash
code .
```

Ouvrez le fichier `index.html` et écrivez du code HTML.

<details><summary markdown='span'>Un peu d'inspiration
</summary>

👉 Voici quelques [inspirations](https://gist.github.com/ssaunier/faa9965201153555bc954fb4713eea7c) si besoin.
</details>

Vous pouvez ouvrir ce fichier dans Chrome, puis cliquer sur le bouton "Raw". Vous pouvez maintenant copier le code html et le mettre dans votre propre fichier `index.html`.
Vous avez maintenant un exemple à modifier.

Lorsque vous êtes satisfait de votre code et de la façon dont il s'affiche dans le navigateur, il est temps de versionner !

```bash
git status # Quels fichiers ont été modifiés ?
git diff index.html # Quels changements ont été effectués ?

git add index.html
git commit -m "Add basic skeleton HTML"
```

Le versionnage est maintenant fait localement. Il est temps de pousser. Quelle sera la commande ?

<details><summary markdown='span'>Voir la solution
</summary>

```bash
git push origin html-skeleton
```
</details>

Accédez maintenant à votre repository sur GitHub et rafraîchissez la page. Vous devriez voir ceci :

![](https://res.cloudinary.com/wagon/image/upload/v1560714729/html-skeleton-pr-suggestion_ilh5o4.png)

Cliquez sur le bouton vert pour créer votre première pull request.

### Relecture

Vous avez maintenant besoin de quelqu'un pour examiner votre code, donner son avis et éventuellement le merger (une des règles dans l'utilisation  GitHub flow est que quelqu'un d'autre que l'auteur doit merge une Pull Request).

Rendez-vous sur `github.com/<user.github_nickname>/github-flow/settings/collaboration` (accessible par `Settings` > `Collaborators`) et ajoutez votre voisin de table au repository en lui demandant son nom sur GitHub. Il devrait recevoir une invitation par e-mail à accepter.

Une fois cette configuration effectuée, demandez-leur d'aller sur la page Pull Request (qui devrait être PR #1) et de revoir le code. S'ils ont des commentaires (indentation, erreur, etc.), c'est que vous devez faire quelques corrections : retournez dans VS Code, dans la même branche, mettez à jour le code et faites un autre versionnage. Poussez ce versionnage sur GitHub : vous verrez que la Pull Request se met automatiquement à jour !

A la fin, si vous et votre relecteur êtes d'accord sur le code, le relecteur doit **merger** la Pull Request. Après le merge, il y a un bouton "Delete branch". Nous vous conseillons de cliquer dessus, car dans le GitHub flow, une branche **mergée est une branche morte** et plus rien ne doit être pushé sur cette branche désormais.

### Que se passe-t-il ensuite ?

Merger une Pull Request sur GitHub permet de créer un merge de versionnage sur la branche `master`. Cela signifie que votre repository local sur votre ordinateur n'est plus à jour.

Voici ce que vous devez faire :

```bash
# Retournez sur la branche
git checkout master

# Mettez votre branche `master` à jour avec GitHub
git pull origin master

# La branche de fonctionnalité est morte. Supprimez-la ! Gardez un repo vide
git branch -d html-skeleton
```

C'est tout ! Vous êtes prêt à travailler sur la prochaine fonctionnalité sur une nouvelle branche. Recommencez à l'étape `git checkout -b <branch>`.

## S'améliorer par la pratique

Prenez le temps de vous entrainer avec ce flow. Par exemple, vous pouvez créer les branches de fonctionnalités suivantes :

- `add-basic-css-style`
- `add-background-image`
- ...

Rappelez-vous, c'est toujours le même flow :

```bash
# IMPORTANT : Commencez depuis `master` avec un `git status` **vide**.

git checkout -b $FEATURE_BRANCH

# Écrivez du code

git status # Quels fichiers ont été modifiés ?
git add <file1> <file2> ...
git commit -m "Quickly describe to your teammates what you did here"
git push origin $FEATURE_BRANCH

# Allez sur github.com - Ouvrez une Pull Request. Demandez à votre buddy de la relire

# Faites d'autres versionnages sur la branche avec les commentaires de votre buddy

# Votre budy est satisfait des modifications apportées et il **merge** la Pull Request.

git status # ⚠️ Assurez-vous qu'il n'y a pas de travail en attente avant de changer de branche !
git checkout master
git pull upstream master
git branch -d $FEATURE_BRANCH

# Recommencez !
```

## Bonus - GitHub Pages

Si vous avez un simple site **statique** à héberger, GitHub propose une excellente solution : [GitHub Pages](https://pages.github.com/). Vous pouvez transformer un repository en un fournisseur d'hébergement !

Il est très simple à activer. Dans votre repository `github-flow`, allez dans `Settings` > `Options` et scrollez vers le bas jusqu'à ce que vous atteigniez la section `GitHub Pages` juste avant `Danger Zone`.

Sous la rubrique `Source`, cliquez sur la liste déroulante et sélectionnez la branche `master`. Cliquez ensuite sur `Save`.

![](https://res.cloudinary.com/wagon/image/upload/v1560714628/enable-github-pages_w5clbv.png)

Cela va recharger la page. Si vous scrollez vers le bas, vous devriez voir la phrase : Your site is ready to be published at:...  Et voilà, vous y êtes ! L'URL de votre site :

```bash
https://<user.github_nickname>.github.io/$REPO_NAME/
```

Chaque fois qu'un versionnage se produit dans `master` (par le biais d'une Pull Request en utilisant le GitHub flow), GitHub Pages va automatiquement déployer les changements sur cette URL. Avec cette configuration, le bouton `Merge` dans une Pull Request devient un bouton **Deploy**.

Si vous possédez un nom domaine, vous pouvez le mettre en place avec la configuration du [`CNAME`](https://help.github.com/articles/using-a-custom-domain-with-github-pages/) via GitHub Pages.

## Dernières réflexions

La puissance du flow GitHub vient du fait qu'il est accessible même aux débutants de `git`. `git` est un outil très puissant et peut être intimidant s'il n'est pas introduit correctement. Avec ce flow, n'importe qui dans l'équipe peut s'approprier le processus de collaboration avec un peu d'entraînement (ce que vous venez de faire !) et en apprenant ces quelques commandes : `status` (et `diff`), `checkout -b`, `add`, `commit -m`, `push`, `checkout`, `pull`, `branch -d` et c'est tout.

Si vous discutez de `git` avec d'autres développeurs, certains concepts avancés pourront être évoqués, comme `stash`, `cherry-pick`, `rebase`, `reset` ou `reflog`. Vous aurez le temps d'en apprendre plus sur ces sujets (`stash` étant à notre avis le plus facile et le plus utile) et d'adapter vos connaissances à votre équipe. Nous ne couvrirons pas ces sujets mais au moins vous avez quelques mots-clés à chercher sur Google !

## C'est terminé !

Avant de passer à l'exercice suivant, sauvegardez votre avancement avec ce qui suit :

```bash
cd ~/code/<user.github_nickname>/reboot-python
cd 02-Best-Practices/01-Github-Flow
touch DONE.md
git add DONE.md && git commit -m "02-Best-Practices/01-Github-Flow done"
git push origin master
```
