---
id: computing-software.web-development.django.admin-forms-fieldsets-and-autocomplete
name: admin-forms-fieldsets-and-autocomplete
category: computing-software
field: web-development
product: django
tags: [autocomplete-fields, admin-fieldsets, readonly-fields, admin-forms, django-admin]
level: practitioner
status: verified
description: "Shaping Django admin edit forms: fieldsets, readonly_fields and computed displays, autocomplete_fields and raw_id_fields for big relations, custom ModelForms and per-user forms."
sources:
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-options
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_form
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admin forms, fieldsets, readonly and autocomplete_fields

## 1. Layout
```python
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["customer", ("status", "priority")]}),           # tuple = same row
        ("Shipping", {"fields": ["address", "shipped_at"], "classes": ["collapse"], "description": "Filled by the warehouse."}),
        ("Audit", {"fields": ["created_at", "updated_by", "total_display"]}),
    ]
    readonly_fields = ["created_at", "updated_by", "total_display"]
    @admin.display(description="Total")
    def total_display(self, obj): return f"${obj.total:,.2f}" if obj.pk else "-"
```
- `readonly_fields` can include methods/properties for computed values; they must also be listed in `fields`/`fieldsets` to show.
- `classes: ["collapse"]` renders as a `<details>`/`<summary>` expander from Django 5.1, and only when the fieldset has a name; the unnamed `(None, ...)` fieldset is never collapsed (5.1 release notes; the admin change page was rendered and contains `<details`).

## 2. Large relations
```python
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer", "products"]    # Select2-style search widget via AJAX
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ["name", "email"]                 # required on the related admin (else system check admin.E040)
```
- Default selects render every related row: a 100k-customer table makes the page time out. Use `autocomplete_fields` or `raw_id_fields` (plain id input + lookup popup).
- Autocomplete respects the related admin's `get_search_results` and permission checks; override to filter (e.g. only active customers).

## 3. Custom form and validation
```python
class OrderAdminForm(forms.ModelForm):
    class Meta: model = Order; fields = "__all__"
    def clean(self):
        c = super().clean()
        if c.get("status") == "shipped" and not c.get("shipped_at"):
            self.add_error("shipped_at", "Required when status is shipped.")
        return c
class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user; super().save_model(request, obj, form, change)
```

## 4. Per-user or per-object behaviour
```python
def get_readonly_fields(self, request, obj=None):
    ro = list(super().get_readonly_fields(request, obj))
    if obj and obj.status == "paid": ro += ["total", "customer"]
    if not request.user.is_superuser: ro += ["priority"]
    return ro
def get_form(self, request, obj=None, **kwargs):
    form = super().get_form(request, obj, **kwargs)
    form.base_fields["customer"].queryset = Customer.objects.filter(active=True)
    return form
```
Also `get_fieldsets`, `get_exclude`, `formfield_for_foreignkey` (filter choices per request).

## Verify
- [ ] Change pages load fast with large related tables; locked fields read-only for the right states and users; validation errors show on the correct fields.

## Checked
Django 6.1.2 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: the Order admin (fieldsets with a tuple row, collapse class, readonly total_display, autocomplete_fields, custom ModelForm with add_error, get_form narrowing the customer queryset, get_readonly_fields): change page returned 200, rendered `<details>`, `form-multiline` row, the computed `$1,234.50`, the inactive customer absent from the select, and the invalid POST showed "Required when status is shipped.".
- Run: `autocomplete_fields` pointing at an admin with no `search_fields` fails system check `admin.E040`.
- Fetched: Django 5.1 release notes (collapse and `<details>`); `autocomplete.py` source (uses `get_search_results` and `has_view_permission`).
- Run: `raw_id_fields` swaps the widget to `ForeignKeyRawIdWidget`.
