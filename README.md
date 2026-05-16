# Secure Coding Mobile e IaC

Tutorial practico de seguridad para desarrollo Android e infraestructura como codigo. En 10 pasos aprenderás a proteger las capas mas vulnerables de un sistema moderno: el dispositivo movil, la infraestructura cloud y la cadena de entrega de software.

## Por que importa este tutorial

Los errores de seguridad en movil e IaC son especialmente costosos porque:

- Una APK comprometida llega a millones de dispositivos de usuarios reales.
- Un bucket S3 publico puede exponer terabytes de datos en segundos.
- Un pipeline de CI/CD con permisos excesivos da acceso directo al codigo de produccion.
- Las vulnerabilidades en IaC se reproducen en cada despliegue hasta que alguien las detecta.

Este tutorial cubre exactamente esos vectores de ataque con codigo real y explicaciones de por que cada vulnerabilidad es un problema y por que cada mitigacion funciona.

## Tabla de pasos

| Paso | Tema | Vulnerabilidad que resuelves | Por que es peligrosa |
|------|------|------------------------------|----------------------|
| 01 | Almacenamiento inseguro | Datos sensibles en SharedPreferences sin cifrar | Un backup del dispositivo o una app maliciosa puede leer los datos directamente |
| 02 | Comunicacion insegura | Sin certificate pinning en OkHttp | Un atacante MITM puede interceptar todo el trafico aunque uses HTTPS |
| 03 | Autenticacion movil | Token de sesion sin proteccion biometrica del Keystore | El token filtrado permite impersonar al usuario indefinidamente |
| 04 | Configuraciones IaC | S3 publico, security groups abiertos, RDS accesible | Una configuracion incorrecta en Terraform se propaga a cada despliegue |
| 05 | Secretos en IaC | Contraseñas hardcodeadas en variables de Terraform | Git recuerda todo; un secreto en el historial es un secreto comprometido |
| 06 | IAM con exceso de permisos | Politicas con `Action: *` y `Resource: *` | Si las credenciales se filtran, el atacante tiene acceso total a la cuenta AWS |
| 07 | Seguridad en contenedores | Proceso como root, imagen completa, sin multi-stage | Container running as root + exploit = acceso root al host |
| 08 | Seguridad en CI/CD | Workflow con write-all, acciones sin version fija | Un pipeline comprometido puede modificar el codigo y los deployments |
| 09 | Ingenieria inversa | ProGuard con keeps demasiado amplios | Sin ofuscacion, la logica de negocio y los endpoints son visibles en el APK |
| 10 | Medalla final | Consolidacion de todos los controles | Checklist de referencia para auditorias y nuevos proyectos |

## Empezar tutorial

1. Haz fork de este repositorio.
2. Abre el archivo `.tutorial/steps/00-introduccion.md` para ver la introduccion.
3. Completa cada paso en orden, modificando los archivos indicados.
4. Cada push activa el validador automatico en GitHub Actions.

## Tabla de pasos (resumen de progreso)

| Paso | Archivo a modificar | Estado |
|------|---------------------|--------|
| Paso 0 | Introduccion — lee primero | Empezar aqui |
| Paso 1 | `src/android/storage/UserPreferences.kt` | Pendiente |
| Paso 2 | `src/android/network/ApiClient.kt` | Pendiente |
| Paso 3 | `src/android/auth/SessionManager.kt` | Pendiente |
| Paso 4 | `src/iac/terraform/main.tf` | Pendiente |
| Paso 5 | `src/iac/terraform/secrets.tf` | Pendiente |
| Paso 6 | `src/iac/terraform/iam.tf` | Pendiente |
| Paso 7 | `src/docker/Dockerfile` | Pendiente |
| Paso 8 | `src/pipeline/.github/workflows/deploy.yml` | Pendiente |
| Paso 9 | `src/android/proguard-rules.pro` | Pendiente |
| Paso 10 | `docs/secure-coding-mobile-iac-checklist.md` | Pendiente |

## Nivel

Profesional. Requiere conocimientos basicos de Android (Kotlin), Terraform y GitHub Actions.

## Estructura del repositorio

```
src/
  android/
    storage/    — UserPreferences.kt (Jetpack Security)
    network/    — ApiClient.kt (OkHttp CertificatePinner)
    auth/       — SessionManager.kt (Android Keystore)
    proguard-rules.pro
  iac/terraform/
    main.tf     — S3, VPC, security groups, RDS
    secrets.tf  — SSM Parameter Store data sources
    iam.tf      — Roles y politicas con minimo privilegio
  docker/
    Dockerfile  — Multi-stage, non-root
  pipeline/.github/workflows/
    deploy.yml  — Permissions, actions fijadas por SHA
docs/
  secure-coding-mobile-iac-checklist.md
scripts/
  validate-step-01.py ... validate-step-10.py
```
