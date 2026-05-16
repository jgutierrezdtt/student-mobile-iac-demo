#!/usr/bin/env python3
"""Validate step 07 — Dockerfile non-root y multi-stage"""

STEP = "07"
EXPECTED_ARTIFACT = "src/docker/Dockerfile"
REQUIRED_MARKERS = [
    "USER ",
    "AS builder",
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

    # USER root is not acceptable
    if "USER root" in content:
        print(f"[FAIL] Step {STEP}: USER root found in {EXPECTED_ARTIFACT} — use a non-root user")
        return 1

    print(f"[PASS] Step {STEP}: all markers found in {EXPECTED_ARTIFACT}")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
