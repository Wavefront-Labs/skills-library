---
id: computing-software.web-development.django.signals-and-when-not-to-use-them
name: signals-and-when-not-to-use-them
category: computing-software
field: web-development
product: django
tags: [django, django-signals, post-save, on-commit, receivers, decoupling, python, web-development]
level: practitioner
status: verified
description: "Using Django signals deliberately: connecting receivers in AppConfig.ready, post_save pitfalls, transaction.on_commit, bulk operations that skip signals, and alternatives."
sources:
  - https://docs.djangoproject.com/en/stable/topics/signals/
  - https://docs.djangoproject.com/en/stable/ref/signals/
  - https://docs.djangoproject.com/en/stable/topics/db/transactions/#performing-actions-after-commit
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signals and when not to use them

**Goal:** use signals only for real decoupling (reacting to third-party or framework models), and keep business flow explicit.

## 1. Connecting correctly
```python
# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="create_profile")
def create_profile(sender, instance, created, raw, **kwargs):
    if created and not raw:                      # raw=True during loaddata fixtures
        Profile.objects.get_or_create(user=instance)

# accounts/apps.py
class AccountsConfig(AppConfig):
    name = "accounts"
    def ready(self):
        from . import signals  # noqa: F401
```
Receivers must accept `**kwargs`: Django enforces it only when `DEBUG = True` (`ValueError: Signal receivers must accept keyword arguments (**kwargs)`); with DEBUG off a receiver without it connects and then fails with `TypeError` on the first send. `dispatch_uid` prevents double registration (two `connect` calls fired the receiver once). `sender` may be a string such as `settings.AUTH_USER_MODEL` for model signals.

## 2. Side effects after commit
`post_save` fires inside the transaction. Sending email or enqueueing Celery there can act on data that later rolls back, or a worker may read before commit:
```python
transaction.on_commit(lambda: send_welcome.delay(instance.pk))
```

## 3. What doesn't fire signals
`QuerySet.update()`, `bulk_create()` (no `pre_save`/`post_save`), `bulk_update()`, raw SQL. (`QuerySet.delete()` does send `pre_delete`/`post_delete` per object, but loads them all.) Logic that must always run can't rely on signals.

## 4. Problems signals cause
- Hidden control flow: reading `Order.save()` doesn't reveal that it sends emails.
- Ordering between receivers isn't guaranteed.
- Exceptions in receivers propagate into the caller's save (`send_robust` exists, but `post_save` uses `send`).
- Tests become slow/flaky because every factory triggers side effects.

## 5. Prefer
- Explicit service functions: `create_order(...)` that saves and then notifies.
- Overriding `save()` for logic about the model itself.
- Signals for: models you don't own (User, third-party apps), cross-app hooks where the sender must not import the receiver, `request_finished`/`user_logged_in` framework events.

## 6. Custom signals
```python
order_paid = Signal()            # document the kwargs in a docstring
order_paid.send(sender=Order, order=order)
```

## 7. Testing
Disconnect or mute in tests that don't need them; assert a receiver ran by mocking the function it calls.

## Verify
- [ ] `grep -rn "@receiver\|\.connect(" .` - each receiver documented with why a signal is used.
- [ ] No external side effects directly in `post_save` (all wrapped in `on_commit`).
- [ ] Bulk paths that need the logic call it explicitly.

## Checked
Django 6.1.2, DRF 3.18.3 (Python 3.14, Windows, scratch venv, SQLite) with a scratch project that reproduces the skill's snippets.
- Run: `post_save` receiver got `created=True, raw=False` on `create()`; `bulk_create`, `QuerySet.update` and `bulk_update` fired nothing; `QuerySet.delete()` fired `post_delete` once per object (2 of 2).
- Run: a receiver without `**kwargs` is accepted with DEBUG off (TypeError on the next save) and rejected with `ValueError` under DEBUG on; duplicate `dispatch_uid` fired once; an exception in a receiver propagated out of `save()`; `send_robust` returned the exception instead of raising; a custom `Signal().send(sender=..., order=...)` delivered the kwarg.
- Run: `transaction.on_commit` callbacks do not run inside `TestCase` unless `captureOnCommitCallbacks(execute=True)` is used (callback ran once under it, not otherwise), and are skipped when the atomic block rolls back.
- Run: `post_save.connect(f, sender=settings.AUTH_USER_MODEL)` with a string sender.
