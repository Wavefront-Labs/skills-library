---
id: computing-software.cloud-infrastructure-engineering.graylog.input-tls-enable
name: input-tls-enable
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [input-tls, enable-tls, certificate-key, secure-inputs]
level: practitioner
status: docs-checked
description: "Enable TLS on a Graylog input by uploading a certificate and key to the server and ticking Enable TLS."
sources:
  - https://go2docs.graylog.org/current/getting_in_log_data/secure_inputs_with_tls.htm
  - https://go2docs.graylog.org/current/getting_in_log_data/inputs.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# input tls enable

1. Obtain a certificate and private key, from a service or your own CA.
2. Upload both files to the Graylog server filesystem and note the paths (many use `/etc/graylog/server/`).
3. In **System > Inputs**, launch a new input or edit an existing one.
4. Fill in the certificate and key fields and select **Enable TLS**.
5. Select Launch Input (new) or Update input (existing) to apply.

Not every input supports TLS: check the table on the Inputs page (GELF supports TLS on HTTP and TCP only, CEF on TCP only, IPFIX none). An expired or invalid certificate stops the input from starting; the Input Diagnosis page shows this.

## Checked

2026-11-04. Confirmed against the cited page. Nothing removed.

Method: documentation only; no commands were run.
