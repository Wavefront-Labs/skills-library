---
id: computing-software.software-engineering.csharp-dotnet.data-protection-and-antiforgery
name: data-protection-and-antiforgery
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-security, data-protection-api, antiforgery, key-ring, csrf, dataprotection]
level: advanced
status: docs-checked
description: "ASP.NET Core Data Protection key ring persistence across instances and antiforgery (CSRF) tokens for forms and SPAs, with key lifetime and container pitfalls."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/security/data-protection/introduction", "https://learn.microsoft.com/en-us/aspnet/core/security/data-protection/configuration/overview", "https://learn.microsoft.com/en-us/aspnet/core/security/anti-request-forgery"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data Protection and antiforgery

## Data Protection
Protects payloads such as authentication cookies and tokens. Keys live in a key ring; the default key lifetime is 90 days (`SetDefaultKeyLifetime` changes it).
```csharp
builder.Services.AddDataProtection()
    .SetApplicationName("shop")                                          // must match across apps sharing cookies
    .PersistKeysToAzureBlobStorage(blobUri)                              // or ...ToStackExchangeRedis / ...ToDbContext<KeysDb> / ...ToFileSystem(dir)
    .ProtectKeysWithAzureKeyVault(keyId, credential);                    // encrypt keys at rest (or certificate)
```
In a Docker container, keep keys in a folder on a Docker volume that persists beyond the container's lifetime (shared or host-mounted), or in another store such as a database or Azure Blob Storage, and set the same application name on apps that share protected data. Protect keys at rest (for example with Azure Key Vault or a certificate).

## Antiforgery
Token-based validation is opt-in with `app.UseAntiforgery()` (also implied by `AddMvc`, `MapRazorPages` or `AddRazorComponents`). An invalid verdict becomes an HTTP 400 only when a component that processes form data, such as Minimal API form binding, observes it. The current page also describes an automatic CSRF middleware that protects apps that do not call `UseAntiforgery()`; check which behaviour your target framework version has.
```csharp
builder.Services.AddAntiforgery(o => { o.HeaderName = "X-XSRF-TOKEN"; o.Cookie.SecurePolicy = CookieSecurePolicy.Always; });
app.MapGet("/csrf", (IAntiforgery af, HttpContext c) => { var t = af.GetAndStoreTokens(c); return Results.Ok(new { t.RequestToken }); });
```
SPA: set `HeaderName` and send the request token in that header; if `HeaderName` is null only form data is considered. Endpoints secured only by non-cookie authentication (bearer tokens, API keys) or not callable from a browser can be opted out individually; do not disable CSRF protection on cookie-authenticated browser endpoints.

## Gotchas
- Multiple apps sharing protected data need the same application name and key ring.
- `SameSite` cookies help but are defence in depth: older browsers and non-browser clients may not enforce it, and `Lax` cookies are still sent on top-level GET requests, so state-changing GET endpoints stay vulnerable.

## Verify
Restart the app (or a second replica) and confirm existing cookies still decrypt; a form POST without a valid token returns 400.

## Checked
2026-11-09. Confirmed against the Microsoft Learn pages Data Protection introduction, Configure ASP.NET Core Data Protection and Prevent Cross-Site Request Forgery (XSRF/CSRF) attacks: 90-day default key lifetime, `SetApplicationName`, `PersistKeysTo*`/`ProtectKeysWith*` providers, Docker key persistence, `UseAntiforgery()`, `HeaderName`, `CookieSecurePolicy.Always`, the 400 verdict, SameSite caveats, non-cookie endpoint opt-out. Removed (not stated on the pages): time-limited protector, TempData and antiforgery-token claims, ephemeral default location, purpose-string and clock-skew gotchas, password-hasher and archival remarks, .NET 8 Minimal API default wording. Also removed the `CreateProtector`/`Protect` example (not on the pages read).
Method: documentation only; no commands were run.
