---
id: computing-software.messaging-and-integration.celery.beat-crontab-solar-schedules
name: beat-crontab-solar-schedules
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery, beat, crontab, solar, ephem, schedules, celery-beat-crontab]
level: practitioner
status: docs-checked
description: "Write Celery crontab expressions and solar schedules for beat, with the day_of_week and hour patterns from the docs, solar event types, and lat/long signs."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: schedule tasks by wall-clock time (crontab) or by sun events (solar).

## crontab

```python
from celery.schedules import crontab
app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}
```

Examples from the page:

- `crontab()` every minute
- `crontab(minute=0, hour=0)` daily at midnight
- `crontab(minute=0, hour='*/3')` every three hours (same as `hour='0,3,6,9,12,15,18,21'`)
- `crontab(minute='*/15')` every 15 minutes
- `crontab(day_of_week='sunday')` every minute (!) on Sundays
- `crontab(minute='*/10', hour='3,17,22', day_of_week='thu,fri')` every ten minutes during 3-4am, 5-6pm and 10-11pm on Thursdays or Fridays
- `crontab(minute=0, hour='*/2,*/3')` every hour except 1am, 5am, 7am, 11am, 1pm, 5pm, 7pm, 11pm
- `crontab(minute=0, hour='*/5')` hours divisible by 5, so 3pm (15) not 5pm
- `crontab(minute=0, hour='*/3,8-17')` hours divisible by 3 plus office hours
- `crontab(0, 0, day_of_month='2')` second day of each month
- `crontab(0, 0, day_of_month='2-30/2')` every even day
- `crontab(0, 0, day_of_month='1-7,15-21')` first and third weeks
- `crontab(0, 0, day_of_month='11', month_of_year='5')` 11 May each year
- `crontab(0, 0, month_of_year='*/3')` every day in the first month of each quarter

Since 5.7 a crontab whose `day_of_month` never occurs in its `month_of_year` (e.g. 30 February) raises `ValueError` on creation; previously beat exited when computing the next run.

## solar

Requires the `ephem` library: `pip install celery[solar]`.

```python
from celery.schedules import solar
app.conf.beat_schedule = {
    'add-at-melbourne-sunset': {
        'task': 'tasks.add',
        'schedule': solar('sunset', -37.81753, 144.96715),
        'args': (16, 16),
    },
}
```

Signature: `solar(event, latitude, longitude)`. Latitude: + north, - south. Longitude: + east, - west.

Events: `dawn_astronomical` (sun 18 degrees below horizon), `dawn_nautical` (12), `dawn_civil` (6), `sunrise`, `solar_noon`, `sunset`, `dusk_civil` (6), `dusk_nautical` (12), `dusk_astronomical` (18).

Solar events are computed in UTC and ignore the `timezone` setting. In polar regions or at high latitudes an event that doesn't occur on a day is skipped until the next day it does (since 5.7; earlier it raised `TypeError` and beat exited). `solar_noon` is the exception and occurs every day.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/periodic-tasks.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
