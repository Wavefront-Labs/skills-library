---
id: computing-software.devops-ci-cd.helm.chart-tests
name: chart-tests
category: computing-software
field: devops-ci-cd
product: helm
tags: [chart-tests, helm-test, test-hook, logs, filter, pod, smoke-test]
level: practitioner
status: docs-checked
description: "Write chart tests as Pods with the helm.sh/hook: test annotation under templates/tests and run them with helm test."
sources:
  - "https://helm.sh/docs/topics/chart_tests/"
  - "https://helm.sh/docs/helm/helm_test/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A chart test is a Job or Pod resource in `templates/` that exits with code 0 on success, carrying the hook annotation `helm.sh/hook: test`. Place tests under `templates/tests/` so they are easy to find; `helm create` makes `templates/tests/test-connection.yaml`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ .Release.Name }}-credentials-test"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: main
      image: busybox
      command: ["sh", "-c", "exit 0"]
  restartPolicy: Never
```

Run tests against an installed release:

```bash
helm test RELEASE
helm test RELEASE --logs --filter name=my-test
```

- `--logs` prints test pod logs.
- `--filter` selects tests by `name=`, `!name=` and similar.
- `--timeout` is the time to wait for any individual Kubernetes operation (default 5m0s).
- `--hide-notes` hides the notes in the test output.

You can define as many tests as you like in one YAML file or several files under `templates/`. A test is a Helm hook, so `helm.sh/hook-weight` and `helm.sh/hook-delete-policy` annotations apply. Before Helm 3 the annotations were `test-success` or `test-failure`; `helm.sh/hook: test-success` is still accepted as an alternative to `test`.

If you run `helm test` immediately after install, pods may not be active yet and the test can fail transiently; re-test.

Typical test content: validate that values were injected, that credentials work (and wrong ones do not), and that services are up and load balancing.

## Checked

2026-11-08. Read the Chart Tests page and helm test page in full. Removed unsupported claims (pass criteria, weight-order run, default pod retention) and corrected --timeout wording; added test-success compatibility, hook annotations and transient-failure note.

Method: documentation only; no commands were run.
