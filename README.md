# CyberGuard

CyberGuard est un forum web orienté cybersécurité développé en Python avec Flask.
Le projet sert de plateforme de discussion pour partager des sujets liés à la sécurité informatique, tout en intégrant des bonnes pratiques DevSecOps comme l’analyse SAST, DAST et le scan de vulnérabilités dans une pipeline CI/CD.

Le projet met l’accent sur :

- la sécurité applicative
- la conteneurisation
- l’automatisation des tests de sécurité
- une architecture simple et pédagogique

## Architecture du projet
```
cyberguard/
│
├── Dockerfile
├── docker-compose.yml
├── LICENSE.txt
├── README.md
├── requirements.txt
├── run.py
├── .gitignore
│
├── app/
│ ├── init.py
│ ├── models.py
│ └── routes.py
│
├── templates/
│ ├── base.html
│ ├── category.html
│ ├── create_topic.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── secret.html
│ └── topic.html
│
└── static/
├── Cynatar.woff2
├── Guardians.ttf
├── image1.png
├── image2.png
├── image3.png
├── 1383930.png
├── audio.js
└── style.css
```

## Technologies utilisées

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML
- CSS
- JavaScript

### DevOps / Sécurité
- Docker
- GitHub Actions
- SAST
- DAST
- Container scanning

### Outils de sécurité intégrés dans la pipeline
- Bandit
- Flake8
- pip-audit
- Gitleaks
- Trivy
- Nikto
- OWASP ZAP

## Fonctionnalités

### Authentification
- Inscription utilisateur
- Connexion
- Inscription utilisateur / Google Oauth
- Connexion / Google Oauth
- Déconnexion sécurisée
- Protection CSRF
- Sessions sécurisées

### Forum
- Création de topics
- Réponses aux topics
- Catégories
- Limitation de taille des messages
- Protection contre les requêtes trop lourdes

### Sécurité
Implémentations actuelles :
- CSP (Content Security Policy)
- CSRF protection
- gestion sécurisée des sessions
- validation des entrées utilisateur
- limitation de taille des requêtes
- suppression des fichiers sensibles (.env, db locale)

### Divers
- thème graphique personnalisé
- musique d’ambiance
- easter egg
- dockerisation complète de l’application

## Installation

### Installation locale

#### Cloner le projet

```bash
git clone https://github.com/Shrekye/CyberGuard.git
cd CyberGuard
```

Installer les dépendances

```bash
pip install -r requirements.txt
```

Lancer l'application

```bash
python run.py
```
Application disponible sur : http://localhost:5000

--- 

### Lancer avec Docker

#### Build de l'image

```bash
docker build -t cyberguard .
```

#### Lancer le container

```bash
docker run -p 5000:5000 cyberguard
```
#### Ou avec docker-compose :

```bash
docker swarm init
docker build -t cyberguard:latest .
docker stack deploy -c docker-compose.yml cyberguard
```

## CI/CD et DevSecOps

Le projet intègre une pipeline de sécurité automatisée.

### Étapes principales

1. **Secret scan** - gitleaks

2. **Linting** - flake8

3. **Analyse SAST** - bandit

4. **Scan de dépendances** - pip-audit

5. **Scan de secrets** - gitleaks

6. **Scan du filesystem** - trivy

7. **Build de l'image Docker**

8. **Scan de l'image container** - trivy image scan

9. **DAST** - nikto, zap baseline scan

**Objectif :** appliquer le principe Shift Left Security.

## Sécurité implémentée dans l'application

- CSRF token custom
- Content Security Policy
- limitation de taille des messages
- validation des formulaires
- gestion sécurisée des sessions
- suppression des secrets du dépôt
- scan automatique des vulnérabilités

## Roadmap

### Fonctionnalités à ajouter

- page compte utilisateur
- suppression du compte
- changement de mot de passe
- récupération de mot de passe
- upload d’images dans les topics
- amélioration du système de chat

### Améliorations techniques

- intégration de Ruff
- amélioration de la pipeline CI/CD
- correction des rapports ZAP
- optimisation du frontend
- volumes pour la db

## Difficultés rencontrées

Des exemples de difficultés rencontrées lors des différentes phases de développement du projet sont renseignés dans les fichiers suivants :

- `difficulties.md`
- ...

---

## Licence

Projet sous licence présente dans `LICENSE.txt`