---
id: computing-software.cryptography-implementation.protocol-implementation.sslyze-tls-scans-in-ci
name: sslyze-tls-scans-in-ci
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, sslyze, tls-scanning, protocol-conformance, mozilla-tls, ci, tls-configuration, compliance]
level: practitioner
status: docs-checked
description: "Run SSLyze against TLS endpoints in CI: Mozilla config compliance checks via exit code, custom TLS config files, the Python API for custom gates and deploy gating."
sources: ["https://github.com/nabla-c0d3/sslyze", "https://raw.githubusercontent.com/nabla-c0d3/sslyze/release/README.md", "https://nabla-c0d3.github.io/sslyze/documentation/running-a-scan-in-python.html", "https://nabla-c0d3.github.io/sslyze/documentation/available-scan-commands.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSLyze TLS scans in CI

## Install and run
```
pip install --upgrade sslyze
python -m sslyze example.com api.example.com
echo $?            # non-zero if a server is not compliant with the chosen Mozilla configuration
python -m sslyze --mozilla_config=modern example.com
python -m sslyze --custom_tls_config custom_tls_config_example.json example.com
```
By default SSLyze checks results against Mozilla's "intermediate" TLS configuration and exits non-zero when the server
is not compliant. `--mozilla_config` takes `old`, `intermediate` or `modern`; `--custom_tls_config` takes your own JSON
file in Mozilla's TLS configuration format (the repository ships `custom_tls_config_example.json`). The failure output
lists the deviations (certificate types, certificate signatures, TLS versions, cipher suites). Run
`python -m sslyze --help` for the other scan options; they differ between releases.

SSLyze also scans non-HTTP servers (SMTP, XMPP, LDAP, POP, IMAP, RDP, Postgres, FTP).

## Python API (custom gates)
```python
from sslyze import Scanner, ServerScanRequest, ServerNetworkLocation, ScanCommand
req = ServerScanRequest(server_location=ServerNetworkLocation("example.com", 443),
                        scan_commands={ScanCommand.TLS_1_0_CIPHER_SUITES, ScanCommand.CERTIFICATE_INFO})
scanner = Scanner(); scanner.queue_scans([req])
for result in scanner.get_results():
    tls10 = result.scan_result.tls_1_0_cipher_suites.result
    assert not tls10.accepted_cipher_suites, "TLS 1.0 still enabled"
```
Other scan commands include `ELLIPTIC_CURVES`, `HEARTBLEED`, `ROBOT` and `OPENSSL_CCS_INJECTION`. Check
`result.scan_status` first: an unreachable server has no `scan_result`.

## CI pattern
- Scan staging after each deploy of edge/proxy config; fail the pipeline on non-compliance.
- Scan production nightly; alert on drift and on certificate expiry under a threshold.
- Pin the SSLyze version: Mozilla profile definitions and CLI options change between releases.

## Verify
- [ ] Pipeline fails when TLS 1.0 is re-enabled in staging.
- [ ] Nightly report archived for audit evidence.

## Checked

2026-10-31. Confirmed in the SSLyze README (pip install; `python -m sslyze`; default "intermediate" check with non-zero
exit; `--mozilla_config={old, intermediate, modern}`; `--custom_tls_config`; non-HTTP protocols listed) and the
documentation pages on running a scan in Python (`ServerScanRequest`, `ServerNetworkLocation`, `Scanner.queue_scans`,
`get_results`, `scan_result.<command>.result`) and available scan commands (`TLS_1_0_CIPHER_SUITES`,
`CERTIFICATE_INFO`, `ELLIPTIC_CURVES`, `HEARTBLEED`, `ROBOT`, `OPENSSL_CCS_INJECTION`, `accepted_cipher_suites`).
Removed (CLI option reference not readable): `--json_out`, `--certinfo`, `--tlsv1_2`, `--tlsv1_3`, `--elliptic_curves`,
`--heartbleed`, `--robot`, `--openssl_ccs`, `--starttls`, `--sni`, the profile-coverage list (curves, key size,
lifetime, HSTS), and the Mozilla wiki source (script stub).
Method: documentation only; no commands were run.
