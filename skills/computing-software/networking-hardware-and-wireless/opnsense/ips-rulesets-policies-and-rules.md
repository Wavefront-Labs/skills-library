---
id: computing-software.networking-hardware-and-wireless.opnsense.ips-rulesets-policies-and-rules
name: ips-rulesets-policies-and-rules
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [ids-policies, suricata-rules, rulesets, et-open, abuse-ch]
level: advanced
status: docs-checked
description: "Manage Suricata rule sources and policies on OPNsense: download tab, policy priority and actions, installed rules filters, ET Pro oinkcode and abuse.ch lists."
sources: ["https://docs.opnsense.org/manual/ips.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IDS/IPS rulesets, policies and rules

A fresh IDS/IPS has no rules and detects nothing until rulesets are downloaded on the Download tab, which lists available rulesets (extensible by plugins) and their last download time. Before 21.1, per-download filters changed alert to block; since then Policies do this, and old filters migrate automatically.

Policies are the preferred way to alter behaviour. Editing many single rules on the Rules tab is more fragile and can slow the interface. A policy has: general data (description, enabled, priority; overlapping policies are processed in order, with the lowest priority number winning), match criteria (rulesets, current rule action: default disabled, alert or drop, plus metadata such as affected product or deployment like datacenter or perimeter) and the new action: disable selected rules, alert only, or drop. Metadata options depend on the vendor; if the source rule has none it cannot be used.

The Installed rules grid filters by the same metadata. Use the matched_policy filter to see which policy set a rule; manual single-rule changes show the policy "__manual__".

Available sets: Emerging Threats Open (free, BSD licensed, not full coverage, so not standalone for regulated environments); ETPro Telemetry (free from Proofpoint); ETPro commercial, which needs the os-intrusion-detection-content-et-pro plugin and then an etpro.oinkcode in the Administration / Download settings; abuse.ch SSL Blacklist (SHA1 fingerprints of bad certificates), Feodo Tracker (versions A to D of the Feodo/Cridex/Dridex family), URLHaus (malware distribution sites, from 18.1.7) and the app detection ruleset (from 18.1.11, mostly blocking web services by URL).

## Checked

2026-11-03. Confirmed against the OPNsense Intrusion Prevention System manual page: download tab, the 21.1 change to policies, policy sections and priority, matched_policy and __manual__, and the ruleset descriptions with the 18.1.7 and 18.1.11 versions. Nothing removed.

Method: documentation only; no commands were run.
