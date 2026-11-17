---
id: computing-software.web-development.django.custom-management-commands
name: custom-management-commands
category: computing-software
field: web-development
product: django
tags: [django, management-commands, basecommand, manage-py, cli, cron, python, web-development]
level: practitioner
status: verified
description: "Writing Django management commands: BaseCommand structure, arguments, output and exit codes, transactions and batching, dry-run flags, testing with call_command."
sources:
  - https://docs.djangoproject.com/en/stable/howto/custom-management-commands/
  - https://docs.djangoproject.com/en/stable/ref/django-admin/#running-management-commands-from-your-code
  - https://docs.python.org/3/library/argparse.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom management commands

**Goal:** operational scripts (backfills, imports, cleanup jobs) that run with Django settings, are safe to re-run and are tested.

## 1. Layout
```
shop/management/__init__.py
shop/management/commands/__init__.py
shop/management/commands/purge_carts.py      ->  python manage.py purge_carts
```

## 2. Command
```python
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from shop.models import Cart   # the example's model (with updated_at and an order FK)

class Command(BaseCommand):
    help = "Delete abandoned carts older than N days."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=30)
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--batch-size", type=int, default=1000)

    def handle(self, *args, days, dry_run, batch_size, **opts):
        if days < 7:
            raise CommandError("Refusing to purge carts younger than 7 days.")   # exit code 1, clean message
        cutoff = timezone.now() - timedelta(days=days)
        qs = Cart.objects.filter(updated_at__lt=cutoff, order__isnull=True)
        total = qs.count()
        self.stdout.write(f"{total} carts to delete (cutoff {cutoff:%Y-%m-%d})")
        if dry_run:
            return
        deleted = 0
        while ids := list(qs.values_list("pk", flat=True)[:batch_size]):
            with transaction.atomic():
                Cart.objects.filter(pk__in=ids).delete()
            deleted += len(ids)
            self.stdout.write(f"  {deleted}/{total}")
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted} carts"))
```

## 3. Conventions
- Write to `self.stdout`/`self.stderr` (capturable in tests), not `print`.
- Idempotent and resumable: select what still needs work each batch.
- Batch writes with short transactions; avoid one giant transaction locking tables.
- `--dry-run` for anything destructive; log counts before acting.
- `verbosity` option (`-v 2`) is built in: `opts["verbosity"]`.
- `requires_system_checks = []` for commands that must run on a half-configured system.

## 4. Scheduling
Cron/systemd timers/Kubernetes CronJobs running `python manage.py purge_carts`. Prevent overlap (`flock -n /tmp/purge.lock ...`, `concurrencyPolicy: Forbid`). For app-level schedules with retries, Celery beat calling the same service function.

## 5. Testing
```python
from io import StringIO
from django.core.management import call_command
def test_purge_dry_run(db):
    CartFactory(updated_at=timezone.now() - timedelta(days=60))
    out = StringIO()
    call_command("purge_carts", "--dry-run", stdout=out)
    assert "1 carts to delete" in out.getvalue()
    assert Cart.objects.count() == 1
```

Run on Django 6.1.2 with this command: `--days 3` printed `CommandError: Refusing...` with exit code 1; `--batch-size=2` over 5 carts printed `2/5 4/5 5/5`; the test below passed (the test needs your own `CartFactory`).

## Verify
- [ ] `python manage.py help purge_carts` shows useful help text.
- [ ] Re-running after an interruption completes without duplicates.
- [ ] Tests cover dry-run and the guard `CommandError`.
