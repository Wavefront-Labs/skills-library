---
id: computing-software.systems-network-administration.keepalived.genhash-digest-workflow
name: genhash-digest-workflow
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, genhash, digest, md5, http-get, real-server]
level: practitioner
status: docs-checked
description: "Workflow to obtain the MD5 digest for an HTTP_GET url block: run genhash -s -p -u against each real server, copy the final MD5 Digest line into keepalived.conf."
sources:
  - https://keepalived.readthedocs.io/en/latest/case_study_healthcheck.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Getting the digest with genhash

Syntax and example from the healthcheck case study:
```
genhash -s <server_ip> -p <port> -u <url_path>
genhash -s 192.168.100.2 -p 80 -u /testurl/test.jsp
```
Output: an HTTP header buffer dump, an HTML body buffer dump, and a final `MD5 Digest` line (the example yields ec90a42b99ea9a2f5ecbe213ac9eba03).

Steps:
1. Run genhash against each real server and each URL you will check.
2. Copy the MD5 digest from the last line.
3. Paste it into the `digest` keyword for that URL.

The case study's own example output is a 401 Unauthorized page.

## Checked

2026-11-04: command form, output sections, example digest and the paste-into-digest step confirmed against the healthcheck case study. Removed an inference about error pages and the Verify line.
Method: documentation only; no commands were run.
