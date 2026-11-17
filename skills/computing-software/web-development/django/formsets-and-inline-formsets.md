---
id: computing-software.web-development.django.formsets-and-inline-formsets
name: formsets-and-inline-formsets
category: computing-software
field: web-development
product: django
tags: [django, formsets, inline-formsets, modelformset, management-form, dynamic-forms, python, web-development]
level: practitioner
status: verified
description: "Editing multiple objects with Django formsets and inlineformset_factory: management form, extra/can_delete, validation across forms, and adding rows dynamically."
sources:
  - https://docs.djangoproject.com/en/stable/topics/forms/formsets/
  - https://docs.djangoproject.com/en/stable/topics/forms/modelforms/#inline-formsets
  - https://docs.djangoproject.com/en/stable/topics/forms/modelforms/#model-formsets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Formsets and inline formsets

**Goal:** edit a parent and its child rows (order + line items) on one page, safely.

## 1. Inline formset
```python
from django.forms import inlineformset_factory
LineFormSet = inlineformset_factory(
    Order, OrderLine, fields=["product", "quantity"],
    extra=1, can_delete=True, min_num=1, validate_min=True, max_num=50, validate_max=True,
)

def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    form = OrderForm(request.POST or None, instance=order)
    formset = LineFormSet(request.POST or None, instance=order)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        with transaction.atomic():
            form.save(); formset.save()
        return redirect(order)
    return render(request, "orders/edit.html", {"form": form, "formset": formset})
```
`instance=order` scopes the queryset to that parent's children - a line id from another order is silently ignored (the formset validates, nothing is created, the other order's line is unchanged).

## 2. Template
```django
<form method="post">{% csrf_token %}
  {{ form }}
  {{ formset.management_form }}
  {{ formset.non_form_errors }}
  {% for f in formset %}
    <div class="line">{{ f.id }}{{ f.product }}{{ f.quantity }}{% if formset.can_delete %}{{ f.DELETE }}{% endif %}{{ f.errors }}</div>
  {% endfor %}
  <button>Save</button>
</form>
```
Forgetting `management_form` fails validation: a plain formset reports "ManagementForm data is missing or has been tampered with..." as a non-form error, while the inline formset above (with `validate_min`) showed "Please submit at least 1 form." plus "This field is required." on the hidden `TOTAL_FORMS`/`INITIAL_FORMS` fields. Forgetting `{{ f.id }}` on an existing row fails with "id: This field is required." (no duplicate is created).

## 3. Cross-form validation
```python
class BaseLineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        products = [f.cleaned_data["product"] for f in self.forms
                    if f.cleaned_data and not f.cleaned_data.get("DELETE")]
        if len(products) != len(set(products)):
            raise forms.ValidationError("Each product can appear only once.")
LineFormSet = inlineformset_factory(Order, OrderLine, formset=BaseLineFormSet, fields=[...])
```

## 4. Adding rows dynamically
Render `formset.empty_form` (with `__prefix__` placeholders) into a `<template>`; on "Add", clone it, replace `__prefix__` with `TOTAL_FORMS`, then increment `id_<prefix>-TOTAL_FORMS`. Or use htmx to fetch a new row from the server.

## 5. Model formsets and plain formsets
`modelformset_factory(Model, fields=..., queryset=...)` for editing a set of objects not tied to one parent - always pass a scoped `queryset`. `formset_factory(Form)` for non-model repeating data.

## 6. Performance
Each form's ModelChoiceField runs its own query (GET of the edit page: 8 queries for 5 lines, 23 for 20). Pass a shared queryset or cache choices; `max_num` bounds the work (and `absolute_max`, default `max_num + 1000`, i.e. 2000 with the default `max_num=1000`, blocks abuse).

## Verify
- [ ] Editing, adding and deleting lines persist correctly in one submit.
- [ ] Submitting a line id from another order is ignored/rejected.
- [ ] Debug toolbar query count stays bounded with 20 rows.

## Checked
Django 6.1.2, DRF 3.18.3, drf-spectacular 0.30.0 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: the inline formset view with `validate_min` / `validate_max`: update saved, new row saved, `validate_max` with 51 forms -> "Please submit at most 50 forms.", `validate_min` with no forms -> "Please submit at least 1 form.".
- Run: a line id from another order -> formset valid, saved nothing for the foreign line and left it unchanged; missing id with INITIAL_FORMS=1 -> "This field is required." on `id`.
- Run: `formset_factory(Form).absolute_max` is 2000 and `max_num` 1000 (the skill said absolute_max defaults to 1000); a plain formset with no management data gives the "ManagementForm data is missing or has been tampered with" message (formsets.py).
- Run: GET edit page query counts 8 (5 lines) and 23 (20 lines), i.e. one extra query per row.
