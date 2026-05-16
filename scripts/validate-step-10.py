#!/usr/bin/env python3
"""Validate step 10 — Checklist final con los cuatro frentes"""

STEP = "10"
EXPECTED_ARTIFACT = "docs/secure-coding-mobile-iac-checklist.md"
REQUIRED_MARKERS = [
    "Frente 1",
    "Frente 2",
    "Frente 3",
    "Frente 4",
]

import sys
import os

def validate():
    artifact_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), EXPECTED_ARTIFACT)
    if not os.path.exists(artifact_path):
        print(f"[FAIL] Step {STEP}: artifact not found: {EXPECTED_ARTIFACT}")
        return 1

    with open(artifact_path, "r", encoding="utf-8") as f:
        content = f.read()

    missing = [m for m in REQUIRED_MARKERS if m not in content]
    if missing:
        print(f"[FAIL] Step {STEP}: missing markers in {EXPECTED_ARTIFACT}: {missing}")
        return 1

    print(f"[PASS] Step {STEP}: all markers found in {EXPECTED_ARTIFACT}")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
