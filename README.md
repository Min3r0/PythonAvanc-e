# PythonAvanc-e

# 🐌 ESCARGOT HACK – Mini-jeu IA

## 🎬 Introduction

Bienvenue dans **Escargot Hack**, une aventure interactive en plusieurs étapes mêlant **cryptographie**, **scraping**, **API secrète**, **Serveur socket**, et **intelligence artificielle**.

Le hacker masqué connu sous le nom de *S-Car-Go* a corrompu le jeu **jeu.fr** en truquant les courses d’escargots pour favoriser le rouge. Ton objectif : pirater le hackeur, restaurer le jeu et libérer les escargots ! 🐌⚡

Chaque étape du jeu est un mini-challenge technique. Pour progresser, tu devras fouiller du HTML, décrypter, , bidouiller des requêtes API, répondre à un QCM très très dur..  et battre L'IA qui pour le coup est vraiment nulle..
Prouvons que nous sommes meilleur que l'IA ( si tu perds une partie ca craint, tu peux arreter le mini-jeu..)

---

## 🧩 Étapes du scénario

### 🔐 ÉTAPE 1 – Github

Tu devras avoir besoin d'un IDE et de clone notre code que tu trouveras ici : https://github.com/Min3r0/PythonAvanc-e/tree/mdp

/!\ PLUSIEURS BRANCHES sont présentes , choisis la bonne à utiliser (mdp)

Une fois que tu auras trouver la bonne branche tu n'as plus qu'à lancer l'aventure ( petite aide => Ouvre un terminal => python app.py )

Un fichier `escargot_hacked.zip` est trouvé dans le cache du navigateur de jeu.fr. Il contient un message chiffré. Tu devras :

- Lire `message_chiffre.txt`
- Utiliser `decrypt_zip.py` pour le déchiffrer :
  - Vigenère (clé : `escargot`)
  - César (décalage : 3)
  - Base64
- Obtenir une URL locale vers une fausse page HTML

---

### 🌐 ÉTAPE 2 – Scraping de la page HTML

L’URL mène vers une copie locale piégée du site de notre enfance. Patience, jeune Padawan.. un jeu secret tu trouveras. (◕‿◕)🟢

Etapes
- Analyse la page et trouve le bon jeu 
- Avant de démarrer la course, tu es l'escargot bleu et l'IA l'escargot rouge. Elle IrA toujours plus vite que toi sauf si tu gagnes le morpion.
- Lance la course et depeche toi de gagner le morpion ! PENDANT ! la course 

Bravo tu as gagné !! Enfin je l'espère... 

---

### 🔌 ÉTAPE 3 – Server Socket , Rasta Rockett

Petit QCM histoire de se détendre apres cette course plus rapide que Usain Bolt.



- Lancer `app.py` (API Flask)
- Faire une requête POST vers `/api/snail-race/start` avec le header :
