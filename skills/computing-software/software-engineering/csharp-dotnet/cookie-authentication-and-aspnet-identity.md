---
id: computing-software.software-engineering.csharp-dotnet.cookie-authentication-and-aspnet-identity
name: cookie-authentication-and-aspnet-identity
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-security, cookie-authentication, aspnet-identity, passwordhasher, lockout, claims]
level: practitioner
status: draft
description: "Secure cookie authentication and ASP.NET Core Identity: cookie flags, sliding expiry, lockout, password policy, Identity API endpoints (.NET 8), claims and common session pitfalls."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/security/authentication/cookie", "https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity", "https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity-api-authorization"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cookie authentication and ASP.NET Core Identity

## Cookie auth
```csharp
builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
  .AddCookie(o => {
      o.Cookie.HttpOnly = true;
      o.Cookie.SecurePolicy = CookieSecurePolicy.Always;
      o.Cookie.SameSite = SameSiteMode.Lax;          // Strict breaks inbound links; None needs Secure
      o.Cookie.Name = "__Host-app";                  // __Host- prefix: Secure, Path=/, no Domain
      o.ExpireTimeSpan = TimeSpan.FromHours(8); o.SlidingExpiration = true;
      o.LoginPath = "/login"; o.AccessDeniedPath = "/denied";
      o.Events.OnRedirectToLogin = c => { if (c.Request.Path.StartsWithSegments("/api")) { c.Response.StatusCode = 401; return Task.CompletedTask; } c.Response.Redirect(c.RedirectUri); return Task.CompletedTask; };
  });
await ctx.SignInAsync(new ClaimsPrincipal(new ClaimsIdentity(claims, "cookie")), new AuthenticationProperties { IsPersistent = false });
```
The cookie is encrypted and signed by Data Protection; share keys across instances (see data protection skill) or users get logged out per node.

## Identity
```csharp
builder.Services.AddIdentity<AppUser, IdentityRole>(o => {
    o.Password.RequiredLength = 12; o.Lockout.MaxFailedAccessAttempts = 5;
    o.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15); o.User.RequireUniqueEmail = true;
    o.SignIn.RequireConfirmedEmail = true;
}).AddEntityFrameworkStores<AppDb>().AddDefaultTokenProviders();
var r = await signIn.PasswordSignInAsync(email, pw, isPersistent: false, lockoutOnFailure: true);
```
.NET 8: `AddIdentityApiEndpoints<AppUser>()` + `MapIdentityApi<AppUser>()` provides register/login/refresh/2FA endpoints for SPAs (bearer or cookie). `PasswordHasher` uses PBKDF2 (HMAC-SHA512, 100k iterations since .NET 7); hashes upgrade on login. `SecurityStamp` validation (default every 30 min) signs out users after password change.

## Gotchas
- Always `lockoutOnFailure: true`; return identical messages for unknown user and wrong password.
- Sensitive actions: re-authenticate; call `SignOutAsync` and rotate on privilege change (session fixation).
- Do not store roles/permissions only in the cookie when revocation matters; validate with `OnValidatePrincipal`.
- Cross-site API calls need CORS credentials and `SameSite=None; Secure`, plus antiforgery.
- Large claims inflate the cookie (4 KB limit chunks).

## Verify
Integration test: unauthenticated API call returns 401 not 302; five bad passwords lock the account; response `Set-Cookie` contains `secure; httponly; samesite=lax`.
