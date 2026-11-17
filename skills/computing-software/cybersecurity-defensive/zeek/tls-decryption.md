---
id: computing-software.cybersecurity-defensive.zeek.tls-decryption
name: tls-decryption
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, tls-decryption, sslkeylogfile, tls-keylog, pre-master-secret]
level: advanced
status: docs-checked
description: "Decrypt TLS 1.2 ECDHE-RSA-AES256-GCM traces in Zeek using SSLKEYLOGFILE secrets, converting the keylog to a Zeek tsv, ZEEK_TLS_KEYLOG_FILE and suspend_processing."
sources: ["https://docs.zeek.org/en/current/frameworks/tls-decryption.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tls decryption

Support is limited: only TLS 1.2 with the `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384` cipher can be decrypted. Other versions and ciphers are not decrypted, and there is no plan to extend this. Decrypted data can flow to other analyzers such as HTTP.

Most practical use is a trace captured with key material. Firefox and Chrome write the pre-master secrets when `SSLKEYLOGFILE` is set:

```
export SSLKEYLOGFILE=$HOME/keylogfile.txt
```

Lines look like `CLIENT_RANDOM <client random> <secret>`. Live decryption is possible in principle but needs real-time key transport.

Convert the keylog to a Zeek tsv file with header `#fields client_random secret`, taking the `CLIENT_RANDOM` lines, dropping the first 16 hex characters of the client random (Zeek does not use the first 8 bytes for matching), and writing each hex pair as `\xNN`. The page provides a bash script for this.

Run Zeek with a script that pauses processing until the keylog has loaded:

```
@load protocols/ssl/decryption
@load base/protocols/http

event zeek_init() { suspend_processing(); }

event Input::end_of_data(name: string, source: string)
    {
    if ( name == "tls-keylog-file" )
        continue_processing();
    }
```

```
export ZEEK_TLS_KEYLOG_FILE=~/keylogfile.log
zeek -C -r tls/tls-1.2-stream-keylog.pcap tls_decryption-1-suspend-processing.zeek
```

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
