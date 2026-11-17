---
id: computing-software.web-development.astro.server-islands-defer
name: server-islands-defer
category: computing-software
field: web-development
product: astro
tags: [server-islands, server-defer, fallback-slot, serializable-props]
level: practitioner
status: docs-checked
description: "Defer personalized components with server:defer, add fallback slot content, and respect the serializable-props rule for server islands."
sources:
  - https://raw.githubusercontent.com/withastro/docs/main/src/content/docs/en/guides/server-islands.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A server island is a server-rendered Astro component told to delay rendering. The page renders immediately with fallback content; the component's content is fetched on the client when available. An adapter is required. Add `server:defer`:

```astro title="src/pages/index.astro"
---
import Avatar from '../components/Avatar.astro';
---
<Avatar server:defer />
```

The component can do anything an on-demand page can, e.g. read cookies:

```astro title="src/components/Avatar.astro"
---
import { getUserAvatar } from '../sessions';
const userSession = Astro.cookies.get('session');
const avatarURL = await getUserAvatar(userSession);
---
<img alt="User avatar" src={avatarURL} />
```

Fallback via the named `"fallback"` slot (generic avatar, placeholder, spinner):

```astro
<Avatar server:defer>
  <GenericAvatar slot="fallback" />
</Avatar>
```

Props must be serializable. Functions and objects with circular references cannot be passed. Supported: plain object, `number`, `string`, `Array`, `Map`, `Set`, `RegExp`, `Date`, `BigInt`, `URL`, `Uint8Array`, `Uint16Array`, `Uint32Array`, and `Infinity`.

How it works: at build time each island is split into its own route and replaced by a small script plus the fallback; the browser requests it from a special endpoint. Islands load independently, and the pattern does not depend on server infrastructure.

## Checked

2026-11-04. Confirmed against the Astro server islands guide: server:defer with an adapter, cookies example, fallback slot, serializable prop types and exclusions, how it works. Nothing removed.

Method: documentation only; no commands were run.
