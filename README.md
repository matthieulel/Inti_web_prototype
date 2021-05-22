<h1 align="center"> INTI</h1>

INTI est une application Web qui traite les fichiers SER vidéo pour générer une image monochromatique du soleil, avec toutes les corrections appliquées de manière entièrement automatique.

<br/>

# Comment ça fonctionne ?

Une seule action : ajoutez votre fichier video .ser en cliquant sur le bouton uploads.
Vos pouvez directement télécharger les résultats du traitement.

<br/>

# Utilisation en ligne

L'application est utilisable en ligne à l'adresse suivante : [https://inti-solex.herokuapp.com](https://inti-solex.herokuapp.com)


<br/>

# Utilisation sur machine personnelle

Les fichiers .ser peuvent parfois devenir très volumineux. Cette taille de fichier associé à une connexion internet potentiellement variable peut entraîner des chargements très longs.

Il est possible d'utiliser INTI tel quel sur sa machine personnelle grâce au container docker qui a été créé pour réduire les temps de traitements.

## Docker ?
Docker est un logiciel libre permettant de lancer des applications dans des conteneurs logiciels. Cela permet dans notre cas d'utiliser INTI (développé en Python), sans avoir à installer Python et les modules nécessaires sur notre machine. Plus d'informations ici :  [Docker - Wikipedia](https://fr.wikipedia.org/wiki/Docker_(logiciel)


<br/>

## 1 - Installer Docker Desktop

Se rendre à cette adresse, télécharger et installer Docker Desktop : https://www.docker.com/products/docker-desktop


Sur windows10, il est parfois demandé d'installer la nouvelle version du WSL2 comme l'image 1.1 ci-dessous)

![1.1-pull_container](https://github.com/Vdesnoux/Inti/tree/main/docs/container/wsl2_install.png "1.1")


<br/>

## 2 - Lancer Docker Destop

 Une fois installé, lancez Docker Desktop. Une fois le Docker Engine démarré, la baleine doit être en vert, comme l'image 2.1 ci-dessous.

![2.1-pull_container](https://github.com/Vdesnoux/Inti/tree/main/docs/container/docker_started.png "2.1")


<br/>

 ## 3 - Télécharger le container

 Lancer une Invite de commande (pour Windows) ou un terminal (sur Linux & Mac) et télécharger le container en tapant cette commande :

```bash 
 docker pull matthieulel/inti_flask
```

![3.1-pull_container](https://github.com/Vdesnoux/Inti/tree/main/docs/container/docker_pull_inti_flask.png "3.1")


Voici ce que vous devriez avoir une fois le téléchargement terminé.

![3.2-pull_result](https://github.com/Vdesnoux/Inti/tree/main/docs/container/docker_pull_finish.png "3.2")



## 4 - Lancer l'application

Pour lancer l'application INTI, il faut lancer le container avec cette commande, toujours dans l'invite de commande (Windows) ou le terminal (Linux/Mac) : 

```bash
docker run -p 5000:5000 matthieulel/inti_flask
```

![4.1-launch_application](https://github.com/Vdesnoux/Inti/tree/main/docs/container/launch_inti_flask.png "4.1")



Il est également possible de lancer le container en utilisant l'application Docker Desktop, dans le menu Image. Il suffit de cliquer sur le bouton RUN de l'image correspondant à inti_flask, et de renseigner le port sur 5000, comme le montre l'image 4.2 ci-dessous.

![4.1-launch_application](https://github.com/Vdesnoux/Inti/tree/main/docs/container/launch_from_desktop.png "4.2")



## 5 - Accéder à l'application

Pour accéder à l'application, ouvrez un navigateur et tapez l'adresse suivante : 127.0.0.1:5000

![5.1-access_application](https://github.com/Vdesnoux/Inti/docs/container/result.png "5.1")

Il est également possible d'y accéder en appuyant sur le bouton "Open in browser" dans le menu Container de docker engine, sur notre inti_flask.

Enjoy.

