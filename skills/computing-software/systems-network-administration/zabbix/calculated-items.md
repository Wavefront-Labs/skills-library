---
id: computing-software.systems-network-administration.zabbix.calculated-items
name: calculated-items
category: computing-software
field: systems-network-administration
product: zabbix
tags: [calculated-item, formula, aggregate, history-poller, calculated]
level: practitioner
status: docs-checked
description: "Create virtual metrics from other items' history using the calculated item formula syntax and its failure cases."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/calculated
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A calculated item computes a value on the server from other items' stored data. It is evaluated by history poller processes at the item's update interval, not when new data arrives, and the result is stored with history and trends like any item.

Formula syntax: function(/host/key,<parameters>). Omit the host to mean the current host: last(//vfs.fs.size[/,free]). The key of the calculated item has no connection to its formula. The formula syntax is shared with trigger expressions, and comparison to strings is allowed.

Examples from the docs:
- 100*last(//vfs.fs.size[/,free])/last(//vfs.fs.size[/,total]) for percent free.
- avg(/Zabbix server/zabbix[wcache,values],10m) for an average over 10m.
- last(//net.if.in[eth0,bytes])+last(//net.if.out[eth0,bytes]) for total bandwidth.

The item becomes unsupported when a referenced item is missing, disabled, on a disabled host or unsupported (nodata() excepted), when there is no data for a function, on division by zero, or on bad syntax. If you rename a referenced item key, update the formula by hand.

Other notes: a float result is trimmed if the type of information is Numeric (unsigned). With no recent cached data and no period in the function, Zabbix looks back as far as one week in the database. User macros expand only in parameters and constants, not in function, host, key or operator positions.

Calculated items can read history of items the author cannot access; set StartHistoryPollers to 0 to disable them.

## Checked

2026-11-09. Confirmed against the Zabbix manual page Calculated items (current): history poller evaluation on the server, update-interval processing, formula syntax with the omitted-host form, key independent of formula, Numeric (unsigned) trimming, user macro positions, one-week lookback, unsupported cases, the three example formulas, StartHistoryPollers=0. Reworded the precedence sentence and corrected the host name case in the example.

Method: documentation only; no commands were run.
