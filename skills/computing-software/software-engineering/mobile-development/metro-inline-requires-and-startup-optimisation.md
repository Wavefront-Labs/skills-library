---
id: computing-software.software-engineering.mobile-development.metro-inline-requires-and-startup-optimisation
name: metro-inline-requires-and-startup-optimisation
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, metro, inline-requires, ram-bundles, hermes, bytecode, js-loading, startup-time, cold-start, require-in-the-middle, transform-options, bundle-optimisation, lazy-loading, app-performance]
level: advanced
status: docs-checked
description: "Cut React Native startup time by deferring module evaluation: inline requires, blockList, require-in-the-middle, and why RAM bundles are not supported under Hermes."
sources: ["https://reactnative.dev/docs/optimizing-javascript-loading", "https://reactnative.dev/docs/hermes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Metro inline requires and startup optimisation

**Goal:** reduce how much JavaScript is parsed, evaluated and held in memory during app startup, by
deferring module evaluation until a module is actually used.

The docs' premise: "Parsing and running JavaScript code requires memory and time", so as an app
grows it is often useful to delay loading code until it is needed for the first time. The docs also
recommend using Hermes and lazy-loading large components (typically screen-level components) with
React's `lazy` API before the advanced techniques below.

## Inline requires
**With the React Native CLI**, `require()` calls (not `import`s) are inlined **automatically** -
both in your code and inside third-party packages in `node_modules`. A top-level `require` is then
evaluated lazily as part of the component that uses it.

**With Expo, inlining is off by default.** Turn it on in Metro config:

```js
// metro.config.js
module.exports = {
  transformer: {
    async getTransformOptions() {
      return {
        transform: {
          inlineRequires: true,
        },
      };
    },
  },
};
```

Only `require` calls are inlined, not `import` statements.

### Excluding modules
```js
transform: {
  inlineRequires: {
    blockList: {
      // require() calls in this file are not inlined
      [require.resolve('./src/DoNotInlineHere.js')]: true,
    },
  },
  // require('react') is never inlined anywhere
  nonInlinedRequires: ['react'],
},
```

Setting `inlineRequires: false` in `getTransformOptions` disables all automatic inlining. The docs
point to Metro's `getTransformOptions` documentation for further tuning (that page was not
readable when this skill was checked).

## The side-effect hazard
Inlining **changes the order in which modules evaluate, and some may never evaluate at all**. A
side-effect-free module is safe. A module that patches a global, initialises logging or registers
listeners at its top level may now run late, in a different order, or never - producing bugs that
look nothing like a bundler problem.

The docs' examples of side effects: initialising a logging mechanism (`global.logger = new
Logger()`) or patching a global API used by the rest of your code. Exclude such modules with
`blockList` or `nonInlinedRequires`, or disable inlining entirely.

## The require-in-the-middle pattern (manual)
Defer a module without `React.lazy` or dynamic `import()`:

```tsx
let VeryExpensive: typeof import('./VeryExpensive').default | null = null;

export default function Optimize() {
  const [needs, setNeeds] = useState(false);
  const didPress = useCallback(() => {
    if (VeryExpensive == null) {
      VeryExpensive = require('./VeryExpensive').default;
    }
    setNeeds(true);
  }, []);
  return (
    <>
      <TouchableOpacity onPress={didPress}><Text>Load</Text></TouchableOpacity>
      {needs ? <VeryExpensive /> : null}
    </>
  );
}
```
The moving parts in the docs' example: a module-level `let`, a null check, and the `require()`
inside the handler. The docs introduce it as a way to defer loading code without `lazy` or an
asynchronous `import()`.

## Hermes
Hermes is the default engine for new React Native apps and is "highly optimized for efficient code
loading": **in release builds JavaScript is fully compiled to bytecode ahead of time**, and bytecode
is loaded to memory on demand and does not need to be parsed. The Hermes page says you can confirm
use with `!!global.HermesInternal`, and warns that with a non-standard way of loading the bundle
you may not be using the pre-compiled `.hbc` bytecode.

## RAM bundles - non-Hermes only
RAM bundles store each module as a separate string or file that is only parsed when the module needs
to be executed, either as split files or in the indexed format (a lookup table in a single file).

**"Hermes bytecode is not compatible with the RAM bundle format, and provides the same (or better)
performance in all use cases."** The docs mark them as not supported with Hermes, so use them
only on a non-Hermes app:
- Android: `project.ext.react = [ bundleCommand: "ram-bundle" ]` in `app/build.gradle` (before
  `react.gradle` is applied); add `extraPackagerArgs: ["--indexed-ram-bundle"]` for the single-file
  form.
- iOS: RAM bundles are always indexed; add `export BUNDLE_COMMAND="ram-bundle"` in the "Bundle
  React Native code and images" build phase, before `react-native-xcode.sh`.

## Verify
- [ ] `inlineRequires: true` in `getTransformOptions` (Expo), or confirmed automatic inlining
      (CLI), and the app still boots with modules that have top-level side effects accounted for.
- [ ] Startup measured before and after on a release build on a low-end device (the Hermes page
      advises comparing release builds).
- [ ] No module relied on for first paint is lazily required.
- [ ] If RAM bundles were configured previously, either the app is not on Hermes, or the config
      was removed.
- [ ] A deliberate `blockList` entry demonstrably keeps a side-effectful module eager.

## Checked
2026-11-08. Confirmed against the reactnative.dev Optimizing JavaScript loading and Using Hermes
pages (last updated 2026-10-27): Hermes bytecode behaviour, inline-require behaviour for CLI and
Expo, the `getTransformOptions` examples including `blockList` and `nonInlinedRequires`, pitfalls,
the require-in-the-middle example, and the RAM bundle Android and iOS instructions and Hermes
incompatibility. Removed: claims about hundreds of startup modules and the single biggest lever,
polyfill examples, the claim that the null guard prevents re-evaluation, and the "older advice"
remark. Dropped the Metro configuration source (404).
Method: documentation only; no commands were run.
