# Paso 3. Autenticacion movil — tokens, biometria y gestion de sesion

## Objetivo de aprendizaje

Entender como gestionar de forma segura los tokens de sesion en una aplicacion movil, como integrar la autenticacion biometrica correctamente, y por que la gestion de sesion en movil tiene consideraciones distintas a las de una aplicacion web.

## Por que importa esto

En una aplicacion movil, el token de sesion que permite acceder a la API vive en el dispositivo del usuario. Si ese token se filtra (por backup inseguro, por extraccion de la app, por analisis del APK), el atacante puede impersonar al usuario indefinidamente.

La autenticacion biometrica en movil es una herramienta muy util para mejorar la experiencia de usuario, pero su implementacion tiene errores frecuentes. El error mas comun es usar la biometria como factor de autenticacion que el servidor conoce y verifica, cuando en realidad la biometria del dispositivo es un mecanismo de desbloqueo local que deberia proteger el acceso al token almacenado, no transmitirse al servidor.

## Que vas a cambiar y por que

En este paso vas a trabajar sobre `src/android/auth/SessionManager.kt`. La clase gestiona el ciclo de vida del token de sesion. El cambio protege el token con una clave del Keystore vinculada a la autenticacion biometrica del dispositivo.

## Archivo y seccion que debes modificar

- Archivo objetivo: `src/android/auth/SessionManager.kt`
- Funcion de almacenamiento del token: `saveSession()`
- Funcion de acceso al token: `getSessionToken()`
- Funcion de autenticacion biometrica: `authenticateWithBiometrics()`

## Cambio base recomendado

```kotlin
// SEGURO: Clave del Keystore que requiere autenticacion biometrica para desbloquear
val keyGenParameterSpec = KeyGenParameterSpec.Builder(
    KEY_ALIAS,
    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setUserAuthenticationRequired(true)
    .setUserAuthenticationParameters(0, KeyProperties.AUTH_BIOMETRIC_STRONG)
    .build()

// El token solo puede descifrarse despues de autenticacion biometrica exitosa
// La biometria desbloquea la clave del Keystore, no se transmite al servidor
```

Invalidar la sesion ante cambios de biometria:

```kotlin
// SEGURO: setInvalidatedByBiometricEnrollment(true) invalida la clave si el usuario
// añade nuevas huellas, forzando re-autenticacion con contraseña
.setInvalidatedByBiometricEnrollment(true)
```

## Que te esta enseñando este cambio

- `setUserAuthenticationRequired(true)` vincula la clave criptografica del Keystore a la autenticacion del usuario. Eso significa que la clave solo puede usarse despues de que el sistema operativo confirme que el usuario se ha autenticado biometricamente en los ultimos N segundos.
- La biometria del dispositivo no es algo que debas enviar al servidor. Es un mecanismo local del sistema operativo para confirmar la presencia del usuario. El servidor no sabe ni necesita saber que tipo de biometria tiene el usuario.
- `setInvalidatedByBiometricEnrollment(true)` es una decision de seguridad importante: si alguien con acceso fisico al dispositivo añade su propia huella dactilar, la clave queda invalidada y el usuario tiene que re-autenticarse con contraseña. Sin esta opcion, añadir una nueva huella podria dar acceso a un atacante.
- Los tokens de sesion deben tener tiempo de vida limitado. En movil, combina tokens de corta duracion con refresh tokens que se usan para obtener nuevos tokens sin requerir credenciales completas.

## Como adaptarlo correctamente

- Implementa revocacion de sesion en el servidor: cuando el usuario cierra sesion desde la app, el token debe invalidarse en el servidor aunque siga siendo valido por tiempo.
- Diseña el manejo de sesiones multiples: si el usuario tiene la app en varios dispositivos, cada dispositivo debe tener su propio token con capacidad de revocacion independiente.
- Cuando la autenticacion biometrica falla repetidamente (por cambio de huellas, por lesion), la app debe ofrecer un camino de recuperacion seguro que no exponga el token de otra forma.
- Audita los logs de la aplicacion: no deben contener tokens de sesion, ni siquiera parcialmente.

## Que deberia verse al terminar

- `SessionManager.kt` usa una clave del Keystore con `setUserAuthenticationRequired(true)`.
- La clave usa `setInvalidatedByBiometricEnrollment(true)`.
- No hay tokens de sesion en SharedPreferences sin cifrar ni en logs.

## Que valida el workflow automaticamente

- `scripts/validate-step-03.py` comprueba que `src/android/auth/SessionManager.kt` contiene los marcadores.
- El validador busca `setUserAuthenticationRequired`.
- El validador busca `setInvalidatedByBiometricEnrollment`.

## Criterio de finalizacion

El paso 3 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores.
