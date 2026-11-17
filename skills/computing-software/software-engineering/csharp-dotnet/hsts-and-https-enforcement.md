---
id: computing-software.software-engineering.csharp-dotnet.hsts-and-https-enforcement
name: hsts-and-https-enforcement
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-security, hsts-https, https-redirection, security-headers, kestrel-certificates, dev-certs]
level: practitioner
status: docs-checked
description: "Enforce HTTPS in ASP.NET Core: UseHttpsRedirection, HSTS configuration, redirect status and port, dev certificates and TLS termination behind proxies."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/security/enforcing-ssl", "https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-dev-certs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HSTS and HTTPS enforcement

```csharp
builder.Services.AddHsts(o => { o.MaxAge = TimeSpan.FromDays(365); o.IncludeSubDomains = true; o.Preload = false; });
if (!builder.Environment.IsDevelopment())
    builder.Services.AddHttpsRedirection(o => { o.RedirectStatusCode = StatusCodes.Status308PermanentRedirect; o.HttpsPort = 443; });
if (!app.Environment.IsDevelopment()) app.UseHsts();
app.UseHttpsRedirection();
```
- `UseHttpsRedirection` sends `307 Temporary Redirect` by default; the docs recommend temporary redirects because link caching causes unstable behaviour in development. For a permanent redirect, set `RedirectStatusCode` to 308 only when not in Development, as above.
- `AddHttpsRedirection` is only needed to change `HttpsPort` or `RedirectStatusCode`.
- The HTTPS port is found from `HttpsRedirectionOptions.HttpsPort`, the `https_port` host setting (including `ASPNETCORE_HTTPS_PORT` or a top-level `https_port` in appsettings.json), or `IServerAddressesFeature` (not available behind a reverse proxy). With no port, no redirect happens and a warning `Failed to determine the https port for redirect` is logged.
- `ASPNETCORE_HTTPS_PORT` (redirect target) is not the same as `ASPNETCORE_HTTPS_PORTS` (Kestrel/HTTP.sys endpoints).
- Edge deployments must listen on both the secure port and the insecure port, or the client can never reach the redirect.

## HSTS
- The browser stores the policy for the domain and forces HTTPS; it needs at least one successful HTTPS request first, and the client must support HSTS.
- Do not call `UseHsts` in development: settings are highly cacheable. By default it excludes the loopback address. `HstsOptions` has `MaxAge`, `IncludeSubDomains`, `Preload` and `ExcludedHosts`.
- First HTTPS rollout: set `MaxAge` small, from hours to no more than a day, in case you must revert to HTTP; raise it (commonly one year) once the HTTPS setup is proven.

## Behind a TLS-terminating proxy
Run forwarded headers middleware before `UseHttpsRedirection`. It sets `Request.Scheme` from `X-Forwarded-Proto`; without it the app may redirect forever ("too many redirects").

## Dev certificates
`dotnet dev-certs https --trust` trusts the generated certificate (untrusted by default); `--check` with `--trust` verifies trust; `dotnet dev-certs https --clean` removes dev certificates.

## Checked
2026-11-08. Confirmed against the ASP.NET Core "Enforce HTTPS" page (307 default, 308 production example, HttpsPort resolution, warning text, edge ports, forwarded headers and redirect loops, HSTS options, loopback exclusion, small initial max-age) and the dotnet dev-certs page (--trust, --check, --clean). Removed as unconfirmed on those pages: preload irreversibility, API redirect advice, Kestrel SslProtocols and certificate configuration keys, security-header list, AddServerHeader, Linux trust note, curl and openssl verification steps.
Method: documentation only; no commands were run.
