---
id: computing-software.software-engineering.csharp-dotnet.aspnet-core-jwt-bearer-and-authorization-policies
name: aspnet-core-jwt-bearer-and-authorization-policies
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet, aspnet-core, jwt-bearer, authorization-policies, claims, resource-based-authorization]
level: practitioner
status: docs-checked
description: "Secure ASP.NET Core APIs with JWT bearer authentication, policy-based and resource-based authorization, claim mapping pitfalls and tests for 401/403 behaviour."
sources:
  - https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication
  - https://learn.microsoft.com/en-us/aspnet/core/security/authorization/policies
  - https://learn.microsoft.com/en-us/aspnet/core/security/authorization/resourcebased
  - https://learn.microsoft.com/en-us/aspnet/core/security/authentication/jwt-authn
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT bearer authentication and authorization policies

**Goal:** tokens from your identity provider are validated strictly, and authorization rules live in named policies rather than scattered role checks.

## 1. JWT bearer
```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(o =>
    {
        o.Authority = "https://login.example.com/realms/acme";   // OIDC discovery + signing keys
        o.Audience = "orders-api";
        o.MapInboundClaims = false;                               // keep "sub", "roles" as-is
        o.TokenValidationParameters = new()
        {
            ValidateIssuer = true, ValidateAudience = true, ValidateLifetime = true,
            ClockSkew = TimeSpan.FromSeconds(30),                 // default is 5 minutes
            NameClaimType = "sub", RoleClaimType = "roles",
        };
    });
```
- `MapInboundClaims = false` stops renaming `sub` to `http://schemas.xmlsoap.org/.../nameidentifier`, the classic "claim not found" bug.
- Never disable signature validation: the docs state the signature must be validated so the token can be trusted.

## 2. Policies
```csharp
builder.Services.AddAuthorizationBuilder()
    .SetFallbackPolicy(new AuthorizationPolicyBuilder().RequireAuthenticatedUser().Build())  // secure by default
    .AddPolicy("orders:write", p => p.RequireClaim("scope", "orders:write"))
    .AddPolicy("support", p => p.RequireRole("support", "admin"))
    .AddPolicy("adult", p => p.Requirements.Add(new MinimumAgeRequirement(18)));

app.MapPost("/orders", CreateOrder).RequireAuthorization("orders:write");
app.MapGet("/status", () => "ok").AllowAnonymous();
```
`RequireClaim` compares claim values exactly, so check how your identity provider encodes scopes (one claim per scope or one combined string) before relying on it.

## 3. Custom requirements
```csharp
public sealed record MinimumAgeRequirement(int Age) : IAuthorizationRequirement;
public sealed class MinimumAgeHandler : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(AuthorizationHandlerContext ctx, MinimumAgeRequirement req)
    {
        if (ctx.User.FindFirst("birthdate") is { } c && Age(c.Value) >= req.Age) ctx.Succeed(req);
        return Task.CompletedTask;
    }
}
builder.Services.AddSingleton<IAuthorizationHandler, MinimumAgeHandler>();
```

## 4. Resource-based authorization (is this my order?)
```csharp
var order = await db.Orders.FindAsync(id);
var result = await authz.AuthorizeAsync(User, order, "SameOwner");
if (!result.Succeeded) return Results.Forbid();
```
URL/role rules cannot express ownership; check after loading the resource.

## 5. Testing
Replace the scheme in `WebApplicationFactory` with a test handler that issues configurable claims, or generate tokens with a local signing key (`dotnet user-jwts create --scope orders:write` for dev).

## Gotchas
- 401 = missing/invalid token; 403 = valid identity lacking permission. Returning 404 for others' resources avoids leaking existence.
- Multiple schemes: specify `AuthenticationSchemes` on the policy or `[Authorize]` attribute, otherwise the default scheme is used.
- Middleware order: `UseAuthentication` before `UseAuthorization`.

## Verify
- Tests cover no token (401), expired/wrong-audience token (401), missing scope (403), other user's resource (403/404), valid (200).

## Checked

Checked 2026-10-25 against aspnet/AspNetCore.Docs (configure-jwt-bearer-authentication, policies, resource-based, claims, jwt-authn) and the Microsoft.IdentityModel source on main.
Confirmed: `AddJwtBearer` `Authority`/`Audience` and `MapInboundClaims = false`; `AddAuthorizationBuilder().SetFallbackPolicy(...)` (default fallback policy is null); `AuthorizeAsync(user, resource, policyName)`; `dotnet user-jwts create --scope` (one per scope); `TokenValidationParameters.DefaultClockSkew` is 300 s (5 minutes).
Removed as unconfirmed: `RequireHttpsMetadata` advice, the IdentityModel PII logging tip, the space-separated scope claim behaviour.

Method: documentation only; no commands were run.
