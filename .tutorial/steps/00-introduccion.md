# Paso 0. Introduccion al tutorial de Secure Coding para Mobile e IaC

Bienvenido al tutorial de programacion segura para aplicaciones moviles e infraestructura como codigo.

## Que vas a aprender

Este tutorial cubre las vulnerabilidades mas frecuentes en desarrollo de aplicaciones moviles (Android e iOS) y en la definicion de infraestructura mediante codigo (Terraform, CloudFormation, Docker, pipelines de CI/CD). Cada paso explica el riesgo, muestra el patron inseguro y enseña la mitigacion correcta con su razonamiento.

| Paso | Tema |
| ---- | ---- |
| 1 | Almacenamiento inseguro — SharedPreferences, NSUserDefaults, SQLite sin cifrar |
| 2 | Comunicacion insegura — TLS, certificate pinning |
| 3 | Autenticacion movil — tokens, biometria, gestion de sesion |
| 4 | Configuraciones erroneas en IaC — S3 publico, security groups abiertos |
| 5 | Secretos en IaC — credenciales hardcodeadas, variables de entorno, parameter store |
| 6 | IAM con exceso de permisos — principio de minimo privilegio en cloud |
| 7 | Seguridad en contenedores — hardening de Dockerfile, non-root, imagenes minimas |
| 8 | Seguridad en pipelines de CI/CD — permisos de workflow, tokens, supply chain |
| 9 | Ingenieria inversa y ofuscacion — ProGuard, R8, proteccion de logica critica |
| 10 | Medalla final — consolidacion del programa de secure coding mobile e IaC |

## A quien va dirigido

A desarrolladores moviles (Android/iOS) y equipos DevOps que trabajan con IaC y quieren entender los riesgos de seguridad en sus tecnologias especificas. No se asume conocimiento previo de seguridad.

## Como funciona el tutorial

1. Lee el paso correspondiente en `.tutorial/steps/`.
2. Estudia el codigo vulnerable o la configuracion insegura en `src/`.
3. Aplica el cambio indicado siguiendo el patron de mitigacion.
4. El workflow de GitHub Actions valida automaticamente que el cambio es correcto.

## Empezar tutorial

Ejecuta el workflow `Start Tutorial` desde la pestana Actions de este repositorio.

## Tabla de pasos

| Paso | Archivo de instrucciones |
| ---- | ------------------------ |
| Paso 0 | `.tutorial/steps/00-introduccion.md` |
| Paso 1 | `.tutorial/steps/01-almacenamiento-inseguro.md` |
| Paso 2 | `.tutorial/steps/02-comunicacion-insegura.md` |
| Paso 3 | `.tutorial/steps/03-autenticacion-movil.md` |
| Paso 4 | `.tutorial/steps/04-iac-misconfigurations.md` |
| Paso 5 | `.tutorial/steps/05-secretos-en-iac.md` |
| Paso 6 | `.tutorial/steps/06-iam-overpermissive.md` |
| Paso 7 | `.tutorial/steps/07-container-security.md` |
| Paso 8 | `.tutorial/steps/08-cicd-security.md` |
| Paso 9 | `.tutorial/steps/09-obfuscation.md` |
| Paso 10 | `.tutorial/steps/10-medalla-final.md` |
