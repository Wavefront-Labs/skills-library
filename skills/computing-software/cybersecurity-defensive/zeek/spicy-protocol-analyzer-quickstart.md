---
id: computing-software.cybersecurity-defensive.zeek.spicy-protocol-analyzer-quickstart
name: spicy-protocol-analyzer-quickstart
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, spicy, evt-file, spicyz, protocol-analyzer]
level: advanced
status: docs-checked
description: "Build a minimal Zeek protocol analyzer with Spicy: unit grammar, .evt file, spicyz compile to an HLTO, and a script event handler."
sources: ["https://docs.zeek.org/en/current/advanced/devel/spicy/getting-started.html", "https://docs.zeek.org/en/current/advanced/devel/spicy/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Spicy analyzer quickstart

Spicy is a parser generator producing C++ parsers. Zeek integrates Spicy analyzers as protocol, packet or file analyzers. For a new analyzer, `zkg create` can scaffold it with `--features=spicy-protocol-analyzer`, `spicy-packet-analyzer` or `spicy-file-analyzer`.

Grammar `my-http.spicy` defines a public unit (`RequestLine` with `method`, `uri`, `version`). Control file `my-http.evt`:

```
protocol analyzer spicy::MyHTTP over TCP:
    parse originator with MyHTTP::RequestLine,
    port 12345/tcp;

on MyHTTP::RequestLine -> event MyHTTP::request_line($conn, self.method, self.uri, self.version.number);
```

The first block names the analyzer, its entry unit for originator payload and the port that activates it. The second maps a fully parsed unit to a Zeek event. `$conn` is a magic keyword passing the connection, and `self` is the unit instance. The Zeek side:

```
event MyHTTP::request_line(c: connection, method: string, uri: string, version: string)
    {
    print fmt("Zeek saw from %s: %s %s %s", c$id$orig_h, method, uri, version);
    }
```

Compile and run:

```
spicyz my-http.spicy my-http.evt -o my-http.hlto
zeek -Cr request-line.pcap my-http.hlto my-http.zeek
```

Spicy-side `print` output is suppressed unless you add `Spicy::enable_print=T`. Zeek installs its built-in grammars for reuse; for example Finger is at `<PREFIX>/share/spicy/finger/finger.spicy`, imported with `import Finger from finger;`.

## Checked

2026-11-08. Read the Spicy Getting Started page and the Writing Analyzers with Spicy index page in full; every claim confirmed.

Method: documentation only; no commands were run.
