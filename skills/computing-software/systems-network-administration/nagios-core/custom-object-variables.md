---
id: computing-software.systems-network-administration.nagios-core.custom-object-variables
name: custom-object-variables
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, custom-variables, custom-macros, underscore-variables, host-macro, service-macro, contact-macro, environment-variables]
level: practitioner
status: docs-checked
description: "Define custom variables on Nagios Core hosts, services and contacts with a leading underscore and read them as $_HOSTxxx$ macros or NAGIOS__ environment variables."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/customobjectvars.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom object variables

Add to a host, service or contact by starting the name with an underscore:

```
define host {
    host_name     sw1
    _mac_address  00:06:5B:A6:AD:AA
}
```

- Names are upper-cased internally (`MAC_ADDRESS`).
- They inherit through templates like standard variables.

| Object | Variable | Macro | Environment |
|---|---|---|---|
| Host | MAC_ADDRESS | `$_HOSTMAC_ADDRESS$` | `NAGIOS__HOSTMAC_ADDRESS` |
| Service | SNMP_COMMUNITY | `$_SERVICESNMP_COMMUNITY$` | `NAGIOS__SERVICESNMP_COMMUNITY` |
| Contact | AIM_USERNAME | `$_CONTACTAIM_USERNAME$` | `NAGIOS__CONTACTAIM_USERNAME` |

The `_HOST`/`_SERVICE`/`_CONTACT` prefix separates same-named variables on different object types.

Since 4.5.13, values are stripped of characters in `illegal_macro_output_chars`.

Typical use: store a per-object value (for example an SNMP community) once and reference its macro from one shared command, notification or event handler.

Self-check: run the check with debug_level for macros (2048) and see the expanded value.

## Checked

2026-11-04. Confirmed on the Custom Object Variables page: leading underscore, upper-casing, template inheritance, the _HOST/_SERVICE/_CONTACT macro and NAGIOS__ environment names in the table, and the 4.5.13 sanitising by illegal_macro_output_chars; debug_level 2048 for macros confirmed on the main configuration page. Replaced the check_snmp example, which is not on the page, with a generic use.

Method: documentation only; no commands were run.
