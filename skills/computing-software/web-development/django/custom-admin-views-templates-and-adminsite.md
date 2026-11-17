---
id: computing-software.web-development.django.custom-admin-views-templates-and-adminsite
name: custom-admin-views-templates-and-adminsite
category: computing-software
field: web-development
product: django
tags: [adminsite, admin-templates, custom-admin-views, django-admin, django]
level: advanced
status: docs-checked
description: "Extending the Django admin: custom AdminSite, extra views via get_urls with admin_view, overriding admin templates per app or model, dashboards and keeping permissions intact."
sources:
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#adminsite-objects
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls
  - https://docs.djangoproject.com/en/stable/ref/contrib/admin/#overriding-admin-templates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom admin views, templates and AdminSite

## 1. Custom AdminSite
```python
# core/admin.py
class OpsAdminSite(admin.AdminSite):
    site_header = "Acme Operations"; site_title = "Acme Ops"; index_title = "Dashboard"
    def get_urls(self):
        return [path("metrics/", self.admin_view(self.metrics_view), name="metrics")] + super().get_urls()
    def metrics_view(self, request):
        ctx = {**self.each_context(request), "title": "Metrics", "stats": compute_stats()}
        return TemplateResponse(request, "admin/metrics.html", ctx)

# core/apps.py - replace the default site everywhere
class CoreAdminConfig(AdminConfig): default_site = "core.admin.OpsAdminSite"
# settings: replace "django.contrib.admin" with "core.apps.CoreAdminConfig"
```
Just changing titles? Set `admin.site.site_header = ...` without subclassing.

## 2. Extra views on a ModelAdmin
```python
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def get_urls(self):
        return [path("<int:pk>/refund/", self.admin_site.admin_view(self.refund_view), name="orders_order_refund")] + super().get_urls()
    def refund_view(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if not self.has_change_permission(request, order): raise PermissionDenied
        if request.method == "POST":
            refund(order); self.message_user(request, "Refunded"); return redirect("admin:orders_order_change", pk)
        return TemplateResponse(request, "admin/orders/refund.html", {**self.admin_site.each_context(request), "order": order, "opts": self.model._meta})
```
- `admin_site.admin_view()` runs the permission check that only active staff users pass and applies `never_cache`; still check model/object permissions yourself.
- Custom URLs must come **before** `super().get_urls()` (the catch-all `<path:object_id>/` would swallow them).
- `each_context()` supplies sidebar, site header and theme variables to extended templates.

## 3. Overriding templates
Lookup order per page: `admin/<app>/<model>/change_form.html` -> `admin/<app>/change_form.html` -> `admin/change_form.html`.
```django
{# templates/admin/orders/order/change_form.html #}
{% extends "admin/change_form.html" %}
{% block object-tools-items %}
  <li><a href="{% url 'admin:orders_order_refund' original.pk %}">Refund</a></li>{{ block.super }}
{% endblock %}
```
Extend and override blocks: Django's docs say replacing an entire admin template is usually neither necessary nor advisable. Put the `admin/` directory in a template `DIRS` directory; with custom `loaders`, the filesystem loader must come before the app_directories loader.

## 4. Dashboards
Override `admin/index.html` blocks for summary widgets. Keep heavy queries cached.

## Verify
- [ ] Custom views require staff and the right permissions (test as a limited staff user); templates extend rather than copy; custom URLs resolve and appear with admin chrome.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (ref/contrib/admin: AdminSite, get_urls, overriding admin templates).
Confirmed: `default_site` on an `AdminConfig` subclass, `get_urls` with `admin_site.admin_view()`, custom URLs placed before the built-in ones, `each_context`, template override directories and the `object-tools-items` block, the template `DIRS` and loader ordering rule.
Corrected or removed: the claim that `admin_view` adds CSRF handling (the docs list the permission check and `never_cache`), the "never copy" wording, and unsupported theme package names.
Method: documentation only; no commands were run.
