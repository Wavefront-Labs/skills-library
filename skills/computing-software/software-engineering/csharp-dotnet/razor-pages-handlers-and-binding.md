---
id: computing-software.software-engineering.csharp-dotnet.razor-pages-handlers-and-binding
name: razor-pages-handlers-and-binding
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, aspnet-ui, razor-pages, pagemodel, bindproperty, tag-helpers, post-redirect-get]
level: practitioner
status: draft
description: "Write ASP.NET Core Razor Pages: PageModel handlers, BindProperty, post-redirect-get, tag helpers, partials and view components, validation, and common over-posting and XSS pitfalls."
sources: ["https://learn.microsoft.com/en-us/aspnet/core/razor-pages/", "https://learn.microsoft.com/en-us/aspnet/core/mvc/views/tag-helpers/intro", "https://learn.microsoft.com/en-us/aspnet/core/security/cross-site-scripting"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Razor Pages

```csharp
// Pages/Products/Edit.cshtml.cs
public class EditModel(AppDb db) : PageModel
{
    [BindProperty] public ProductInput Input { get; set; } = new();            // POST only unless SupportsGet = true
    [BindProperty(SupportsGet = true)] public int Id { get; set; }

    public async Task<IActionResult> OnGetAsync()
    {
        var p = await db.Products.FindAsync(Id); if (p is null) return NotFound();
        Input = new(p.Name, p.Price); return Page();
    }
    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid) return Page();                                // redisplay with errors
        var p = await db.Products.FindAsync(Id); if (p is null) return NotFound();
        p.Name = Input.Name; p.Price = Input.Price;
        await db.SaveChangesAsync();
        TempData["Msg"] = "Saved";
        return RedirectToPage("Index");                                        // Post-Redirect-Get avoids double submit
    }
    public async Task<IActionResult> OnPostDeleteAsync() { /* handler: asp-page-handler="Delete" */ return RedirectToPage("Index"); }
}
public record ProductInput([Required, StringLength(80)] string Name, [Range(0, 100000)] decimal Price);
```
```cshtml
@page "{id:int}"
@model EditModel
<form method="post"><input asp-for="Input.Name" /><span asp-validation-for="Input.Name"></span>
  <button type="submit">Save</button><button asp-page-handler="Delete">Delete</button></form>
<partial name="_Footer" /> <vc:cart-summary />
@section Scripts { <partial name="_ValidationScriptsPartial" /> }
```
## Rules
- Bind to an input model, not the EF entity (over-posting). Or use `[BindProperty]` on specific properties and `TryUpdateModelAsync(entity, "Input", e => e.Name)`.
- Antiforgery is automatic for POST in Razor Pages; keep it on.
- `@Model.Text` is HTML-encoded by default; `Html.Raw` with user data is XSS. JavaScript context: use `@Json.Serialize` / data attributes.
- Page routes: `@page "{id:int?}"`, convention folder layout maps to URLs. Layouts in `_Layout.cshtml`, global imports in `_ViewImports.cshtml`.
- Use `[ResponseCache]`/output cache carefully with personalised pages.

## Gotchas
- `OnPost` binding sets `[BindProperty]` for all of them, so a hidden field the user alters is still bound; re-check ownership/authorisation server side.
- Handler names: `OnPostDeleteAsync` pairs with `?handler=Delete`.
- Returning `Page()` after success reposts on refresh.

## Verify
WebApplicationFactory test posts invalid data (expects 200 with validation text) and valid data (expects 302 to Index).
