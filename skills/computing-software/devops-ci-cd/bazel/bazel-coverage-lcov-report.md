---
id: computing-software.devops-ci-cd.bazel.bazel-coverage-lcov-report
name: bazel-coverage-lcov-report
category: computing-software
field: devops-ci-cd
product: bazel
tags: [bazel-coverage, lcov, genhtml, instrumentation-filter, combined-report, instrument-test-targets]
level: practitioner
status: docs-checked
description: "Produce a merged lcov coverage report with bazel coverage and render it to HTML with genhtml."
sources: ["https://bazel.build/configure/coverage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Code coverage with bazel coverage

Prerequisites: test targets, a toolchain with the language coverage tools, and a correct instrumentation configuration. Instrumentation is controlled by `--instrumentation_filter` (which targets are instrumented; by default Bazel matches the tested packages and prints the filter as an INFO message) and `--instrument_test_targets` (also instrument test targets themselves).

```bash
bazel coverage --combined_report=lcov //foo:all
genhtml --branch-coverage --output genhtml \
  "$(bazel info output_path)/_coverage/_coverage_report.dat"
```

The merged report is `$(bazel info output_path)/_coverage/_coverage_report.dat` in lcov format. Run `genhtml` (from the lcov project) at the workspace root, since it reads sources to annotate gaps, then open `genhtml/index.html`. Reports are also produced when some tests fail, but only passing tests contribute.

Language notes from the docs: C++ works out of the box on Linux; on macOS `GCOV_PREFIX_STRIP` is almost certainly wrong by default, so set it, e.g. `bazel coverage //foo:foo_test --test_env=GCOV_PREFIX_STRIP=10`. Java works out of the box (the Bazel toolchains include what remote execution needs, including JUnit). Python needs extra steps from the rules_python coverage docs.

## Checked

2026-11-04. Read against the Bazel docs page(s): Code coverage with Bazel (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the closing Verify line (widen the filter advice was not on the page).
Method: documentation only; no commands were run.
