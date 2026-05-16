package com.myapp.storage

import android.content.Context
import android.content.SharedPreferences

// TODO (step 01): este archivo usa SharedPreferences en texto claro.
// Los tokens y datos de usuario quedan expuestos en el sistema de archivos.
// Lee .tutorial/steps/01-almacenamiento-inseguro.md para implementar cifrado.
class UserPreferences(context: Context) {

    private val prefs: SharedPreferences =
        context.getSharedPreferences("user_prefs", Context.MODE_PRIVATE)

    fun saveUserToken(token: String) {
        prefs.edit().putString(KEY_TOKEN, token).apply()
    }

    fun getUserToken(): String? {
        return prefs.getString(KEY_TOKEN, null)
    }

    fun saveUserId(userId: String) {
        prefs.edit().putString(KEY_USER_ID, userId).apply()
    }

    fun getUserId(): String? {
        return prefs.getString(KEY_USER_ID, null)
    }

    fun clearAll() {
        prefs.edit().clear().apply()
    }

    companion object {
        private const val KEY_TOKEN = "auth_token"
        private const val KEY_USER_ID = "user_id"
    }
}
