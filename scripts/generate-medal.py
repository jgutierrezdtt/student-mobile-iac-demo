#!/usr/bin/env python3
"""
Actualiza el README con el progreso del tutorial y genera la medalla
cuando todos los validators pasan.

- En progreso: actualiza la tabla de pasos en el README con Pendiente/Completado.
- Completado: reemplaza el README entero con una pagina de certificado visual.
- Siempre escribe docs/MEDALLA.md cuando todos pasan.
"""

import glob
import os
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

STEP_TOPICS = {
    "validate-step-01": "Almacenamiento cifrado con EncryptedSharedPreferences",
    "validate-step-02": "Certificate pinning con OkHttp",
    "validate-step-03": "Autenticacion biometrica con Android Keystore",
    "validate-step-04": "S3 y RDS sin acceso publico",
    "validate-step-05": "Outputs sensibles marcados en Terraform",
    "validate-step-06": "Politicas IAM con minimo privilegio",
    "validate-step-07": "Imagen Docker multi-stage con usuario non-root",
    "validate-step-08": "Workflow CI/CD con permisos minimos",
    "validate-step-09": "Ofuscacion activa con ProGuard",
    "validate-step-10": "Checklist de seguridad completado",
}


STEP_COMPLETED_SUMMARY = {
    "validate-step-01": (
        "`src/android/storage/UserPreferences.kt` actualizado con "
        "`EncryptedSharedPreferences` y `MasterKey`."
    ),
    "validate-step-02": (
        "`src/android/network/ApiClient.kt` actualizado con `CertificatePinner`."
    ),
    "validate-step-03": (
        "`src/android/auth/SessionManager.kt` actualizado con "
        "`setUserAuthenticationRequired` y `setInvalidatedByBiometricEnrollment`."
    ),
    "validate-step-04": (
        "`src/iac/terraform/main.tf` actualizado con "
        "`aws_s3_bucket_public_access_block` y `publicly_accessible = false`."
    ),
    "validate-step-05": (
        "`src/iac/terraform/secrets.tf` actualizado con data sources de "
        "`aws_ssm_parameter` y `sensitive = true`."
    ),
    "validate-step-06": (
        "`src/iac/terraform/iam.tf` actualizado con statements IAM especificos "
        "con `sid` y ARNs."
    ),
    "validate-step-07": (
        "`src/docker/Dockerfile` actualizado con multi-stage build y usuario non-root."
    ),
    "validate-step-08": (
        "`src/pipeline/.github/workflows/deploy.yml` actualizado con `permissions` "
        "especificos y `env:` para inputs."
    ),
    "validate-step-09": (
        "`src/android/proguard-rules.pro` actualizado con `-keepclassmembers` "
        "especificos y `-obfuscationdictionary`."
    ),
    "validate-step-10": (
        "`docs/secure-coding-mobile-iac-checklist.md` completado con los cuatro "
        "frentes de seguridad."
    ),
}

# Instrucciones completas de cada paso.
# Se muestran cuando el paso es el siguiente pendiente.
STEP_CONTENT = {}

STEP_CONTENT["validate-step-01"] = """\

### Por que importa esto

SharedPreferences en Android guarda los datos en texto plano en un archivo del sistema.
Esos archivos son accesibles a cualquier aplicacion con permisos de root, a herramientas
de backup sin cifrar, y a cualquier investigador que analice el APK en un emulador.

### Que debes cambiar

**Archivo:** `src/android/storage/UserPreferences.kt`

La clase almacena el token de autenticacion en SharedPreferences sin cifrar.
Reemplazalo con `EncryptedSharedPreferences`, que usa el Android Keystore para derivar
una clave de cifrado vinculada al dispositivo.

Antes (vulnerable):

```kotlin
// VULNERABLE: token en texto plano en SharedPreferences
val prefs = context.getSharedPreferences("user_prefs", Context.MODE_PRIVATE)
prefs.edit().putString("auth_token", token).apply()
```

Despues (seguro):

```kotlin
// SEGURO: EncryptedSharedPreferences con clave del Android Keystore
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "secure_user_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

encryptedPrefs.edit().putString("auth_token", token).apply()
```

### Que valida el workflow

`scripts/validate-step-01.py` busca en `src/android/storage/UserPreferences.kt`:
- `EncryptedSharedPreferences`
- `MasterKey`
"""

