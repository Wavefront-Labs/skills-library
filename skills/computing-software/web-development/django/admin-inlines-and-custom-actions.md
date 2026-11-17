---
id: computing-software.web-development.django.admin-inlines-and-custom-actions
name: admin-inlines-and-custom-actions
category: computing-software
field: web-development
product: django
tags: [django-admin, admin-inlines, admin-actions, tabularinline, stackedinline, bulk-actions, admin-messages]
level: practitioner
status: verified
description: "Editing related objects with TabularInline/StackedInline and adding admin bulk actions with confirmation pages, permissions and user messages."
sources:
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#inlinemodeladmin-objects
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/actions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admin inlines and custom actions

**Goal:** staff edit parent and child records on one page, and run bulk operations safely.

## 1. Inlines
```python
class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0                          # no blank rows by default
    fields = ("product", "quantity", "unit_price")
    readonly_fields = ("unit_price",)
    autocomplete_fields = ("product",)
    show_change_link = True            # link only renders if the inline model has its own registered ModelAdmin
    max_num = 200

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]
```
- `TabularInline` = compact rows; `StackedInline` = full forms.
- Many inline rows x FK `<select>` widgets = huge pages; use `autocomplete_fields`/`raw_id_fields` and `get_queryset` with `select_related`.
- Generic relations: `GenericTabularInline` from `django.contrib.contenttypes.admin`.
- Validation across inline rows: custom `BaseInlineFormSet.clean()`.

## 2. Actions
```python
@admin.action(description="Mark selected orders as shipped", permissions=["change"])
def mark_shipped(modeladmin, request, queryset):
    updated = queryset.filter(status="paid").update(status="shipped")
    modeladmin.message_user(request, f"{updated} orders marked shipped.", messages.SUCCESS)

class OrderAdmin(admin.ModelAdmin):
    actions = [mark_shipped]
```
- `queryset.update()` skips `save()` and signals and writes no admin `LogEntry` (0 change entries after running the action below) - if business logic lives in `save()`/signals, loop and call it (or call a service function).
- `permissions=["change"]` hides the action from users lacking `change_order`; custom permission `["publish"]` requires a `has_publish_permission(self, request)` method on the ModelAdmin: without it the changelist raises `AttributeError: ... has no attribute 'has_publish_permission'`.
- Disable the dangerous built-in bulk delete when deletes need business logic: `admin.site.disable_action("delete_selected")` or override `get_actions`.

## 3. Confirmation step
Return a `TemplateResponse` from the action rendering a confirm page that re-posts `action` and `_selected_action` ids with a `post` flag; perform the work only when `request.POST.get("post")`. Large operations: enqueue a background job and message "Started".

## Verify
- [ ] Order page with 100 lines loads quickly (query count, page size).
- [ ] Action hidden for users without the permission; message shows the affected count.
- [ ] Side effects (emails, audit log) still happen for bulk actions.

## Checked
Django 6.1.2 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: TabularInline with extra=0, autocomplete_fields, readonly_fields and max_num rendered on the Order change page; the `mark_shipped` action updated 2 rows and showed "2 orders marked shipped."; a view-only staff user did not see the action (permissions=["change"]); the changelist makes 9 queries for 5 rows and for 50 rows.
- Run: with no `has_publish_permission` the changelist raised AttributeError; once defined only superusers saw the action.
- Run: `LogEntry` change count stayed 0 after the `update()` action; `show_change_link` produced no link because the inline model was not registered.
- Imported: `GenericTabularInline` from `django.contrib.contenttypes.admin`, `admin.site.disable_action` exists and `delete_selected` is registered by default.
