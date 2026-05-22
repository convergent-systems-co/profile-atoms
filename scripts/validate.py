#!/usr/bin/env python3
"""Validate every profile under profiles/ against schemas/profile-atom-v1.json.

Per-file checks: (1) JSON Schema validation; (2) the canonical_name's slug
matches the filename stem (e.g., `jmfamily/profiles/developer` lives at
profiles/jmfamily-developer.json — the filename uses the dash-joined form).

Cross-catalog reference resolution is NOT done in this catalog because the
referenced catalogs (role-packs-atoms, etc.) don't all exist yet. Once they
do, this validator can be extended to walk the umbrella's submodule tree.

Exit 0 on full pass; exit 1 on any failure.
"""
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("error: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / "schemas" / "profile-atom-v1.json"
PROFILES_DIR = REPO / "profiles"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)

    files = sorted(PROFILES_DIR.glob("*.json"))
    if not files:
        print(f"no profiles found under {PROFILES_DIR}", file=sys.stderr)
        return 1

    total_errors = 0
    for path in files:
        rel = path.relative_to(REPO)
        errors: list[str] = []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"✗ {rel}: invalid JSON ({e})")
            total_errors += 1
            continue

        for err in validator.iter_errors(data):
            loc = "/".join(str(x) for x in err.absolute_path) or "<root>"
            errors.append(f"schema: {err.message} at {loc}")

        # canonical_name's path tail compared to filename stem
        cn = data.get("canonical_name", "")
        if "/profiles/" in cn:
            namespace, slug = cn.split("/profiles/", 1)
            expected = f"{namespace.replace('/', '-')}-{slug}"
            stem = path.stem
            if stem != expected:
                errors.append(
                    f"filename stem {stem!r} does not match canonical_name "
                    f"{cn!r} (expected {expected!r})"
                )

        if errors:
            print(f"✗ {rel}")
            for e in errors:
                print(f"    {e}")
            total_errors += len(errors)
        else:
            print(f"✓ {rel}")

    if total_errors:
        print(f"\n{total_errors} error(s) across {len(files)} profile(s)")
        return 1
    print(f"\nall {len(files)} profile(s) valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
