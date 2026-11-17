---
id: computing-software.software-engineering.csharp-dotnet.model-validation-and-problemdetails
name: model-validation-and-problemdetails
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, model-validation, aspnet-problem-details, data-annotations, fluentvalidation, iexceptionhandler, aspnet-core]
level: practitioner
status: docs-checked
description: "Validate ASP.NET Core input and return RFC 9457 errors: DataAnnotations and ApiController 400s, minimal API validation, FluentValidation, AddProblemDetails and IExceptionHandler."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/mvc/models/validation", "https://learn.microsoft.com/en-us/aspnet/core/fundamentals/error-handling-api", "https://learn.microsoft.com/en-us/aspnet/core/web-api/handle-errors", "https://docs.fluentvalidation.net/en/latest/aspnet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model validation and ProblemDetails

**Goal:** bad input is rejected with a precise 400 listing each field, and every error
response has one consistent shape.

## DataAnnotations
```csharp
public sealed record CreateOrder(
    [property: Required] Guid CustomerId,
    [property: MinLength(1)] IReadOnlyList<OrderLine> Lines,
    [property: StringLength(500)] string? Note);
public sealed record OrderLine([property: Required, RegularExpression("^[A-Z0-9-]+$")] string Sku,
                               [property: Range(1, 1000)] int Qty);
```
With `[ApiController]`, invalid models automatically return 400 with a
`ValidationProblemDetails` body (`errors: { "Lines[0].Qty": ["..."] }`) before the action runs.
For records, attributes need `property:` targets. `IValidatableObject` handles cross-field rules.

## Minimal APIs
Use endpoint filters or FluentValidation (check the ASP.NET Core docs for built-in minimal API validation in your version):
```csharp
app.MapPost("/orders", (CreateOrder cmd, IValidator<CreateOrder> v) => ...)
   .AddEndpointFilter<ValidationFilter<CreateOrder>>();
// in the filter: var r = await v.ValidateAsync(arg); if (!r.IsValid) return TypedResults.ValidationProblem(r.ToDictionary());
```

## FluentValidation for complex rules
```csharp
public sealed class CreateOrderValidator : AbstractValidator<CreateOrder>
{
    public CreateOrderValidator(ICatalog catalog)
    {
        RuleFor(x => x.Lines).NotEmpty();
        RuleForEach(x => x.Lines).ChildRules(l => l.RuleFor(x => x.Qty).InclusiveBetween(1, 1000));
        RuleFor(x => x.Lines).MustAsync(async (lines, ct) => await catalog.AllExistAsync(lines, ct))
            .WithMessage("Unknown SKU");
    }
}
```
Register with `AddValidatorsFromAssemblyContaining<CreateOrderValidator>()` and call the validator
explicitly (manual validation).

## Consistent errors
```csharp
builder.Services.AddProblemDetails(o => o.CustomizeProblemDetails = c =>
    c.ProblemDetails.Extensions["traceId"] = Activity.Current?.Id ?? c.HttpContext.TraceIdentifier);
builder.Services.AddExceptionHandler<DomainExceptionHandler>();
app.UseExceptionHandler();
app.UseStatusCodePages();          // empty 404/405 responses get ProblemDetails too

sealed class DomainExceptionHandler(IProblemDetailsService pds) : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(HttpContext ctx, Exception ex, CancellationToken ct)
    {
        if (ex is not NotFoundException nf) return false;          // fall through to default 500
        ctx.Response.StatusCode = StatusCodes.Status404NotFound;
        return await pds.TryWriteAsync(new() { HttpContext = ctx, Exception = ex,
            ProblemDetails = { Title = "Not found", Detail = nf.Message } });
    }
}
```
Production 500s must not leak exception details; `Developer exception page` only in Development.

## Verify
- [ ] Integration tests assert 400 bodies contain field-level errors and `application/problem+json`.
- [ ] Unhandled exceptions produce a ProblemDetails 500 with traceId and no stack trace.

## Checked

- Date: 2026-10-28
- Confirmed on Microsoft Learn (model validation, error handling, handle-errors) and FluentValidation ASP.NET docs: ValidationProblemDetails, UseStatusCodePages, IExceptionHandler, manual validation approach.
- Removed: .NET 10 AddValidation claim and the MVC auto-validation deprecation claim.
Method: documentation only; no commands were run.
