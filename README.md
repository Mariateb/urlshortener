# URL SHORTENER
   
## Description   
Ce projet permet de raccourcir une URL.    
L'utilisateur a accès à un formulaire où il peut entrer une URL et reçoit une clé. Grâce à cette clé, il peut être redirigé sur l'URL raccourcie.   
   
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
