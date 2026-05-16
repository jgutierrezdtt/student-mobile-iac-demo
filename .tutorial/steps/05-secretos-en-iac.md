# Paso 5. Secretos en IaC — credenciales hardcodeadas, variables de entorno y AWS Parameter Store

## Objetivo de aprendizaje

Entender por que los secretos nunca deben aparecer en archivos de IaC ni en variables de entorno en texto plano, y como integrar un gestor de secretos (AWS Parameter Store, AWS Secrets Manager) en la definicion de infraestructura como codigo.

## Por que importa esto

Un secreto en un archivo de Terraform o CloudFormation es un secreto en el repositorio de git. Git recuerda todo: aunque borres el secreto en el proximo commit, sigue visible en el historial. Cualquier persona con acceso al repositorio (actual o futuro) puede ver el secreto con un simple `git log -S`.

El mismo problema afecta a los archivos de variables de entorno (`.env`) que se suben al repositorio, a los archivos de estado de Terraform (`terraform.tfstate`) que contienen el estado desplegado incluyendo valores sensibles, y a los outputs de Terraform que pueden exponer secretos en los logs del pipeline.

La solucion no es tratar los secretos con mas cuidado: es no tenerlos en el repositorio en absoluto. Los secretos deben vivir en un gestor de secretos y referenciarse desde el codigo de IaC, no incrustarse en el.

## Que vas a cambiar y por que

En este paso vas a trabajar sobre `src/iac/terraform/secrets.tf`. El archivo tiene la contraseña de la base de datos como valor literal y una clave de API en una variable sin marcar como sensible. El cambio referencia esos valores desde AWS Parameter Store usando el data source de Terraform.

## Archivo y seccion que debes modificar

- Archivo objetivo: `src/iac/terraform/secrets.tf`
- Variable con contraseña de DB: debe venir de Parameter Store, no estar hardcodeada
- Variable de API key: debe marcarse como `sensitive = true` y venir de Parameter Store

## Cambio base recomendado

Antes (vulnerable):

```hcl
# VULNERABLE: contraseña hardcodeada en el codigo de IaC
resource "aws_db_instance" "main" {
  password = "supersecretpassword123"
}
```

Despues (seguro):

```hcl
# SEGURO: la contraseña viene de Parameter Store, no del codigo
data "aws_ssm_parameter" "db_password" {
  name            = "/prod/db/password"
  with_decryption = true
}

resource "aws_db_instance" "main" {
  password = data.aws_ssm_parameter.db_password.value
}
```

Marcar outputs sensibles:

```hcl
# SEGURO: marcar como sensitive para que no aparezca en logs del pipeline
output "api_key" {
  value     = data.aws_ssm_parameter.api_key.value
  sensitive = true
}
```

## Que te esta enseñando este cambio

- `with_decryption = true` en el data source de SSM Parameter Store descifra el valor usando KMS en el momento de la ejecucion de Terraform. El secreto nunca aparece en el codigo fuente ni en el repositorio.
- `sensitive = true` en un output de Terraform hace que Terraform oculte el valor en los logs de `terraform apply`. Sin esa marcacion, cualquier pipeline que ejecute Terraform mostraria el secreto en texto plano en los logs, que generalmente son accesibles a toda la organizacion.
- El archivo `terraform.tfstate` contiene el estado de la infraestructura desplegada, incluyendo valores sensibles. Debe almacenarse en un backend remoto con cifrado habilitado (S3 + DynamoDB con SSE), nunca en el repositorio.
- Variables de entorno en texto plano en archivos `.tfvars` subidos al repositorio tienen el mismo problema que las credenciales hardcodeadas: estan en git para siempre.

## Como adaptarlo correctamente

- Añade `terraform.tfstate`, `*.tfstate.backup`, y `*.tfvars` al `.gitignore` del repositorio.
- Configura el backend de Terraform con cifrado: `encrypt = true` en el bucket S3 y `encrypt_at_rest = true`.
- Para rotar secretos, actualiza el valor en Parameter Store y re-ejecuta Terraform: el data source tomara el nuevo valor sin cambios en el codigo.
- Usa AWS Secrets Manager cuando necesites rotacion automatica de secretos (credenciales de base de datos, API keys con TTL).

## Que deberia verse al terminar

- `secrets.tf` usa data sources de `aws_ssm_parameter` para los secretos.
- No hay valores de contraseñas o API keys como literales en el codigo de Terraform.
- Los outputs sensibles tienen `sensitive = true`.

## Que valida el workflow automaticamente

- `scripts/validate-step-05.py` comprueba que `src/iac/terraform/secrets.tf` contiene los marcadores.
- El validador busca `aws_ssm_parameter` en los data sources.
- El validador busca `sensitive = true` en los outputs.
- El validador verifica que no hay valores de contraseña como literales evidentes.

## Criterio de finalizacion

El paso 5 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores.
