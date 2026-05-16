package com.myapp.auth

import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyStore
import javax.crypto.KeyGenerator

/**
 * Gestion de sesion con tokens protegidos por el Android Keystore.
 *
 * La clave criptografica que protege el token de sesion requiere
 * autenticacion biometrica del usuario para ser usada. Si el usuario
 * añade nuevas huellas, la clave se invalida automaticamente.
 */
class SessionManager {

    companion object {
        private const val KEY_ALIAS = "session_token_key"
        private const val ANDROID_KEYSTORE = "AndroidKeyStore"
    }

    init {
        generateKeyIfNeeded()
    }

    private fun generateKeyIfNeeded() {
        val keyStore = KeyStore.getInstance(ANDROID_KEYSTORE)
        keyStore.load(null)

        if (!keyStore.containsAlias(KEY_ALIAS)) {
            val keyGenerator = KeyGenerator.getInstance(
                KeyProperties.KEY_ALGORITHM_AES,
                ANDROID_KEYSTORE
            )

            // TODO (step 03): esta clave no requiere autenticacion del usuario.
            // Lee el paso 03 en .tutorial/steps/03-autenticacion-movil.md
            // para ver como vincularla al biometrico del dispositivo.
            val keyGenParameterSpec = KeyGenParameterSpec.Builder(
                KEY_ALIAS,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
            )
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .build()

            keyGenerator.init(keyGenParameterSpec)
            keyGenerator.generateKey()
        }
    }

    fun isSessionActive(): Boolean {
        return try {
            val keyStore = KeyStore.getInstance(ANDROID_KEYSTORE)
            keyStore.load(null)
            keyStore.containsAlias(KEY_ALIAS)
        } catch (e: Exception) {
            false
        }
    }

    fun clearSession() {
        try {
            val keyStore = KeyStore.getInstance(ANDROID_KEYSTORE)
            keyStore.load(null)
            if (keyStore.containsAlias(KEY_ALIAS)) {
                keyStore.deleteEntry(KEY_ALIAS)
            }
        } catch (e: Exception) {
            // Log error but do not expose exception details
        }
    }
}
