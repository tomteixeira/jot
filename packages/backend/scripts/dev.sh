set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

# Convention: venv local au backend
VENV_DIR="${VENV_DIR:-$BACKEND_DIR/.venv}"
PYTHON_BIN="$VENV_DIR/bin/python"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Python venv introuvable: $VENV_DIR"
  echo "Crée-le avec:"
  echo "  python3 -m venv \"$VENV_DIR\""
  echo "  \"$PYTHON_BIN\" -m pip install -r \"$BACKEND_DIR/requirements.txt\""
  exit 1
fi

exec "$PYTHON_BIN" -m uvicorn app.main:app --reload --app-dir "$BACKEND_DIR"


