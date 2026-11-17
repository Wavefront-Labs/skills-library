---
id: computing-software.software-engineering.mobile-development.react-native-web-and-multiplatform-code
name: react-native-web-and-multiplatform-code
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, react-native-web, multi-platform, web-compatibility, appregistry, web-rendering, platform-agnostic, expo-web, shared-components, dom-rendering, responsive, cross-platform-ui]
level: practitioner
status: docs-checked
description: "Render React Native components in the browser with react-native-web: what it is, installation, the Babel plugin, aliasing, platform-specific files, and Platform.OS."
sources: ["https://necolas.github.io/react-native-web/", "https://necolas.github.io/react-native-web/docs/", "https://necolas.github.io/react-native-web/docs/installation/", "https://necolas.github.io/react-native-web/docs/multi-platform/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# react-native-web: React Native components on the web

**Goal:** run a React Native component tree in the browser, so one codebase serves mobile and web
without a parallel web app drifting behind it.

React Native for Web is "a compatibility layer between React DOM and React Native". It uses React DOM to render React
Native compatible JavaScript in a browser, makes direct use of DOM APIs where useful, and can be adopted in new or
existing, web-only or multi-platform apps. Its stated strengths:
- Accessible HTML: supports different devices and input modes and renders semantic tags.
- High-quality interactions: gestures and multiple input modes (touch, mouse, keyboard); core components carry the
  responder system props.
- Reliable styles: styles are authored in JavaScript, converted to CSS, scoped and automatically vendor-prefixed, with
  RTL layout support.
- Responsive containers that respond to element resize events.
- Incremental adoption: interoperates with existing React DOM components, and you bundle only what you use.

It powers web support in Expo, React Native Elements, React Native Paper and NativeBase.

## Install
```
npm install react-dom react-native-web
npm install --save-dev babel-plugin-react-native-web
```
The Babel plugin is recommended for build-time optimisation. React Native's Babel preset rewrites ES modules to
CommonJS, which prevents bundlers tree-shaking unused modules; the plugin rewrites imports so only used modules are
bundled.

Quickstarts: Expo (uses React Native for Web, with web build optimisations), or Create React App, which has built-in
aliasing of `react-native-web` to `react-native`; the docs recommend Expo. For a multi-platform app the docs strongly
recommend Expo, which includes web support and the configuration work.

## Custom bundler setup (webpack example)
- Alias the exact import: `resolve.alias: { 'react-native$': 'react-native-web' }`.
- Put web-specific files first in resolution: `resolve.extensions: ['.web.js', '.js']`.
- Compile uncompiled React Native ecosystem packages with `babel-loader` by adding their directories to `include`, with
  the `module:@react-native/babel-preset` preset and the `react-native-web` plugin.
- Metro is React Native's bundler, with undocumented web support.

## Web-specific code
- Minor differences: `Platform.OS === 'web'` from `react-native`, for example
  `height: Platform.OS === 'web' ? 200 : 100` in a `StyleSheet`.
- Larger differences: platform-specific files such as `MyComponent.android.js`, `MyComponent.ios.js` and
  `MyComponent.web.js`; `import MyComponent from './MyComponent'` resolves the right variant per target (the web
  variant needs the `.web.js` extension in the bundler config).
- Third-party React Native packages with web support are listed in the React Native Directory.

## Verify
- [ ] The resolve alias (or Expo web support) is configured and `Platform.OS` reports `'web'`.
- [ ] The Babel plugin is installed so only used modules are bundled.
- [ ] Each native-only dependency has a web variant or a platform guard.
- [ ] The same component renders and behaves on iOS, Android and web for the flows you support.

## Checked
2026-11-08. Confirmed against the four cited React Native for Web pages (home, Introduction, Installation, Multi-platform setup): compatibility-layer description, feature list, install commands, Babel plugin purpose, Expo and Create React App notes, webpack alias and extensions, `Platform.OS` and platform-specific file examples. Removed: the component and API lists, the `AppRegistry` runApplication snippet, the Unstable APIs and compatibility-page claims, and the failure-mode and native-module paragraphs (those pages are not among the cited ones and were not read).
Method: documentation only; no commands were run.
