# Devoir Cloud Computing - FastAPI + PostgreSQL + Nginx

Application web minimale avec:
- Backend FastAPI
- Base de donnees PostgreSQL
- Frontend HTML/CSS/JS (CRUD simple)
- Nginx pour reverse proxy

## 1. Architecture

- `app/Backend/main.py`: point d'entree FastAPI
- `app/Backend/api/routes.py`: routes API CRUD + health
- `app/Backend/db.py`: configuration SQLAlchemy + modele `Submission`
- `app/frontend/src/index.html`: interface formulaire
- `app/frontend/src/app.js`: appels API CRUD
- `app/frontend/src/style.css`: style de la page
- `scripts/setup.sh`: setup local backend + database
- `requirements.sh`: install systeme + appel du setup

## 2. Prerequis

- Linux avec `systemd`
- Python 3.12+
- PostgreSQL
- Nginx

## 3. Installation

### Option A (setup complet)

Depuis la racine du projet:

```bash
bash requirements.sh
```

Ce script:
1. Installe les dependances systeme
2. Cree l'environnement virtuel
3. Installe les packages Python
4. Demarre PostgreSQL
5. Cree la base `devoir_cc`
6. Cree `.env` avec `DATABASE_URL`

### Option B (deja installe, juste setup projet)

```bash
bash scripts/setup.sh
```

## 4. Lancer le backend

Depuis la racine du projet:

```bash
.venv/bin/uvicorn app.Backend.main:app --reload --host 0.0.0.0 --port 8000
```

Verification:

```bash
curl -sS http://127.0.0.1:8000/api/health
```

## 5. Endpoints disponibles

Base API: `/api`

### Health

- `GET /api/health`
- Reponse: statut backend + connexion DB

### CRUD submissions

- `POST /api/submissions`
- `GET /api/submissions`
- `GET /api/submissions/{submission_id}`
- `PUT /api/submissions/{submission_id}`
- `DELETE /api/submissions/{submission_id}`

#### Payload JSON (create/update)

```json
{
  "name": "yoshi",
  "email": "test@example.com",
  "message": "hehehe"
}
```

Contraintes validation:
- `name`: 2 a 120 caracteres
- `email`: 5 a 180 caracteres
- `message`: 2 a 1000 caracteres

## 6. Variables d'environnement

Le backend lit `DATABASE_URL`.

Valeur par defaut actuelle dans le code:

```text
postgresql+psycopg://postgres:postgres@localhost:5432/devoir_cc
```

Valeur recommandee dans `.env`:

```text
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/devoir_cc
```

## 7. Nginx (minimal)

Exemple de reverse proxy vers FastAPI:

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 8. Troubleshooting rapide

### Erreur "connection refused" sur 5432

```bash
sudo systemctl start postgresql
pg_isready -h 127.0.0.1 -p 5432
```

### Erreur import Uvicorn

Toujours lancer avec le module package depuis la racine:

```bash
.venv/bin/uvicorn app.Backend.main:app --reload
```

## 9. Contraintes de modification de l'interface

L'interface est modifiable (HTML/CSS/JS), mais les appels API suivants doivent rester compatibles pour ne pas casser le backend:

1. Creer une entree: `POST /api/submissions`
2. Lister les entrees: `GET /api/submissions`
3. Lire une entree: `GET /api/submissions/{submission_id}`
4. Mettre a jour: `PUT /api/submissions/{submission_id}`
5. Supprimer: `DELETE /api/submissions/{submission_id}`
6. Sante applicative: `GET /api/health`

Le format JSON attendu doit conserver ces champs:
- `name`
- `email`
- `message`

Si tu changes les noms de champs cote frontend, il faut aussi adapter les schemas dans `app/Backend/api/routes.py`.