STEP_CONTENT["validate-step-02"] = """\

### Por que importa esto

HTTPS cifra la comunicacion, pero ese cifrado solo es util si la aplicacion verifica
que el certificado del servidor es legitimo. Un `TrustManager` que acepta cualquier
certificado anula completamente la proteccion TLS. Con un certificado de CA confiada,
un atacante puede hacer un ataque MITM sin que la aplicacion lo detecte.

### Que debes cambiar

**Archivo:** `src/android/network/ApiClient.kt`

La configuracion de OkHttp tiene un `TrustManager` que acepta cualquier certificado.
Implementa certificate pinning con el `CertificatePinner` de OkHttp.

Antes (vulnerable):

```kotlin
// VULNERABLE: acepta cualquier certificado
val trustAllCerts = arrayOf<TrustManager>(object : X509TrustManager {
    override fun checkClientTrusted(chain: Array<X509Certificate>, authType: String) {}
    override fun checkServerTrusted(chain: Array<X509Certificate>, authType: String) {}
    override fun getAcceptedIssuers(): Array<X509Certificate> = arrayOf()
})
```

Despues (seguro):

```kotlin
// SEGURO: certificate pinning
val certificatePinner = CertificatePinner.Builder()
    .add("api.myapp.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .add("api.myapp.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=") // backup
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

Siempre aniade un pin de backup: si solo tienes el pin del certificado actual y ese
certificado expira, la app deja de funcionar hasta que los usuarios actualicen.

### Que valida el workflow

`scripts/validate-step-02.py` busca en `src/android/network/ApiClient.kt`:
- `CertificatePinner` o `certificatePinner`
- Ausencia de `checkServerTrusted` con implementacion vacia
"""

STEP_CONTENT["validate-step-03"] = """\

### Por que importa esto

Un token de sesion guardado sin proteccion puede ser extraido por alguien con acceso
fisico o logico. Sin autenticacion biometrica, el atacante puede impersonar al usuario
indefinidamente.

El Android Keystore permite vincular la clave criptografica que protege el token a la
autenticacion biometrica: sin pasar biometria, la clave no puede usarse aunque se tenga
acceso al archivo del sistema.

### Que debes cambiar

**Archivo:** `src/android/auth/SessionManager.kt`

Protege el token con una clave del Keystore vinculada a autenticacion biometrica.

```kotlin
// SEGURO: clave del Keystore que requiere autenticacion biometrica para desbloquear
val keyGenParameterSpec = KeyGenParameterSpec.Builder(
    KEY_ALIAS,
    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setUserAuthenticationRequired(true)
    .setUserAuthenticationParameters(0, KeyProperties.AUTH_BIOMETRIC_STRONG)
    .setInvalidatedByBiometricEnrollment(true)
    .build()
```

`setInvalidatedByBiometricEnrollment(true)`: si alguien con acceso fisico aniade su
propia huella, la clave queda invalidada. Sin esta opcion, aniadir una nueva huella
podria dar acceso a un atacante.

### Que valida el workflow

`scripts/validate-step-03.py` busca en `src/android/auth/SessionManager.kt`:
- `setUserAuthenticationRequired`
- `setInvalidatedByBiometricEnrollment`
"""

STEP_CONTENT["validate-step-04"] = """\

### Por que importa esto

Algunos de los incidentes de seguridad mas costosos no vinieron de vulnerabilidades en
el codigo sino de buckets S3 publicos, bases de datos con el puerto abierto a internet,
o security groups con `0.0.0.0/0`. Un error de configuracion aplicado con
`terraform apply` puede exponer terabytes de datos en segundos.

### Que debes cambiar

**Archivo:** `src/iac/terraform/main.tf`

La configuracion tiene un bucket S3 sin restriccion de acceso publico, un security
group que permite SSH desde cualquier IP, y una instancia de RDS con acceso publico.

Bloqueo de acceso publico en S3:

```hcl
resource "aws_s3_bucket_public_access_block" "app_bucket" {
  bucket = aws_s3_bucket.app_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

Security group con SSH restringido:

```hcl
ingress {
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["10.0.0.0/8"]  # VPN -- no 0.0.0.0/0
}
```

RDS sin acceso publico:

```hcl
resource "aws_db_instance" "main" {
  publicly_accessible = false
}
```

### Que valida el workflow

`scripts/validate-step-04.py` busca en `src/iac/terraform/main.tf`:
- `block_public_acls`
- `publicly_accessible = false`
- Ausencia de `cidr_blocks = ["0.0.0.0/0"]` en el puerto 22
"""

