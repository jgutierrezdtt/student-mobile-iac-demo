# Checklist de seguridad — Secure Coding Mobile e IaC

## Frente 1: Almacenamiento seguro en el dispositivo

- [x] Implementar almacenamiento cifrado con EncryptedSharedPreferences
- [x] Usar MasterKey con esquema AES256_GCM

## Frente 2: Autenticacion y comunicacion segura

- [x] Proteger conexiones de red con certificate pinning
- [x] Gestionar sesiones con autenticacion biometrica via AndroidKeyStore

## Frente 3: IaC sin misconfiguraciones

- [x] Bloquear acceso publico a buckets S3
- [x] Configurar RDS como no publicamente accesible
- [x] Marcar outputs sensibles con sensitive = true
- [x] Identificar statements IAM con sid y effect explicito

## Frente 4: Contenedores y pipelines seguros

- [x] Imagen Docker multi-stage con usuario no privilegiado
- [x] Workflow de CI con permissions minimos declarados
- [x] Reglas de ofuscacion activas en ProGuard
- [ ] Construir imagenes de contenedor con aislamiento por etapas
- [ ] Configurar permisos minimos en los pipelines de CI/CD
- [ ] Aplicar ofuscacion al codigo del APK
