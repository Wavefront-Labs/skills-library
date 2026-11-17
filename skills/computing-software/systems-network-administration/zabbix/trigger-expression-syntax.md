---
id: computing-software.systems-network-administration.zabbix.trigger-expression-syntax
name: trigger-expression-syntax
category: computing-software
field: systems-network-administration
product: zabbix
tags: [trigger, expression, functions, time-shift, history-functions, function]
level: practitioner
status: docs-checked
description: "Write trigger expressions with function(/host/key,param) syntax, #N value counts, time shifts and nested expressions."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/triggers/expression
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The basic form is function(/host/key,parameter)<operator><constant>. Example: min(/Zabbix server/net.if.in[eth0,bytes],5m)>100K fires when received traffic stayed above 100 KB for five minutes.

Parameters:
- /host/key names the item. Dropping the host (//key) works only in calculated item formulas and expression macros (event name, graph name, map labels); elsewhere it is an error. The referenced item must be supported, except for nodata().
- Time can be seconds or with suffixes. A hash mark changes meaning: sum(/host/key,10m) is the last ten minutes, sum(/host/key,#10) the last ten values. For last(), #2 is the previous value, not a count.
- Time shift: avg(/host/key,1h:now-1d) is the one-hour average from a day ago. Shifts in M and y are valid only for trend functions; others take s, m, h, d, w.
- Absolute periods use /unit: 1d:now/d is yesterday, 1d:now/d+1d today, 1w:now/w last week.

Functions can take other expressions as parameters, for example min(min(/host/key,1h),min(/host2/key2,1h)*10). That is not allowed when the function reads item history: min(/host/key,#5*10) is invalid.

Examples from the docs:
- Either high load: last(/www.example.com/system.cpu.load[all,avg1])>5 or min(/www.example.com/system.cpu.load[all,avg1],10m)>2
- Value changed: last(/h/vfs.file.cksum[/etc/passwd],#1)<>last(/h/vfs.file.cksum[/etc/passwd],#2)
- Count: count(/h/icmpping,30m,,"0")>5

A problem expression alone is both the problem and recovery threshold.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/triggers/expression): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