STEP_CONTENT["validate-step-05"] = """\

### Por que importa esto

Un secreto en un archivo de Terraform es un secreto en el repositorio de git. Git
recuerda todo: aunque borres el secreto en el proximo commit, sigue visible en el
historial. El mismo problema afecta a los outputs que pueden exponer secretos en texto
plano en los logs del pipeline.

### Que debes cambiar

**Archivo:** `src/iac/terraform/secrets.tf`

El archivo tiene la contrasena de la base de datos como valor literal y una clave de
API sin marcar como sensible. Referencia esos valores desde AWS Parameter Store.

Antes (vulnerable):

```hcl
resource "aws_db_instance" "main" {
  password = "supersecretpassword123"
}
```

Despues (seguro):

```hcl
data "aws_ssm_parameter" "db_password" {
  name            = "/prod/db/password"
  with_decryption = true
}

resource "aws_db_instance" "main" {
  password = data.aws_ssm_parameter.db_password.value
}
```

Outputs sensibles:

```hcl
output "api_key" {
  value     = data.aws_ssm_parameter.api_key.value
  sensitive = true
}
```

### Que valida el workflow

`scripts/validate-step-05.py` busca en `src/iac/terraform/secrets.tf`:
- `aws_ssm_parameter` en los data sources
- `sensitive = true` en los outputs
"""

STEP_CONTENT["validate-step-06"] = """\

### Por que importa esto

En AWS, una identidad con mas permisos de los necesarios es una superficie de ataque
que espera ser explotada. `"Action": "*"` y `"Resource": "*"` en politicas IAM son
errores frecuentes que llegan a produccion porque "si funciona, no lo toques".

### Que debes cambiar

**Archivo:** `src/iac/terraform/iam.tf`

La politica del rol Lambda tiene `actions = ["*"]` y `resources = ["*"]`.
Reemplazala con permisos especificos sobre los recursos concretos.

Antes (vulnerable):

```hcl
data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions   = ["*"]
    resources = ["*"]
  }
}
```

Despues (seguro):

```hcl
data "aws_iam_policy_document" "lambda_policy" {
  statement {
    sid    = "AllowS3ReadFromAppBucket"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::my-app-bucket",
      "arn:aws:s3:::my-app-bucket/*"
    ]
  }

  statement {
    sid    = "AllowSSMParameterAccess"
    effect = "Allow"
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters"
    ]
    resources = [
      "arn:aws:ssm:us-east-1:123456789012:parameter/prod/myapp/*"
    ]
  }
}
```

### Que valida el workflow

`scripts/validate-step-06.py` busca en `src/iac/terraform/iam.tf`:
- Ausencia de `actions = ["*"]` y `resources = ["*"]`
- Presencia de `sid` en los statements
- ARNs especificos en lugar de wildcards globales
"""

STEP_CONTENT["validate-step-07"] = """\

### Por que importa esto

Si el proceso dentro del contenedor se ejecuta como root y hay una vulnerabilidad
que permite salir del contenedor, el atacante obtiene acceso root al host. Una imagen
base con cientos de herramientas instaladas amplifica el dano en caso de compromiso.

### Que debes cambiar

**Archivo:** `src/docker/Dockerfile`

El Dockerfile usa `node:18` (imagen completa), ejecuta la aplicacion como root, y
no usa multi-stage build.

Antes (vulnerable):

```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "server.js"]
```

Despues (seguro):

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS runtime
WORKDIR /app
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=appuser:appgroup . .
USER appuser
EXPOSE 3000
CMD ["node", "server.js"]
```

### Que valida el workflow

`scripts/validate-step-07.py` busca en `src/docker/Dockerfile`:
- Instruccion `USER` con un usuario non-root
- `AS builder` o `AS runtime` (multi-stage)
- Imagen base alpine o minimal
"""

STEP_CONTENT["validate-step-08"] = """\

### Por que importa esto

El pipeline de CI/CD tiene acceso a secretos de produccion y puede desplegar codigo
directamente. `permissions: write-all`, acciones sin version fija y la interpolacion
directa de inputs del usuario son vectores de ataque de supply chain.

### Que debes cambiar

**Archivo:** `src/pipeline/.github/workflows/deploy.yml`

Permisos minimos por scope:

```yaml
permissions:
  contents: read
  id-token: write
```

Fijar acciones al commit SHA:

```yaml
# SHA inmutable -- los tags son mutables
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

Evitar inyeccion de comandos:

```yaml
# VULNERABLE: interpolacion directa
- run: echo "Deploying ${{ github.event.pull_request.title }}"

# SEGURO: via variable de entorno
- run: echo "Deploying $PR_TITLE"
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
```

### Que valida el workflow

`scripts/validate-step-08.py` busca en `src/pipeline/.github/workflows/deploy.yml`:
- La clave `permissions` con scopes especificos, sin `write-all`
- Uso de `env:` para pasar variables a comandos shell
"""

