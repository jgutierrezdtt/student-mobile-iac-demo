-obfuscationdictionary proguard-dictionary.txt
-classobfuscationdictionary proguard-dictionary.txt
-packageobfuscationdictionary proguard-dictionary.txt

-keepclassmembers class * implements java.io.Serializable {
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}

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
