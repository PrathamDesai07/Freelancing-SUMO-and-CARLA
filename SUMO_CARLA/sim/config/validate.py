## File: sim/config/validate.py
import sys
from sim.config.loader import ConfigLoader

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python -m sim.config.validate <config.yml>")
        sys.exit(1)

    path = sys.argv[1]
    try:
        loader = ConfigLoader(path)
        print(f"[validate] {path}: ✅ OK")
    except Exception as e:
        print(f"[validate] {path}: ❌ {e}")
        sys.exit(1)
