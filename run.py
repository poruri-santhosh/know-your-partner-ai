"""Convenience runner for Know Your Partner AI."""

import sys
from pathlib import Path
import uvicorn

# Setup paths
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
    load_dotenv(BACKEND_DIR / ".env")
except ImportError:
    pass

if __name__ == "__main__":
    print("=" * 65)
    print("❤️  KNOW YOUR PARTNER AI")
    print("🔬 Behavioral Science + Machine Learning Compatibility Engine")
    print("👉 Open your browser at: http://127.0.0.1:8000")
    print("=" * 65)
    from app.main import app
    uvicorn.run(app, host="127.0.0.1", port=8000)
