---
id: computing-software.data-engineering.kestra.script-outputs-and-metrics
name: script-outputs-and-metrics
category: computing-software
field: data-engineering
product: kestra
tags: [outputs, metrics, counter, timer, python-library, shell-markers]
level: practitioner
status: docs-checked
description: "Emit outputs and metrics from Kestra scripts with the Python and Node.js libraries or the ::{}:: shell marker, and the rules for counter and timer metrics."
sources:
  - https://kestra.io/docs/scripts/outputs-metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Kestra scans stdout and stderr for `::{}::` markers holding a JSON payload.

- `outputs` must be a dictionary.
- `metrics` must be a list of dictionaries with mandatory `name`, `type` (`counter` or `timer`) and numeric `value`; `tags` are optional.
- `counter`: Integer or Double, counts rows, bytes. `timer`: Double, seconds.

Python:

```python
from kestra import Kestra

Kestra.outputs({'data': data, 'nr': 42})
Kestra.counter('nr_rows', len(df), tags={'file': filename})
Kestra.timer('ingestion_duration', duration, tags={'file': filename})
```

Node.js: install with `beforeCommands: - npm i @kestra-io/libs`, then `require("@kestra-io/libs")` and call `Kestra.outputs`, `Kestra.counter`, `Kestra.timer`.

Shell:

```shell
echo '::{"outputs":{"test":"value","int":2}}::'
echo '::{"metrics":[{"name":"count","type":"counter","value":1}]}::'
```

Caveats:

- In shell, give the JSON payload without any spaces.
- Metrics take only numbers; use outputs for strings, lists, dictionaries or files.
- Encrypted outputs (`::{"encryptedOutputs":{"key":"value"}}::`) exist only in Enterprise and Cloud.
- Outputs pass data between tasks; metrics track values across executions.

## Checked

2026-11-04. Confirmed against "Track Metadata and Pass Data Between Tasks via Script Outputs" (scripts/outputs-metrics): ::{}:: marker scan of stdout and stderr, outputs as dictionary, metrics list with name, type, value, optional tags, counter and timer types, Python, Node.js and shell examples, no-spaces shell rule, encrypted outputs on Enterprise and Cloud, outputs versus metrics guidance. No claims removed.
Method: documentation only; no commands were run.
