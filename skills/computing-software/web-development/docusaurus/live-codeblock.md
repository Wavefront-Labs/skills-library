---
id: computing-software.web-development.docusaurus.live-codeblock
name: live-codeblock
category: computing-software
field: web-development
product: docusaurus
tags: [live-codeblock, react-live, reactlivescope, noinline, interactive-editor]
level: practitioner
status: docs-checked
description: "Add interactive React Live code editors with theme-live-codeblock: the live and noInline flags, and exposing extra imports by ejecting ReactLiveScope."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/markdown-features/markdown-features-code-blocks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install and register the theme (powered by React Live):

```sh
npm install --save @docusaurus/theme-live-codeblock
```

```js title="docusaurus.config.js"
themes: ['@docusaurus/theme-live-codeblock'],
```

Add `live` to the language meta string:

````md
```jsx live
function Clock(props) {
  const [date, setDate] = useState(new Date());
  return <h2>It is {date.toLocaleTimeString()}.</h2>;
}
```
````

Imports: you cannot import components in the editor; define what is available upfront. All React imports are available by default. To add more, eject the scope:

```sh
npm run swizzle @docusaurus/theme-live-codeblock ReactLiveScope -- --eject
```

```jsx title="src/theme/ReactLiveScope/index.js"
const ReactLiveScope = {
  React,
  ...React,
  ButtonExample,
};
export default ReactLiveScope;
```

`ButtonExample` can then be used inside live blocks.

`noInline` avoids errors when code spans multiple components or variables. React Live then does not wrap your code in an inline function, so you must call `render()` yourself:

````md
```jsx live noInline
const Greeting = () => <p>Hello!</p>;

render(<Greeting />);
```
````

In JSX, pass `metastring="live"` to `CodeBlock`.

## Checked

2026-11-04. Read in full against the Docusaurus Code blocks page (markdown-features-code-blocks.mdx), Interactive code editor section: theme-live-codeblock install and themes entry, the live flag, no direct imports, ReactLiveScope swizzle with --eject, noInline with explicit render(), and metastring=live for CodeBlock all match. Nothing removed.

Method: documentation only; no commands were run.
