---
id: computing-software.software-engineering.mobile-development.expo-router-file-based-routing
name: expo-router-file-based-routing
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, expo-router, expo, file-based-routing, route-groups, deep-linking, navigation, protected-routes]
level: practitioner
status: docs-checked
description: "Route an Expo React Native app from the filesystem with Expo Router: src/app rules, route groups, root layout, protected routes for auth, custom-scheme deep links."
sources: ["https://docs.expo.dev/router/basics/core-concepts/", "https://docs.expo.dev/router/advanced/authentication/", "https://docs.expo.dev/guides/deep-linking/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expo Router: file-based routing

**Goal:** derive routes from the `src/app` directory so the navigation structure is visible in the
file tree, with auth gating and deep links following from it.

## Core rules
1. All screens are files in `src/app`. Each file has a default export that is one page (except
   `_layout` files). Directories group related screens.
2. Every page has a URL matching its path: `src/app/home.tsx` is `/home` (`yourapp.com/home` on web,
   `yourapp://home` natively); `src/app/profile/friends.tsx` is `/profile/friends`. This is the
   universal deep-linking model.
3. There is no initial route in code: the first `index.tsx` matching `/` is used. To start deeper,
   use a route group (a directory named in parentheses), which does not count in the URL. For tabs
   put pages in `src/app/(tabs)` with the default tab as `index.tsx`; `/` then reaches
   `src/app/(tabs)/index.tsx`.
4. The root `src/app/_layout.tsx` replaces `App.jsx`: it renders before any route and is where
   fonts, theme providers and splash screen handling go.
5. Platform-specific files use extensions: in the default template `app-tabs.native.tsx` (Android and
   iOS, native tabs) and `app-tabs.tsx` (web, custom tabs from `expo-router/ui`).
6. Keep components, hooks and utilities outside `src/app`. Anything inside it is treated as a route.
7. Stack and tab navigators take options for headers, animations and gestures (see the Stack and
   Tabs guides).

## Authentication with protected routes
- Wrap the root layout in a session provider; keep the splash screen visible until authentication
  loads (`SplashScreen.preventAutoHideAsync()`, then `SplashScreen.hide()` once not loading), with the
  controller component inside the provider.
- Gate screens with `Stack.Protected`:
```tsx
<Stack>
  <Stack.Protected guard={!!session}><Stack.Screen name="(app)" /></Stack.Protected>
  <Stack.Protected guard={!session}><Stack.Screen name="sign-in" /></Stack.Protected>
</Stack>
```
- Put authenticated screens in an `(app)` group with its own `_layout.tsx`. `sign-in` is outside that
  group, so the group's checks do not run for logged-out users. Signing out is just clearing the
  session: the guard redirects to sign-in. A deep link to a guarded route also lands on sign-in.
- The docs' sample stores the token with `expo-secure-store` natively and local storage on web.
- Alternative: a sign-in modal over the app (`presentation: 'modal'`, with
  `unstable_settings = { anchor: '(root)' }`) partly preserves deep links after sign-in, but the
  background routes must handle loading data without authentication.
- On web, Expo Router currently supports only build-time static generation and no custom middleware;
  use client-side redirects with a loading state.

## Deep links
- Set `"scheme": "myapp"` in app config; a new development build is needed after changing it. If no
  scheme is set, `android.package` and `ios.bundleIdentifier` are used as default schemes.
- Test with `npx uri-scheme open myapp://somepath/details --ios` (or `--android`). In Expo Go the
  scheme is `exp://`, for example `exp://127.0.0.1:8081/--/somepath/into/app?hello=world`.
- For links from a web domain use Android App Links / iOS Universal Links (the universal linking
  guide).

## Verify
- [ ] Every non-route file is outside `src/app`.
- [ ] Cold-starting signed out shows sign-in, and signing out returns there.
- [ ] A deep link to a guarded route lands on sign-in when signed out.

## Checked
Read the three cited Expo pages as downloaded text (core concepts, authentication, deep linking). Removed as unconfirmed: the dynamic and catch-all route table, `useRouter` and params API details, typed routes setup, the Redirect-in-layout auth pattern (replaced with the documented `Stack.Protected` pattern), the `origin` plugin option, adb command, migration advice and failure modes.
Method: docs-checked 2026-11-09 against the Expo Router core concepts, authentication and deep linking pages.
