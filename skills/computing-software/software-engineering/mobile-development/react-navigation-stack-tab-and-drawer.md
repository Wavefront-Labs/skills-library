---
id: computing-software.software-engineering.mobile-development.react-navigation-stack-tab-and-drawer
name: react-navigation-stack-tab-and-drawer
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, react-navigation, native-stack, bottom-tabs, drawer-navigation, navigation-container, navigation-state, deep-linking, navigate-vs-push, screen-options, nested-navigators, mobile-navigation, routing]
level: practitioner
status: docs-checked
description: "Structure a React Native app with React Navigation: native stack, tabs, nesting rules, navigate/push/replace/reset semantics and deep link configuration."
sources: ["https://reactnavigation.org/docs/getting-started", "https://reactnavigation.org/docs/native-stack-navigator", "https://reactnavigation.org/docs/bottom-tab-navigator", "https://reactnavigation.org/docs/nesting-navigators", "https://reactnavigation.org/docs/configuring-links", "https://reactnavigation.org/docs/navigation-actions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# React Navigation: stack, tab and drawer

**Goal:** choose the right navigator and control navigation state deliberately rather than discovering the difference between `navigate` and `push` from a bug report.

## Setup
- `@react-navigation/native` is the core package. Most navigators also need `react-native-screens` and `react-native-safe-area-context`. Minimum requirements stated: react-native >= 0.72.0, expo >= 52 (Expo Go) and typescript >= 5.0.0.
- On Android, `react-native-screens` needs `RNScreensFragmentFactory` set in `MainActivity` (avoids crashes when View state is not persisted across Activity restarts).
- React Navigation does not yet support Android's predictive back gesture; set `android:enableOnBackInvokedCallback="false"` in `AndroidManifest.xml` so the system back gesture works properly.
- Navigators can be configured statically (recommended: object-based, with automatic TypeScript types and deep linking) or dynamically (component-based, supports dynamic screen lists, more boilerplate for TypeScript and deep linking). Examples below use the dynamic form.

## Native stack
`@react-navigation/native-stack` uses `UINavigationController` on iOS and `Fragment` on Android, so animations and gestures are handled by the platform, with smoother transitions and better performance than the JavaScript-based Stack navigator. It exposes native features (large titles, form sheets) but may not support customisations the platform lacks. Report bugs with `createNativeStackNavigator` to `react-native-screens`. A custom header disables native features such as large titles and the search bar.

```tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

<NavigationContainer>
  <Stack.Navigator screenOptions={{ headerBackTitle: 'Back' }}>
    <Stack.Screen name="Home" component={HomeScreen} />
    <Stack.Screen name="Detail" component={DetailScreen} options={{ presentation: 'modal' }} />
  </Stack.Navigator>
</NavigationContainer>
```

## Navigation calls
| Call | Effect |
|---|---|
| `navigate('Detail', params)` | in a stack: if already on a screen with that name it updates its params and does not push; from a different screen it pushes the new screen; if `getId` is set and another screen has the same ID it focuses that one and updates its params |
| `navigate(name, params, { merge, pop })` | `merge` (default false) merges params instead of replacing them; `pop` (default false) pops screens to reach a matching screen |
| `push('Detail', params)` | pushes a new screen on top of the stack |
| `replace('Detail', params)` | replaces the current screen with a new one |
| `pop(count)` | pops the current screen (optionally `count` screens) |
| `popTo(name, params)` | pops back to a previous screen; if none matches, pops the current screen and adds a new one |
| `popToTop()` | pops all screens except the first |
| `reset(state)` | replaces the whole navigation state; routes without a key (or with different keys) remove the existing screens |
| `goBack()` | back to the previous route in history |
| `setParams` / `replaceParams` | merge into, or replace, a route's params |
| `preload(name, params)` | renders a screen in the background before navigating; a preloaded stack screen cannot dispatch actions, call `setOptions` or listen to navigator events until it is navigated to |

- Dispatching an unhandled action does not throw; nothing happens.
- Rewriting history with `reset` to alter the back stack is not recommended in most cases: it confuses users and, on web, the browser history still reflects the old state. Consider the navigator state object internal: use only `index` and `routes`.
- Because `navigate` to a screen already open only updates its params, use `push` when duplicates are correct, or `navigate` with `merge` when you want to keep old params.

## Tabs
```tsx
const Tab = createBottomTabNavigator();
<Tab.Navigator screenOptions={{ headerShown: false, tabBarActiveTintColor: '#0a7' }}>
  <Tab.Screen name="Feed" component={Feed} options={{ tabBarBadge: unread }} />
</Tab.Navigator>
```
- Install `@react-navigation/bottom-tabs`. `tabBarBadge` accepts a string or a number; `tabBarBadgeStyle` styles it.
- `lazy` (default true) renders a tab screen only after it is first accessed; set it to false to render on the navigator's initial render. `freezeOnBlur` (default false) stops inactive screens re-rendering.
- `popToTopOnBlur` (default false) pops a nested stack to its top when leaving the tab; `tabBarRepeatedPressBehavior` (`scrollToTop` and `popToTop`, both default true) controls pressing the focused tab again.
- A drawer is a separate navigator (`@react-navigation/drawer`); its page was not among this skill's sources, so check its install requirements on reactnavigation.org.

## Nesting
- Nesting a navigator means rendering it inside a screen of another. Each navigator keeps its own history, options and per-screen params. Actions go to the current navigator first and bubble up to the parent if it cannot handle them. Nested navigators do not receive the parent's events; use `navigation.getParent(id)` to listen to them.
- The parent navigator's UI renders on top of the child. Patterns: a tab navigator in a stack's first screen means pushed screens cover the tab bar; stacks inside each tab keep the tab bar always visible (pressing a tab again usually pops that stack to top); a drawer in a stack's first screen with the stack header hidden can only be opened from the first screen.
- Navigate into a nested navigator with `navigation.navigate('More', { screen: 'Messages', params: { user: 'jane' } })`. `screen` and `params` are reserved for internal use. By default the named screen becomes the nested navigator's initial screen and `initialRouteName` is ignored; pass `initial: false` to render the navigator's own initial route.
- To avoid double headers set `headerShown: false` on the parent screen that holds the child navigator.
- Minimise nesting: deep hierarchies can cause memory and performance issues on lower-end devices, nesting the same navigator type (tabs in tabs, drawer in drawer) gives confusing UX, and deep links get harder. Use groups (`Stack.Group` / `groups`) to organise screens, for example logged-in and guest screens, rather than nesting.

## Deep linking
Configure on the container with a `linking` prop:

```tsx
const linking = {
  prefixes: ['myapp://', 'https://app.example.com'],
  config: {
    screens: {
      Home: '',
      Detail: 'item/:itemId',
      Settings: { path: 'settings', screens: { Profile: 'profile' } },
    },
  },
};
<NavigationContainer linking={linking}>...</NavigationContainer>
```
- `prefixes` can be custom schemes (`example://`) and host or domain names (`https://example.com`) if Universal Links or Android App Links are configured; wildcards such as `https://*.example.com` are allowed. `prefixes` has no effect on web. A path with params cannot be put in a prefix.
- `enabled: 'auto'` generates paths automatically from screen names (a `Profile` screen gets `profile`), for leaf screens only.
- Query strings become params (`/profile?user=jane` passes `user`). A `:param` path segment becomes a string in `route.params`; all params are strings unless you supply `parse` and `stringify` functions.
- The `config` object must match the navigation structure of the app, including nested navigators.

## Verify
- Sign-out and similar flows are deliberate: decide between `reset`, `replace` and conditional screen groups, and test the back gesture afterwards.
- A deep link for each route resolves to the right screen with params parsed to the right type.
- `headerShown` is set so nested navigators do not show two headers.

## Checked
2026-11-08: read the six cited React Navigation pages (Getting started, Native stack navigator, Bottom Tabs navigator, Nesting navigators, Configuring links, CommonActions reference). Corrected: `navigate` in a stack updates the existing same-name screen's params rather than popping back to it (the `pop` option defaults to false); native stack does not provide Android predictive back (the docs say it is unsupported). Removed claims not in those pages: TypeScript param-list typing and global `RootParamList`, drawer peer dependencies, "tabBarBadge 0 shows a zero", distinct navigator `id`s, JS stack-in-native-stack header flicker, non-serialisable param warnings, the exact "not handled by any navigator" message, and the Universal Link association-file note. The Drawer navigator page was not read.
Method: documentation only; no commands were run.
