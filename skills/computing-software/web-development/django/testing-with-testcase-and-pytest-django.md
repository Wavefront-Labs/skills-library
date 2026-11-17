---
id: computing-software.web-development.django.testing-with-testcase-and-pytest-django
name: testing-with-testcase-and-pytest-django
category: computing-software
field: web-development
product: django
tags: [django, pytest-django, django-testcase, test-client, factory-boy, assertnumqueries, python, web-development]
level: practitioner
status: verified
description: "Testing Django apps with TestCase or pytest-django: transaction isolation, Client and RequestFactory, factory_boy, assertNumQueries, settings overrides and speed."
sources:
  - https://docs.djangoproject.com/en/stable/topics/testing/overview/
  - https://docs.djangoproject.com/en/stable/topics/testing/tools/
  - https://pytest-django.readthedocs.io/
  - https://factoryboy.readthedocs.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TestCase, Client and pytest-django

**Goal:** fast, isolated tests that cover views, forms, models and query counts.

## 1. Test classes
| Class | Isolation | Use |
|---|---|---|
| `SimpleTestCase` | no DB access allowed | pure logic |
| `TestCase` | each test in a transaction, rolled back | default |
| `TransactionTestCase` | truncates tables | testing `on_commit`, transaction behaviour, threads |
| `LiveServerTestCase` | real server | Selenium/Playwright |
`TestCase.setUpTestData` creates data once per class (fast); `captureOnCommitCallbacks(execute=True)` runs `on_commit` hooks inside `TestCase`.

## 2. View tests with Client
```python
class OrderViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.other = OrderFactory()
    def test_cannot_view_others_order(self):
        self.client.force_login(self.user)
        r = self.client.get(reverse("orders:detail", args=[self.other.pk]))
        self.assertEqual(r.status_code, 404)
    def test_list_query_count(self):
        OrderFactory.create_batch(10, customer=self.user)
        self.client.force_login(self.user)
        with self.assertNumQueries(4):
            self.client.get(reverse("orders:list"))
```
`RequestFactory` builds requests for calling views directly without middleware.

## 3. pytest-django
```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.test
addopts = --reuse-db -p no:cacheprovider
```
```python
import pytest
@pytest.mark.django_db
def test_create(client, django_user_model):
    user = django_user_model.objects.create_user("a", password="x")
    client.force_login(user)
    assert client.post("/orders/", {"sku": "A1"}).status_code == 302
def test_queries(django_assert_num_queries, client): ...
```
Fixtures: `client`, `admin_client`, `rf`, `settings` (auto-restored), `mailoutbox`, `django_capture_on_commit_callbacks`.

## 4. Factories
```python
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta: model = Order
    customer = factory.SubFactory(UserFactory)
    total = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
```
Use `build()` when you don't need the DB.

## 5. Speed
- `PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]` in test settings.
- `--reuse-db`, `pytest -n auto` (pytest-xdist), `--parallel` for `manage.py test`.
- Locmem email and cache backends in test settings (the test runner already swaps in the locmem email backend, `mail.outbox`; Django 6.1 adds a `MAILERS` setting that will replace `EMAIL_BACKEND`).
- Use the same database engine as production (PostgreSQL in a container), not SQLite.

## 6. Overrides
`@override_settings(FEATURE_X=True)`; `self.settings(...)` as a context manager; mock external HTTP with `responses`/`respx`.

## Verify
- [ ] CI runs tests against PostgreSQL with `makemigrations --check`.
- [ ] Key list views have `assertNumQueries` guards.
- [ ] Authorisation tests exist for every object-level view.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets. pytest-django 4.14.0, pytest-xdist, factory_boy 3.3.3, Faker 40, responses and respx (names confirmed on PyPI).
- Run (pytest, `--reuse-db -p no:cacheprovider` in pytest.ini): `TestCase` with `setUpTestData`, `captureOnCommitCallbacks(execute=True)` (1 callback, 1 mail in `mail.outbox`), `assertNumQueries(0)` around `Factory.build()`, `assertNumQueries(1)`; `SimpleTestCase` DB access -> `DatabaseOperationForbidden`; no `django_db` mark -> "Database access not allowed, use the "django_db" mark..."; fixtures `client`, `django_user_model`, `admin_client`, `rf`, `settings`, `mailoutbox`, `django_capture_on_commit_callbacks`, `django_assert_num_queries` all worked.
- Run: `factory.django.DjangoModelFactory` with `SubFactory` and `factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)` produced a positive `Decimal`; `PASSWORD_HASHERS = [MD5PasswordHasher]` -> hashes start `md5$`.
- Run: `pytest -n 2` (xdist) passed 8 tests; `manage.py test --parallel 2` ran with three test DB clones.
- Fetched: topics/testing/tools.txt (`TestCase.captureOnCommitCallbacks`, `TransactionTestCase`), 6.1 release notes (`MAILERS`).
