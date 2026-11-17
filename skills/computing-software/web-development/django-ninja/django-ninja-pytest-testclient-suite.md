---
id: computing-software.web-development.django-ninja.django-ninja-pytest-testclient-suite
name: django-ninja-pytest-testclient-suite
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, pytest, pytest-django, testclient, fixtures, parametrize, testing]
level: practitioner
status: docs-checked
description: "Set up pytest-django and fixtures for Django Ninja, then test JSON, queries, tokens, permissions and uploads with ninja.testing.TestClient."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/tutorial/part-7.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: a fast pytest suite that exercises Django Ninja operations without a running server.

## Setup

```console
$ pip install pytest pytest-django
```

```ini
# pytest.ini (next to manage.py)
[pytest]
DJANGO_SETTINGS_MODULE = taskflow.settings
testpaths = tests
```

pytest-django creates a test database per run, applies migrations, and rolls back each test. With SQLite the test database is in memory. A top-level `tests/` folder needs no `__init__.py`; the folder with `manage.py` is on the import path.

## Fixtures (tests/conftest.py)

```python
@pytest.fixture(autouse=True)
def test_settings(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path  # uploads go to a temporary folder
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

@pytest.fixture
def alice(db):
    return User.objects.create_user("alice", password="wonderland-42")

@pytest.fixture
def project(alice, bob):
    project = Project.objects.create(name="Website redesign", description="New marketing site")
    project.memberships.create(user=alice, role=Role.OWNER)
    project.memberships.create(user=bob, role=Role.MEMBER)
    return project

@pytest.fixture
def client_for():
    def make_client(user):
        token = create_token_pair(user.id)["access"]
        return TestClient(api, headers={"Authorization": f"Bearer {token}"})
    return make_client
```

- The fast MD5 hasher avoids Django's deliberately slow default; it is unsafe for real passwords. The tutorial measured 51 s without it and 0.5 s with it.
- Create tokens directly instead of calling the login endpoint, so other tests do not depend on it.
- `tmp_path` as `MEDIA_ROOT` keeps uploads out of your real media folder.

## What TestClient does

`TestClient(api)` finds the operation in the `NinjaAPI` and calls it with a fake request; it skips `urls.py` and middleware. Paths are relative to the API (`/projects/`, not `/api/projects/`). Auth, validation, your view, the response schema and error handlers still run. A path matching no operation raises an exception rather than returning `404`.

## Call patterns

```python
client.post("/auth/token", json={"username": "alice", "password": "nope"})
client.get("/projects/", headers={"Authorization": f"Bearer {token}"})   # adds to / overrides defaults
client.get(f"/projects/{project.id}/tasks/?status=todo&status=in_progress")
client.get(url, query_params={"status": ["todo", "in_progress"]})        # dict alternative
client.post(url, data={"name": "Meeting notes"}, FILES={"file": SimpleUploadedFile("notes.txt", b"hi")})
```

- `json=` sends a JSON body, `data=` form fields, `FILES=` files (`django.core.files.uploadedfile.SimpleUploadedFile`).
- The fake request answers `build_absolute_uri()` with host `testlocation`, so absolute URLs look like `http://testlocation/media/...`.
- Create an expired token by passing a negative lifetime to the token helper rather than waiting.

## Patterns worth copying

- Assert both sides of permission rules: non-member gets `404`, member without the role gets `403`; also check the database (`refresh_from_db()`).
- Compare the whole `detail` list for a validation error so a change in type, location or message breaks the test.
- Use `@pytest.mark.parametrize` for tables of cases (status transitions, filter query strings with expected titles, checking order and `count`). Set the starting state through the ORM, not through earlier API calls.
- Check stored files via `settings.MEDIA_ROOT / attachment.file.name`.

## Running

`pytest` from the folder with `manage.py`; `-k name` selects tests, `-v` lists them. pytest-django runs tests that do not use the database last, so a file can appear twice in the progress output.

To test the full stack (middleware, the `/api` prefix), use Django's own `django.test.Client` with real URLs.

## Checked

2026-11-08: Read django-ninja docs/docs/tutorial/part-7.md from GitHub. Confirmed against the whole page: pytest and pytest-django setup, pytest.ini, conftest fixtures, the MD5 hasher timing (51 s versus 0.5 s), TestClient behaviour and relative paths, call patterns, the testlocation host, permission and parametrize patterns, and the run notes. Nothing removed.

Method: documentation only; no commands were run.
