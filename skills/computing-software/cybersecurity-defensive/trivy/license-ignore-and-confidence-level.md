---
id: computing-software.cybersecurity-defensive.trivy.license-ignore-and-confidence-level
name: license-ignore-and-confidence-level
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [ignored-licenses, license-confidence-level, classifier, spdx, mit, mpl]
level: advanced
status: docs-checked
description: "Remove chosen licenses from results with --ignored-licenses and tune the classifier match threshold with --license-confidence-level."
sources:
  - https://trivy.dev/latest/docs/guide/scanner/license/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two flags tune license scanning output.

`--ignored-licenses` removes licenses identified by name from the results:

```shell
trivy image --scanners license --ignored-licenses MPL-2.0,MIT --severity HIGH grafana/grafana:latest
```

In the documented run the remaining table showed only GPL-2.0 Restricted packages (`alpine-baselayout`, `ssl_client`) with a total of 2 findings at HIGH.

`--license-confidence-level` adjusts the classifier confidence between 0.0 and 1.0, default 0.9. By default Trivy only classifies licenses matched with a confidence of 0.9 or more. Lowering the level lets Trivy classify licenses matched with lower confidence.

The page demonstrates it against the SPDX license list data text. With the default level, full license scanning detects only 258 licenses:

```shell
trivy fs --scanners license --license-full <path/to/spdx/list/data>
```

With the level set to 0.8 it detects 282:

```shell
trivy fs --scanners license --license-full --license-confidence-level 0.8 <path/to/spdx/list/data>
```

The totals reported were 258 (UNKNOWN 70, LOW 90, MEDIUM 18, HIGH 58, CRITICAL 22) and 282 (UNKNOWN 81, LOW 97, MEDIUM 24, HIGH 58, CRITICAL 22). Note that a lower threshold detects more licenses, but the extra detections are matched with less confidence.

## Checked

2026-11-03. Read and confirmed against the License Scanning page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
