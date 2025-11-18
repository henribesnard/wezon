# Tâches restantes pour finaliser le backend

Ce dépôt fournit un squelette FastAPI. Les tâches ci-dessous décrivent ce qu'il reste à implémenter pour rendre le backend pleinement fonctionnel.

## Pipelines et agents IA
- [ ] Agent d'ingestion RSS/web : collecter les articles, détecter la langue, normaliser les métadonnées, et alimenter la base via SQLAlchemy (modèles dans `app/models.py`).
- [ ] Classification/catégorisation automatique : enrichir les articles avec `ArticleCategory` et `ArticleEntity` à partir de NLP (NER, taxonomie métiers).
- [ ] Traduction et détection de langue : aligner les textes sources et populater `ArticleTranslation` selon les langues cibles.
- [ ] RAG pour `/chat` : connecter la recherche vectorielle (`Settings.vector_store_url`) et un LLM ; construire les prompts et gérer le reranking.
- [ ] Résumés quotidiens : orchestrer la génération de `DailySummary` (par pays/région/thème) à partir des articles ingérés.

## Orchestration & stockage
- [ ] Orchestrateur de tâches (ex. Celery/RQ) branché sur Redis (`Settings.redis_url`) pour planifier l'ingestion, les résumés et la mise à jour des index vectoriels.
- [ ] Gestion des files/états de jobs dans `/health` avec des métriques réelles plutôt qu'un statut `pending` statique.
- [ ] Migrations et schéma : ajouter des migrations (Alembic) et scripts de bootstrap (tables de référence pays/langues/sources).
- [ ] Indexation vectorielle : pipeline d'embedding des articles, synchronisation avec le store (`Settings.vector_store_url`), et stratégie d'upsert/suppression.

## API et sécurité
- [ ] Authentification admin durable : remplacer le token statique `X-Admin-Token` par des JWT signés (`Settings.admin_jwt_secret`) avec rotation/expiration.
- [ ] Validation et pagination avancées sur `/articles` et `/daily-summaries` (limites, tri, offsets sécurisés).
- [ ] Gestion des erreurs cohérente (schémas d'erreurs, codes HTTP, journalisation structurée) sur tous les routeurs de `app/api`.

## Observabilité et QA
- [ ] Journalisation structurée et corrélation (trace IDs) pour les appels aux agents et au LLM.
- [ ] Metrics/alerts (Prometheus, OpenTelemetry) pour suivre ingestion, RAG, latence des dépendances externes.
- [ ] Tests unitaires et d'intégration (FastAPI + DB + vector store) couvrant les routes et services.

## Variables d'environnement à renseigner
Utiliser les variables déjà déclarées dans `app/core/config.py` et les renseigner dans `.env` :
- `APP_NAME`
- `DATABASE_URL`
- `REDIS_URL`
- `VECTOR_STORE_URL`
- `ADMIN_JWT_SECRET`

Ajouter au besoin des variables supplémentaires (ex. credentials LLM, clés API de recherche web) en étendant `Settings` sans modifier les valeurs par défaut ici.
