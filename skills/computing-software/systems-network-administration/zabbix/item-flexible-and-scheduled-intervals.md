---
id: computing-software.systems-network-administration.zabbix.item-flexible-and-scheduled-intervals
name: item-flexible-and-scheduled-intervals
category: computing-software
field: systems-network-administration
product: zabbix
tags: [update-interval, flexible-interval, scheduling, time-period, interval, flexible]
level: practitioner
status: docs-checked
description: "Vary item polling with flexible intervals or schedule exact check times using the md wd h m s scheduling syntax."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/items/item/custom_intervals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zabbix has two ways to bend an item's default update interval.

Flexible intervals pair an Interval with a Period. Inside the period the new interval applies; outside it the default does. Examples from the docs:
- 10 with period 1-5,09:00-18:00: every 10 seconds during working hours.
- 0 with period 1-7,00:00-7:00: no polling at night.
- 0 with period 7-7,00:00-24:00: no polling on Sundays.

If intervals overlap, the smallest value wins, and if that smallest is 0 nothing is polled. A flexible interval equal to the period length checks exactly once; greater than the period may check once or not at all (not recommended); less than the period checks at least once.

Scheduling intervals run in parallel with the update interval and fire at specific times. The syntax is md<filter>wd<filter>h<filter>m<filter>s<filter>, where md is month days (1-31), wd is week days (1-7), h hours (0-23), m minutes (0-59) and s seconds (0-59). A filter is [from[-to]][/step][,filter]. At least one filter is required, and each must have a range or a step. An empty filter matches 0 if no lower-level filter is present, otherwise all values. Omitting the hour filter while minutes are present therefore means every hour.

The docs note that a 60 second interval with a 1 minute period (12:00-12:01) was a workaround for scheduled checks, and recommend scheduling intervals instead. Proxies and agents use their local time zones for scheduling intervals, so align them with the server.

## Checked

2026-11-09. Confirmed against the Zabbix manual page Custom intervals (current): flexible interval examples, overlap rule, interval versus period length behaviour, scheduling syntax and ranges, filter grammar, empty filter rule, the workaround note and the time zone note.

Method: documentation only; no commands were run.
