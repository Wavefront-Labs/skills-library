---
id: computing-software.systems-network-administration.keepalived.global-defs-lvs-id
name: global-defs-lvs-id
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, global-defs, lvs-id, identification]
level: intro
status: docs-checked
description: "global_defs lvs_id names the LVS director; the case studies use LVS_MAIN. Placed with the email settings at the top of keepalived.conf."
sources:
  - https://keepalived.readthedocs.io/en/latest/configuration_synopsis.html
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# global_defs: lvs_id

`lvs_id` is an alphanumeric name for the LVS director. The case studies set:
```
global_defs {
    lvs_id LVS_MAIN
    ...
}
```
It sits in the `global_defs` block alongside the notification email and SMTP keywords. The synopsis documents only this and the email keywords for `global_defs`; it states no default.

Give each director a distinct, recognisable value so alerts and logs can be traced to a node.

Verify: the daemon starts cleanly with the keyword present and the dumped configuration (-d) shows the value.

## Checked

2026-11-04. Confirmed lvs_id as an alphanumeric director name on the configuration synopsis page, LVS_MAIN in the Healthcheck case study, and the LVS ID line in the configuration dump on the programs synopsis page. Nothing removed.

Method: documentation only; no commands were run.
