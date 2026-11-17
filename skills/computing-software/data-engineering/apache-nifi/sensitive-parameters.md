---
id: computing-software.data-engineering.apache-nifi.sensitive-parameters
name: sensitive-parameters
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, sensitive-parameters, secrets, parameter-context, registry]
level: practitioner
status: docs-checked
description: "Rules for sensitive parameters in NiFi: immutable sensitivity, property pairing rules, single-reference requirement, hidden values and exclusion from Registry commits."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sensitive parameters

- Sensitive Value defaults to No; once a parameter is created its sensitivity flag cannot be changed.
- Once applied, a sensitive parameter's value is not shown in the UI.
- A sensitive property can only reference a sensitive parameter; a non-sensitive property can only reference a non-sensitive one.
- A sensitive property's value must be a single parameter reference: `#{password}123` and `#{password}#{suffix}` are not allowed (a non-sensitive property may use `#{path}/child/file.txt`).
- In versioned flows, the sensitive parameter's value is not sent to the flow registry, only the fact that the property references it.
- Properties that reference Controller Services cannot use parameters.

Verify: the referencing property saves, and the value never appears in the UI or in a committed version.

## Checked

Confirmed against the NiFi user guide (Parameters, Parameter Contexts, Using a Parameter in a Property, Parameters in Versioned Flows).

Method: docs-only read of cited pages, 2026-11-08
