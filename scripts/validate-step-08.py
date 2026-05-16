#!/usr/bin/env python3
"""Validate step 08 — CI/CD pipeline con permissions y env: para inputs"""

STEP = "08"
EXPECTED_ARTIFACT = "src/pipeline/.github/workflows/deploy.yml"
REQUIRED_MARKERS = [
    "permissions:",
    "env:",
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

    # Must not have write-all permissions
    if "write-all" in content:
        print(f"[FAIL] Step {STEP}: write-all permissions found in {EXPECTED_ARTIFACT} — use specific scopes")
        return 1

    print(f"[PASS] Step {STEP}: all markers found in {EXPECTED_ARTIFACT}")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
