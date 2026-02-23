from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ALEMBIC_INI = PROJECT_ROOT / "alembic.ini"

def run_alembic_upgrade():
    if not ALEMBIC_INI.exists():
        print("Alembic config not found. Skipping migrations.")
        return

    result = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(ALEMBIC_INI), "upgrade", "head"],
        cwd=PROJECT_ROOT,
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print("Alembic migration successful.")
    else:
        print("Alembic migration failed:")
        print(result.stderr)
        sys.exit(1)

def check_db():
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(ALEMBIC_INI), "current"],
        cwd=PROJECT_ROOT,
        capture_output=True, text=True
    )
    return result.returncode == 0

def run():
    run_alembic_upgrade()
