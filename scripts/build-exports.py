#!/usr/bin/env python3
"""Build exports/catalog.json from validated profiles.

Walks profiles/, validates each against schemas/profile-atom-v1.json, and
assembles a single machine-readable catalog manifest.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("error: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / "schemas" / "profile-atom-v1.json"
PROFILES_DIR = REPO / "profiles"
EXPORT_PATH = REPO / "exports" / "catalog.json"
CATALOG_NAME = "profile-atoms"
CATALOG_VERSION = "0.1.0"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)

    compositions: list[dict] = []
    for path in sorted(PROFILES_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        errs = list(validator.iter_errors(data))
        if errs:
            print(f"✗ {path.relative_to(REPO)}", file=sys.stderr)
            for err in errs:
                loc = "/".join(str(x) for x in err.absolute_path) or "<root>"
                print(f"    {err.message} at {loc}", file=sys.stderr)
            sys.exit(1)
        compositions.append(data)

    catalog = {
        "catalog": CATALOG_NAME,
        "version": CATALOG_VERSION,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "atoms": [],
        "compositions": compositions,
        "rules": [],
    }

    EXPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPORT_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {EXPORT_PATH.relative_to(REPO)} — 0 atoms, {len(compositions)} compositions, 0 rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
