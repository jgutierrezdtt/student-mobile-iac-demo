# Paso 2. Comunicacion insegura — TLS y certificate pinning

## Objetivo de aprendizaje

Entender por que aceptar cualquier certificado TLS en una aplicacion movil equivale a no tener cifrado en la comunicacion, y como el certificate pinning añade una capa de proteccion contra ataques de intermediario incluso cuando el atacante tiene un certificado de CA confiada.

## Por que importa esto

HTTPS cifra la comunicacion entre la aplicacion y el servidor, pero ese cifrado solo es util si la aplicacion verifica que el certificado presentado por el servidor es legitimo. Muchos desarrolladores, al encontrar errores de SSL en pruebas, añaden codigo que acepta cualquier certificado. Eso anula completamente la proteccion TLS.

Con un certificado de CA confiada (que un atacante puede obtener o que una CA comprometida puede emitir), o en una red corporativa con inspeccion SSL, un atacante puede hacer un ataque de intermediario (MITM) sin que la aplicacion lo detecte. El certificate pinning va un paso mas alla: la aplicacion verifica no solo que el certificado es valido segun las CAs del sistema, sino que es exactamente el certificado (o la clave publica) que espera del servidor.

## Que vas a cambiar y por que

En este paso vas a trabajar sobre `src/android/network/ApiClient.kt`. La configuracion de OkHttp tiene un `TrustManager` personalizado que acepta cualquier certificado. El cambio implementa certificate pinning usando el `CertificatePinner` de OkHttp.

## Archivo y seccion que debes modificar

- Archivo objetivo: `src/android/network/ApiClient.kt`
- La configuracion de `OkHttpClient` o `SSLContext` que acepta cualquier certificado

## Cambio base recomendado

Antes (vulnerable):

```kotlin
// VULNERABLE: acepta cualquier certificado — TLS sin verificacion
val trustAllCerts = arrayOf<TrustManager>(object : X509TrustManager {
    override fun checkClientTrusted(chain: Array<X509Certificate>, authType: String) {}
    override fun checkServerTrusted(chain: Array<X509Certificate>, authType: String) {}
    override fun getAcceptedIssuers(): Array<X509Certificate> = arrayOf()
})
```

Despues (seguro):

```kotlin
// SEGURO: certificate pinning — solo acepta el certificado exacto del servidor
val certificatePinner = CertificatePinner.Builder()
    .add("api.myapp.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .add("api.myapp.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=") // backup pin
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

## Que te esta enseñando este cambio

- Un `TrustManager` que no lanza excepciones en `checkServerTrusted` es el equivalente en codigo a quitar el candado de la puerta pero dejar la puerta cerrada: parece seguro pero no lo esta.
- El certificate pinning usa el hash SHA-256 de la clave publica del certificado. Cuando el servidor presenta su certificado, la aplicacion verifica que el hash de su clave publica esta en la lista de pins. Si no lo esta, rechaza la conexion.
- Siempre añade un pin de backup (del certificado de la CA o de un certificado de renovacion futuro). Si solo tienes el pin del certificado actual y ese certificado expira, la aplicacion deja de funcionar para todos los usuarios hasta que actualicen a una version con el nuevo pin.
- Para iOS, el equivalente es `NSURLSession` con `URLSessionDelegate` que implementa `urlSession(_:didReceive:completionHandler:)`, o usar `TrustKit` que facilita la gestion de pins.

## Como adaptarlo correctamente

- Genera el hash del pin con: `openssl x509 -in cert.pem -noout -pubkey | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | base64`
- Si el backend usa un CDN o balanceador de carga con certificados rotativos, el pinning puede ser al certificado de la CA intermedia en lugar del certificado del servidor final.
- El pinning tiene un coste operativo: requiere un proceso para actualizar pins antes de que los certificados venzan. Documenta ese proceso en el runbook de la aplicacion.
- Network Security Configuration en Android (archivo XML) es otra forma de configurar el pinning que no requiere cambios en el codigo de la app.

## Que deberia verse al terminar

- No hay ningun `TrustManager` que acepte todos los certificados (`checkServerTrusted` sin logica).
- El `OkHttpClient` o la configuracion de red incluye `CertificatePinner` o `certificatePinner`.
- Hay al menos dos pins configurados para el dominio principal.

## Que valida el workflow automaticamente

- `scripts/validate-step-02.py` comprueba que `src/android/network/ApiClient.kt` contiene los marcadores.
- El validador busca `CertificatePinner` o `certificatePinner`.
- El validador verifica que no existe `checkServerTrusted` con implementacion vacia.

## Criterio de finalizacion

El paso 2 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores.
