# artifact-fetcher
## Description
Script personnel me permettant de palier au soucis de récupération des artifacts de mes projets dans mon réseau professionnel.
Lors de construction d'un projet Alfresco (./run build_start), celui-ci var chercher les artifact en dépendences du POM sur notre réseau en intene de manière parallèle. Celui-ci, ne répondant pas toujours, (parce qu'il y a trop d'appels, ou autre raison...) la construction du projet s'arrête parce qu'il n'a pas réussi à charger les amps du projet. 
Ce script est dans un premier temps là pour résoudre à ce problème de non récupération d'un artifact et ses dépendences car le lancement (une seconde fois) du build n'assure pas la récupération des amps manquant m'obigeant de vérifer et récupérer à la "main" l'existence de l'artifact et son rapatriement sur ma machine de développement.
## Fonctionnement
### Récupération d'un artifact manquant
C'est pour le moment un script réservé pour windows (car il répond à mon besoin de développment sur mon environnement de travail)
