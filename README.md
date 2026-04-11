# BACKEND FASTAPI
# Tantsaha Mivarotra - Plateforme de Commerce Agricole

## 📋 Description du Projet
**Tantsaha Mivarotra** est une plateforme web qui connecte directement les **producteurs agricoles** et les **acheteurs** à Madagascar.
Elle élimine les intermédiaires, optimise les déplacements et propose un **matching intelligent** entre offres et demandes.

**Thème** : Numérique Malagasy 2035
**Étudiant** : RAMAHEFASOLO Tojosoa Eric (SE20240335)
**Niveau** : L2 - Projet Transversal ESMIA INNOVATION

## 🚀 Fonctionnalités Principales
- Authentification (Register + Login JWT)
- Gestion des offres et demandes
- **Algorithme de Matching** (scoring glouton basé sur prix, quantité, distance)
- **Calcul d’itinéraire optimal** (Nearest Neighbor TSP)
- **Moteur de recherche rapide** avec Trie (gestion des accents)
- CRUD complet (Create, Read, Update, Delete) avec protection par rôle
- Support multi-régions
- Base de données avec Alembic (migrations)

## 🛠️ Technologies Utilisées
- **Backend** : FastAPI + Python 3.10+
- **Base de données** : PostgreSQL + SQLAlchemy 2.0 + Alembic
- **Authentification** : JWT + Passlib (bcrypt)
- **Algorithmes** :
  - Matching : scoring pondéré + approche gloutonne
  - Routing : Nearest Neighbor (approximation TSP)
  - Recherche : Trie (arbre de préfixes) avec normalisation Unicode
- **Autres** : Pydantic, CORS, dotenv

## 📁 Structure du Projet
app/
├── core/          → config, database, security
├── models/        → SQLAlchemy models
├── schemas/       → Pydantic models
├── routers/       → routes API
├── algorithms/    → matching, routing, trie
├── crud/          → opérations CRUD génériques
└── main.py
alembic/           → migrations


## 🧪 Données de Test (prêtes à utiliser)

Voir la section **Données de Test** plus bas dans ce README.

## ▶️ Installation et Lancement

```bash
# 1. Cloner le projet
git clone <ton-repo>
cd backend

# 2. Créer l'environnement
python -m venv venv
source venv/bin/activate    # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer la base de données
# Créer une base PostgreSQL nommée "tantsaha_db"
# Puis modifier le .env :
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/tantsaha_db

# 5. Appliquer les migrations
alembic upgrade head

# 6. Lancer le serveur
uvicorn app.main:app --reload
Accéder à la documentation : http://127.0.0.1:8000/docs
