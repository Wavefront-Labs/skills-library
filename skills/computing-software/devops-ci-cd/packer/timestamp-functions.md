---
id: computing-software.devops-ci-cd.packer.timestamp-functions
name: timestamp-functions
category: computing-software
field: devops-ci-cd
product: packer
tags: [timestamp, formatdate, regex-replace, naming, fn-time]
level: intro
status: docs-checked
description: "Generate unique image names with timestamp() and formatdate(), noting timestamp uses RFC 3339."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/functions/datetime/timestamp/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`timestamp()` returns the current date and time as a string in RFC 3339 "Date and Time format", for example `2018-05-13T07:44:12Z`. The docs note that the result changes every second.

`formatdate(spec, timestamp)` converts an RFC 3339 timestamp string into another layout:

```hcl
locals {
  build_time = formatdate("YYYYMMDD-hhmmss", timestamp())
  image_name = "app-${local.build_time}"
}
```

Format sequences (from the `formatdate` page):

- `YYYY` four-digit year, `MM` zero-padded month, `DD` zero-padded day.
- `hh` 24-hour zero-padded hour (`HH` is the 12-hour form), `mm` minute, `ss` second.
- `ZZZ` timezone offset with a special case "UTC"; `Z` gives "Z" for UTC.
- Non-letter characters such as punctuation are copied verbatim. To include literal letters, enclose them in single quotes, e.g. `"YYYY-MM-DD'T'hh:mm:ssZ"`.
- It is not locale-aware: month and day names are English only.

Example outputs: `formatdate("MMM DD, YYYY", "2018-01-02T23:12:01Z")` gives `Jan 02, 2018`.

Packer used to let you choose your own format for timestamps. With HCL2, and for parity with Terraform, it uses RFC 3339 as a string; `formatdate` still lets you format it.

Put the formatted value in a local so one named value is reused in image names and tags.

## Checked

Method: docs-checked 2026-11-09 against the Packer `timestamp` function page and the `formatdate` page (both read in full as published page source). Dropped regex_replace, hcl2_upgrade mapping, Unix-timestamp and per-run-evaluation claims, which the pages do not support (the timestamp page says the result changes every second).
