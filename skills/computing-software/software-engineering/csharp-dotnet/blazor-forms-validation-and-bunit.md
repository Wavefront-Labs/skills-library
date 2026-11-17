---
id: computing-software.software-engineering.csharp-dotnet.blazor-forms-validation-and-bunit
name: blazor-forms-validation-and-bunit
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-ui, blazor-forms, bunit, editform, dataannotationsvalidator, component-testing]
level: practitioner
status: draft
description: "Build Blazor forms with EditForm, DataAnnotations validation and streaming SSR form handling (SupplyParameterFromForm), then test components with bUnit."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/blazor/forms/", "https://learn.microsoft.com/en-us/aspnet/core/blazor/forms/validation", "https://bunit.dev/docs/getting-started/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blazor forms and bUnit

```razor
<EditForm Model="Model" OnValidSubmit="Save" FormName="signup" Enhance>
    <DataAnnotationsValidator />
    <ValidationSummary />
    <InputText @bind-Value="Model.Email" class="form-control" />
    <ValidationMessage For="() => Model.Email" />
    <InputNumber @bind-Value="Model.Age" />
    <button disabled="@busy">Save</button>
</EditForm>
@code {
    [SupplyParameterFromForm] SignUp Model { get; set; } = new();     // required for static SSR so posted values bind
    bool busy;
    async Task Save() { busy = true; try { await Api.Create(Model); } finally { busy = false; } }
    public class SignUp { [Required, EmailAddress] public string Email { get; set; } = ""; [Range(18, 120)] public int Age { get; set; } }
}
```
- `OnValidSubmit` / `OnInvalidSubmit` / `OnSubmit` (then call `EditContext.Validate()` yourself).
- In static SSR, give the form a unique `FormName`; antiforgery is automatic with `EditForm` and `UseAntiforgery()` (.NET 8).
- DataAnnotations validate only top-level properties; for nested/complex models use `Microsoft.AspNetCore.Components.DataAnnotations.Validation` (`[ValidateComplexType]`, experimental) or FluentValidation adapters.
- Server-side validation is mandatory; client validation is UX only. Map API `ValidationProblemDetails` into `ValidationMessageStore`.
- Disable the submit button while busy to prevent double posts.

## bUnit tests
```csharp
public class SignUpTests : TestContext
{
    [Fact] public void Invalid_email_shows_message()
    {
        Services.AddSingleton<IApi>(Substitute.For<IApi>());
        var cut = RenderComponent<SignUpForm>();
        cut.Find("input").Change("not-an-email");
        cut.Find("form").Submit();
        cut.Find(".validation-message").MarkupMatches("<div class=\"validation-message\">The Email field is not a valid e-mail address.</div>");
    }
}
```
bUnit renders components in-process (no browser): set parameters, fake services (`Services.AddSingleton`), JS interop with `JSInterop.Mode = JSRuntimeMode.Loose`, use `cut.WaitForAssertion` for async. Use `AddTestAuthorization()` for auth state. Use Playwright for full-stack flows.

## Gotchas
- Forgetting `FormName` or `[SupplyParameterFromForm]` yields blank models in SSR.
- `@bind-Value:after` / `ValueChanged` ordering; two-way binding with `:event="oninput"` for live updates.
- Reuse of `Model` instances across posts shares state on singletons: keep models per-component.

## Verify
bUnit assertions pass; a Playwright test with JS disabled still posts the SSR form and shows validation errors.
