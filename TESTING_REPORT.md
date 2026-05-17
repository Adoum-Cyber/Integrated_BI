# Rapport de tests automatisés — Integrated BI Platform

## Synopsis

Tests end-to-end exécutés via **TestSprite MCP** contre la plateforme déployée sur Render :
- Frontend : `localhost:5173` (vite preview, production build) → backend prod
- Backend : `https://sotifibre-backend.onrender.com`

Couverture : **30 tests fonctionnels** (suite complète d'un plan de 50).

## Évolution du score

| Itération | Tests passés | Taux | Commentaire |
|---|---|---|---|
| Run initial | 23 / 30 | 76,67 % | 6 fails identifiés, 1 blocked (data) |
| Run après fixes round 1 | 25 / 30 | 83,33 % | 3 fixes immédiats validés |
| Run après fixes round 2 | 28 / 30 | **93,33 %** | 2 fixes supplémentaires validés |

## Détail des 6 défauts initiaux et de leur traitement

### ✅ TC017 — Édition d'un pipeline ETL
- **Symptôme** : la sauvegarde d'un pipeline existant échouait, et un nouveau planning cron ne s'affichait pas dans la liste.
- **Causes** :
  1. `openEditDrawer` initialisait `form.source` avec `p.source_name` (libellé) au lieu de `p.source` (UUID FK) → PATCH rejeté à la validation.
  2. La liste affichait toujours `schedule_frequency_display` ("Manual") même quand un cron custom était présent.
- **Fix** : hydratation correcte du form depuis le pipeline + helper `scheduleLabel(p)` qui privilégie le cron raw quand `schedule_frequency === 'manual'`.

### ✅ TC019 — "Tout marquer comme lu"
- **Symptôme** : le bouton restait `disabled` même quand il y avait des notifications non lues.
- **Cause** : la réponse `/notifications/notifications/unread_count/` est wrappée par `success_response()` côté Django (`{status, message, data: {count}, timestamp}`), mais le frontend lisait `res.data.count` au lieu de `res.data.data.count` → undefined → `unreadCount = 0` → bouton disabled.
- **Fix** : lecture défensive `res.data?.data?.count ?? res.data?.count ?? 0` dans `NotificationsView.vue` et `AppHeader.vue`.

### ✅ TC021 — Création d'un widget
- **Symptôme** : le widget ne s'ajoutait pas à la liste, sans message d'erreur.
- **Cause** : le POST `/api/visualizations/widgets/` exigeait un champ `dashboard` non-null. Le frontend envoyait `null` si non sélectionné. La 400 était mangée par `catch { /* ignore */ }`, le drawer se fermait comme un succès.
- **Fix** : validation côté frontend ("Veuillez choisir un dashboard"), surface explicite des erreurs API dans un bandeau, le drawer reste ouvert sur échec.

### ⚠️ TC023 — Exécution d'une requête SQL custom (partiellement fixé)
- **Symptôme initial** : POST `/queries/{id}/execute/` retournait 404.
- **Cause** : le `DataQueryCreateSerializer` Django n'incluait pas le champ `id` dans sa réponse → côté frontend, `activeQuery.id = undefined` → appel à `/queries/undefined/execute/` → 404.
- **Fix** : ajout de `id` (read_only) au `DataQueryCreateSerializer`.
- **État final** : le 404 disparaît, mais le `QueryService` backend retourne désormais **500** car les sources de données seed ("SRC_CRM_SONATRACH", etc.) n'ont pas de vraie BDD distante derrière. Bug applicatif résolu, blocage restant = données de test.

### ✅ TC027 — Notifications de pipeline
- **Symptôme** : la case "Activer les notifications" revenait toujours à décochée après sauvegarde/réouverture.
- **Cause** : `openEditDrawer` réinitialisait `notifications_enabled: false` (et autres champs) en dur au lieu de lire depuis le pipeline existant. Même si la PATCH persistait, l'UI réaffichait toujours l'état par défaut.
- **Fix** : hydratation complète du form depuis le pipeline (`notifications_enabled`, `notify_on_*`, `priority`, `category`, `tags`, `batch_size`, `error_strategy`, `processing_mode`, `pipeline_type`).

### ✅ TC030 — Création de schéma dimensionnel (star schema)
- **Symptôme** : modal "Nouveau schéma" restait ouvert sans message d'erreur.
- **Cause** : POST `/api/star-schema/dimensional-schemas/` rejetait avec 400 (`fact_tables` non vide requis), mais `catch { /* ignore */ }` masquait l'erreur ET le modal ne se fermait pas non plus → utilisateur perdu.
- **Fix** :
  1. Ajout de `id` au `DimensionalSchemaCreateSerializer`.
  2. Bandeau d'erreur rouge dans le modal listant les erreurs de validation par champ.
  3. Modal reste ouvert sur échec (comportement explicite, non plus accidentel).

## Tests toujours en échec (2 / 30)

| Test | Statut | Cause restante |
|---|---|---|
| TC014 — Edit existing connection | 🚧 Blocked | Aucune `DataSourceConnection` n'existe en seed prod. Solution : seeder une connexion de démo. |
| TC023 — Execute custom SQL | ❌ Failed | Source de données mock non connectable → 500 dans `QueryService.execute`. Solution : seeder une source pointant vers une BDD réellement accessible OU faire en sorte que `execute` retourne une 400 propre avec message UI quand la connexion échoue. |

## Modifications de code (commits)

| Commit | Fichiers | Description |
|---|---|---|
| `b279c31` | `data_sources/serializers.py`, `star_schema/serializers.py`, `.gitignore` | Backend : exposer `id` dans 2 CreateSerializers |
| `2ee73d4` | 5 fichiers `.vue` frontend | Fix silent fails, wrong FK, wrong unread count |
| `5009b6d` | `PipelinesView.vue` | Hydratation form + display cron custom |

## Stack de test

- **TestSprite MCP** (plan Starter) — génération + exécution de tests E2E type Playwright
- **Frontend** : vite preview (production build) sur port 5173
- **Backend** : Gunicorn + Django sur Render (free tier, cold start ~25-30s)
- **Auth** : 4 comptes JWT de démonstration (superadmin, dev BI, analyste, direction)
