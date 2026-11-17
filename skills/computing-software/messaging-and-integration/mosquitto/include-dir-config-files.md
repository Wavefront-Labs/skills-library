---
id: computing-software.messaging-and-integration.mosquitto.include-dir-config-files
name: include-dir-config-files
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [include-dir, config-files, load-order, conf-d]
level: practitioner
status: docs-checked
description: "Split Mosquitto configuration into .conf fragments with include_dir and predict the case-sensitive load order."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: load extra config files from a directory.

`include_dir dir` names a directory searched for config files. All files ending in `.conf` are loaded as configuration files. It is best as the last option in the main file. It is only processed from the main configuration file, and the directory must not contain the main configuration file.

Order: case sensitive alphabetical, with the upper case of each letter ordered before lower case. Given `b.conf`, `A.conf`, `01.conf`, `a.conf`, `B.conf`, `00.conf` the order is:

```
00.conf
01.conf
A.conf
a.conf
B.conf
b.conf
```

If `include_dir` is used multiple times, each is processed completely, in the order written. With `one.d` holding `B.conf` and `C.conf` and `two.d` holding `A.conf` and `D.conf`:

```
include_dir one.d
include_dir two.d
```
the load order is B.conf, C.conf, A.conf, D.conf.

File format reminder: lines whose first character is `#` are comments. Configuration lines start with a variable name and the value is separated from the name by a single space.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed the unsupported --test-config claim; load-order examples match the page.
