---
id: computing-software.software-engineering.php.php-php-profiling
name: php-php-profiling
category: computing-software
field: software-engineering
product: php
tags: [php, php-profiling, performance]
level: advanced
status: docs-checked
description: "Find PHP bottlenecks with the Xdebug profiler, SPX and Blackfire; read cachegrind call graphs and re-profile after each change."
sources: ["https://xdebug.org/docs/profiler", "https://github.com/NoiseByNorthwest/php-spx", "https://docs.blackfire.io/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling PHP

Tool choices (from the Xdebug, SPX and Blackfire documentation):
- Xdebug profiler: set `xdebug.mode` to `profile`; it writes `cachegrind.out.<pid>` files (name set by `xdebug.profiler_output_name`) into `xdebug.output_dir`. Output can be enormous for complex scripts, so check disk space. Open the files in KCacheGrind or QCacheGrind (or Webgrind). To profile selectively set `xdebug.start_with_request` to `trigger` and pass `XDEBUG_TRIGGER` as an environment value, GET/POST parameter or cookie. Profiled requests get an `X-Xdebug-Profile-Filename` response header.
- SPX: `SPX_ENABLED=1` before a CLI command prints a flat profile to STDERR; add `SPX_REPORT=full` for a report in the web UI at `/?SPX_KEY=dev&SPX_UI_URI=/`. For web requests profiling is switched on per browser session with the `SPX_ENABLED` and `SPX_KEY` cookies. `SPX_SAMPLING_PERIOD` enables sampling, which can be more accurate when small functions are called many times. A loaded but disabled SPX adds a little overhead.
- Blackfire: its docs describe a profiler plus assertions to check code against a performance budget; profiles run on synthetic requests by default so real traffic sees no overhead.

Method:
1. Reproduce one slow request or command with realistic data.
2. In KCacheGrind's Flat Profile, sort by time (the Self column excludes children) and read the Called column as well as durations; the callers and callees panes show where time goes.
3. Change one thing, re-profile, record before and after.

```sh
php -d xdebug.mode=profile -d xdebug.output_dir=/tmp/prof script.php
SPX_ENABLED=1 SPX_REPORT=full php script.php
```

## Gotchas
- Profiling output can be very large; do not leave profilers enabled globally in production.

Verify: after the fix, the same profile shows the targeted function's call count or time reduced.

## Checked
2026-11-09. Confirmed against the Xdebug Profiling page, the php-spx README and the Blackfire documentation introduction. Removed because those pages do not state them: XHProf/Tideways, `php --ri spx`, the OPcache and JIT remarks, the 10x to 100x slowdown figure, wall versus CPU time advice, the list of usual suspects (N+1, stat cache, `preg_*` loops), and "commercial service" for Blackfire.
Method: documentation only; no commands were run.
