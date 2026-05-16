# Paso 6. IAM con exceso de permisos — principio de minimo privilegio en cloud

## Objetivo de aprendizaje

Entender por que los roles y politicas IAM con permisos excesivos son un riesgo de seguridad critico en entornos cloud, y como aplicar el principio de minimo privilegio para limitar el impacto de un compromiso de credenciales.

## Por que importa esto

En AWS, una identidad (usuario, rol, funcion Lambda, instancia EC2) con mas permisos de los necesarios es una superficie de ataque que espera ser explotada. Si un atacante compromete esa identidad (a traves de una vulnerabilidad en la aplicacion, un secreto filtrado o una configuracion incorrecta), tiene acceso a todo lo que esa identidad puede hacer.

El error mas frecuente es usar `"Action": "*"` o `"Resource": "*"` en politicas IAM por comodidad durante el desarrollo. Esas politicas se quedan en produccion porque nadie tiene tiempo de revisarlas y porque "si funciona, no lo toques".

La pregunta correcta al diseñar una politica IAM no es "que permisos necesito para que esto funcione?", sino "cuales son los permisos minimos sin los cuales esto no puede funcionar?".

## Que vas a cambiar y por que

En este paso vas a trabajar sobre `src/iac/terraform/iam.tf`. La politica del rol de la funcion Lambda tiene `"Action": "*"` y `"Resource": "*"`. El cambio reemplaza esa politica con permisos especificos: solo las acciones que la funcion realmente necesita, sobre los recursos concretos que debe acceder.

## Archivo y seccion que debes modificar

- Archivo objetivo: `src/iac/terraform/iam.tf`
- Recurso `aws_iam_policy_document`: bloque `statement` con actions y resources demasiado amplios

## Cambio base recomendado

Antes (vulnerable):

```hcl
# VULNERABLE: acceso total a todos los recursos de AWS
data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions   = ["*"]
    resources = ["*"]
  }
}
```

Despues (seguro):

```hcl
# SEGURO: solo las acciones necesarias sobre los recursos especificos
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

## Que te esta enseñando este cambio

- Dividir la politica en multiples statements con `sid` descriptivos hace que la politica sea legible y auditable. Otro revisor puede entender exactamente que puede hacer esta identidad y por que, sin necesidad de documentacion adicional.
- El ARN del recurso especifico (`arn:aws:s3:::my-app-bucket`) en lugar de `*` limita el radio de explosion: si la funcion Lambda es comprometida, el atacante solo puede acceder a ese bucket especifico, no a todos los buckets de la cuenta.
- `effect = "Allow"` es el default pero escribirlo explicitamente hace la politica mas clara. En politicas complejas, tener el effect explicito reduce errores de interpretacion.
- IAM Access Analyzer de AWS puede analizar las politicas existentes e identificar permisos que no se han usado en los ultimos 90 dias, lo que ayuda a limpiar politicas que se volvieron mas permisivas de lo necesario con el tiempo.

## Como adaptarlo correctamente

- Usa el principio de menor sorpresa al nombrar los roles: `lambda-myapp-s3-reader` es mas informativo que `lambda-role-1`.
- Establece un proceso de revision periodica de politicas IAM. Los permisos tienden a acumularse con el tiempo si no hay revision activa.
- Para entornos con muchos recursos, usa variables de Terraform para construir ARNs dinamicamente y evitar ARNs hardcodeados que se dessincronizan cuando cambian los nombres de los recursos.
- Activa AWS CloudTrail para tener un log de todas las acciones IAM. Es la unica forma de saber si una identidad con demasiados permisos ha sido utilizada de forma sospechosa.

## Que deberia verse al terminar

- La politica IAM en `iam.tf` no usa `"*"` en `actions` ni en `resources`.
- Los statements tienen `sid` descriptivos.
- Los recursos son ARNs especificos o con wildcards acotados a un prefijo.

## Que valida el workflow automaticamente

- `scripts/validate-step-06.py` comprueba que `src/iac/terraform/iam.tf` contiene los marcadores.
- El validador verifica que no existe `actions = ["*"]` ni `resources = ["*"]`.
- El validador busca la presencia de `sid` en los statements.
- El validador busca ARNs especificos en lugar de wildcards globales.

## Criterio de finalizacion

El paso 6 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores.
