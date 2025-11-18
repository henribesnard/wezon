# Wezon Backend Skeleton

Ce dépôt contient une première ossature FastAPI alignée avec les spécifications
fonctionnelles et techniques fournies (agrégation d'actualités africaines,
chatbot RAG, administration des sources). Le code fournit des modèles SQLAlchemy,
des schémas Pydantic et des routeurs prêts à être branchés aux agents
(d'ingestion, RAG, résumé, etc.).

## Structure

- `app/main.py` : instancie l'application FastAPI et monte les routeurs.
- `app/core/config.py` : configuration (PostgreSQL, Redis, vector store, secret admin).
- `app/core/database.py` : moteur SQLAlchemy asynchrone et dépendance de session.
- `app/models.py` : tables `countries`, `languages`, `sources`, `articles`,
  `article_categories`, `article_entities`, `article_translations`,
  `daily_summaries`.
- `app/schemas.py` : schémas d'E/S pour les endpoints publics et admin.
- `app/api/` : routeurs FastAPI pour les articles, résumés quotidiens, chatbot,
  sources et santé.
- `app/services/` : services applicatifs minimalistes pour préparer l'arrivée des
  agents (ingestion, classification, RAG, etc.).

## Endpoints exposés

- `GET /health` : sonde basique.
- `GET /articles` et `GET /articles/{id}` : lecture avec filtres.
- `GET /daily-summaries` : accès aux résumés quotidiens.
- `POST /chat` : stub de réponse orchestrée (RAG + web dans la version finale).
- `GET /sources` : liste publique des sources.
- `POST /admin/sources` et `PUT /admin/sources/{id}` : gestion des sources avec
  un jeton admin temporaire (`X-Admin-Token`).

## Lancement local

1. Installer les dépendances principales (à titre indicatif, sans modifier de
   fichier `requirements.txt`) :
   - `fastapi`
   - `uvicorn[standard]`
   - `sqlalchemy[asyncio]`
   - `asyncpg`
   - `pydantic-settings`

2. Exporter les variables d'environnement si besoin (`DATABASE_URL`, `REDIS_URL`,
   `VECTOR_STORE_URL`, `ADMIN_JWT_SECRET`).

3. Démarrer l'API :
   ```bash
   uvicorn app.main:app --reload
   ```

Les futures étapes consistent à connecter les agents décrits dans la
"Spécification Technique Complète" (ingestion RSS/web, classification,
traduction, RAG, génération de résumés) et à enrichir les services pour
orchestrer ces pipelines.