STEP_CONTENT["validate-step-09"] = """\

### Por que importa esto

Una APK puede ser decompilada con jadx o apktool a codigo Kotlin/Java legible. Sin
ofuscacion, la logica de negocio, los endpoints de la API y los algoritmos propietarios
quedan expuestos. Las reglas `-keep` demasiado amplias desactivan la ofuscacion para
toda la aplicacion.

### Que debes cambiar

**Archivo:** `src/android/proguard-rules.pro`

Antes (vulnerable -- ofuscacion desactivada):

```proguard
-keep class com.myapp.** { *; }
-keepclassmembers class * { *; }
```

Despues (seguro -- ofuscacion activa):

```proguard
-keepclassmembers class com.myapp.models.** {
    <fields>;
}

-keep public class * extends android.app.Activity
-keep public class * extends android.app.Service
-keep public class * extends android.content.BroadcastReceiver

-keepclassmembers class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
}

-obfuscationdictionary proguard-dictionary.txt
-classobfuscationdictionary proguard-dictionary.txt
-packageobfuscationdictionary proguard-dictionary.txt
```

Guarda siempre el `mapping.txt` de cada build de release para desofuscar los
stack traces de crashes en produccion.

### Que valida el workflow

`scripts/validate-step-09.py` busca en `src/android/proguard-rules.pro`:
- `-keepclassmembers` especificos
- `-obfuscationdictionary`
- Ausencia de `-keep class com.** { *; }`
"""

STEP_CONTENT["validate-step-10"] = """\

### Por que importa esto

La seguridad en movil y en IaC no son problemas aislados: estan interconectados.
Un fallo en cualquier eslabon puede comprometer el conjunto. Este checklist es tu
referencia para futuros proyectos y auditorias.

### Que debes cambiar

**Archivo:** `docs/secure-coding-mobile-iac-checklist.md`

Completa el archivo con los cuatro frentes de seguridad:

```markdown
# Checklist de seguridad -- Mobile e IaC

## Frente 1: Almacenamiento y comunicacion segura

- [ ] EncryptedSharedPreferences con MasterKey.Builder y AES256_GCM
- [ ] Certificate pinning con OkHttp CertificatePinner
- [ ] No existe checkServerTrusted vacio

## Frente 2: Autenticacion movil y gestion de sesion

- [ ] setUserAuthenticationRequired(true) en la clave del Keystore
- [ ] setInvalidatedByBiometricEnrollment(true)
- [ ] Tokens con tiempo de vida limitado

## Frente 3: Cloud e IaC security

- [ ] aws_s3_bucket_public_access_block con los cuatro atributos en true
- [ ] Security groups sin 0.0.0.0/0 en puertos de administracion
- [ ] RDS con publicly_accessible = false
- [ ] Secretos desde Parameter Store, no hardcodeados
- [ ] sensitive = true en outputs sensibles de Terraform
- [ ] Politicas IAM con acciones y recursos especificos

## Frente 4: Pipeline y supply chain

- [ ] permissions especificos en workflows de GitHub Actions
- [ ] Acciones de terceros fijadas al commit SHA
- [ ] Inputs via env: en lugar de interpolacion directa
- [ ] Imagenes Docker basadas en alpine
- [ ] Proceso ejecutandose como usuario non-root
- [ ] Multi-stage build
- [ ] -keepclassmembers especificos en ProGuard
- [ ] -obfuscationdictionary activo
```

### Que valida el workflow

`scripts/validate-step-10.py` busca en `docs/secure-coding-mobile-iac-checklist.md`:
- `Frente 1`, `Frente 2`, `Frente 3`, `Frente 4`
"""


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
# README: modo progresivo (reconstruye entero segun pasos completados)
# ---------------------------------------------------------------------------

