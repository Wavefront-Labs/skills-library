---
id: computing-software.web-development.bun.security-scanner
name: security-scanner
category: computing-software
field: web-development
product: bun
tags: [security-scanner, install-security, advisory-level, supply-chain-scan]
level: advanced
status: docs-checked
description: "Configure and write a Bun security scanner that checks packages at install time: bunfig setting, scanner interface, fatal versus warn levels and scope."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/security-scanner-api.mdx
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/auto-install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Configure in `bunfig.toml`, after `bun add -d <scanner-package>`:

```toml
[install.security]
scanner = "@oven/bun-security-scanner"
```

A scanner module exports `scanner: Bun.Security.Scanner` with `version: "1"` and an async `scan({ packages })` returning advisories (`level`, `package`, `url`, `description`).

```ts
export const scanner: Bun.Security.Scanner = {
  version: "1",
  async scan({ packages }) {
    return packages
      .filter(p => p.name === "event-stream" && Bun.semver.satisfies(p.version, ">=3.3.6 <4.0.0"))
      .map(p => ({ level: "fatal" as const, package: p.name, url: "https://example.com/advisory", description: "compromised" }));
  },
};
```

Levels: `fatal` stops installation with a non-zero exit; `warn` prompts in a terminal and exits immediately in CI.

Gotchas:
- Scanners get transitive dependencies. In a project with a lockfile and a `node_modules` directory, `bun add`/`bun install <pkg>`/`bun update <pkg>` send only the named packages, their dependencies and changed versions; plain `bun install` sends everything.
- Also applies to `bun patch`, `bun link`, `bun dedupe`. Workspace packages are excluded.
- Non-registry versions are not semver, so `Bun.semver.satisfies()` returns false for them.
- Auto-install is disabled when a scanner is configured.

## Checked

2026-11-04. Confirmed against bun docs pm/security-scanner-api.mdx and runtime/auto-install.mdx: bunfig [install.security] scanner, scanner interface and advisory fields, fatal and warn levels, which commands scan and what they send, workspace exclusion, non-semver versions for non-registry sources, auto-install disabled with a scanner. Added the node_modules condition for partial scans.

Method: documentation only; no commands were run.
