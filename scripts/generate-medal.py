#!/usr/bin/env python3
"""
Genera la medalla de completacion del tutorial.

Solo escribe docs/MEDALLA.md si TODOS los validators pasan.
La prueba de integridad es la URL publica del run de GitHub Actions:
cualquiera puede abrir esa URL y verificar que los 10 validators
pasaron en ese commit exacto.

No requiere ningun secret — el alumno no necesita configurar nada.

Uso:
  GITHUB_REPOSITORY=owner/repo GITHUB_ACTOR=user GITHUB_RUN_ID=123 \
  GITHUB_SHA=abc123 python3 scripts/generate-medal.py
"""

import glob
import os
import subprocess
import sys
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Ejecucion de validators
# ---------------------------------------------------------------------------

def run_validators(repo_root: str) -> dict:
    scripts_dir = os.path.join(repo_root, "scripts")
    validator_files = sorted(
        glob.glob(os.path.join(scripts_dir, "validate-step-*.py"))
    )

    if not validator_files:
        print("[FAIL] No se encontraron scripts de validacion en scripts/validate-step-*.py")
        sys.exit(1)

    results = {}
    for script_path in validator_files:
        step_name = os.path.basename(script_path).replace(".py", "")
        print(f"[CHECK] {step_name} ...", end=" ", flush=True)
        proc = subprocess.run(
            [sys.executable, script_path],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        ok = proc.returncode == 0
        results[step_name] = ok
        print("PASS" if ok else "FAIL")
        if proc.stdout.strip():
            for line in proc.stdout.strip().splitlines():
                print(f"        {line}")
        if proc.stderr.strip():
            for line in proc.stderr.strip().splitlines():
                print(f"        {line}")

    return results


# ---------------------------------------------------------------------------
# Escritura del archivo de medalla
# ---------------------------------------------------------------------------

def write_medal(repo_root, repo, actor, run_id, sha, completed_steps):
    total = len(completed_steps)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    run_url = f"https://github.com/{repo}/actions/runs/{run_id}"
    commit_url = f"https://github.com/{repo}/commit/{sha}"

    rows = "\n".join(f"| {s} | PASS |" for s in sorted(completed_steps))

    content = f"""\
# Medalla de completacion

**Completado por:** {actor}
**Repositorio:** {repo}
**Fecha:** {now}
**Pasos completados:** {total}/{total}

## Prueba de integridad

Esta medalla fue generada automaticamente por GitHub Actions cuando los {total} validators pasaron.
La prueba de completacion es publica y verificable:

- **Run de Actions:** {run_url}
- **Commit validado:** {commit_url}
- **SHA:** `{sha}`

Para verificar: abre el run de Actions y comprueba que todos los validators
retornaron PASS en ese commit. El historial de GitHub es inmutable.

## Pasos completados

| Paso | Estado |
|------|--------|
{rows}

---
_Generado por github-actions[bot] — no editar manualmente._
"""

    out_path = os.path.join(repo_root, "docs", "MEDALLA.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] Medalla escrita en {out_path}")
    print(f"[OK] Prueba de integridad: {run_url}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    repo = os.environ.get("GITHUB_REPOSITORY", "unknown/unknown")
    actor = os.environ.get("GITHUB_ACTOR", "unknown")
    run_id = os.environ.get("GITHUB_RUN_ID", "0")
    sha = os.environ.get("GITHUB_SHA", "unknown")

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("=== Ejecutando validators ===")
    results = run_validators(repo_root)

    failed = [s for s, ok in results.items() if not ok]
    passed = [s for s, ok in results.items() if ok]

    print(f"\n=== Resultado: {len(passed)}/{len(results)} pasos completados ===")

    if failed:
        print("\n[FAIL] Los siguientes pasos no estan completos:")
        for s in sorted(failed):
            print(f"  - {s}")
        print("\nCompleta todos los pasos antes de solicitar la medalla.")
        sys.exit(1)

    print("\n[OK] Todos los validators pasaron. Generando medalla...")
    write_medal(repo_root, repo, actor, run_id, sha, passed)


if __name__ == "__main__":
    main()
