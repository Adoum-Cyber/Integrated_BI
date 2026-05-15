# Integrated BI Platform — Sotifibre

> **Projet de Fin d'Études (PFE) — 2026**
> Plateforme de Business Intelligence complète pour l'analyse de données d'entreprise

---

## Aperçu

**Integrated BI** est une plateforme de Business Intelligence full-stack conçue pour centraliser, transformer et visualiser les données métier de SOTIFibre. Elle couvre l'ensemble du cycle de vie de la donnée : ingestion, transformation ETL, modélisation dimensionnelle, visualisation, alertes et rapports automatisés.

---

## Stack Technique

### Backend
| Technologie | Version | Rôle |
|-------------|---------|------|
| Python | 3.12 | Langage principal |
| Django | 6.0.3 | Framework web |
| Django REST Framework | 3.17.0 | API REST (349 endpoints) |
| PostgreSQL | 18.3 | Base de données principale |
| Simple JWT | 5.5.1 | Authentification JWT (access + refresh) |
| drf-spectacular | 0.29.0 | Documentation OpenAPI 3.0 |
| Celery + Beat | 5.6.2 / 2.9.0 | Tâches planifiées et workflows asynchrones |
| django-import-export | 4.4.0 | Import/export CSV/Excel dans l'admin |
| Jazzmin | 3.0.4 | Thème admin Django professionnel |

### Frontend
| Technologie | Version | Rôle |
|-------------|---------|------|
| Vue 3 | 3.5.34 | Framework UI (Composition API) |
| TypeScript | 6.0.2 | Typage statique |
| Vite | 8.0.12 | Bundler |
| Pinia | 3.0.4 | Gestion d'état |
| Vue Router | 4.6.4 | Routage SPA |
| Axios | 1.16.0 | Client HTTP |
| lucide-vue-next | 1.0.0 | Bibliothèque d'icônes |
| Chart.js | 4.5.1 | Graphiques et visualisations |

### Infrastructure
| Composant | Détail |
|-----------|--------|
| Serveur | Ubuntu 22.04 LTS |
| IP Backend | 192.168.224.128:8000 |
| Gestionnaire de paquets | uv (Python) + npm (Node) |
| Admin Django | Jazzmin (thème personnalisé SOTIFibre) |

---

## Architecture

```
Integrated_BI/
├── sotifibre_backend_django/    # API Django
│   ├── apps/
│   │   ├── core/               # Config système
│   │   ├── users/              # Utilisateurs, rôles, équipes
│   │   ├── data_sources/       # Sources de données, connexions DB, fichiers
│   │   ├── data_warehouse/     # Entrepôt, tables de faits/dimensions, mesures
│   │   ├── etl_engine/         # Pipelines ETL, transformations, exécutions
│   │   ├── star_schema/        # Schémas dimensionnels, Galaxy, hiérarchies
│   │   ├── ml_analytics/       # Modèles ML, prévisions, anomalies
│   │   ├── visualizations/     # Dashboards, KPIs, rapports, widgets
│   │   └── notifications/      # Alertes, canaux, abonnements
│   └── config/                 # Settings, URLs, WSGI
└── integrated-bi-frontend/     # SPA Vue 3
    └── src/
        ├── views/              # 22 pages complètes
        ├── stores/             # Pinia (auth)
        ├── router/             # Vue Router
        ├── api/                # Axios instance
        └── assets/             # Design system (CSS tokens)
```

---

## Fonctionnalités

### Backend — 8 applications Django, 77+ modèles, 349 endpoints REST

