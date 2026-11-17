---
id: computing-software.devops-ci-cd.renovate.skip-installs-and-ignore-scripts
name: skip-installs-and-ignore-scripts
category: computing-software
field: devops-ci-cd
product: renovate
tags: [ignore-scripts, skip-installs, allow-scripts, renovate]
level: advanced
status: docs-checked
description: "Control package manager scripts during artifact updates with ignoreScripts, allowScripts and skipInstalls."
sources:
  - https://docs.renovatebot.com/configuration-options/
  - https://docs.renovatebot.com/self-hosted-configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

When Renovate updates lock files it runs the package manager, which may execute dependency lifecycle scripts. Two layers control that.

- By default Renovate disables package manager scripts. The `ignoreScripts` option documents the risk: untrusted repository users or malicious package authors could use scripts to exploit the Renovate host or exfiltrate source and secrets. Free Mend-hosted Renovate does not allow script execution.
- `ignoreScripts` defaults to `true` and applies to the `npm`, `bun`, `composer` and `copier` managers.
- The global `allowScripts` option (default `false`) is the administrator's switch for permitting repositories to run install scripts. To run scripts when self-hosting, set `allowScripts` to `true` and set `ignoreScripts` to `false` for the managers you allow.
- `skipInstalls` defaults to using the most efficient approach, which usually avoids a full module install. Setting it to `false` forces a full install. It applies to `npm` only and is for cases where npm bugs produce incorrect lock files.
- `ignorePlugins` (default `false`) and the global `allowPlugins` (default `false`) are the matching options for plugins; `ignorePlugins` is applicable to Composer only for now.

```json
{
  "ignoreScripts": true,
  "skipInstalls": false
}
```

Global:

```json
{
  "allowScripts": false
}
```

Why it matters: per the docs, untrusted or compromised repository users could use package manager scripts to exploit the system where Renovate runs, and malicious package authors could use them to exfiltrate source code and secrets. Enable scripts only for repositories you trust.

## Checked

2026-11-09: read the ignoreScripts, ignorePlugins and skipInstalls sections of https://docs.renovatebot.com/configuration-options/ and allowScripts and allowPlugins in https://docs.renovatebot.com/self-hosted-configuration/. Added defaults and supported managers; removed the unsourced `minimumReleaseAge` advice.

Method: documentation only; no commands were run.
