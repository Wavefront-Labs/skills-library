---
id: computing-software.software-engineering.csharp-dotnet.minimal-api-route-groups-and-endpoint-filters
name: minimal-api-route-groups-and-endpoint-filters
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-minimal-apis, route-groups, endpoint-filters, minimal-api-binding, typedresults, validation]
level: practitioner
status: docs-checked
description: "Organise ASP.NET Core minimal APIs with MapGroup, shared filters, parameter binding rules, TypedResults and validation (IEndpointFilter)."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/route-handlers", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/min-api-filters", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis/parameter-binding"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minimal API groups, filters and binding

## Groups
```csharp
var api = app.MapGroup("/api/v1").RequireAuthorization().WithTags("Orders").AddEndpointFilter<RequestLoggingFilter>();
var orders = api.MapGroup("/orders");
orders.MapGet("/{id:int}", GetOrder);
orders.MapPost("/", CreateOrder).AddEndpointFilter<ValidationFilter<NewOrder>>();
orders.MapDelete("/{id:int}", DeleteOrder).RequireAuthorization("admin");

static async Task<Results<Ok<Order>, NotFound>> GetOrder(int id, IOrderRepo repo, CancellationToken ct) =>
    await repo.FindAsync(id, ct) is { } o ? TypedResults.Ok(o) : TypedResults.NotFound();
```
The prefix, authorization requirement, metadata (such as `WithTags`) and filters on a group apply as if added to each child endpoint, before any extra filters or metadata on an inner group or the endpoint itself. Group extension methods (`MapOrders(this IEndpointRouteBuilder)`) keep `Program.cs` small. A group prefix can be empty, to add metadata or filters without changing the route pattern.

## Endpoint filter
```csharp
public class ValidationFilter<T> : IEndpointFilter where T : class {
    public async ValueTask<object?> InvokeAsync(EndpointFilterInvocationContext ctx, EndpointFilterDelegate next) {
        var arg = ctx.Arguments.OfType<T>().FirstOrDefault();
        if (arg is null) return TypedResults.BadRequest();
        var results = new List<ValidationResult>();
        if (!Validator.TryValidateObject(arg, new ValidationContext(arg), results, true))
            return TypedResults.ValidationProblem(results.ToDictionary(r => r.MemberNames.FirstOrDefault() ?? "", r => new[] { r.ErrorMessage ?? "" }));
        return await next(ctx);
    }
}
```
Filter code before `next` runs first-in-first-out and code after `next` runs first-in-last-out. Outer group filters run before inner group filters regardless of the order they were added; order matters only for filters on the same group or endpoint.

## Binding rules
- Binding sources are explicit (`[FromQuery]`, `[FromHeader]`, `[FromForm]` and similar) or inferred from the HTTP method and parameter type. `[AsParameters]` binds a parameter object; `IFormFile` binds uploads.
- `[FromForm]` parameters carry an antiforgery token that is validated when the request is processed (antiforgery is available in .NET 8 or later).
- A non-nullable `string[]` bound from the query string is empty, not null, when the query value is absent.
- Custom binding: static `TryParse(string, out T)` or `BindAsync(HttpContext)`.

## Gotchas
- Handler parameters are required: a missing one is an error and the handler does not run. Make one optional with a nullable type or a default value.
- A route value that cannot be converted (for example `/users/hello/books/3` for an `int`) throws `BadHttpRequestException`.
- Endpoint filters do not run for body-reading failures such as malformed JSON.

## Verify
Integration-test the endpoints: assert 400 for an invalid body, 401 without a token and 200 on the happy path.

## Checked
2026-11-09. Confirmed against the Microsoft Learn pages Route handlers in Minimal API apps, Filters in Minimal API apps and Parameter binding in Minimal API apps (route groups and nested filter order, FIFO/FILO filter order, required parameters, `TryParse`/`BindAsync`, antiforgery for `[FromForm]` in .NET 8 or later). Removed: CORS and rate-limiting group claims, the .NET 10 `AddValidation()` note, the one-body-parameter and GET-body claims, nullable-annotation 400 wording, lambda attribute and anonymous-object remarks, and the `WebApplicationFactory` line (none stated on the pages). Code samples were not compiled.
Method: documentation only; no commands were run.
