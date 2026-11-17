---
id: computing-software.software-engineering.mobile-development.react-native-svg-components-and-usage
name: react-native-svg-components-and-usage
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, react-native-svg, svg, vector-graphics, svgxml, svguri, gradients, svg-transformer, metro-transformer, icons, current-color, filters]
level: practitioner
status: docs-checked
description: "Render vector graphics with react-native-svg: common props, gradients and masks in Defs, SvgXml/SvgUri error handling, Metro transformer for .svg, filters."
sources: ["https://github.com/software-mansion/react-native-svg", "https://github.com/software-mansion/react-native-svg/blob/main/USAGE.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# react-native-svg: vector graphics

**Goal:** draw resolution-independent graphics in React Native (icons, illustrations, charts) with the
SVG element set, and load existing `.svg` assets without hand-porting them.

## Install and versions
- Expo: `npx expo install react-native-svg` (the Expo client already has the native code).
- Bare React Native: `npm install react-native-svg`, then `cd ios && pod install`.
- Pairing with React Native: >=15.0.0 needs RN >=0.70, >=15.8.0 needs >=0.73, >=15.13.0 needs >=0.78,
  >=15.16.0 needs >=0.80. Fabric is supported from 13.0.0 and only for RN 0.69+.

## Common props and theming
- Fill and stroke props on shapes: `fill`, `fillOpacity`, `fillRule`, `stroke`, `strokeWidth`,
  `strokeOpacity`, `strokeLinecap`, `strokeLinejoin`, `strokeDasharray`, `strokeDashoffset`.
- Placement props: `x`, `y` (translate), `rotation`, `scale`, `origin`, `originX`, `originY`.
  Example: `<G rotation="50" origin="100, 50">`.
- The `color` prop on `Svg` colours nothing by itself; it defines a colour variable that children
  reference with `currentColor`, for example `<Path stroke="currentColor" />`. It works in any prop that
  accepts a colour.

## Defs, gradients, masks, reuse
- `Defs` holds shapes that are invisible until referenced. Gradients, masks and patterns are defined
  there and referenced with `fill="url(#id)"`.
- `gradientUnits="userSpaceOnUse"` (likewise `maskUnits`, `patternUnits`) changes the coordinate system.
- `LinearGradient` also accepts percentages, but the docs recommend exact numbers for performance.
- `Use` references a shape by `href="#id"`: the shape needs an `id` set, and note the `#` prefix.
- v10 added experimental support for masks with native elements; native elements inside an `Svg` root
  may now render transforms and masks differently after upgrading.

## Loading SVG
- `SvgXml` renders an XML string; `SvgUri` loads a remote URL. When the SVG contains `<style>` CSS use
  `SvgCss` or `SvgCssUri` from `react-native-svg/css`.
- `SvgUri` and `SvgCssUri` log errors to the console and otherwise ignore them. Set `onError` to
  handle failures such as a missing resource, and `fallback` to render another component instead.
- For `.svg` files the docs suggest `react-native-svg-transformer` for compile-time conversion and
  cached transforms. Metro config: set `transformer.babelTransformerPath` to
  `require.resolve('react-native-svg-transformer')`, remove `svg` from `resolver.assetExts` and add it
  to `resolver.sourceExts`. The alternative is `SvgXml` with `babel-plugin-inline-import`, with
  transforms done at run time.

## Touch and filters
- Elements accept `onPress`, `onPressIn` and `onPressOut` (and other touch props listed in USAGE.md).
- Implemented filters: `FeBlend`, `FeComposite`, `FeColorMatrix`, `FeDropShadow`, `FeFlood`,
  `FeGaussianBlur`, `FeMerge`, `FeOffset`. Not all filters are implemented on native platforms; they
  work on web, and some display a warning that they are unsupported.

## Known issue
Applying the focus point of `RadialGradient` is not possible on Android.

## Verify
- [ ] Every gradient, mask and pattern sits inside `<Defs>` with a matching `id`.
- [ ] Remote SVGs have an `onError` or `fallback` path.
- [ ] The react-native-svg version matches the React Native version in the table.
- [ ] Any filter effect uses the implemented set and was checked on a device.

## Checked
Read the react-native-svg README and USAGE.md as downloaded text. Removed as unconfirmed: the claim that no `transform` component prop exists, the rules about `Marker`, element list completeness, the claim that unsupported filters silently do nothing (docs say some warn), svgr advice, and the failure-modes list.
Method: docs-checked 2026-11-09 against the react-native-svg README and USAGE.md.
