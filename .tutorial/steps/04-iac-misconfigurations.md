# Paso 4. Configuraciones erroneas en IaC — S3 publico, security groups abiertos

## Objetivo de aprendizaje

Entender que los errores de configuracion en infraestructura como codigo (IaC) tienen el mismo impacto que las vulnerabilidades en el codigo de aplicacion, y que Terraform y CloudFormation tienen patrones de configuracion inseguros que son faciles de introducir si no se conocen.

## Por que importa esto

Algunos de los incidentes de seguridad mas costosos de los ultimos anos no vinieron de explotar vulnerabilidades en el codigo de la aplicacion: vinieron de buckets de S3 publicos, de bases de datos con el puerto 5432 abierto a internet, o de security groups que permitian `0.0.0.0/0` en puertos criticos.

La ventaja de IaC (Terraform, CloudFormation) es que la infraestructura es codigo revisable, versionable y auditable. La desventaja es que un error de configuracion que se aplica con `terraform apply` puede exponer terabytes de datos o permitir acceso remoto a toda la infraestructura en segundos.

Los errores mas frecuentes son tres: buckets de S3 sin bloqueo de acceso publico, security groups con `0.0.0.0/0` en puertos de administracion (22, 3389, 5432), y bases de datos con `publicly_accessible = true`.

## Que vas a cambiar y por que

En este paso vas a trabajar sobre `src/iac/terraform/main.tf`. La configuracion de Terraform tiene un bucket S3 sin restriccion de acceso publico, un security group que permite SSH desde cualquier IP, y una instancia de RDS con acceso publico habilitado.

## Archivo y seccion que debes modificar

- Archivo objetivo: `src/iac/terraform/main.tf`
- Recurso S3: falta el bloque `aws_s3_bucket_public_access_block`
- Recurso security group: `cidr_blocks = ["0.0.0.0/0"]` en puerto 22
- Recurso RDS: `publicly_accessible = true`

## Cambio base recomendado

Bloqueo de acceso publico en S3:

```hcl
# SEGURO: bloquear todo acceso publico al bucket
resource "aws_s3_bucket_public_access_block" "app_bucket" {
  bucket = aws_s3_bucket.app_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

Security group con acceso SSH restringido:

```hcl
# SEGURO: SSH solo desde el rango de IPs de la VPN corporativa
ingress {
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["10.0.0.0/8"]  # Rango de VPN — no 0.0.0.0/0
}
```

RDS sin acceso publico:

```hcl
# SEGURO: la base de datos no es accesible directamente desde internet
resource "aws_db_instance" "main" {
  publicly_accessible = false
  # ...
}
```

## Que te esta enseñando este cambio

- `block_public_acls = true` no es suficiente por si solo. Necesitas los cuatro atributos del bloque `aws_s3_bucket_public_access_block` para una proteccion completa. Cada uno bloquea un mecanismo distinto por el que un bucket puede volverse publico.
- `0.0.0.0/0` en un security group significa "cualquier IP del mundo". Para SSH, eso significa que cualquier persona puede intentar autenticarse en el servidor. Aunque la autenticacion sea robusta, la superficie de ataque es maxima.
- `publicly_accessible = false` en RDS hace que la base de datos solo sea accesible desde dentro de la VPC. Aunque las credenciales de la base de datos se filtren, el atacante necesita estar dentro de la red privada para conectarse.
- Estos tres errores de configuracion aparecen en el top de los hallazgos en auditorias de seguridad cloud porque son faciles de introducir durante el desarrollo rapido y pasan desapercibidos en revisiones de codigo si el revisor no conoce los defaults de AWS.

## Como adaptarlo correctamente

- Usa herramientas de analisis estatico de IaC (tfsec, checkov, terrascan) en el pipeline de CI para detectar configuraciones inseguras antes de aplicarlas.
- Activa AWS Config con reglas como `s3-bucket-public-read-prohibited` y `restricted-ssh` para detectar derivas en la configuracion desplegada.
- Para entornos de desarrollo donde el acceso temporal desde IPs externas es necesario, usa Security Group rules temporales con fecha de expiracion o gestionalas a traves de un bastion host.
- El principio de minimo privilegio aplica a la red: cada recurso debe ser accesible solo desde los origenes que necesita, no desde `0.0.0.0/0` por conveniencia.

## Que deberia verse al terminar

- `main.tf` incluye `aws_s3_bucket_public_access_block` con los cuatro atributos en `true`.
- El security group no tiene `0.0.0.0/0` en el puerto 22.
- El recurso RDS tiene `publicly_accessible = false`.

## Que valida el workflow automaticamente

- `scripts/validate-step-04.py` comprueba que `src/iac/terraform/main.tf` contiene los marcadores.
- El validador busca `block_public_acls`.
- El validador verifica que `publicly_accessible = false` esta presente.
- El validador verifica que no existe `cidr_blocks = ["0.0.0.0/0"]` en el puerto 22.

## Criterio de finalizacion

El paso 4 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores.
