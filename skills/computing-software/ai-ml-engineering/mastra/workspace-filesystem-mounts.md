---
id: computing-software.ai-ml-engineering.mastra.workspace-filesystem-mounts
name: workspace-filesystem-mounts
category: computing-software
field: ai-ml-engineering
product: mastra
tags: [mastra, workspace, filesystem, mounts, sandbox, composite-filesystem, s3, fuse]
level: advanced
status: docs-checked
description: "Configure a Mastra Workspace filesystem or path-prefixed mounts, composite routing, per-user resolvers, read-only mode and containment for agent file tools."
sources:
  - https://mastra.ai/docs/sandbox/filesystem
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: give a Mastra agent file tools (and optionally sandbox command access) to local or remote storage, with correct policies.

## Pick one: `filesystem` or `mounts`
Configure either, never both: both throws a `WorkspaceError` with code `INVALID_CONFIG`.

- `filesystem`: one provider, a resolver, or a `CompositeFilesystem` you built yourself.
- `mounts`: path-prefixed providers; Mastra builds the `CompositeFilesystem` and, when sandbox and provider support it, mounts them in the sandbox automatically.

## File tools the agent gets
`mastra_workspace_read_file`, `write_file`, `edit_file`, `list_files`, `delete`, `file_stat`, `mkdir`, `grep`; `ast_edit` when `@ast-grep/napi` is installed; `apply_patch` is off by default.

Enable `apply_patch` with its own entry (top-level `tools.enabled` does not turn it on):

```typescript
import { Workspace, LocalFilesystem, WORKSPACE_TOOLS } from '@mastra/core/workspace'

export const workspace = new Workspace({
  filesystem: new LocalFilesystem({ basePath: './workspace' }),
  tools: {
    [WORKSPACE_TOOLS.FILESYSTEM.APPLY_PATCH]: { enabled: true },
  },
})
```

## Direct access
```typescript
const workspace = new Workspace({
  filesystem: new LocalFilesystem({ basePath: './knowledge-base' }),
})
```
Paths resolve under `basePath`; no sandbox is needed.

## Mounts
```typescript
import { S3Filesystem } from '@mastra/s3'
import { DaytonaSandbox } from '@mastra/daytona'

const workspace = new Workspace({
  mounts: {
    '/workspace': new S3Filesystem({ bucket: process.env.S3_BUCKET!, region: 'us-east-1' }),
  },
  sandbox: new DaytonaSandbox(),
})
```
Files written via file tools or commands are saved by the provider and survive sandbox stop. Mounts suit programs that need a directory tree or large/binary files.

- Composite routing strips the mount prefix before calling the provider. Mount paths cannot be nested (`/data` and `/data/archive` together are invalid).
- `mounts` without a sandbox works: file tools only, no command tools.
- `new CompositeFilesystem({ mounts: {...} })` passed via `filesystem` gives routing without automatic sandbox mount wiring.
- `LocalSandbox` makes a symlink inside its `workingDirectory` (a `/workspace` mount becomes `<workingDirectory>/workspace`).

## Mount availability
Remote mounts use FUSE. Built in: `LocalSandbox` + `LocalFilesystem`; E2B and Daytona + S3/GCS/Azure Blob; Blaxel + S3/GCS. May need `s3fs`, `gcsfuse` or `blobfuse2` in the sandbox. Other combos need an `onMount` hook. If a mount fails, file tools still work but commands cannot see the path.

## Per user or thread
`filesystem` accepts a resolver:
```typescript
filesystem: ({ requestContext }) => {
  const userId = requestContext.get('user-id') as string
  return new S3Filesystem({ bucket: process.env.S3_BUCKET!, region: process.env.S3_REGION!, prefix: `users/${userId}` })
}
```
`mounts` takes no resolver and cannot combine with a sandbox resolver; mount inside the sandbox resolver instead.

## Policies and containment
- Configure per tool via `WORKSPACE_TOOLS.FILESYSTEM.*` constants (approval, read-before-write, output limits).
- `LocalFilesystem` is contained to `basePath`; use `allowedPaths: ['../shared-policies']` for extra directories. Containment covers file tools and search indexing, not shell commands. In composites keep `contained: true` unless unrestricted host access is intended.
- `readOnly: true` removes write tools for a static provider; with a resolver the tools stay registered and the provider rejects writes at runtime.

## Gotchas
File-tool and command-tool policies are independent: requiring approval for `write_file` does not stop `execute_command` writing the same mounted path. To restrict to file tools, disable sandbox command tools.

## Checked
Method: 2026-11-08 read the Mastra sandbox/filesystem docs page in full (served as markdown). Tool list, filesystem-versus-mounts rule, composite routing, mount availability table, resolver limits and containment/readOnly claims match the page; no content changed.
