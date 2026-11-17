---
id: computing-software.software-engineering.clojure.nrepl-and-editor-integration-cider-calva
name: nrepl-and-editor-integration-cider-calva
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, nrepl, cider, calva, cursive, conjure, editor-integration, middleware, clojure-main, repl-nrepl-editors]
level: practitioner
status: docs-checked
description: "Connect editors to a running Clojure process with nREPL (CIDER, Calva, Cursive, Conjure): start a server, .nrepl-port, middleware, transports, security, clojure.main."
sources: ["https://nrepl.org", "https://clojure.org/reference/repl_and_main"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nREPL and editor integration

**Goal:** evaluate code from the editor in a live process.

## Start a server
```bash
clj -Sdeps '{:deps {nrepl/nrepl {:mvn/version "<current>"}}}' -M -m nrepl.cmdline
lein repl
bb nrepl-server
```
- nREPL is a network REPL server evaluating code in a running program; values, output and errors come back as
  separate messages, each request ending with a `done` status. CIDER, Calva, Cursive and Conjure build on it.
- The server prints its address and writes its port to `.nrepl-port`, which is how editors find it. The
  nrepl.org page does not state a default port number.
- Sessions keep state such as the current namespace and `*print-length*` (`clone` creates one). `interrupt`
  stops a running evaluation without dropping the session; on Java 21+ this needs
  `-Djdk.attach.allowAttachSelf`. Built-in ops include `completions`, `lookup` and `describe`.
- Every op is implemented by middleware; tools add ops (cider-nrepl adds many; Piggieback adds ClojureScript).
- Transports: bencode (default, supported by all servers), EDN (Clojure clients), TTY (plain connections like
  telnet).

## Security
- Anyone who can connect can run any code: treat the port "like a shell". The server listens only on localhost
  by default. For remote access use TLS with mutual authentication or an SSH tunnel.

## clojure.main (REPL and scripts)
- `clj` launches a REPL via `clojure.main`. Init options (`-i`, `-e`, `--report`) come before main options
  (`-r`, a script path, `-`, `-m ns`, `-h`). `user.clj` on the classpath is loaded at startup (dev-time
  facility, not recommended in production).
- REPL vars: `*1`, `*2`, `*3` (last three results) and `*e` (most recent exception).
- Run a script: `clj -M /path/to/myscript.clj`; arguments land in `*command-line-args*`.

## Self-check
Start a headless nREPL, connect your editor, evaluate `(+ 1 1)`, and check the port is bound to localhost.

## Checked
Method: 2026-11-08 read nrepl.org and clojure.org/reference/repl_and_main. Removed unsupported claims: socket REPL and prepl guidance, editor-specific connect commands (jack-in etc.), `lein repl :headless :port`, the `--port` flag, and the failure modes. Unchanged: the self-check.
