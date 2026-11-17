---
id: computing-software.messaging-and-integration.apache-camel.ftp-component
name: ftp-component
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, component, ftp, sftp, ftps, file-transfer]
level: practitioner
status: docs-checked
description: "Camel ftp, sftp and ftps: URI form and ports, passiveMode and binary defaults, download and localWorkDirectory, fileExist, and differences from the file component."
sources:
  - https://camel.apache.org/components/next/ftp-component.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ftp: / sftp: / ftps:

Form: `ftp://[username@]hostname[:port]/directoryname[?options]`. Ports: FTP 21, SFTP 22, FTPS 2222. The directory must be relative (leading slashes trimmed with a WARN). No username means anonymous login. FTP and FTPS use Apache Commons Net; SFTP uses JSch.

Defaults: `passiveMode` false (try `true` first if nothing downloads), `binary` false (ASCII), `disconnect` false, `stepwise` true, `useList` true (false loses size and timestamp), `connectTimeout` 10000, `soTimeout` 300000, `timeout` 30000, `throwExceptionOnConnectFailed` false, `reconnectDelay` 1000, `autoCreate` true.

Consumer: `download` true (false = null body), `delete` false, `noop` false, `localWorkDirectory` unset (downloads as `.inprogress`, then renames), `streamDownload` false (needs `stepwise=false`), `resumeDownload` false (needs `localWorkDirectory` and `binary=true`), `readLock` none, `readLockCheckInterval` 5000, `readLockTimeout` 20000, `jailStartingDirectory` true.

Producer: `fileExist` `Override` (also Append, Fail, Ignore, Move, TryRename), `tempFileName`/`tempPrefix`, `eagerDeleteTargetFile` true, `allowNullBody` false.

Versus the file component:
- Consumer leaves files untouched (no `.camel` move).
- `markerFile` and `fileLock` read locks are unavailable.
- `move` and `preMove` are restricted to the FTP root folder.
- One consumer endpoint does not support concurrency (client not thread-safe); producers do.

Use TRACE logging to diagnose.

Verify: with `passiveMode=true` a previously empty listing returns files.

## Checked

Method: docs-checked 2026-11-09 against the camel.apache.org ftp-component page (URI format, component and endpoint option tables through the lock options, concurrency, default-when-consuming, limitations, timeouts, local work directory and troubleshooting sections).
