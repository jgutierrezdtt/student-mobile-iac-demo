# Paso 9. Ingenieria inversa y ofuscacion — ProGuard, R8 y proteccion del codigo Android

## Objetivo de aprendizaje

Entender por que una aplicacion Android sin ofuscacion puede ser revertida a codigo legible en minutos, que informacion es critica proteger con ofuscacion, y como configurar ProGuard y R8 para maximizar la proteccion sin romper la funcionalidad de la aplicacion.

## Por que importa esto

Una APK es un archivo ZIP con bytecode Dalvik/ART que cualquier herramienta de decompilacion (jadx, apktool, dex2jar) puede convertir en codigo Java o Kotlin legible. Sin ofuscacion, el atacante puede leer la logica de negocio, encontrar los endpoints de la API, descubrir algoritmos propietarios, y buscar secretos hardcodeados o valores constantes criticos.

La ofuscacion no es criptografia: un atacante con suficiente tiempo y habilidad puede invertir codigo ofuscado. Pero la ofuscacion aumenta significativamente el costo de ese analisis, lo que es el objetivo: hacer que el ataque sea suficientemente costoso como para que no valga la pena. Combinada con certificate pinning y almacenamiento seguro, crea una defensa en profundidad efectiva.

## Que vas a cambiar y por que

En este paso vas a trabajar sobre `src/android/proguard-rules.pro`. El archivo tiene reglas de `keep` demasiado amplias que efectivamente desactivan la ofuscacion para toda la aplicacion. El cambio restringe los keeps a lo estrictamente necesario y activa la ofuscacion para el resto del codigo.

## Archivo y seccion que debes modificar

- Archivo objetivo: `src/android/proguard-rules.pro`
- Reglas `-keep` demasiado amplias: reemplazar con keeps especificos para modelos y componentes de Android
- Reglas de ofuscacion activa: añadir `-obfuscationdictionary` y configuracion de renaming agresivo

## Cambio base recomendado

Antes (vulnerable — ofuscacion desactivada):

```proguard
# VULNERABLE: keep demasiado amplio — desactiva la ofuscacion para toda la app
-keep class com.myapp.** { *; }
-keepclassmembers class * { *; }
```

Despues (seguro — ofuscacion activa con keeps especificos):

```proguard
# SEGURO: mantener solo lo que necesita ser legible en runtime

# Modelos de datos que se serializan/deserializan con Gson o Moshi
-keepclassmembers class com.myapp.models.** {
    <fields>;
}

# Componentes de Android que el framework debe poder instanciar por nombre
-keep public class * extends android.app.Activity
-keep public class * extends android.app.Service
-keep public class * extends android.content.BroadcastReceiver
-keep public class * extends android.content.ContentProvider

# Parcelables
-keepclassmembers class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
}

# Activa renaming agresivo con diccionario de ofuscacion
-obfuscationdictionary proguard-dictionary.txt
-classobfuscationdictionary proguard-dictionary.txt
-packageobfuscationdictionary proguard-dictionary.txt
```

## Que te esta enseñando este cambio

- `-keep class com.myapp.** { *; }` con el wildcard `{ *; }` mantiene todos los nombres de clases, todos los campos y todos los metodos con sus nombres originales en todo el paquete. Es equivalente a no tener ofuscacion. La regla correcta es usar `-keepclassmembers` para clases especificas y solo para los miembros que necesitan sus nombres originales.
- `-obfuscationdictionary` le dice a ProGuard o R8 que use los tokens del archivo como nombres para las clases y metodos ofuscados en lugar de los nombres generados automaticamente (a, b, c...). Un diccionario bien elegido puede hacer que el codigo ofuscado sea aun mas confuso para un analista humano.
- La diferencia entre `-keep` y `-keepclassmembers` es importante: `-keep` preserva la clase y todos sus miembros con sus nombres. `-keepclassmembers` ofusca el nombre de la clase pero preserva los nombres de los miembros especificados. Para modelos de datos, quieres `-keepclassmembers` porque Gson necesita los nombres de los campos pero no el nombre de la clase.
- La ofuscacion debe configurarse y probarse en cada build de release. Cambios en la estructura del codigo pueden requerir actualizar las reglas de ProGuard.

## Como adaptarlo correctamente

- Ejecuta siempre un test completo de la aplicacion despues de cambios en las reglas de ProGuard. Reglas incorrectas pueden causar crashes en runtime por reflection que no puede encontrar clases o metodos.
- Guarda el archivo de mapping generado por cada build de release (`mapping.txt`). Es necesario para desofuscar los stack traces de crashes en produccion.
- Para librerias de terceros, consulta su documentacion de ProGuard: la mayoria publica las reglas necesarias para funcionar correctamente con ofuscacion activada.
- Considera usar Android App Bundle en lugar de APK directa: el sistema de Play Protect aplica ofuscacion adicional automaticamente en algunos casos.

## Que deberia verse al terminar

- `proguard-rules.pro` no tiene reglas `-keep` con wildcards que cubran todo el paquete.
- Las reglas `-keepclassmembers` son especificas a clases y miembros concretos.
- Hay instrucciones de `-obfuscationdictionary` activas.

## Que valida el workflow automaticamente

- `scripts/validate-step-09.py` comprueba que `src/android/proguard-rules.pro` contiene los marcadores.
- El validador busca `-keepclassmembers` (reglas especificas en lugar de amplias).
- El validador busca `-obfuscationdictionary` como indicador de ofuscacion activa.
- El validador verifica que no existe `-keep class com.** { *; }` u otras reglas ampliamente permisivas.

## Criterio de finalizacion

El paso 9 queda completado cuando el workflow de GitHub Actions valida este cambio sin errores.
