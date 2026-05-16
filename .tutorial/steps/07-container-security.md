# Paso 7. Seguridad en contenedores — hardening de Dockerfile, non-root e imagenes minimas

## Objetivo de aprendizaje

Entender por que los Dockerfiles inseguros amplian la superficie de ataque de una aplicacion contenida, y como aplicar las practicas de hardening que limitan el impacto de un compromiso del contenedor.

## Por que importa esto

Un contenedor Docker no es una barrera de seguridad completa: es un nivel de aislamiento del sistema operativo. Si el proceso dentro del contenedor se ejecuta como root, y hay una vulnerabilidad que permite salir del contenedor (container escape), el atacante obtiene acceso root al host. Si la imagen base tiene cientos de herramientas instaladas, el atacante tiene un arsenal completo dentro del contenedor comprometido.

Los errores mas frecuentes en Dockerfiles son: usar imagenes base con sistema operativo completo (ubuntu, debian) cuando podria usarse una imagen minimal o distroless, ejecutar el proceso de la aplicacion como usuario root, instalar dependencias de build en la imagen final, y no fijar las versiones de las dependencias base.

## Que vas a cambiar y por que

En este paso vas a trabajar sobre `src/docker/Dockerfile`. El Dockerfile usa `node:18` como imagen base (imagen completa con herramientas de sistema), ejecuta la aplicacion como root, y no usa multi-stage build, lo que incluye las dependencias de desarrollo en la imagen final.

## Archivo y seccion que debes modificar

- Archivo objetivo: `src/docker/Dockerfile`
- `FROM`: cambiar a imagen minimal o alpine
- Usuario: añadir `USER` para ejecutar como non-root
- Estructura: convertir a multi-stage build para separar build de runtime

## Cambio base recomendado

Antes (vulnerable):

```dockerfile
# VULNERABLE: imagen completa, usuario root, dependencias de dev incluidas
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "server.js"]
```

Despues (seguro):

```dockerfile
# SEGURO: multi-stage build con imagen minimal y usuario non-root

# Stage 1: build con todas las dependencias
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: imagen final minimal
FROM node:18-alpine AS runtime
WORKDIR /app

# Crear usuario non-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copiar solo el resultado del build, no las dev dependencies
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=appuser:appgroup . .

# Cambiar a usuario non-root antes de ejecutar la aplicacion
USER appuser

EXPOSE 3000
CMD ["node", "server.js"]
```

## Que te esta enseñando este cambio

- `node:18-alpine` es una imagen basada en Alpine Linux que pesa unos 50 MB en lugar de los 350 MB de `node:18`. Menos herramientas instaladas significa menos vectores de ataque si el contenedor es comprometido.
- El multi-stage build separa el entorno de build (con compiladores, herramientas de desarrollo y dependencias de dev) del entorno de runtime (solo lo necesario para ejecutar). Las dependencias de dev no deben estar en produccion.
- `USER appuser` antes del `CMD` garantiza que el proceso de la aplicacion no tiene permisos de root. Si hay una vulnerabilidad en la aplicacion que permite ejecutar comandos arbitrarios, esos comandos se ejecutan con permisos de usuario limitado, no como root.
- `--chown=appuser:appgroup` en la instruccion `COPY` asegura que los archivos pertenecen al usuario de la aplicacion, no a root. Sin eso, el usuario non-root podria no tener permisos para leer sus propios archivos.

## Como adaptarlo correctamente

- Para aplicaciones que no necesitan shell en produccion, considera imagenes distroless (gcr.io/distroless/nodejs18-debian12). No tienen shell, gestores de paquetes ni utilidades de sistema, lo que hace imposible muchos tipos de ataque post-explotacion.
- Fija las versiones de la imagen base con el digest SHA256 ademas del tag: `FROM node:18-alpine@sha256:...`. Los tags son mutables; los digests no.
- Usa `npm ci` en lugar de `npm install` en CI/CD: instala exactamente lo que esta en `package-lock.json` sin modificarlo.
- Analiza las imagenes con herramientas como Trivy o Grype para detectar CVEs en las dependencias del sistema operativo incluidas en la imagen base.

## Que deberia verse al terminar

- `Dockerfile` usa imagen alpine o minimal en lugar de imagen completa.
- Hay una instruccion `USER` que cambia a un usuario non-root antes del `CMD`.
- El Dockerfile usa multi-stage build con `AS builder` y `AS runtime`.

## Que valida el workflow automaticamente

- `scripts/validate-step-07.py` comprueba que `src/docker/Dockerfile` contiene los marcadores.
- El validador busca `USER` seguido de un usuario non-root.
- El validador busca `AS builder` o `AS runtime` como indicador de multi-stage.
- El validador verifica que la imagen base usa alpine o imagen minimal.

## Criterio de finalizacion

El paso 7 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores.
