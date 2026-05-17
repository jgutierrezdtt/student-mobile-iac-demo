#!/usr/bin/env python3
"""
Actualiza el README con el progreso del tutorial y genera la medalla
cuando todos los validators pasan.

Siempre actualiza README.md con el estado actual de cada paso.
Solo escribe docs/MEDALLA.md si TODOS los validators pasan.
No requiere ningun secret.
"""

import glob
import os
import re
import subprocess
import sys
from datetime import datetime, timezone


STEP_FILES = {
    "validate-step-01": "`src/android/storage/UserPreferences.kt`",
    "validate-step-02": "`src/android/network/ApiClient.kt`",
    "validate-step-03": "`src/android/auth/SessionManager.kt`",
    "validate-step-04": "`src/iac/terraform/main.tf`",
    "validate-step-05": "`src/iac/terraform/secrets.tf`",
    "validate-step-06": "`src/iac/terraform/iam.tf`",
    "validate-step-07": "`src/docker/Dockerfile`",
    "validate-step-08": "`src/pipeline/.github/workflows/deploy.yml`",
    "validate-step-09": "`src/android/proguard-rules.pro`",
    "validate-step-10": "`docs/secure-coding-mobile-iac-checklist.md`",
}


# ---------------------------------------------------------------------------
# Ejecucion de validators
# ---------------------------------------------------------------------------

def run_validators(repo_root):
    scripts_dir = os.path.join(repo_root, "scripts")
    validator_files = sorted(glob.glob(os.path.join(scripts_dir, "validate-step-*.py")))

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
# Actualizacion del README
# ---------------------------------------------------------------------------

def update_readme(repo_root, results, medal_url=None):
    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    passed_count = sum(1 for ok in results.values() if ok)
    total = len(results)

    rows = ["| Paso 0 | Introduccion — lee primero | Empezar aqui |"]
    for step, file_ref in STEP_FILES.items():
        num = int(step.replace("validate-step-", ""))
        estado = "Completado" if results.get(step, False) else "Pendiente"
        rows.append(f"| Paso {num} | {file_ref} | {estado} |")

    medal_line = ""
    if medal_url:
        medal_line = f"\n**Medalla obtenida:** [Ver MEDALLA.md]({medal_url})\n"

    new_section = (
        "## Tabla de pasos (resumen de progreso)\n\n"
        f"**Progreso: {passed_count}/{total} pasos completados**\n\n"
        "| Paso | Archivo a modificar | Estado |\n"
        "|------|---------------------|--------|\n"
        + "\n".join(rows)
        + "\n"
        + medal_line
    )

    # Reemplaza la seccion existente preservando lo que viene despues
    pattern = r"## Tabla de pasos \(resumen de progreso\).*?(\n## )"
    new_content = re.sub(pattern, new_section + r"\1", content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[OK] README actualizado: {passed_count}/{total} pasos completados")


# ---------------------------------------------------------------------------
# Escritura de la medalla
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

    passed = [s for s, ok in results.items() if ok]
    failed = [s for s, ok in results.items() if not ok]

    print(f"\n=== Resultado: {len(passed)}/{len(results)} pasos completados ===")

    medal_url = None
    if not failed:
        print("\n[OK] Todos los validators pasaron. Generando medalla...")
        write_medal(repo_root, repo, actor, run_id, sha, passed)
        medal_url = "docs/MEDALLA.md"
    else:
        print(f"\n[INFO] {len(failed)} pasos pendientes:")
        for s in sorted(failed):
            print(f"  - {s}")

    update_readme(repo_root, results, medal_url)


if __name__ == "__main__":
    main()
