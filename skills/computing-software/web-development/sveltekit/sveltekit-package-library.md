---
id: computing-software.web-development.sveltekit.sveltekit-package-library
name: sveltekit-package-library
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, packaging, svelte-package, exports, npm, typescript, library]
level: advanced
status: docs-checked
description: "Package a Svelte component library with svelte-package: configure package.json exports, sideEffects, types resolution, source maps, options and publishing."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/70-packaging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packaging a SvelteKit library

Goal: publish `src/lib` as an npm package using `@sveltejs/package` (`npx sv create` can scaffold it).

In a library, `src/lib` is the public surface and the root `package.json` is the one published; `src/routes` is a demo or sandbox. `svelte-package` turns `src/lib` into `dist`: Svelte components are preprocessed, TypeScript transpiled, `d.ts` files generated next to implementations (needs `typescript >= 4.0.0`), hand-written `d.ts` copied as-is. Version 1 generated a `package.json`; now it validates yours.

## package.json fields

```json
{
	"name": "your-library",
	"license": "MIT",
	"files": ["dist"],
	"exports": {
		".": {
			"types": "./dist/index.d.ts",
			"svelte": "./dist/index.js"
		}
	},
	"svelte": "./dist/index.js",
	"sideEffects": ["**/*.css"]
}
```

- `files`: what npm uploads. Add `.npmignore` to exclude tests and modules only used by `src/routes`. Include a `LICENSE` file.
- `exports`: omit `types` if you ship no definitions. For a library with no Svelte components usable outside Svelte, replace `svelte` with `default`. Extra entries look like `"./Foo.svelte": { "types": "./dist/Foo.svelte.d.ts", "svelte": "./dist/Foo.svelte" }`.
- `svelte`: legacy field for old tooling; point it at the root entry.
- `sideEffects`: lets bundlers tree-shake. Newly created projects mark all scripts side-effect free, so list any file that does have side effects (e.g. `"./dist/sideEffectfulFile.js"`) or functionality can break.

## Types for non-root exports

TypeScript does not resolve `types` for `./foo` by default. Either require consumers to set `moduleResolution` to `bundler`, `node16` or `nodenext`, or add `typesVersions`:

```json
"typesVersions": {
	">4.0": {
		"foo": ["./dist/foo.d.ts"]
	}
}
```

If you use `typesVersions` you must declare all type imports through it, including the root (`"index.d.ts": [..]`).

## Best practices

- Avoid SvelteKit-specific modules like `$app/env` unless the library is SvelteKit-only; use `BROWSER` from `esm-env` instead, and pass URLs/navigation as props.
- Use subpath imports (`#` entries in `imports`); `svelte-package` rewrites them to relative paths.
- Removing paths or export conditions from `exports` (including changing `svelte` to `default`) is a breaking change; adding entries is fine.
- Declaration maps: set `"declarationMap": true` in tsconfig and publish `src/lib` in `files` (excluding tests) so editors can jump to source.

## CLI options

`-w/--watch`, `-i/--input` (default `src/lib`), `-o/--output` (default `dist`), `-p/--preserve-output` (default false: output is emptied first), `-t/--types` (default true), `--tsconfig`. Publish with `npm publish`.

## Caveat

Relative imports must be fully specified per Node ESM: `./something/index.js`. For TypeScript files import with a `.js` ending, not `.ts`; `"moduleResolution": "NodeNext"` helps. Other files are copied as-is.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 30-advanced/70-packaging.md in full: package.json fields, exports, sideEffects, TypeScript resolution, typesVersions, esm-env, subpath imports, svelte-package options and defaults, publishing. No claims trimmed.