| Application | Modèles clés |
|-------------|-------------|
| `core` | Config système |
| `users` | User, Role, Team, AuditLog |
| `data_sources` | DataSource, DataTable, Connection, DataFile |
| `data_warehouse` | DataWarehouseTable (FactTable/DimensionTable proxy), Measure, Aggregation |
| `etl_engine` | ETLPipeline, Transformation, Execution, SourceSchema, TargetSchema |
| `star_schema` | DimensionalSchema, GalaxySchema, FactRelationship, DimensionHierarchy, CustomCalculation |
| `ml_analytics` | MLModel, Forecast, Anomaly, SegmentationResult, Recommendation, ModelTrainingLog |
| `visualizations` | Dashboard, Widget, KPI, Report, Favorite, VisualizationActivity |
| `notifications` | Notification, AlertRule, NotificationChannel, Subscription |

### Frontend — 22 pages complètes

| # | Page | Route | Description |
|---|------|-------|-------------|
| 1 | Login | `/login` | Authentification JWT |
| 2 | Dashboard | `/` | KPIs temps réel + graphiques |
| 3 | Sources de données | `/sources` | CRUD sources + tables de données |
| 4 | Monitoring source | `/sources/:id/monitoring` | Logs + métriques de synchronisation |
| 5 | Power Queries | `/sources/power-queries` | Requêtes visuelles avancées |
| 6 | Requêtes SQL | `/sources/queries` | Éditeur SQL interactif |
| 7 | Connexions DB | `/sources/connections` | CRUD connexions base de données + test |
| 8 | Fichiers de données | `/sources/files` | Upload, prévisualisation, traitement |
| 9 | Pipelines ETL | `/pipelines` | Orchestration ETL complète |
| 10 | Exécutions ETL | `/executions` | Historique et monitoring des runs |
| 11 | Data Warehouse | `/warehouse` | Explorer tables faits/dimensions + agrégations |
| 12 | Schémas étoile | `/star-schema` | Modélisation dimensionnelle + Galaxy |
| 13 | ML Analytics | `/ml-analytics` | Modèles, prévisions, anomalies, recommandations |
| 14 | Visualisations | `/visualizations` | Galerie de visualisations |
| 15 | Tableaux de bord | `/dashboards` | Dashboards + widgets |
| 16 | KPIs | `/kpis` | Indicateurs clés de performance |
| 17 | Rapports | `/reports` | Génération et planification CRON |
| 18 | Notifications | `/notifications` | Alertes, canaux, abonnements |
| 19 | Administration | `/admin` | Utilisateurs, rôles, équipes, audit |
| 20 | Profil | `/profile` | Profil utilisateur |
| 21 | Favoris | `/favorites` | Favoris personnels |
| 22 | Système | (dans Admin) | Liens admin Django, Celery Beat |

---

## Design System

| Token | Valeur |
|-------|--------|
| Font UI | Figtree |
| Font titres | Barlow Condensed |
| Couleur accent | oklch(76% 0.14 62) — ambre chaud |
| Surfaces | Navy-slate sombre |

---

## Démarrage rapide

### Backend
```bash
cd sotifibre_backend_django
uv sync
uv run python manage.py migrate
uv run python manage.py runserver 0.0.0.0:8000
```

### Frontend
```bash
cd integrated-bi-frontend
npm install
npm run dev
```

### Admin Django
- URL : http://192.168.224.128:8000/admin/
- Documentation API : http://192.168.224.128:8000/api/schema/swagger-ui/

---

## Endpoints API

### Authentification
| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/api/auth/jwt/token/` | Obtenir access + refresh token |
| POST | `/api/auth/jwt/refresh/` | Rafraîchir le token |

### Principaux préfixes
| Préfixe | Application |
|---------|-------------|
| `/api/users/` | Utilisateurs, rôles, équipes |
| `/api/data-sources/` | Sources, connexions, fichiers, tables |
| `/api/etl/` | Pipelines, transformations, exécutions |
| `/api/data-warehouse/` | Entrepôt de données |
| `/api/star-schema/` | Schémas dimensionnels |
| `/api/ml-analytics/` | Analyses ML |
| `/api/visualizations/` | Dashboards, KPIs, rapports |
| `/api/notifications/` | Alertes et notifications |

---

*Réalisé dans le cadre du PFE — Abdoulaye Adoum, 2026*
