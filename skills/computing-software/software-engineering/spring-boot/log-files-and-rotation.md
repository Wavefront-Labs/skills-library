---
id: computing-software.software-engineering.spring-boot.log-files-and-rotation
name: log-files-and-rotation
category: computing-software
field: software-engineering
product: spring-boot
tags: [spring-boot, logging, logging-file-name, logging-file-path, log-rotation, rollingpolicy, logback, log4j2]
level: practitioner
status: docs-checked
description: "Write Spring Boot logs to a file with logging.file.name or logging.file.path and tune Logback or Log4j2 rotation with rollingpolicy properties."
sources:
  - https://docs.spring.io/spring-boot/reference/features/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Boot logs only to the console. To also write a file set `logging.file.name` or `logging.file.path`.

| logging.file.name | logging.file.path | Result |
|---|---|---|
| none | none | console only |
| `my.log` | none | writes to that file (absolute or relative to the current directory) |
| none | `/var/log` | writes `spring.log` to that directory |
| set | set | `logging.file.name` is used, `logging.file.path` ignored |

Files rotate at 10 MB and log ERROR, WARN and INFO by default. Log4j2 needs `logging.file.path` set for such configuration. Logging keys are independent of the logging system, so keys like `logback.configurationFile` are not managed by Boot.

Rotation properties apply only to Logback and Log4j2; for other systems configure rotation yourself.

Logback (`logging.logback.rollingpolicy.*`):
- `file-name-pattern`: archive file name pattern
- `clean-history-on-start`: clean archives at start
- `max-file-size`: size before archiving
- `total-size-cap`: maximum total archive size before deletion
- `max-history`: archives to keep (default 7)

Log4j2 (`logging.log4j2.rollingpolicy.*`):
- `file-name-pattern`
- `max-file-size` (default 10MB)
- `max-history` (default 7)
- `strategy` (default `size`; also `cron`, `time`, `size-and-time`)
- `cron` (default every day at midnight, when strategy is cron)
- `time-interval` (default 1, for time or size-and-time)
- `time-modulate` (default false: align the next rollover to the top of the interval)

## Checked

2026-11-07

Read logging.adoc (docs-repo source of the cited Logging page) in full (935 lines), using the File Output and File Rotation sections.
Confirmed: console-only default; logging.file.name / logging.file.path table including spring.log in the directory and name winning over path; absolute or relative locations; 10 MB rotation and ERROR/WARN/INFO defaults; Log4j2 requiring logging.file.path; independence of logging keys such as logback.configurationFile; rotation properties only for Logback and Log4j2; Logback file-name-pattern, clean-history-on-start, max-file-size, total-size-cap, max-history (default 7); Log4j2 file-name-pattern, max-file-size (10MB), max-history (7), strategy (size; cron, time and size-and-time named in the property descriptions), cron (daily at midnight), time-interval (1), time-modulate (false).
Nothing trimmed.

Method: documentation only; no commands were run.
