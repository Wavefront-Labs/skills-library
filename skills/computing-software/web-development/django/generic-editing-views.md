---
id: computing-software.web-development.django.generic-editing-views
name: generic-editing-views
category: computing-software
field: web-development
product: django
tags: [createview, generic-editing-views, updateview, deleteview, formview, django]
level: practitioner
status: verified
description: "Django CreateView, UpdateView, DeleteView and FormView: fields vs form_class, setting the owner in form_valid, restricting querysets against IDOR, success URLs and messages."
sources:
  - https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-editing/
  - https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-editing/
  - https://ccbv.co.uk/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic editing views

## 1. Create and update with ownership
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class ProjectCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Project
    fields = ["name", "description"]                # explicit list; never "__all__" on user-facing forms
    success_message = "Project %(name)s created"
    def form_valid(self, form):
        form.instance.owner = self.request.user     # set server-side fields here
        return super().form_valid(form)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    def get_queryset(self):                         # IDOR guard: only the user's own objects
        return Project.objects.filter(owner=self.request.user)

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("project-list")
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
```
- Mixins go **left** of the view class (MRO): `LoginRequiredMixin` must run first.
- Success URL: `success_url = reverse_lazy(...)` (lazy because URLconf is not loaded at import) or define `get_absolute_url()` on the model.
- Templates: `<app>/<model>_form.html` (create/update) and `<model>_confirm_delete.html`; override with `template_name`.

## 2. Passing extra data to forms
```python
def get_form_kwargs(self):
    kwargs = super().get_form_kwargs(); kwargs["user"] = self.request.user; return kwargs
```
The form pops `user` in `__init__` to limit choice querysets (e.g. only the user's teams).

## 3. DeleteView changes
Since Django 4.0, DeleteView uses `FormMixin`: put custom logic in `form_valid()` (the old `delete()` override is no longer called on POST).

## 4. FormView
For forms not tied to a model instance (contact, search): `form_class`, `template_name`, `success_url`, and `form_valid` to send email/enqueue jobs.

## Gotchas
- `fields` and `form_class` together raise ImproperlyConfigured.
- Object-level permissions need `get_queryset` filtering or `UserPassesTestMixin`; `PermissionRequiredMixin` checks model-level perms only.

## Verify
- [ ] Another user's object id in the update/delete URL returns 404; created objects have the right owner regardless of POSTed data.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: CreateView with `SuccessMessageMixin` (`Project %(name)s created` produced "Project P1 created"), `form_valid` setting the owner server-side (a POSTed `owner` was ignored; owner was the logged-in user), UpdateView/DeleteView `get_queryset` scoping (another user's pk -> 404), `get_form_kwargs` passing the user to a form that pops it, `success_url = reverse_lazy(...)` redirect after delete.
- Run: `fields` together with `form_class` -> `ImproperlyConfigured: Specifying both 'fields' and 'form_class' is not permitted.`
- Run: a DeleteView subclass overriding both `delete()` and `form_valid()` handled a POST through `form_valid` only (`delete()` not called).
