---
id: computing-software.web-development.django.modeladmin-list-display-filters-search
name: modeladmin-list-display-filters-search
category: computing-software
field: web-development
product: django
tags: [django-admin, modeladmin, list-display, list-filter, search-fields, admin-customization, readonly-fields, fieldsets, simplelistfilter, admin-search]
level: practitioner
status: verified
description: "Configuring Django ModelAdmin: list_display with computed columns, list_filter and custom SimpleListFilter, search_fields, fieldsets, readonly and autocomplete fields."
sources:
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/filters/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ModelAdmin: list_display, filters and search

**Goal:** an admin changelist staff can actually use: useful columns, filters, search and an edit form organised for the job.

## 1. Changelist
```python
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number", "customer", "status", "total_display", "created_at")
    list_display_links = ("number",)
    list_filter = ("status", ("created_at", admin.DateFieldListFilter), "customer__country")
    search_fields = ("number", "customer__email", "=customer__id")   # '=' exact, '^' startswith
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_per_page = 50
    list_select_related = ("customer",)            # avoid N+1 for FK columns

    @admin.display(description="Total", ordering="total")
    def total_display(self, obj):
        return f"{obj.total:.2f} {obj.currency}"
```
- Computed columns via `@admin.display` (set `ordering` to make them sortable, `boolean=True` for icons).
- `search_fields` across relations do `icontains` joins - can be slow and produce duplicates on to-many relations (Django adds `distinct` when needed). Use `^`/`=` prefixes for indexed lookups.

## 2. Custom filter
```python
class HighValueFilter(admin.SimpleListFilter):
    title, parameter_name = "value", "value"
    def lookups(self, request, model_admin): return [("high", "Over 1000")]
    def queryset(self, request, qs): return qs.filter(total__gt=1000) if self.value() == "high" else qs
```

## 3. Edit form
```python
    fieldsets = (
        (None, {"fields": ("number", "customer", "status")}),
        ("Amounts", {"fields": ("total", "currency"), "classes": ("collapse",)}),
    )
    readonly_fields = ("number", "created_at")
    autocomplete_fields = ("customer",)     # requires search_fields on CustomerAdmin
    raw_id_fields = ("assigned_to",)        # alternative for huge FK tables
```
`autocomplete_fields`/`raw_id_fields` avoid rendering a `<select>` with 1M options (the classic admin page that never loads).

## 4. Per-request behaviour
`get_queryset`, `get_readonly_fields(request, obj)`, `get_list_display(request)` let you vary by user/permissions.

## Verify
- [ ] Changelist query count stays constant as page size grows (django-debug-toolbar).
- [ ] Search and filters return expected rows; FK widgets load instantly.
- [ ] Non-superusers see only what their permissions allow.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: the OrderAdmin from the skill (list_display with a computed `@admin.display(ordering=...)` column, `list_display_links`, `list_filter` with a tuple filter and a related-field filter, `search_fields` with `=customer__id`, `date_hierarchy`, `list_select_related`, `autocomplete_fields`, fieldsets with a collapsed section): changelist and `?q=1&status=paid` returned 200; the changelist ran 9 queries for 5 rows and for 50 rows (constant); all admin system checks passed.
- Run: `autocomplete_fields` needs `search_fields` on the related admin (check `admin.E040`).
