#!/usr/bin/env python3
"""Validate step 06 — IAM minimo privilegio sin wildcards globales"""

STEP = "06"
EXPECTED_ARTIFACT = "src/iac/terraform/iam.tf"
REQUIRED_MARKERS = [
    "sid",
    "effect = \"Allow\"",
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

    # Must not have wildcard actions
    if 'actions   = ["*"]' in content or 'actions = ["*"]' in content:
        print(f"[FAIL] Step {STEP}: wildcard actions found in {EXPECTED_ARTIFACT} — apply least privilege")
        return 1

    print(f"[PASS] Step {STEP}: all markers found in {EXPECTED_ARTIFACT}")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
