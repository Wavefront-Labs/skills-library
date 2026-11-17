---
id: computing-software.cloud-infrastructure-engineering.kubernetes.label-syntax-rules
name: label-syntax-rules
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, labels, label-syntax, label-selector, annotations]
level: practitioner
status: docs-checked
description: "Kubernetes label key and value syntax (prefix, 63-character name, allowed characters), reserved prefixes, and errors from invalid labels."
sources: ["https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#syntax-and-character-set", "https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/", "https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Label syntax

## Keys
`[prefix/]name`
- **name**: required, 63 characters or less, beginning and ending with an alphanumeric
  (`[a-z0-9A-Z]`), with dashes, underscores, dots and alphanumerics between.
- **prefix**: optional; if given it must be a DNS subdomain (DNS labels separated by dots, not
  longer than 253 characters in total) followed by `/`.
- With no prefix the key is presumed private to the user. Automated components (scheduler,
  controller-manager, apiserver, kubectl, third-party automation) that add labels to end-user
  objects must specify a prefix.
- The `kubernetes.io/` and `k8s.io/` prefixes are reserved for Kubernetes core components.
- A label key must be unique on a given object.

## Values
63 characters or less (may be empty); unless empty, begin and end with an alphanumeric
`[a-z0-9A-Z]`, with dashes, underscores, dots and alphanumerics between.

## Valid and invalid
| Label | OK? |
|---|---|
| `app.kubernetes.io/name: web` | yes (recommended application label) |
| `team: payments` | yes |
| `example.com/owner: alice` | yes |
| `owner: alice@example.com` | no: `@` is not allowed |
| `version: v1.2.3+build5` | no: `+` is not allowed |
| `branch: feature/login` | no: `/` is not allowed in a value |
| `description: a long sentence ...` | no: spaces and length; use an annotation |

## Practical rules
- Put free text, URLs, emails and JSON in annotations (non-identifying information), not
  labels. The total size of all annotations on one object, keys and values combined, must not
  exceed 256 KiB.
- Sanitise values taken from CI (for example branch names): replace disallowed characters,
  truncate to 63 characters and strip leading and trailing non-alphanumerics.
- Labels allow efficient queries and watches; they are not unique, so many objects can share one.

## Verify
```bash
kubectl label pod x 'branch=feature-login' --dry-run=server
```

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Labels and Selectors", "Recommended
Labels" and "Annotations" (current docs; latest release v1.37.1). Confirmed: key and value
rules, prefix rules, reserved prefixes, 256 KiB annotation total. Removed unconfirmed claims
(exact validation error text, reserved-subdomain wording, cardinality advice and the shell
sanitising one-liner).
Method: documentation only; no commands were run.
