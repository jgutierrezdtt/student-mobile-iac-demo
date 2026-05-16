#!/usr/bin/env python3
"""Validate step 02 — CertificatePinner en OkHttp"""

STEP = "02"
EXPECTED_ARTIFACT = "src/android/network/ApiClient.kt"
REQUIRED_MARKERS = [
    "CertificatePinner",
    "certificatePinner",
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

    # At least one of the two marker variants must be present
    if not any(m in content for m in REQUIRED_MARKERS):
        print(f"[FAIL] Step {STEP}: missing markers in {EXPECTED_ARTIFACT}: {REQUIRED_MARKERS}")
        return 1

    # Must not have empty checkServerTrusted
    if "fun checkServerTrusted" in content and "Unit { }" in content:
        print(f"[FAIL] Step {STEP}: empty checkServerTrusted found in {EXPECTED_ARTIFACT}")
        return 1

    print(f"[PASS] Step {STEP}: all markers found in {EXPECTED_ARTIFACT}")
    return 0

if __name__ == "__main__":
    sys.exit(validate())
