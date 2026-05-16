package com.myapp.network

import okhttp3.OkHttpClient
import java.util.concurrent.TimeUnit

// TODO (step 02): este cliente HTTP no tiene validacion del certificado del servidor.
// Es vulnerable a ataques de intermediario. Lee .tutorial/steps/02-comunicacion-insegura.md
// para implementar pinning criptografico.
object ApiClient {

    private const val API_HOST = "api.myapp.com"

    val httpClient: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
}
