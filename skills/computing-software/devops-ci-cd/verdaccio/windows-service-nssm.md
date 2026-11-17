---
id: computing-software.devops-ci-cd.verdaccio.windows-service-nssm
name: windows-service-nssm
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [windows-service, nssm, winsw, iisnode, windows-install]
level: advanced
status: docs-checked
description: "Run Verdaccio as a Windows service with NSSM (or WinSW), and the community IIS iisnode route with its caveats."
sources:
  - https://verdaccio.org/docs/windows/
  - https://verdaccio.org/docs/iss-server/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install locally, not globally (the author hit npm issues with global installs):
```
mkdir <install-dir>
cd <install-dir>
npm install verdaccio
```
Create `config.yaml` in that folder.

NSSM:
1. Download NSSM, extract, add its folder to PATH.
2. In an administrator prompt: `nssm install verdaccio`.
3. Fill the Application tab: Path `node`; Startup directory `<install-dir>`; Arguments `<install-dir>\node_modules\verdaccio\build\lib\cli.js -c <install-dir>\config.yaml`.
4. Click Install service, then `sc start verdaccio`.

WinSW is the alternative: rename the executable to `verdaccio-winsw.exe`, add `verdaccio-winsw.xml` that runs `node` with the arguments `<install-dir>\node_modules\verdaccio\src\lib\cli.js -c <install-dir>\config.yaml` (the page uses the src path here, unlike the build path in the NSSM steps), then `verdaccio-winsw.exe install` and `start`. The page warns the WinSW download was missing at one point, so prefer NSSM; the page also says `workingdirectory` appears to be ignored.

IIS: the iisnode guide targets Windows Server 2016, Node.js 10 and Verdaccio 3.11. It is not revalidated for supported versions (6.x needs Node.js 22+). Prefer a Windows service, or a reverse proxy in front. If the UI breaks over https under iisnode, set `<iisnode enableXFF="true" />`.

## Checked

Confirmed against the Windows service and IIS pages: local install, config.yaml location, the NSSM steps and field values, sc start verdaccio, WinSW rename and install and start commands, the missing WinSW download note, workingdirectory appearing ignored, the IIS caveats (Windows Server 2016, Node.js 10, Verdaccio 3.11, 6.x needing Node.js 22+) and the enableXFF fix. Corrected the WinSW cli.js path to the src path the page gives, and removed the sc query verification line, which the pages do not state.

Method: docs-checked 2026-11-09 against website/docs/windows.md and website/docs/iis-server.md in verdaccio/website (sources of verdaccio.org/docs/windows/ and /iss-server/), read in full.
