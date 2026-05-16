# TODO (step 09): este archivo no tiene reglas de ofuscacion activa.
# Lee el paso 09 en .tutorial/steps/09-obfuscation.md
# para anadir reglas de ofuscacion con diccionario personalizado.

# Componentes de Android — el framework los instancia por nombre
-keep public class * extends android.app.Activity
-keep public class * extends android.app.Application
-keep public class * extends android.app.Service
-keep public class * extends android.content.BroadcastReceiver
-keep public class * extends android.content.ContentProvider
-keep public class * extends android.view.View

# Parcelables
-keep class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator CREATOR;
}

# Enums
-keepnames enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

# Optimizacion basica
-optimizationpasses 3
