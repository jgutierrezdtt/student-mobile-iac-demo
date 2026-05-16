# Paso 1. Almacenamiento inseguro — SharedPreferences, NSUserDefaults, SQLite sin cifrar

## Objetivo de aprendizaje

Entender por que guardar datos sensibles en almacenamiento local sin proteccion es uno de los riesgos mas frecuentes en aplicaciones moviles, y como elegir el mecanismo de almacenamiento correcto segun la sensibilidad del dato.

## Por que importa esto

Las aplicaciones moviles guardan datos en el dispositivo por muchas razones: preferencias de usuario, cache de sesion, configuracion de la app, y en ocasiones datos que no deberian estar ahi: tokens de autenticacion, contraseñas, numeros de tarjeta o informacion medica.

SharedPreferences en Android y NSUserDefaults en iOS son mecanismos de almacenamiento de clave-valor que guardan los datos en texto plano en un archivo del sistema. Esos archivos son accesibles a cualquier aplicacion con permisos de root, a cualquier herramienta de backup de Android sin cifrar, y a cualquier investigador de seguridad que analice el APK en un emulador.

La regla es simple: lo que guarda una aplicacion movil puede ser recuperado por alguien con acceso fisico o logico al dispositivo. Si el dato es sensible, debe estar en el Keychain de iOS, en el Android Keystore o en una base de datos cifrada. Si no puede estar cifrado, no deberia estar en el dispositivo.

## Que vas a cambiar y por que

En este paso vas a trabajar sobre `src/android/storage/UserPreferences.kt`. La clase almacena el token de autenticacion del usuario en SharedPreferences sin cifrar. El cambio usa EncryptedSharedPreferences, que usa el Android Keystore para derivar una clave de cifrado vinculada al dispositivo.

## Archivo y seccion que debes modificar

- Archivo objetivo: `src/android/storage/UserPreferences.kt`
- Funcion que guarda el token: `saveAuthToken()`
- Funcion que recupera el token: `getAuthToken()`

## Cambio base recomendado

Antes (vulnerable):

```kotlin
// VULNERABLE: token en texto plano en SharedPreferences
val prefs = context.getSharedPreferences("user_prefs", Context.MODE_PRIVATE)
prefs.edit().putString("auth_token", token).apply()
```

Despues (seguro):

```kotlin
// SEGURO: EncryptedSharedPreferences con clave del Android Keystore
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val encryptedPrefs = EncryptedSharedPreferences.create(
    context,
    "secure_user_prefs",
    masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)

encryptedPrefs.edit().putString("auth_token", token).apply()
```

## Que te esta enseñando este cambio

- La diferencia entre SharedPreferences y EncryptedSharedPreferences no es solo de API: es que en el segundo caso los datos en el archivo del sistema estan cifrados con una clave que vive en el Android Keystore, un entorno de hardware aislado que no puede ser extraido directamente.
- El Keystore vincula la clave al dispositivo. Un backup del archivo de SharedPreferences cifrado no sirve de nada en otro dispositivo porque la clave de descifrado no viaja con el backup.
- Para iOS, el equivalente es guardar tokens en el Keychain en lugar de NSUserDefaults. El Keychain de iOS ofrece proteccion similar con niveles de acceso configurables (disponible solo cuando el dispositivo esta desbloqueado, disponible tras primer desbloqueo, etc.).
- Datos que NO son sensibles (preferencias de UI, configuracion no critica) pueden seguir en SharedPreferences normales. El criterio es la sensibilidad del dato, no la comodidad de la API.

## Como adaptarlo correctamente

- Audita todos los puntos de `getSharedPreferences` y `NSUserDefaults.standardUserDefaults()` en el codigo y clasifica que datos guarda cada uno.
- Tokens, contraseñas, identificadores personales y datos financieros deben ir siempre al Keychain (iOS) o EncryptedSharedPreferences / Keystore (Android).
- Si necesitas una base de datos local con datos sensibles, usa SQLCipher en lugar de SQLite estandar. La API es identica pero la base de datos esta cifrada en disco.
- Nunca almacenes tokens de sesion en el portapapeles del sistema: algunas aplicaciones acceden al portapapeles en segundo plano.

## Que deberia verse al terminar

- `UserPreferences.kt` usa `EncryptedSharedPreferences` en lugar de `getSharedPreferences` para el token de autenticacion.
- La inicializacion incluye `MasterKey` con esquema `AES256_GCM`.
- No aparece `getSharedPreferences` ni `putString("auth_token"` sin cifrado.

## Que valida el workflow automaticamente

- `scripts/validate-step-01.py` comprueba que `src/android/storage/UserPreferences.kt` contiene los marcadores.
- El validador busca `EncryptedSharedPreferences`.
- El validador busca `MasterKey`.

## Criterio de finalizacion

El paso 1 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores.
