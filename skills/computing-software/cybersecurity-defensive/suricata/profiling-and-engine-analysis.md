---
id: computing-software.cybersecurity-defensive.suricata.profiling-and-engine-analysis
name: profiling-and-engine-analysis
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [rule-profiling, packet-profiling, engine-analysis-fast-pattern, fast-pattern]
level: sme
status: docs-checked
description: "Find slow rules and fast-pattern choices: engine-analysis rules-fast-pattern, rule and packet profiling, and their build requirements."
sources: ["https://docs.suricata.io/en/latest/configuration/suricata-yaml.html", "https://docs.suricata.io/en/latest/command-line-options.html", "https://docs.suricata.io/en/latest/rules/differences-from-snort.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Profiling and engine analysis

## Fast pattern analysis
Each signature has zero or more patterns, and only one is used by the multi pattern matcher
(MPM). Suricata chooses it unless the `fast_pattern` rule option is used.
Set in `suricata.yaml`:

```
engine-analysis:
  rules-fast-pattern: yes
```

and run `suricata -c suricata.yaml --engine-analysis` (the command-line option prints the
analysis reports and exits). The log directory then holds `rules_fast_pattern.txt`, with per
signature fields: `Fast pattern set`, `Fast pattern only set`, `Fast pattern chop set`
(with offset and length for `fast_pattern:1,2`), `Content negated`, `Original content` and
`Final content`. Example: with `content:"abc"; fast_pattern:1,2;` the final content is `bc`.

Versus Snort (differences page): Suricata does not truncate fast patterns and does not strip
leading NULL bytes, and the `only` in `fast_pattern:only` is silently ignored. Suricata is case
sensitive for the fast pattern unless `nocase` is set. When in doubt which content will be the
fast pattern, set `fast_pattern` explicitly or read `rules_fast_pattern.txt`.

## Rule profiling
```
profiling:
  rules:
    enabled: yes
```
Requires Suricata compiled with `--enable-profiling`; compiling it in affects performance even
if the option is disabled in the config. Statistics print at the end of each session, sorted
by one of `ticks`, `avgticks`, `checks`, `maxticks` or `matches` (high to low), for example
`sort: avgticks` with `limit: 100` signatures. Ticks count CPU computation; the output has
rule, ticks, percent, checks, matches, max ticks and average ticks per rule.

## Packet profiling
Under `profiling: packets:` set `enabled: yes` (default), `filename: packet_stats.log` and
`append: yes` (no overwrites the file). A per-packet CSV (`csv:` with `filename:
packet_stats.csv`) is disabled by default. Both only work when compiled with
`--enable-profiling`. Use runmode `single` to profile code speed, since with several threads the
time threads wait on each other is counted.

## Checked
Confirmed 2026-11-09 against the Suricata configuration page (section Engine analysis and profiling), the command line options page and the differences-from-Snort page (Fast Pattern section).
Removed as unconfirmed: the claim to feed results into `detect.profile`.
Method: docs-checked 2026-11-09 against docs.suricata.io suricata-yaml, command-line-options and differences-from-snort pages
