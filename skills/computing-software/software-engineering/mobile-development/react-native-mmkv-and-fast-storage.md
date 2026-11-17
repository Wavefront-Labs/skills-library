---
id: computing-software.software-engineering.mobile-development.react-native-mmkv-and-fast-storage
name: react-native-mmkv-and-fast-storage
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, react-native-mmkv, mmkv, nitro-modules, key-value-storage, synchronous-storage, storage-encryption, jsi, asyncstorage-replacement, storage-instances, app-groups, mobile-storage, persist-state, encrypted-storage]
level: practitioner
status: docs-checked
description: "Use react-native-mmkv v4 (Nitro Modules, createMMKV) for synchronous key-value storage: typed accessors, custom multi-process and encrypted instances, hooks, and v4 requirements."
sources: ["https://github.com/margelo/react-native-mmkv", "https://github.com/Tencent/MMKV"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# react-native-mmkv: fast synchronous storage

**Goal:** persist small values (tokens, preferences, flags) with synchronous access instead of
`AsyncStorage`'s Promises, using MMKV - the key-value storage framework developed by WeChat -
through direct JS bindings to the native C++ library.

The README lists "fully synchronous calls, no async/await, no Promises, no Bridge", uses JSI and
C++ Nitro Modules, and claims "~30x faster than AsyncStorage" (a vendor claim; its benchmark reads a
value 1000 times on an iPhone 11 Pro).

## Install (v4)
```bash
npm install react-native-mmkv react-native-nitro-modules
cd ios && pod install
# Expo:
npx expo install react-native-mmkv react-native-nitro-modules
npx expo prebuild
```
**v4 requires react-native 0.76 or higher** and is a Nitro Module. If you are still on V3, the
README points to separate V3 docs and a V4 Upgrade Guide (not read for this skill); do not mix
tutorials across the two versions.

## Create an instance
```ts
import { createMMKV } from 'react-native-mmkv';
export const storage = createMMKV();          // default instance id: 'mmkv.default'
```
The README recommends re-using one instance throughout the app, so export it.

To share data with other apps or app extensions in the same app group on iOS, add an
`AppGroupIdentifier` key to `Info.plist` with your app group's value; MMKV then stores data inside
the app group and uses its multi-processing mode.

## Typed accessors
```ts
storage.set('user.name', 'Marc');
storage.set('user.age', 21);
storage.set('is-pro', true);

storage.getString('user.name');   // 'Marc'
storage.getNumber('user.age');    // 21
storage.getBoolean('is-pro');     // true
storage.set('token', arrayBuffer); storage.getBuffer('token');

storage.contains('user.name');    // checks whether a key exists
storage.getAllKeys();             // all keys
storage.remove('user.name');      // returns whether it was removed
storage.clearAll();               // deletes all keys
```
Supported value types are strings, booleans, numbers and ArrayBuffers. For objects the README
serialises with `JSON.stringify` on write and `JSON.parse` on read.

## Custom instances
```ts
const userStorage = createMMKV({
  id: `user-${userId}-storage`,       // required if path or encryptionKey is set
  path: `${USER_DIRECTORY}/storage`,  // default: $(Documents)/mmkv/
  encryptionKey: 'hunter2',
  encryptionType: 'AES-256',          // default AES-128
  mode: 'multi-process',              // for App Clips, Extensions or App Groups
  readOnly: false,
  compareBeforeSet: false,
});
```
- `id`: separates storages, for example global app storage and a logged-in user's storage.
  Defaults to `'mmkv.default'`.
- `encryptionKey`: by default MMKV stores key-values in plain text and relies on the iOS or Android
  sandbox; set a key to encrypt.
- `mode: 'multi-process'`: the instance assumes data can be changed from outside (App Clips,
  Extensions, App Groups).
- `readOnly`: avoids unwanted writes; any call to `set(..)` throws.
- `compareBeforeSet`: off by default; enabling it "might improve performance if values are
  repeatedly written to disk, even if they are already persisted".
- `existsMMKV('id')` and `deleteMMKV('id')` check and delete an instance; `storage.encrypt(key)`
  (optionally `'AES-256'`) and `storage.decrypt()` change encryption on an instance;
  `storage.importAllFrom(other)` imports every key and value and returns the count.
- `storage.byteSize` gives the storage size in bytes and `storage.trim()` cleans unused keys and
  clears the memory cache (the README example trims at 4096 bytes or more).

## React integration
```ts
import { useMMKVString, useMMKVNumber, useMMKVBoolean } from 'react-native-mmkv';

const [name, setName] = useMMKVString('user.name');
```
A mocked MMKV instance is used automatically with Jest or Vitest, so `createMMKV()` works in tests.

## Limitations
- react-native-mmkv V4 requires react-native 0.76 or higher.
- Because it uses JSI for synchronous native calls, remote debugging (for example with Chrome) is no
  longer possible; the README says to use Flipper or React DevTools instead.
- On web, if the user disables LocalStorage the library provides a limited in-memory storage that
  does not persist data; refreshing or closing the browser loses it.
- Native log verbosity is set at build time: `MMKV_logLevel` in `android/gradle.properties`, or
  `$MMKVLogLevel` in the iOS `Podfile` (0 Debug, 1 Info, 2 Warning, 3 Error, 4 None).

## Verify
- [ ] `react-native-mmkv` and `react-native-nitro-modules` are both installed, and the project is on
      React Native 0.76+ for v4.
- [ ] A value written before a reload is read back correctly after it, on both platforms.
- [ ] App-group sharing uses `mode: 'multi-process'` and an `AppGroupIdentifier` on iOS.
- [ ] Remote debugging is not part of the workflow for code touching MMKV.

## Checked
2026-11-08. Confirmed against the margelo/react-native-mmkv README (V4): install commands, v4 and
RN 0.76 requirements, `createMMKV` and its options with defaults, accessor, key, buffer, size,
import, exists and delete APIs, encryption methods, hooks, Jest and Vitest mock, web fallback,
log levels, remote-debugging limitation. Removed because the README does not state them: the v3 to
v4 API mapping table and its "is not a function" claim, the missing-key `undefined` behaviour,
re-render-on-change, per-user sign-out advice, sync-loop warnings and the encryptionKey threat
analysis. Dropped sources that were unreadable or did not mention MMKV (an Expo tools page and a
React Native configuration page).
Method: documentation only; no commands were run.
