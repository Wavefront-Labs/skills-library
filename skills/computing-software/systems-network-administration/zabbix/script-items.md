---
id: computing-software.systems-network-administration.zabbix.script-items
name: script-items
category: computing-software
field: systems-network-administration
product: zabbix
tags: [script-item, javascript, httprequest, timeout, duktape, script]
level: advanced
status: docs-checked
description: "Collect data with JavaScript script items that make multi-step HTTP calls and take macro parameters."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/script
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Script items run user-written JavaScript on the server or proxy pollers. They suit multi-step collection, such as calling one HTTP endpoint, transforming the result and passing it to a second call.

Fields:
- Type: Script, with a unique Key.
- Parameters: name and value pairs passed to the script. User macros are supported. The docs examples read the pairs in the script with JSON.parse(value).
- Script: JavaScript that must return the metric value.
- Timeout: 1-600 seconds; exceeding it returns an error.

Examples from the docs:

var request = new HttpRequest();
return request.get("https://www.example.com/release_notes");

With parameters url set to {$DOMAIN} and subpage set to /release_notes:

var obj = JSON.parse(value);
var request = new HttpRequest();
return request.get(obj.url + obj.subpage);

Multiple requests can be chained in one script: request.get(a) + request.get(b).

For logging, call Zabbix.log(3, 'Log test') in the script; the entry is written to the Zabbix server log and the script can still return a value such as 1.

In the parameters example the docs define the user macro {$DOMAIN}, preferably on the host level, rather than hard-coding the value.

## Checked

2026-11-09. Confirmed against the Zabbix manual page Script item (current): server or proxy pollers, Key, Parameters, Script and Timeout (1-600s) fields, and the four docs examples (simple, parameters, multiple requests, logging). Removed the dependent-items advice, which the page does not state.

Method: documentation only; no commands were run.
