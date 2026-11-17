---
id: computing-software.software-engineering.mobile-development.mobile-networking-retrofit-okhttp-urlsession
name: mobile-networking-retrofit-okhttp-urlsession
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, retrofit, okhttp, urlsession, ktor-client, android, ios, networking, interceptors, http-caching]
level: practitioner
status: draft
description: "Build mobile API clients: Retrofit + OkHttp (interceptors, timeouts, auth refresh, caching) on Android and URLSession async/await on iOS, plus error mapping and retries."
sources: ["https://square.github.io/retrofit/", "https://square.github.io/okhttp/", "https://developer.apple.com/documentation/foundation/urlsession", "https://developer.android.com/develop/connectivity/network-ops/connecting"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile networking (Retrofit / OkHttp / URLSession)

**Goal:** a single, well-configured HTTP client per app with sensible timeouts, auth, logging and
error handling, used off the main thread.

## Android: OkHttp + Retrofit
```kotlin
val okHttp = OkHttpClient.Builder()
    .connectTimeout(10, TimeUnit.SECONDS)
    .readTimeout(20, TimeUnit.SECONDS)
    .callTimeout(30, TimeUnit.SECONDS)                 // whole call including retries/redirects
    .cache(Cache(File(ctx.cacheDir, "http"), 20L * 1024 * 1024))
    .addInterceptor(AuthInterceptor(tokenStore))       // adds Authorization header
    .authenticator(TokenRefreshAuthenticator(tokenStore, authApi))   // on 401
    .apply { if (BuildConfig.DEBUG) addInterceptor(HttpLoggingInterceptor().setLevel(BODY)) }
    .build()

val api = Retrofit.Builder()
    .baseUrl("https://api.example.com/")              // must end with /
    .client(okHttp)
    .addConverterFactory(Json { ignoreUnknownKeys = true }.asConverterFactory("application/json".toMediaType()))
    .build()
    .create(Api::class.java)

interface Api {
    @GET("users/{id}") suspend fun user(@Path("id") id: String): UserDto
    @POST("orders") suspend fun createOrder(@Header("Idempotency-Key") key: String, @Body o: OrderDto): Response<OrderDto>
}
```
- **One OkHttpClient** for the app (connection pool, cache, threads); derive variants with
  `okHttp.newBuilder()`. Creating clients per request leaks threads and sockets.
- `suspend` functions run on OkHttp's dispatcher; no `withContext(IO)` needed for the call itself.
- Non-2xx: a `suspend fun foo(): T` throws `HttpException`; return `Response<T>` to inspect codes.
- Token refresh in an `Authenticator` must be synchronised (one refresh for concurrent 401s) and
  return null to give up, avoiding infinite loops.
- Never log bodies or Authorization headers in release builds (`HttpLoggingInterceptor.redactHeader`).
- Ktor client is the Kotlin Multiplatform alternative (OkHttp engine on Android, Darwin on iOS).

## iOS: URLSession
```swift
struct APIClient {
    let session: URLSession = {
        let cfg = URLSessionConfiguration.default
        cfg.timeoutIntervalForRequest = 20          // idle timeout between packets
        cfg.timeoutIntervalForResource = 60         // whole transfer
        cfg.waitsForConnectivity = true             // wait instead of failing offline
        cfg.urlCache = URLCache(memoryCapacity: 10_000_000, diskCapacity: 50_000_000)
        return URLSession(configuration: cfg)
    }()

    func user(id: String) async throws -> User {
        var req = URLRequest(url: base.appending(path: "users/\(id)"))
        req.setValue("Bearer \(try await tokens.access())", forHTTPHeaderField: "Authorization")
        let (data, response) = try await session.data(for: req)
        guard let http = response as? HTTPURLResponse else { throw APIError.invalidResponse }
        guard (200..<300).contains(http.statusCode) else { throw APIError.status(http.statusCode, data) }
        return try JSONDecoder.api.decode(User.self, from: data)
    }
}
```
- URLSession does not throw on 4xx/5xx - check status codes yourself.
- Reuse sessions; `URLSession.shared` has no custom config. Background transfers need
  `URLSessionConfiguration.background(withIdentifier:)` with delegate callbacks.
- Task cancellation propagates: cancelling the Swift `Task` cancels the request.
- ATS requires HTTPS; exceptions in Info.plist need justification in review.
- Alamofire adds interceptors/retriers similar to OkHttp if wanted.

## Cross-platform practices
- Map transport errors to domain errors: offline, timeout, unauthorised, server error, decode error.
  Show retry UI for transient ones.
- Retry only idempotent requests (GET, or POST with an idempotency key), with exponential backoff and
  jitter; respect `Retry-After`.
- Use HTTP caching headers (`ETag`, `Cache-Control`) rather than ad-hoc caches; both clients honour them.
- Decode leniently (ignore unknown fields) so additive API changes do not break old app versions
  that live for years.
- Observe connectivity (`ConnectivityManager.NetworkCallback`, `NWPathMonitor`) for UX, but always
  handle failures since "connected" does not mean reachable.

## Verify
- [ ] Single shared client instance (check DI graph).
- [ ] Airplane mode, slow network (Network Link Conditioner / emulator throttling) and 401 refresh paths tested.
- [ ] No sensitive data in release logs.
