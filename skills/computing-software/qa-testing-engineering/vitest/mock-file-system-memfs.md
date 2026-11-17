---
id: computing-software.qa-testing-engineering.vitest.mock-file-system-memfs
name: mock-file-system-memfs
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [memfs, mock-fs, in-memory-filesystem, mocks-folder-fs]
level: practitioner
status: docs-checked
description: "Isolate file-system code in Vitest tests by redirecting node:fs to memfs through __mocks__ files, resetting the in-memory volume before each test."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/mocking/file-system.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vitest has no built-in file-system mock. Use `memfs`, an in-memory file system.

Create these at the project root so every `fs` call is redirected:

```js
// __mocks__/fs.cjs
const { fs } = require('memfs')
module.exports = fs
```

```js
// __mocks__/fs/promises.cjs
const { fs } = require('memfs')
module.exports = fs.promises
```

Then in a test:

```ts
import { beforeEach, expect, it, vi } from 'vitest'
import { fs, vol } from 'memfs'
import { readHelloWorld } from './read-hello-world.js'

vi.mock('node:fs')
vi.mock('node:fs/promises')

beforeEach(() => { vol.reset() })

it('reads text', () => {
  fs.writeFileSync('/hello-world.txt', 'hello world')
  expect(readHelloWorld('/hello-world.txt')).toBe('hello world')
})
```

- `vol.fromJSON({ './dir/a.txt': 'x' }, '/base')` creates several files at once.
- Call the two `vi.mock` lines in a setup file if fs should always be mocked.
- With `import` in a mock file, every export must be defined explicitly; `require` avoids that.

## Checked

2026-11-04. Confirmed against guide/mocking/file-system.md: no built-in file-system mocking, memfs recommendation, both __mocks__ files and their contents, the vi.mock lines (which can go in a setup file), vol.reset() in beforeEach, vol.fromJSON with a base directory, and the note that `import` in a mock file needs every export defined. Removed: a generic gotcha line the page does not state.

Method: documentation only; no commands were run.
