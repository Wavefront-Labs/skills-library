---
id: computing-software.cloud-infrastructure-engineering.external-dns.txt-registry-record-formats
name: txt-registry-record-formats
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, txt-registry, txt-new-format-only, record-type-prefix, ownership-records]
level: practitioner
status: docs-checked
description: "How the ExternalDNS TXT registry stores ownership metadata: record-type-prefixed names, legacy vs new format, AWS A ALIAS a- prefix and legacy cleanup."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/registry/txt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TXT registry record formats

The TXT registry is the default registry. It stores ownership metadata in TXT records in the same provider as the managed records.

**v0.18 and later:** one format only. Each TXT record carries the record type in its name (an `a-` prefix for A records). With `--txt-prefix="%{record_type}-abc-."` for apex `ex.com` you get TXT `cname-abc-.ex.com.` beside CNAME `ex.com.`; for `www.ex.com` you get `cname-abc-.www.ex.com.`.

**v0.16.0 and v0.16.1:** two formats. Legacy (no type info) and new (type prefix) are both written by default. `--txt-new-format-only` writes only the new one, which helps with provider record limits. AAAA records and encrypted TXT records always use the new format only. The flag is added to your existing flags; you still need `--managed-record-types=TXT`.

```sh
external-dns --provider=aws --source=ingress --managed-record-types=A --managed-record-types=TXT --txt-new-format-only
```

Switching to new-format-only does not delete legacy records. Make sure every instance supports the new format, enable the flag, then clean old TXT records manually.

**AWS A ALIAS:** Route 53 stores these as A/AAAA, so ownership uses `a-`/`aaaa-`. The old `cname-` record is still recognised, the `a-` record is created on the next reconcile, and the obsolete `cname-` is left with a warning.

**Cleanup:** the repo has `scripts/aws-cleanup-legacy-txt-records.py`; `--alias-cname-cleanup` deletes a `cname-` record only when its `a-` counterpart exists. Deleting registry TXT records causes no downtime, but ExternalDNS then regenerates all records, taking time proportional to the zone size.

## Checked

2026-11-04. Read the TXT registry page (Record Format Options, AWS A ALIAS records, legacy cleanup, v0.16 formats, migration to new format only). Confirmed the v0.18 single format, the cname-abc- examples, --txt-new-format-only behaviour, the a-/aaaa- alias note, --alias-cname-cleanup and the regeneration warning. Removed nothing.

Method: documentation only; no commands were run.
