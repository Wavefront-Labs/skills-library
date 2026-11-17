---
id: computing-software.systems-network-administration.home-assistant.template-dates-times
name: template-dates-times
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [now, strftime, today-at]
level: practitioner
status: docs-checked
description: "Work with dates and times in Home Assistant templates: now(), utcnow(), today_at(), datetime parts, strftime formatting and strptime parsing."
sources:
  - https://www.home-assistant.io/docs/templating/dates-and-times/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build and format times in templates correctly.

Current time:

```text
Local: {{ now() }}
UTC:   {{ utcnow() }}
```

A time today:

```text
{{ today_at('22:00') }}
```

Parts of a datetime:

```text
Year:    {{ now().year }}
Month:   {{ now().month }}
Day:     {{ now().day }}
Hour:    {{ now().hour }}
Minute:  {{ now().minute }}
Weekday: {{ now().weekday() }}
```

Formatting with strftime:

```text
24-hour:    {{ now().strftime('%H:%M') }}
12-hour:    {{ now().strftime('%I:%M %p') }}
Weekday:    {{ now().strftime('%A') }}
Short date: {{ now().strftime('%Y-%m-%d') }}
Long date:  {{ now().strftime('%A, %B %-d, %Y') }}
```

Parsing text into a datetime:

```text
{% set event = strptime('2026-12-25 10:30', '%Y-%m-%d %H:%M') %}
{{ event }}
```

`now()` is in your configured time zone and `utcnow()` in UTC. Datetimes with different time zones can be compared directly, but comparing a datetime that has a time zone with one that has none causes an error: `strptime` (unless the format includes `%z`) and `as_datetime` of text without a zone return a datetime without a time zone, and `as_local` adds yours. The page also covers UNIX timestamp conversion, time differences such as how long ago something happened, countdowns, time zones, and common gotchas. Test any date template in Settings > Tools > Template before using it in an automation.

## Checked

2026-11-04. Confirmed against the Templating dates and times page. Corrected the claim that now() and utcnow() cannot be compared: the page says datetimes with different time zones compare directly, and only mixing with a datetime without a zone errors.

Method: documentation only; no commands were run.
