---
id: computing-software.software-engineering.ktor.ktor-server-oauth-login
name: ktor-server-oauth-login
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, oauth, authentication, kotlin, google, authorization-code, sessions]
level: practitioner
status: docs-checked
description: "Add OAuth authorization-code login to Ktor Server with the oauth provider: HttpClient, urlProvider, settings, login and redirect routes, session token storage."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-oauth.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/auth-oauth-google/src/main/kotlin/com/example/oauth/google/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OAuth login in Ktor Server

The `oauth` provider (artifact `io.ktor:ktor-server-auth`) supports the authorization code flow with external providers such as Google or Facebook. You configure parameters once and Ktor makes the requests.

## Flow

User opens the login page; Ktor redirects to the provider with client ID, redirect URL, scopes, grant type (Authorization Code) and a `state` parameter against CSRF. After consent the provider redirects back with a code; Ktor exchanges it (with client ID and secret) at the access token URL, then you use the token, usually as `Authorization: Bearer`.

## Steps (Google example)

1. **Credentials.** In Google Cloud Console create an `OAuth client ID` of type `Web application`; set the authorised redirect URI, for example `http://localhost:8080/callback`, and keep the client ID and secret.
2. **Sessions.** Install the Sessions plugin so the access token is stored in a session instead of re-authorizing on every request.
3. **HttpClient.** Create an `HttpClient` with the client `ContentNegotiation` plugin and a JSON serializer (needed to deserialize the API response). Pass it into the `main` module function so tests can supply their own.
4. **Provider.**

```kotlin
install(Sessions) {
    cookie<UserSession>("user_session")
}
val redirects = ConcurrentMap<String, String>()
install(Authentication) {
    oauth("auth-oauth-google") {
        urlProvider = { "http://localhost:8080/callback" }
        settings = OAuthServerSettings.OAuth2ServerSettings(
            name = "google",
            authorizeUrl = googleAuthorizeUrl,   // "https://accounts.google.com/o/oauth2/auth"
            accessTokenUrl = googleTokenUrl,     // "https://accounts.google.com/o/oauth2/token"
            requestMethod = HttpMethod.Post,
            clientId = googleClientId,           // System.getenv("GOOGLE_CLIENT_ID").orEmpty()
            clientSecret = googleClientSecret,   // System.getenv("GOOGLE_CLIENT_SECRET").orEmpty()
            defaultScopes = listOf(profileScope), // "https://www.googleapis.com/auth/userinfo.profile"
            extraAuthParameters = listOf("access_type" to "offline"),
            onStateCreated = { call, state ->
                // saves new state with redirect url
                val query = call.request.queryParameters
                query["redirectUrl"]?.let {
                    redirects[state] = it
                }
            }
        )
        fallback = { cause ->
            if (cause is OAuth2RedirectError) {
                respondRedirect("/login-after-fallback")
            } else {
                respond(HttpStatusCode.Forbidden, cause.message)
            }
        }
        client = httpClient
    }
}
```

   - `urlProvider`: the redirect route; it must be in the authorised redirect URIs.
   - `settings`: static `OAuthServerSettings` (preferred over `providerLookup` for fixed config; it also lets Ktor infer OpenAPI metadata).
   - `providerLookup`: still supported for per-call, dynamic settings (such as tenant-specific credentials).
   - `fallback`: handles OAuth flow errors with a redirect or custom response.
   - `client`: the `HttpClient` Ktor uses.
5. **Login route.** Put a route inside `authenticate("auth-oauth-google")`; hitting it redirects to `authorizeUrl`. Permissions depend on `defaultScopes`.
6. **Redirect route.** Inside it, `call.principal<OAuthAccessTokenResponse>()` gives the token. Save it in a session, redirect onward, and fall back to `/home` if no target is found.

```kotlin
routing {
    authenticate("auth-oauth-google") {
        get("/login") {
            // Redirects to 'authorizeUrl' automatically
        }

        get("/callback") {
            val currentPrincipal: OAuthAccessTokenResponse.OAuth2? = call.principal()
            // redirects home if the url is not found before authorization
            currentPrincipal?.let { principal ->
                principal.state?.let { state ->
                    val session = UserSession(state, principal.accessToken)
                    call.sessions.set(session)
                    redirects.remove(state)?.let { url ->
                        call.respondRedirect(url)
                        return@get
                    }
                }
            }
            call.respondRedirect("/home")
        }
    }
}

@Serializable
data class UserSession(val state: String, val token: String)
```

7. **API call.** Use the `HttpClient` with the stored token in the `Authorization` header. The client is created with `HttpClient(CIO) { install(ContentNegotiation) { json(Json { ignoreUnknownKeys = true }) } }` and passed into `fun Application.main(httpClient: HttpClient = applicationHttpClient)`.

```kotlin
private suspend fun getPersonalGreeting(
    httpClient: HttpClient,
    userSession: UserSession
): UserInfo = httpClient.get("https://www.googleapis.com/oauth2/v2/userinfo") {
    headers {
        val bearer = "Bearer ${userSession.token}"
        append(HttpHeaders.Authorization, bearer)
    }
}.body()

get("/{path}") {
    val userSession: UserSession? = getSession(call)
    if (userSession != null) {
        val userInfo: UserInfo = getPersonalGreeting(httpClient, userSession)
        call.respondText("Hello, ${userInfo.name}!")
    }
}
```

Ktor also offers typed OAuth 2.0 flows and an `Oidc` plugin as alternatives.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-oauth.md, codeSnippets/snippets/auth-oauth-google/src/main/kotlin/com/example/oauth/google/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
