---
id: computing-software.web-development.django.testing-drf-apis
name: testing-drf-apis
category: computing-software
field: web-development
product: django
tags: [apitestcase, apiclient, drf-testing, force-authenticate, pytest-django, django]
level: practitioner
status: verified
description: "Testing Django REST framework APIs: APIClient/APITestCase, force_authenticate vs real tokens, JSON format defaults, permission matrices, query-count assertions and schema checks."
sources:
  - https://www.django-rest-framework.org/api-guide/testing/
  - https://pytest-django.readthedocs.io/
  - https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing DRF APIs

## 1. Basics
```python
from rest_framework.test import APITestCase
from django.urls import reverse

class ProjectAPITests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", password="x")
        self.bob = User.objects.create_user("bob", password="x")
        self.project = Project.objects.create(owner=self.alice, name="A")

    def test_owner_can_update(self):
        self.client.force_authenticate(user=self.alice)
        r = self.client.patch(reverse("project-detail", args=[self.project.pk]), {"name": "B"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["name"], "B")

    def test_other_user_gets_404(self):
        self.client.force_authenticate(user=self.bob)
        r = self.client.get(reverse("project-detail", args=[self.project.pk]))
        self.assertEqual(r.status_code, 404)

    def test_anonymous_rejected(self):
        r = self.client.get(reverse("project-list"))
        self.assertIn(r.status_code, (401, 403))
```
- Router names: `<basename>-list`, `<basename>-detail`.
- `REST_FRAMEWORK = {"TEST_REQUEST_DEFAULT_FORMAT": "json"}` avoids passing `format` everywhere (set it in the settings module; `override_settings` at test time is too late because the factory reads it at import).
- `r.data` is the pre-render Python data; `r.json()` parses the rendered body (tests the renderer too).

## 2. Authentication in tests
- `force_authenticate` skips authentication classes: fast, good for permission/logic tests.
- Also test the real path once per auth class: `self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")`, or `self.client.login(...)` for session auth (CSRF is not enforced by APIClient unless `enforce_csrf_checks=True`).

## 3. pytest style
```python
@pytest.fixture
def api(db): return APIClient()
def test_list_paginated(api, user_factory, project_factory):   # factory fixtures from pytest-factoryboy: register(UserFactory) -> user_factory
    u = user_factory(); project_factory.create_batch(30, owner=u)
    api.force_authenticate(u)
    r = api.get("/api/projects/?page=2")
    assert r.status_code == 200 and len(r.data["results"]) == 10
```

## 4. Performance and contract
- `with self.assertNumQueries(3): self.client.get(url)` catches N+1 regressions in serializers.
- Schema: generate with drf-spectacular in CI (`./manage.py spectacular --validate --fail-on-warn`) and diff against the committed schema.
- Drive a role x endpoint permission matrix from data rather than hand-writing each case.

## Verify
- [ ] Each endpoint has tests for anonymous, owner, other user and admin; query counts asserted on list endpoints.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets. pytest-django 4.14.0, pytest-factoryboy installed.
- Run: the `APITestCase` from the skill against a router viewset: owner PATCH 200 with `r.data` a `ReturnDict` and `r.json()` the parsed body, other user's GET 404, anonymous GET 403 (default `SessionAuthentication` has no `WWW-Authenticate`, so 403 not 401), `reverse("project-detail", args=[pk])` router names, `assertNumQueries` works on the client call.
- Run: with `TEST_REQUEST_DEFAULT_FORMAT = "json"` in the settings module, `patch(url, {"name": "B"})` without `format=` worked; `APIClient(enforce_csrf_checks=True)` with a session login got 403 on POST, the default client 201.
- Run: pytest style `api.force_authenticate(u)` paginated list (`PageNumberPagination`, page 2 of 30 rows -> 10 results).