def update_readme_progress(repo_root, results):
    passed = sorted([s for s, ok in results.items() if ok])
    pending = sorted([s for s, ok in results.items() if not ok])
    passed_count = len(passed)
    total = len(results)

    # --- Cabecera e intro ---
    lines = []
    lines.append("# Secure Coding Mobile e IaC\n")
    lines.append("\n")
    lines.append(
        "Tutorial practico de seguridad para desarrollo Android e infraestructura\n"
        "como codigo. Completa los pasos en orden: cada push activa el validador\n"
        "automatico y el README se actualiza con el siguiente paso.\n"
    )
    lines.append("\n")
    lines.append("---\n")
    lines.append("\n")
    lines.append("## Progreso\n")
    lines.append("\n")
    lines.append(f"**{passed_count}/{total} pasos completados**\n")
    lines.append("\n")
    lines.append("| Paso | Archivo a modificar | Estado |\n")
    lines.append("|------|---------------------|--------|\n")
    for step, file_ref in STEP_FILES.items():
        num = int(step.replace("validate-step-", ""))
        estado = "Completado" if results.get(step, False) else "Pendiente"
        lines.append(f"| Paso {num:02d} | {file_ref} | {estado} |\n")

    # --- Pasos completados: resumen breve ---
    for step in passed:
        num = int(step.replace("validate-step-", ""))
        topic = STEP_TOPICS[step]
        summary = STEP_COMPLETED_SUMMARY[step]
        lines.append("\n")
        lines.append("---\n")
        lines.append("\n")
        lines.append(f"## Paso {num:02d}. {topic} -- Completado\n")
        lines.append("\n")
        lines.append(f"{summary}\n")

    # --- Paso actual: instrucciones completas ---
    if pending:
        current = pending[0]
        num = int(current.replace("validate-step-", ""))
        topic = STEP_TOPICS[current]
        content = STEP_CONTENT[current]
        lines.append("\n")
        lines.append("---\n")
        lines.append("\n")
        lines.append(f"## Paso {num:02d}. {topic}\n")
        lines.append(content)

    # --- Proximos pasos: lista compacta ---
    upcoming = pending[1:] if len(pending) > 1 else []
    if upcoming:
        lines.append("\n")
        lines.append("---\n")
        lines.append("\n")
        lines.append("## Proximos pasos\n")
        lines.append("\n")
        lines.append("| Paso | Tema |\n")
        lines.append("|------|------|\n")
        for step in upcoming:
            num = int(step.replace("validate-step-", ""))
            lines.append(f"| {num:02d} | {STEP_TOPICS[step]} |\n")

    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[OK] README actualizado: {passed_count}/{total} pasos completados")


# ---------------------------------------------------------------------------
# README: pagina de certificado cuando todos pasan
# ---------------------------------------------------------------------------

def write_readme_completed(repo_root, actor, repo, run_id, sha, results):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run_url = f"https://github.com/{repo}/actions/runs/{run_id}"
    commit_url = f"https://github.com/{repo}/commit/{sha}"
    total = len(results)

    step_rows = ""
    for step, topic in STEP_TOPICS.items():
        num = int(step.replace("validate-step-", ""))
        step_rows += f"| {num:02d} | {topic} | PASS |\n"

    content = f"""\
# Secure Coding Mobile e IaC — Completado

> Repositorio de **{actor}**

---

## Certificado de finalizacion

Este repositorio ha superado los {total} controles de seguridad del tutorial
**Secure Coding Mobile e IaC**.

| | |
|---|---|
| **Alumno** | {actor} |
| **Repositorio** | [{repo}](https://github.com/{repo}) |
| **Fecha** | {now} |
| **Pasos** | {total}/{total} |
| **Medalla** | [docs/MEDALLA.md](docs/MEDALLA.md) |

---

## Controles de seguridad implementados

| Paso | Control implementado | Resultado |
|------|----------------------|-----------|
{step_rows}
---

## Prueba de integridad

La medalla fue generada automaticamente por `github-actions[bot]` cuando los
{total} validators pasaron. La prueba es publica y permanente:

- **Run:** {run_url}
- **Commit:** {commit_url}
- **SHA:** `{sha}`

Cualquier persona puede abrir el run y verificar que todos los validators
retornaron PASS en ese commit exacto.

---

## Que has aprendido

- Cifrado de datos en reposo en dispositivos Android con Jetpack Security
- Proteccion de conexiones de red contra ataques de intermediario
- Gestion segura de sesiones con Android Keystore y biometria
- Configuracion segura de infraestructura cloud con Terraform
- Principio de minimo privilegio en politicas IAM de AWS
- Hardening de contenedores Docker: multi-stage y non-root
- Seguridad en pipelines de CI/CD con GitHub Actions
- Ofuscacion de codigo movil con ProGuard

---

_Generado por github-actions[bot] — [{repo}](https://github.com/{repo})_
"""

    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("[OK] README reemplazado con pagina de certificado")


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

    if failed:
        print(f"\n[INFO] {len(failed)} pasos pendientes:")
        for s in sorted(failed):
            print(f"  - {s}")
        update_readme_progress(repo_root, results)
    else:
        print("\n[OK] Todos los validators pasaron. Generando certificado...")
        write_medal(repo_root, repo, actor, run_id, sha, passed)
        write_readme_completed(repo_root, actor, repo, run_id, sha, results)


if __name__ == "__main__":
    main()
