from pathlib import Path
import sys

# Ensure the project root is on sys.path so `import app` works even when tests are
# invoked from outside the repo root.
ROOT = Path(__file__).resolve().parents[1]
ROOT_STR = str(ROOT)
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)
