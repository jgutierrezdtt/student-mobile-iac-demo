# Paso 10. Medalla final — consolidacion de controles de seguridad mobile e IaC

## Objetivo de aprendizaje

Consolidar todos los controles de seguridad aprendidos en este tutorial y completar el checklist de seguridad para desarrollo movil y de infraestructura como codigo.

## Por que importa esto

La seguridad en movil y en IaC no son problemas aislados: estan interconectados. La aplicacion movil se comunica con una API protegida por autenticacion. Esa API vive en infraestructura configurada por Terraform. Esa infraestructura es desplegada por un pipeline de CI/CD. El pipeline usa contenedores Docker. Todos esos elementos comparten una cadena de confianza: un fallo en cualquier eslabon puede comprometer el conjunto.

Completar este checklist no es solo marcar cajas: es un mapa de los vectores de ataque que ya has cubierto y una guia para futuros proyectos donde tengas que empezar desde cero.

## Que vas a cambiar y por que

En este paso vas a completar el archivo `docs/secure-coding-mobile-iac-checklist.md`. El checklist tiene cuatro frentes: almacenamiento y comunicacion segura, autenticacion movil, cloud e IaC security, y pipeline y supply chain. Completar el archivo significa que tienes una referencia documentada de todos los controles aplicados.

## Archivo y seccion que debes modificar

- Archivo objetivo: `docs/secure-coding-mobile-iac-checklist.md`
- Frente 1: Almacenamiento y comunicacion segura
- Frente 2: Autenticacion movil y gestion de sesion
- Frente 3: Cloud e IaC security
- Frente 4: Pipeline y supply chain

## Cambio base recomendado

El archivo debe contener los cuatro frentes con sus controles verificados:

```markdown
# Checklist de seguridad — Mobile e IaC

## Frente 1: Almacenamiento y comunicacion segura

- [ ] Datos sensibles almacenados con EncryptedSharedPreferences o EncryptedFile (Jetpack Security)
- [ ] Clave maestra generada con MasterKey.Builder y AES256_GCM
- [ ] Certificate pinning implementado con OkHttp CertificatePinner
- [ ] No existe checkServerTrusted vacio o que acepta cualquier certificado
- [ ] Datos de usuario no se almacenan en almacenamiento externo sin cifrado

## Frente 2: Autenticacion movil y gestion de sesion

- [ ] Tokens de sesion protegidos con clave del Keystore vinculada a biometria
- [ ] setUserAuthenticationRequired(true) activo en la generacion de la clave
- [ ] setInvalidatedByBiometricEnrollment(true) para invalidar ante cambios de huella
- [ ] Tokens con tiempo de vida limitado y refresh tokens separados
- [ ] Revocacion de sesion implementada en el servidor

## Frente 3: Cloud e IaC security

- [ ] Buckets S3 con aws_s3_bucket_public_access_block (cuatro atributos en true)
- [ ] Security groups sin 0.0.0.0/0 en puertos de administracion (22, 3389, 5432)
- [ ] RDS con publicly_accessible = false
- [ ] Secretos referenciados desde Parameter Store o Secrets Manager, no hardcodeados
- [ ] Variables sensibles marcadas con sensitive = true en outputs de Terraform
- [ ] Politicas IAM con acciones y recursos especificos (sin wildcards globales)
- [ ] Backend de Terraform con cifrado habilitado

## Frente 4: Pipeline y supply chain

- [ ] Workflows de GitHub Actions con permissions especificos por scope
- [ ] Acciones de terceros fijadas al commit SHA en lugar de tags mutables
- [ ] Inputs de usuario pasados via env: en lugar de interpolacion directa en run:
- [ ] Imagenes Docker basadas en alpine o distroless (no imagen completa)
- [ ] Proceso de aplicacion ejecutandose como usuario non-root
- [ ] Multi-stage build para excluir dependencias de desarrollo de la imagen final
- [ ] Reglas de ProGuard con keeps especificos (no wildcards que cubren todo el paquete)
- [ ] -obfuscationdictionary activo para ofuscacion agresiva
```

## Que te esta enseñando este cambio

- Los cuatro frentes representan las capas de defensa en un sistema moderno: el dispositivo movil, la autenticacion, la infraestructura cloud, y la cadena de entrega de software. Un atacante que no puede comprometer una capa intentara la siguiente.
- La documentacion de controles de seguridad es tan importante como los controles en si. Un checklist permite que equipos nuevos entiendan rapidamente el posture de seguridad de la aplicacion y que revisores de seguridad verifiquen que nada ha sido omitido.
- Cada control en este checklist tiene una razon de ser especifica: no es una lista de "buenas practicas generales" sino controles derivados de patrones de ataque reales que han comprometido aplicaciones moviles e infraestructura cloud en el mundo real.
- La seguridad no es un estado que se alcanza: es un proceso continuo. Este checklist es un punto de partida, no un punto final.

## Como adaptarlo correctamente

- Convierte este checklist en parte del proceso de code review: ningun PR que afecte a las areas cubiertas deberia ser aprobado sin verificar los controles relevantes.
- Añade los controles de este frente a las definiciones de "done" de los tickets de desarrollo que los requieran.
- Actualiza el checklist cuando el stack tecnologico cambie: las herramientas cambian pero los principios (minimo privilegio, defensa en profundidad, no exponer lo que no necesita ser expuesto) se mantienen.
- Usa este checklist como base para auditorias de seguridad periodicas de la infraestructura existente.

## Que deberia verse al terminar

- `docs/secure-coding-mobile-iac-checklist.md` contiene los cuatro frentes con sus controles.
- El archivo tiene los marcadores `Frente 1`, `Frente 2`, `Frente 3` y `Frente 4`.

## Que valida el workflow automaticamente

- `scripts/validate-step-10.py` comprueba que `docs/secure-coding-mobile-iac-checklist.md` contiene los marcadores.
- El validador busca `Frente 1`, `Frente 2`, `Frente 3` y `Frente 4`.

## Criterio de finalizacion

El paso 10 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores. Has completado el tutorial de Secure Coding Mobile e IaC.
