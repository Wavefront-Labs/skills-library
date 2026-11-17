---
id: computing-software.devops-ci-cd.bazel.bazel-test-size-timeout-and-sharding
name: bazel-test-size-timeout-and-sharding
category: computing-software
field: devops-ci-cd
product: bazel
tags: [bazel-test, test-timeout, test-size, test-sharding, shard-count, test-env, hermetic-tests]
level: practitioner
status: docs-checked
description: "Set test size, timeout and sharding correctly and know the runner environment Bazel provides to tests."
sources: ["https://bazel.build/reference/test-encyclopedia"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel test size, timeout and sharding

A test passes only if its process exits 0; printing PASS or FAIL means nothing. Tests should be hermetic: depend only on declared source files, build products and resources guaranteed constant by the runner.

Timeouts apply to the whole test target:

| timeout | seconds | recommended minimum |
|---|---|---|
| short | 60 | 0 |
| moderate | 300 | 30 |
| long | 900 | 300 |
| eternal | 3600 | 900 |

If `timeout` is unset it follows `size`: small = short, medium = moderate, large = long, enormous = eternal. Size also implies assumed peak resource use. The default size is medium. Override on the command line with `--test_timeout=120` (seconds) for slow environments; `--test_verbose_timeout_warnings` reports tests whose declared size is too large (a moderate test finishing in 5.5 s should be small or short).

Sharding: set `shard_count` and `--test_sharding_strategy`. The runner is launched once per shard with `TEST_TOTAL_SHARDS` and `TEST_SHARD_INDEX` (from 0). A runner that supports sharding must touch the file in `TEST_SHARD_STATUS_FILE`, otherwise Bazel fails the sharded test.

Environment: `HOME` defaults to `$TEST_TMPDIR`; `LANG`, `LC_ALL` and most `LC_*` are unset; `PWD` is `$TEST_SRCDIR/workspace-name`. Pass or override variables with `--test_env=NAME=value`.

If the main process exits while children run, the result comes from the main exit code; do not leak processes.

## Checked

2026-11-04. Read against the Bazel docs page(s): Test Encyclopedia (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the closing Verify line.
Method: documentation only; no commands were run.
