---
id: computing-software.cybersecurity-defensive.zitadel.instance-and-virtual-instances
name: instance-and-virtual-instances
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, instance, virtual-instances, multi-tenancy, issuer]
level: intro
status: docs-checked
description: "Understand ZITADEL's instance as the top of the hierarchy, why one instance maps to one domain and issuer, and how virtual instances are added."
sources:
  - https://zitadel.com/docs/concepts/structure/instance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An instance is the top node in ZITADEL's data hierarchy. Default settings for the whole system live there: branding, login policy, password policy and so on. One instance normally runs on one domain and represents one issuer, for example login.customer.com. Inside an instance you create organizations, which can stand for departments of your own company, business customers or a consumer population.

A fresh installation always creates one instance for you. If you need more, add virtual instances through the system API. This suits a provider whose business customers need their own self-service and custom domain, because each virtual instance has every customization option and still shares your compute resources.

Practical consequences:

- Because one instance normally maps to one domain and issuer, choose the domain deliberately.
- Use organizations to separate teams or customers inside one instance.
- Use virtual instances when each customer needs its own domain and full customization.

The source describes instance settings as the defaults for the system; configure them once at instance level.

## Checked

2026-11-08. Read the instance page in full; removed claims about the system API and fallbacks that the page does not state.

Method: documentation only; no commands were run.
