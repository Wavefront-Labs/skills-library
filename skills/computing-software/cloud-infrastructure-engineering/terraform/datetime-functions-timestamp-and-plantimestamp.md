---
id: computing-software.cloud-infrastructure-engineering.terraform.datetime-functions-timestamp-and-plantimestamp
name: datetime-functions-timestamp-and-plantimestamp
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, datetime-functions, timestamp, plantimestamp, formatdate, timeadd, timecmp, time-provider]
level: practitioner
status: verified
description: "Use timestamp, plantimestamp, formatdate, timeadd and timecmp correctly, avoid perpetual diffs from timestamp(), and store stable times with the time provider."
sources: ["https://developer.hashicorp.com/terraform/language/functions/timestamp", "https://developer.hashicorp.com/terraform/language/functions/plantimestamp", "https://developer.hashicorp.com/terraform/language/functions/formatdate", "https://registry.terraform.io/providers/hashicorp/time/latest/docs/resources/static"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date and time functions

| Function | Returns |
|---|---|
| `timestamp()` | current time, RFC 3339 UTC — **unknown during plan** (evaluated at apply), new on every apply |
| `plantimestamp()` (1.5+) | time the plan was created — known during plan; **not available in `terraform console`** |
| `formatdate(spec, ts)` | `formatdate("YYYY-MM-DD", ts)`, `"DD MMM YYYY hh:mm ZZZ"` |
| `timeadd(ts, dur)` | `timeadd(plantimestamp(), "720h")` (units ns, us, ms, s, m, h; negative ok; no `d` unit, so use `"24h"` for a day) |
| `timecmp(a, b)` (1.3+) | -1/0/1 |

## The perpetual-diff trap
```hcl
tags = { CreatedAt = timestamp() }      # changes on EVERY apply
```
Every plan shows an update. Fix with a stored time:
```hcl
resource "time_static" "created" {}
tags = { CreatedAt = time_static.created.rfc3339 }
```
`time_static` records the time once (re-generated only via `triggers`).

## Rotation and expiry
```hcl
resource "time_rotating" "key" {
  rotation_days = 90
}
resource "aws_iam_access_key" "ci" {
  user = aws_iam_user.ci.name
  lifecycle { replace_triggered_by = [time_rotating.key] }
}
```

## Checks with plantimestamp
```hcl
check "cert_not_expiring" {
  assert {
    condition     = timecmp(aws_acm_certificate.api.not_after, timeadd(plantimestamp(), "720h")) > 0
    error_message = "Certificate expires within 30 days."
  }
}
```
`plantimestamp()` is the right clock for conditions — `timestamp()` would make the
condition unknown at plan.

## formatdate tokens
`YYYY` year, `MM` month, `DD` day, `hh` 24h hour, `mm` minute, `ss` second,
`EEE` weekday short, `MMM` month short, `ZZZ` zone abbreviation; literal text in
single quotes: `formatdate("YYYYMMDD'T'hhmm", ts)`.

## Gotchas
- All times are UTC; there is no timezone conversion function.
- `timestamp()` in `count`/`for_each` makes them unknown: plan fails with `Invalid count argument` (checked on 1.9.8).
- `plantimestamp()` in a saved plan is the plan time, even if applied hours later.

## Verify
- [ ] Two consecutive plans show no diff for timestamp-like tags.
- [ ] `terraform console` → `formatdate("YYYY-MM-DD", timestamp())` prints today (UTC); `plantimestamp()` is rejected there (`There is no function named "plantimestamp"`), so check it through an output and `terraform plan`.
- [ ] A `check` condition must reference at least one object from the configuration (as the example does with the certificate); a condition made only of `plantimestamp()` and literals is rejected.
