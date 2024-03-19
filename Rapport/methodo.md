# URL SHORTENER

## Description

Ce projet permet de raccourcir une URL.    
L'utilisateur a accès à un formulaire où il peut entrer une URL et reçoit une clé. Grâce à cette clé, il peut être
redirigé sur l'URL raccourcie.

## Technique

Langage/Framework: Python, FastAPI   
Base de données: SQlite

## Demande client

Dans un premier temps, un utilisateur peut raccourcir une URL. On garde l'URL raccourcie pendant 6 mois.

Les étapes suivantes:

- Choisir la durée pendant laquelle l'URL est stockée
- Connexion utilisateur
- Historique, un utilisateur connecté peut consulter les URLs qu'il a raccourcies
- Nombre de vues, un utilisateur connecté peut voir combien de personnes ont cliqué sur ses liens raccourcis

Un utilisateur connecté peut choisir entre 1 mois et 10 ans, pour les utilisateurs anonymes c'est 6 mois.

## Notre méthodologie

Il y avait un scrum master: Yacine.
Au milieu du sprint on organise un daily scrum. C'est l'occasion de faire un point sur l'avancement de chacun,
ce qu'il reste à faire et de se mettre d'accord sur l'implémentation.  
Nous avons utilisé Git pour gérer le projet. Nous avons décidé que chaque ticket avait sa branche.
Lorsque le développement est fini le scrum master relit la pull request (PR). Si c'est ok elle est mergée,
sinon elle est renvoyée en correction avec quelques commentaires pour expliquer ce qui ne va pas.  
Conditions pour qu'une PR soit validée: 
- code propre
- respect des conventions de nommage
- respect de l'architecture de l'application  

