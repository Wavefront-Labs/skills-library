---
id: computing-software.web-development.django.modelform-validation-and-clean-methods
name: modelform-validation-and-clean-methods
category: computing-software
field: web-development
product: django
tags: [django, modelform, form-clean, form-validation, validationerror, django-forms, python, web-development, form-clean-methods]
level: practitioner
status: verified
description: "Validating Django ModelForms correctly: field clean_<name>, cross-field clean(), model validation and constraints, error placement, commit=False and excluded fields."
sources:
  - https://docs.djangoproject.com/en/stable/ref/forms/validation/
  - https://docs.djangoproject.com/en/stable/topics/forms/modelforms/
  - https://docs.djangoproject.com/en/stable/ref/models/instances/#validating-objects
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# ModelForm validation and clean methods

**Goal:** validation in the right layer, clear field-level errors, and no mass-assignment holes.

## 1. Declare fields explicitly
```python
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "starts_on", "ends_on", "budget"]     # never "__all__" on user-facing forms
        widgets = {"starts_on": forms.DateInput(attrs={"type": "date"})}
```
`fields = "__all__"` or `exclude` silently exposes new model fields (like `is_approved`) to the form.

## 2. Validation order
`form.is_valid()` runs, per field: `to_python()` -> `validate()` -> validators -> `clean_<field>()`; then `form.clean()`; then for ModelForms `_post_clean()` which builds the instance and calls `model.full_clean()` (model field validators, `Model.clean()`, unique and constraint checks) for fields in the form.

## 3. Field-level clean
```python
    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if Project.objects.filter(owner=self.owner, name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("You already have a project with this name.", code="duplicate")
        return name                           # must return the value
```

## 4. Cross-field clean
```python
    def clean(self):
        cleaned = super().clean()
        s, e = cleaned.get("starts_on"), cleaned.get("ends_on")   # .get: may be missing if field failed
        if s and e and e < s:
            self.add_error("ends_on", "End date must be after the start date.")
        return cleaned
```
`add_error(field, msg)` attaches to a field; raising `ValidationError` in `clean()` gives a non-field error (`form.non_field_errors`).

## 5. Passing context and setting hidden fields
```python
    def __init__(self, *args, owner, **kwargs):
        super().__init__(*args, **kwargs); self.owner = owner
# view
form = ProjectForm(request.POST or None, owner=request.user)
if form.is_valid():
    project = form.save(commit=False)
    project.owner = request.user            # not a form field: can't be tampered with
    project.save(); form.save_m2m()         # m2m needs save_m2m after commit=False
```

## 6. Model-level rules
Put invariants that apply everywhere (admin, API, shell) in `Model.clean()` and DB constraints; form `clean` for UI-specific rules. Note `model.save()` does not call `full_clean()` - only forms/admin do.

## 7. Rendering errors accessibly
Django 5.0+ field rendering adds `aria-describedby` for help text and errors, plus `aria-invalid` on invalid fields (`{{ field.as_field_group }}`; rendered output checked). Keep `{{ form.non_field_errors }}` at the top.

## Verify
- [ ] Tests post invalid data and assert `form.errors` keys and codes.
- [ ] Adding an extra POST field (e.g. `owner=2`) has no effect.
- [ ] Unique/constraint violations show as form errors, not 500s.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: the ProjectForm: `clean_name` duplicate check for the same owner (excluding the instance) returned the form error with code `duplicate`; `clean()` cross-field `add_error("ends_on", ...)` attached to the field; `fields` limited to four names so a POSTed `owner` and `is_approved` were ignored (project saved with the request user and `is_approved=False`); `form.save(commit=False)` plus `save_m2m()` worked.
- Run: `as_field_group()` output contains `aria-describedby="id_a_helptext id_a_error"` and `aria-invalid="true"` for an invalid field with help text.
- Fetched: 5.0 and 5.1 release notes (`aria-describedby`).
- Run: call order traced with a field validator, `clean_name`, `form.clean` and a `_post_clean` override: validator, `clean_name`, `form.clean`, `_post_clean`; `Model.save()` does not call `full_clean()` (a 100-character value for a 30-character field was accepted by SQLite).
