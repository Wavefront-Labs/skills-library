---
id: computing-software.software-engineering.mobile-development.sign-in-with-apple-and-credential-manager
name: sign-in-with-apple-and-credential-manager
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, sign-in-with-apple, credential-manager, passkeys, google-sign-in, authentication, webauthn, nonce]
level: advanced
status: draft
description: "Implement native sign-in: Sign in with Apple (nonce, server token validation, revocation), Android Credential Manager for passkeys, passwords and Google ID, plus iOS passkeys."
sources: ["https://developer.apple.com/documentation/sign_in_with_apple", "https://developer.apple.com/documentation/authenticationservices/implementing_user_authentication_with_sign_in_with_apple", "https://developer.android.com/identity/sign-in/credential-manager", "https://developer.android.com/identity/sign-in/credential-manager-siwg", "https://developer.apple.com/documentation/authenticationservices/public-private-key-authentication"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sign in with Apple and Credential Manager

**Goal:** fast, phishing-resistant sign-in using platform credential APIs, with tokens verified on
your server and policy requirements met.

## Store requirements
- App Store guideline 4.8: apps offering third-party social login (Google, Facebook) as the primary
  account option must also offer an equivalent privacy-focused option - Sign in with Apple
  satisfies it. Exceptions exist (own account system only, enterprise, education).
- Apps that support account creation must support **account deletion** in-app (Apple 5.1.1(v),
  Google Play); for Sign in with Apple, revoke tokens on deletion.

## Sign in with Apple (iOS)
```swift
SignInWithAppleButton(.signIn) { request in
    let nonce = randomNonce()                 // keep raw nonce
    currentNonce = nonce
    request.requestedScopes = [.fullName, .email]
    request.nonce = sha256(nonce)             // hashed nonce goes to Apple
} onCompletion: { result in
    guard case .success(let auth) = result,
          let cred = auth.credential as? ASAuthorizationAppleIDCredential,
          let idToken = cred.identityToken.flatMap({ String(data: $0, encoding: .utf8) }),
          let code = cred.authorizationCode.flatMap({ String(data: $0, encoding: .utf8) }) else { return }
    Task { try await api.appleSignIn(idToken: idToken, code: code, rawNonce: currentNonce, name: cred.fullName) }
}
```
- **Name and email are returned only on the first authorisation** - send them to your server then;
  later sign-ins return only the stable `user` identifier.
- Users can choose **Hide My Email** (`@privaterelay.appleid.com`); register your sending domains in
  the Apple developer portal or emails to relay addresses bounce.
- Server: verify the identity token JWT signature with Apple's JWKS (`https://appleid.apple.com/auth/keys`),
  `iss = https://appleid.apple.com`, `aud = your bundle id / services id`, `exp`, and that the token's
  `nonce` equals SHA-256 of the raw nonce. Exchange the authorization code at
  `https://appleid.apple.com/auth/token` (client secret = JWT signed with your Sign in with Apple key)
  to get a refresh token, needed for **revocation** (`/auth/revoke`) on account deletion.
- Check credential state on launch: `ASAuthorizationAppleIDProvider().getCredentialState(forUserID:)`
  and handle the revocation notification.
- Android/web: Sign in with Apple via the web flow (Services ID + redirect URL).

## Android: Credential Manager
One API for passkeys, saved passwords and federated sign-in (Sign in with Google), replacing
Smart Lock and legacy Google Sign-In APIs:
```kotlin
val credentialManager = CredentialManager.create(context)
val googleOption = GetGoogleIdOption.Builder()
    .setServerClientId(WEB_CLIENT_ID)           // OAuth client of type "Web" for your backend
    .setFilterByAuthorizedAccounts(true)         // returning users first; retry with false for sign-up
    .setNonce(nonce)
    .build()
val request = GetCredentialRequest.Builder()
    .addCredentialOption(GetPublicKeyCredentialOption(requestJsonFromServer))   // passkey
    .addCredentialOption(GetPasswordOption())
    .addCredentialOption(googleOption)
    .build()
try {
    val result = credentialManager.getCredential(activityContext, request)
    when (val c = result.credential) {
        is PublicKeyCredential -> api.finishPasskeyLogin(c.authenticationResponseJson)
        is PasswordCredential -> api.login(c.id, c.password)
        is CustomCredential -> if (c.type == GoogleIdTokenCredential.TYPE_GOOGLE_ID_TOKEN_CREDENTIAL) {
            api.googleSignIn(GoogleIdTokenCredential.createFrom(c.data).idToken)
        }
    }
} catch (e: GetCredentialException) { /* NoCredentialException -> show sign-up options */ }
```
- Passkeys need a **Digital Asset Links** file (`/.well-known/assetlinks.json`) with
  `delegate_permission/common.get_login_creds` linking the app to your relying-party domain; the
  server runs WebAuthn ceremonies (use a library such as SimpleWebAuthn, webauthn4j, py_webauthn).
- Create passkeys after sign-in: `CreatePublicKeyCredentialRequest(registrationJson)`; offer it in
  settings and post-login prompts.
- Verify Google ID tokens server-side (Google's libraries; check `aud` = your web client id).
- Sign-out: `clearCredentialState()` so auto-select does not immediately sign the user back in.

## iOS passkeys
`ASAuthorizationPlatformPublicKeyCredentialProvider(relyingPartyIdentifier: "example.com")` with
assertion/registration requests; associated domains entitlement `webcredentials:example.com` and the
`apple-app-site-association` file. AutoFill-assisted requests show passkeys in the keyboard bar.

## Verify
- [ ] Server validates every token (signature, issuer, audience, nonce, expiry).
- [ ] First-time Apple sign-in captures name/email; relay emails deliverable.
- [ ] Account deletion revokes Apple tokens; passkey sign-in works on a second device via sync.
