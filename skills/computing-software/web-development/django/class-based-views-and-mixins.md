---
id: computing-software.web-development.django.class-based-views-and-mixins
name: class-based-views-and-mixins
category: computing-software
field: web-development
product: django
tags: [django, class-based-views, generic-views, mixins, listview, loginrequiredmixin, python, web-development]
level: practitioner
status: verified
description: "Using Django generic class-based views well: ListView/DetailView/CreateView hooks, get_queryset scoping, mixin order, permissions and when a function view is clearer."
sources:
  - https://docs.djangoproject.com/en/stable/topics/class-based-views/
  - https://docs.djangoproject.com/en/stable/ref/class-based-views/
  - https://ccbv.co.uk/
  - https://docs.djangoproject.com/en/stable/topics/auth/default/#the-loginrequiredmixin-mixin
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic class-based views and mixins

**Goal:** CRUD screens in a few lines, with object scoping and permissions in the right hooks.

## 1. The core generics
```python
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 25
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).select_related("product").order_by("-pk")   # paginate_by on an unordered queryset warns (UnorderedObjectListWarning)

class OrderDetailView(LoginRequiredMixin, DetailView):
    def get_queryset(self):                       # scoping here = no IDOR
        return Order.objects.filter(customer=self.request.user)

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ["product", "quantity"]
    success_url = reverse_lazy("orders:list")
    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)
```
Templates default to `app/order_list.html`, `app/order_detail.html`, `app/order_form.html`; context names `object_list`/`order_list`, `object`/`order`, `form`.

## 2. Which hook to override
| Need | Override |
|---|---|
| filter / scope objects | `get_queryset` |
| extra template data | `get_context_data` (call super) |
| set fields before save | `form_valid` |
| dynamic redirect | `get_success_url` |
| form kwargs (pass user) | `get_form_kwargs` |
| per-request setup | `setup` or `dispatch` |
Browse ccbv.co.uk to see every attribute/method per class.

## 3. Mixin order
Access mixins go **leftmost** so they run first in `dispatch`: `class V(LoginRequiredMixin, PermissionRequiredMixin, UpdateView)`. Python MRO resolves left to right.
```python
class StaffOnly(UserPassesTestMixin):
    def test_func(self): return self.request.user.is_staff
```
`PermissionRequiredMixin` with `permission_required = "shop.change_order"`: a logged-in user without the permission already gets 403; `raise_exception = True` makes anonymous users get 403 too instead of a redirect to the login page.

## 4. URL wiring
`path("orders/<int:pk>/", OrderDetailView.as_view(), name="detail")`. Class attributes can be overridden in `as_view(paginate_by=10)`.

## 5. Writing your own mixin
Keep it small and call `super()`:
```python
class OwnerQuerysetMixin:
    owner_field = "owner"
    def get_queryset(self):
        return super().get_queryset().filter(**{self.owner_field: self.request.user})
```

## 6. When to use a function view
Multiple forms on one page, unusual flows, or when you'd override five hooks - a function view is often clearer. CBVs shine for standard CRUD.

## Verify
- [ ] Requesting another user's object pk returns 404.
- [ ] Anonymous access redirects to login; authenticated without permission gets 403.
- [ ] List views have `paginate_by` and `select_related` to avoid N+1.

## Checked
Django 6.1.2 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: LoginRequiredMixin + ListView/DetailView/CreateView with `get_queryset` scoping: anonymous -> 302 to /accounts/login/?next=; another user's pk -> 404; own pk -> 200; `as_view(paginate_by=10)` gave a paginator of 10.
- Run: PermissionRequiredMixin for a logged-in user without the permission -> 403 without `raise_exception`; anonymous -> 302 by default and 403 with `raise_exception = True`.
- Run: default template names `shop/order_list.html`, `shop/order_detail.html`, `shop/order_form.html` and context names `order_list` / `order`.
- Found: pagination over an unordered queryset logs UnorderedObjectListWarning (now ordered in the snippet).
