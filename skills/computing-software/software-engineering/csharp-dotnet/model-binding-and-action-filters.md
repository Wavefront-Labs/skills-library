---
id: computing-software.software-engineering.csharp-dotnet.model-binding-and-action-filters
name: model-binding-and-action-filters
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-controllers, model-binding, action-filters, apicontroller, custom-model-binder, iasyncactionfilter]
level: practitioner
status: draft
description: "ASP.NET Core controller model binding sources, validation, custom binders and action filters (IAsyncActionFilter, ServiceFilter, TypeFilter) with correct ordering and short-circuiting."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/mvc/models/model-binding", "https://learn.microsoft.com/en-us/aspnet/core/mvc/controllers/filters", "https://learn.microsoft.com/en-us/aspnet/core/web-api/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Model binding and action filters

## Binding
```csharp
[ApiController, Route("api/orders")]
public class OrdersController : ControllerBase
{
    [HttpPut("{id:int}")]
    public IActionResult Update(int id,                       // route
        [FromQuery] bool dryRun,                              // query string
        [FromHeader(Name = "If-Match")] string? etag,         // header
        [FromBody] UpdateOrder body,                          // JSON body (one per action)
        [FromServices] IClock clock) => Ok();                 // DI
}
```
`[ApiController]` infers sources (complex types from body, simple from route/query), auto-returns 400 `ValidationProblemDetails` when `ModelState` is invalid, and requires attribute routing. Validation uses DataAnnotations or `IValidatableObject`; non-nullable reference types are implicitly `[Required]` (disable with `SuppressImplicitRequiredAttributeForNonNullableReferenceTypes`). Over-posting: bind to a dedicated DTO, never the entity. Custom binder: implement `IModelBinder` + `[ModelBinder(typeof(X))]` for odd formats (comma lists).

## Action filters
```csharp
public sealed class AuditFilter(IAuditLog log) : IAsyncActionFilter
{
    public async Task OnActionExecutionAsync(ActionExecutingContext ctx, ActionExecutionDelegate next)
    {
        if (ctx.ActionArguments.TryGetValue("body", out var b) && b is null)
        { ctx.Result = new BadRequestResult(); return; }      // short-circuit: do not call next
        var done = await next();                              // runs action; done.Exception / done.Result available
        log.Write(ctx.ActionDescriptor.DisplayName, done.Result);
    }
}
builder.Services.AddScoped<AuditFilter>();
[ServiceFilter(typeof(AuditFilter))]  // resolved from DI; or [TypeFilter] to construct with DI args
```
Pipeline order: authorization -> resource -> model binding -> action filters -> action -> result filters. Scope: global (`options.Filters.Add`), controller, action; `Order` property controls ties. Exception filters see only controller exceptions; prefer `IExceptionHandler`/`UseExceptionHandler` middleware app-wide.

## Gotchas
- Filter attributes cannot take constructor DI directly; use ServiceFilter/TypeFilter or `IFilterFactory`.
- Minimal APIs use endpoint filters (`AddEndpointFilter`) instead.
- Model binding failures on JSON throw before filters unless `ModelState` is checked; the 400 comes from the automatic filter.
- Do not read the body twice without `EnableBuffering`.

## Verify
Integration test via `WebApplicationFactory`: invalid body returns 400 with errors dictionary; filter short-circuit leaves the action uncalled.
