#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "[setup] Project root: $PROJECT_ROOT"

if [[ ! -d ".venv" ]]; then
	echo "[setup] Creating virtual environment..."
	python3 -m venv .venv
fi

echo "[setup] Installing Python dependencies in .venv..."
"$PROJECT_ROOT/.venv/bin/python" -m pip install --upgrade pip
"$PROJECT_ROOT/.venv/bin/python" -m pip install -r "$PROJECT_ROOT/requirements.txt"

echo "[setup] Starting PostgreSQL service..."
sudo systemctl start postgresql
sudo systemctl enable postgresql >/dev/null 2>&1 || true

echo "[setup] Ensuring database and credentials exist..."
sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='devoir_cc';" | grep -q 1 || \
	sudo -u postgres createdb devoir_cc
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';" >/dev/null

if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
	echo "[setup] Creating .env with DATABASE_URL..."
	cat > "$PROJECT_ROOT/.env" <<'EOF'
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/devoir_cc
EOF
fi

echo "[setup] Setup complete."
echo "[setup] To run API:"
echo "  $PROJECT_ROOT/.venv/bin/uvicorn app.Backend.main:app --reload --host 0.0.0.0 --port 8000"
echo "[setup] Health check:"
echo "  curl -sS http://127.0.0.1:8000/api/health"
