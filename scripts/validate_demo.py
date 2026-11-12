#!/usr/bin/env python3
"""Validate that the public Tactical Recruiting demo stays synthetic and self-contained."""

from pathlib import Path
import re
import sys

DEMO = Path("rrhh-demo/index.html")
if not DEMO.is_file():
    raise SystemExit("ERROR: rrhh-demo/index.html is missing")

html = DEMO.read_text(encoding="utf-8")

checks = {
    "synthetic email placeholders": all(
        address.endswith("@example.com")
        for address in re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", html, re.I)
    ),
    "no former client references": not re.search(r"Alvatross|SATEC|TM Forum", html, re.I),
    "no former sample identities": not re.search(
        r"Carlos Méndez|Laura Gómez|Miguel Ángel Ruiz|carlos\.m@|laura\.g@|miguel\.a@",
        html,
        re.I,
    ),
    "browser-local storage only": "localStorage" in html,
    "visible synthetic-data warning": "DEMO / DATOS FICTICIOS" in html,
    "no remote script imports": not re.search(
        r"<script\b[^>]*\bsrc\s*=\s*['\"]https?://",
        html,
        re.I,
    ),
    "no browser network APIs": not re.search(
        r"\b(fetch|XMLHttpRequest|WebSocket|sendBeacon)\s*\(",
        html,
    ),
}

failed = [label for label, passed in checks.items() if not passed]
for label, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {label}")

if failed:
    print("Demo validation failed: " + ", ".join(failed), file=sys.stderr)
    raise SystemExit(1)

print("Demo validation passed.")
