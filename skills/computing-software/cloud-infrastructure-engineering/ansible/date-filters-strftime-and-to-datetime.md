---
id: computing-software.cloud-infrastructure-engineering.ansible.date-filters-strftime-and-to-datetime
name: date-filters-strftime-and-to-datetime
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, filters, strftime, to-datetime, now, date-arithmetic, certificate-expiry]
level: practitioner
status: docs-checked
description: "Format and compare dates in Ansible with strftime, to_datetime, now() and timedelta arithmetic, e.g. certificate expiry checks and retention cut-offs."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/strftime_filter.html", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/to_datetime_filter.html", "https://github.com/ansible/ansible-documentation", "https://github.com/ansible/ansible"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date filters: strftime and to_datetime

## Formatting: strftime (epoch → string)
```yaml
"{{ '%Y-%m-%d %H:%M:%S' | strftime }}"                 # now, controller local time
"{{ '%Y-%m-%d' | strftime(1735689600) }}"              # given epoch seconds
"{{ '%Y-%m-%dT%H:%M:%SZ' | strftime(second=ts, utc=true) }}"   # utc arg: added in 2.14 per the plugin documentation
"{{ '%Y%m%d' | strftime(ansible_facts.date_time.epoch | int) }}"
```
The format string is the filter **input**, the epoch (seconds) is the argument. Before ansible-core 2.21 the filter was based on Python's `time.strftime`; from 2.21 it passes through to `datetime.datetime.strftime`.

## Parsing: to_datetime (string → datetime)
```yaml
"{{ '2026-12-31 23:59:59' | to_datetime }}"            # default format '%Y-%m-%d %H:%M:%S'
"{{ 'Dec 31 23:59:59 2026 GMT' | to_datetime('%b %d %H:%M:%S %Y %Z') }}"
```

## Arithmetic
datetime minus datetime gives a timedelta with `.days`, `.seconds`, `.total_seconds()`:
```yaml
days_left: >-
  {{ ((cert.not_after | to_datetime('%Y%m%d%H%M%SZ')) - now(utc=true)).days }}
```
`now()` (Jinja global, added in 2.8) takes `utc` (default False) and `fmt` (a strftime string; a formatted string is returned when given). It returns a naive `datetime`, in UTC time when `utc=true`.

Timestamps from files (`stat.mtime`, float epoch):
```yaml
age_days: "{{ ((now().timestamp() - st.stat.mtime) / 86400) | int }}"
```

## Example: alert on certificates expiring soon
`community.crypto.x509_certificate_info` returns `not_after` as an ASN.1 TIME string (`YYYYMMDDHHMMSSZ`).
```yaml
- community.crypto.x509_certificate_info: {path: /etc/ssl/certs/app.pem}
  register: cert
- ansible.builtin.assert:
    that: (( cert.not_after | to_datetime('%Y%m%d%H%M%SZ') ) - now(utc=true)).days > 21
    fail_msg: "app.pem expires {{ cert.not_after }}"
```

## Gotchas
- `now()` and `strftime` run on the **controller**; `ansible_date_time` holds the target's time as of fact gathering. `strftime` without `utc=true` uses the local timezone.
- `to_datetime` takes a `format` argument (default `%Y-%m-%d %H:%M:%S`) that must match the input exactly, including a literal `Z`.
- The `seconds` attribute of a timedelta is only the remainder after whole days; use `.total_seconds()` for the full duration.
- Cast fact values with `| int` before passing them as the epoch to `strftime`.

## Verify
- [ ] A `debug` task with `msg: "{{ ('2026-12-31 00:00:00' | to_datetime - now()).days }}"` prints a plausible number.

## Checked
Date: 2026-10-24. Documentation: Ansible playbook guide, Filters (playbooks_filters.rst), ansible-core plugins/filter docs, Templating now() page, Jinja filters.py.
Confirmed:
- strftime takes the format as input, second and utc arguments (utc added 2.14 per the plugin docs; 2.21 switched to datetime.strftime); to_datetime default format and timedelta attributes (days, seconds is the remainder, total_seconds).
- now() takes utc and fmt, added 2.8, returns a naive datetime (source _jinja_plugins.py); community.crypto x509_certificate_info returns not_after as an ASN.1 TIME string.
- Removed the naive-versus-aware tzinfo workaround and the ansible_date_time claims.

Method: documentation only; no commands were run.
