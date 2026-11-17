---
id: computing-software.networking-hardware-and-wireless.opnsense.system-health-rrd-graphs
name: system-health-rrd-graphs
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [system-health, rrd, reporting, graphs]
level: intro
status: docs-checked
description: "Use Reporting > Health on OPNsense: packets, quality, system and traffic collectors, RRD datasets, inverse, zoom, tables and CSV export."
sources: ["https://docs.opnsense.org/manual/systemhealth.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# System Health (RRD graphs)

Reporting > Health is a dynamic view over RRD data and lets you zoom into problems quicker than static graphs. Collectors: Packets (packets per second per interface), Quality (latency and loss of monitored gateways), System (memory, mbufs, states, processes and CPU temperature when available) and Traffic (per interface, including IPsec). More graphs appear depending on the features in use, for example NTP graphs.

Controls: toggle the top menu collapse; choose a category tab and graph from its dropdown; Select primary dataset (the further left, the lower the maximum resolution; graphs open at the highest resolution by default); Inverse, which flips each odd dataset (times minus one) so inbound and outbound traffic plot in opposite directions; Resolution, which caps the number of datapoints and thereby the scale of averages.

The label filter hides datasets: click once to disable, double-click to show only that one. For example, hiding processes lets the scale adapt so other series are visible. The zoom area below the main graph lets you click and drag to select a period; the main graph, scales and tables update, with more detailed data when available.

Show Tables displays min/max/average per dataset and a detailed table of each plotted value; the time column can switch between timestamps and human-readable dates, and the data can be exported as CSV for your own reporting. RRD statistics are included in configuration backups only if you choose to save them.

## Checked

2026-11-03. Read the System Health manual page (systemhealth.html) and the Configuration page (backups.html) on docs.opnsense.org and confirmed the claims above against them. Nothing needed removing.
Method: documentation only; no commands were run.
