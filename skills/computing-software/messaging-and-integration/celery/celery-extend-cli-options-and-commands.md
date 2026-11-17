---
id: computing-software.messaging-and-integration.celery.celery-extend-cli-options-and-commands
name: celery-extend-cli-options-and-commands
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-extending, celery, cli, click, user-options, preload-options, entry-points, subcommand]
level: advanced
status: docs-checked
description: "Add custom command-line options to celery worker/beat/events, add preload options, and register new celery sub-commands via the celery.commands entry point."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/extending.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extend the celery command line

Goal: add options and sub-commands to the `celery` program.

Celery commands use `click`. Add options to `worker`, `beat` or `events` by adding `click.Option` instances to `app.user_options`:

```python
from celery import Celery
from click import Option

app = Celery(broker='amqp://')
app.user_options['worker'].add(Option(('--enable-my-option',),
                                      is_flag=True,
                                      help='Enable custom option.'))
```

All bootsteps then receive the option as a keyword argument to `__init__`:

```python
class MyBootstep(bootsteps.Step):
    def __init__(self, parent, enable_my_option=False, **options):
        super().__init__(parent, **options)
        if enable_my_option:
            party()

app.steps['worker'].add(MyBootstep)
```

Preload options are special options passed to all sub-commands of the umbrella `celery` command. Add one under `user_options['preload']` and read it from the `user_preload_options` signal:

```python
from celery import signals

app.user_options['preload'].add(Option(('-Z', '--template'),
                                       default='default',
                                       help='Configuration template to use.'))

@signals.user_preload_options.connect
def on_preload_parsed(options, **kwargs):
    use_template(options['template'])
```

Since 5.7 preload options also work with commands installed through the `celery.commands` entry point (for example Flower). A callback that cannot accept an option receives it only through `user_preload_options`, and the signal is sent for every sub-command, including built-ins that never used `handle_preload_options` such as `report`, because `consume_preload_options` wraps every command.

New sub-commands: register a `celery.commands` setuptools entry point whose value is `name = module.path:attribute`, pointing at a valid click command (separate module path and attribute with a colon):

```python
setup(
    name='flower',
    entry_points={'celery.commands': ['flower = flower.command:flower']},
)
```

```python
import click

@click.command()
@click.option('--port', default=8888, type=int, help='Webserver port')
@click.option('--debug', is_flag=True)
def flower(port, debug):
    print('Running our command')
```

Gotcha: entry-point discovery scans the metadata of every installed package and Celery caches the result for the process lifetime, so installing or removing a package providing `celery.commands`, `celery.result_backends` or `celery.beat_schedulers` entry points takes effect only after the process restarts.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/extending.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
