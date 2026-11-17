---
id: computing-software.cybersecurity-defensive.suricata.command-line-run-and-test
name: command-line-run-and-test
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [command-line, config-test, verbosity, daemon]
level: intro
status: docs-checked
description: "Core Suricata command-line options for loading config, testing it, setting log directory, verbosity, daemon mode, pid file and user."
sources: ["https://docs.suricata.io/en/latest/command-line-options.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running Suricata from the command line

- `-c <path>`: load a configuration file. `--include <path>` adds YAML files after it (repeatable, loaded in order).
- `-T`: test the configuration.
- `-v`: raise verbosity: one gives INFO, two PERF, three CONFIG, four DEBUG. It never lowers a level set in the config.
- `-l <dir>`: log directory, overriding `default-log-dir`.
- `-D`: run as a daemon.
- `--pidfile <file>`: write the PID, overriding `pid-file`, even when not daemonised.
- `--user=` and `--group=`: drop to this user and group after startup, overriding `run-as`.
- `-V`: print version. `-h`: usage.

## Rule loading

- `-s <file.rules>`: add signature files to those in the YAML (globs allowed).
- `-S <file.rules>`: load only these, ignoring the YAML rules.
- `--init-errors-fatal`: exit on signature load errors.
- `--strict-rule-keywords`: treat missing classtype or reference values as errors.

## Checked

2026-11-04. Every option above confirmed against the Suricata Command Line Options page.

Changed: the page says only "Test configuration" for `-T`, so "and exit" was dropped.

Method: documentation only; no commands were run.
