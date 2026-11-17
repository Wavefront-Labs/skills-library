---
id: computing-software.web-development.django.form-rendering-widgets-and-crispy-forms
name: form-rendering-widgets-and-crispy-forms
category: computing-software
field: web-development
product: django
tags: [django-form-rendering, crispy-forms, form-widgets, form-templates, django]
level: practitioner
status: docs-checked
description: "Rendering Django forms well: field templates and as_field_group, form renderers, widget attrs, accessible errors and help text, and django-crispy-forms or django-widget-tweaks."
sources:
  - https://docs.djangoproject.com/en/stable/topics/forms/#rendering-fields-manually
  - https://docs.djangoproject.com/en/stable/ref/forms/renderers/
  - https://django-crispy-forms.readthedocs.io/
  - https://docs.djangoproject.com/en/stable/releases/5.0/
  - https://github.com/jazzband/django-widget-tweaks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Form rendering, widgets and crispy-forms

## 1. Built-in rendering (Django 5.0+)
```django
<form method="post" novalidate>{% csrf_token %}
  {{ form.non_field_errors }}
  {{ form.email.as_field_group }}     {# label, widget, errors and help text #}
  {{ form.password.as_field_group }}
  <button type="submit">Sign in</button>
</form>
```
- The default form template is `django/forms/div.html`; `as_field_group` (Django 5.0) and the `field_template_name` option let you control markup per field or form-wide.
- Since Django 5.0, form fields include `aria-describedby` (so screen readers associate them with their help text) and invalid fields include `aria-invalid="true"`; Django 5.1 added `aria-describedby` to fieldsets.

## 2. Project-wide templates
```python
# settings.py
from django.forms.renderers import TemplatesSetting
class CustomFormRenderer(TemplatesSetting):
    form_template_name = "forms/form.html"
    field_template_name = "forms/field.html"
FORM_RENDERER = "core.forms.CustomFormRenderer"
INSTALLED_APPS += ["django.forms"]   # so form templates can be overridden from your templates dirs
```

## 3. Widgets
```python
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "birth_date"]
        widgets = {
            "email": forms.EmailInput(attrs={"autocomplete": "email", "class": "input"}),
            "birth_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }
```
- `DateInput` defaults to `type="text"`; set `type="date"` and an ISO `format` so the value round-trips.
- Add `autocomplete` tokens (WCAG 1.3.5) and `inputmode` where useful.

## 4. Libraries
- **django-crispy-forms** + a template pack (`crispy-bootstrap5`, `crispy-tailwind`): `{% crispy form %}` or `{{ form|crispy }}`; `FormHelper` and `Layout` in Python for rows, fieldsets and buttons.
- **django-widget-tweaks**: `{% render_field form.email class="input" placeholder="you@example.com" %}` to add attributes in templates without Python changes.
- **Template partials** (`{% partialdef %}`, Django 6.0): reusable field fragments inside one template file.

## 5. Accessibility checks
Every field has a visible `<label for>`; errors are text next to the field and summarised at top; required fields indicated in text; help text associated via `aria-describedby`; group radios in `<fieldset><legend>`.

## Verify
- [ ] Rendered HTML has labels, error associations and autocomplete attributes; date inputs show existing values when editing; one rendering approach used consistently.

## Checked
Date: 2026-10-25. Documentation: Django documentation source (django/django main branch, 6.2 in development, commit of 2026-10-23; release notes 4.0 to 6.0) (topics/forms, ref/forms/renderers, ref/forms/widgets, release notes 5.0, 5.1 and 6.0), django-crispy-forms docs source (django-crispy-forms main), django-widget-tweaks README, W3C WCAG repository (Understanding SC 1.3.5 exists).
Confirmed: `as_field_group`, `field_template_name`, `TemplatesSetting` with `django.forms` in `INSTALLED_APPS` and `APP_DIRS=True`, `DateInput` defaults to `type="text"`, `|crispy` filter, `{% crispy %}` tag with `FormHelper`, `crispy-bootstrap5` and `crispy-tailwind` template packs, `render_field` in widget-tweaks, `aria-describedby` and `aria-invalid` (Django 5.0).
Corrected or removed: the vague "varies by version" accessibility note (replaced by the release-note facts), the removed `aria-describedby` comment on `as_field_group`, and the unsupported django-cotton bullet.
Method: documentation only; no commands were run.
