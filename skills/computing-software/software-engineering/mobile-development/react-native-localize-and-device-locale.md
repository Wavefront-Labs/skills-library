---
id: computing-software.software-engineering.mobile-development.react-native-localize-and-device-locale
name: react-native-localize-and-device-locale
category: computing-software
field: software-engineering
product: mobile-development
tags: [software-engineering, mobile-development, react-native, react-native-localize, localization, i18n, locales, find-best-language-tag, rtl, locale-config, number-formatting, currency, expo-plugins, ssr-localization, mobile-l10n, timezone, calendar]
level: practitioner
status: docs-checked
description: "Read the device locale, currency, calendar, temperature unit and number format with react-native-localize: API, platform locale config, findBestLanguageTag, Expo plugin."
sources: ["https://github.com/zoontek/react-native-localize"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# react-native-localize: device locale and format settings

**Goal:** read the device's locale preferences (language, currency, calendar, number and time formats) instead of guessing or shipping an English-only app.

The library follows the React Native release support policy: it supports the latest version and the two previous minor series. Install, then run pod install for iOS.

```bash
npm install --save react-native-localize
cd ios && pod install
```

## The API
| Function | Returns |
|---|---|
| `getLocales()` | preferred locales in order: `{ languageCode, scriptCode?, countryCode, languageTag, isRTL }[]` |
| `getCurrencies()` | preferred currency codes in order, e.g. `["EUR", "GBP", "USD"]` |
| `getCountry()` | country code from the device locale, not the position; Latin American regional settings return `"UN"` instead of `"419"` |
| `getCalendar()` | one of `gregorian`, `buddhist`, `coptic`, `ethiopic`, `ethiopic-amete-alem`, `hebrew`, `indian`, `islamic`, `islamic-umm-al-qura`, `islamic-civil`, `islamic-tabular`, `iso8601`, `japanese`, `persian` |
| `getTemperatureUnit()` | `"celsius"` or `"fahrenheit"` |
| `getNumberFormatSettings()` | `{ decimalSeparator, groupingSeparator }` |
| `uses24HourClock()` | boolean |
| `usesMetricSystem()` | boolean |
| `getTimeZone()` | preferred timezone from device settings, not position, e.g. `"Europe/Paris"` |
| `usesAutoDateAndTime()` / `usesAutoTimeZone()` | Android only; boolean or undefined |
| `findBestLanguageTag(languageTags)` | `{ languageTag, isRTL }` or `undefined`; picks the best translation available and respects the user's preferred-language order |
| `openAppLanguageSettings()` | Promise; Android 13+ only, requires your supported locales to be configured |

Example: `findBestLanguageTag(["en-US", "en", "fr"])` returns `{ languageTag: "en-US", isRTL: false }` for a device whose preferences start with en-US.

## Declaring supported locales
- **iOS:** list locales under `CFBundleLocalizations` in `ios/YourApp/Info.plist`, as `<string>` entries in an `<array>`.
- **Android:** set `android:localeConfig="@xml/locale_config"` on the `<application>` element in `android/app/src/main/AndroidManifest.xml`, then list `<locale android:name="en" />` entries inside `<locale-config>` in `android/app/src/main/res/xml/locale_config.xml`.
- **Expo:** use the config plugin. Dynamic config: `import localize from "react-native-localize/expo"` (use `require` in app.config.js) and `plugins: [localize({ locales: ["en", "fr"] })]`. Static app.json: `[["react-native-localize", { "locales": ["en", "fr"] }]]`. Locales can also be per platform: `{ android: ["en"], ios: ["en", "fr"] }`.

## React and server-side rendering
On the client the library uses `navigator.languages`. During SSR it takes language preferences from the parsed `Accept-Language` header: wrap the app in `ServerLanguagesProvider` with `value` set to a `string[]` of languages (the README parses it with the `accepts` package), and in components call the `useLocalize` hook, e.g. `const { getCountry } = useLocalize();`, instead of calling the API functions directly.

## Pairing with an i18n library
The README gives examples with `@formatjs/intl` in the repo's `/example` directory.

## Testing
It is a native module, so mock it in your `__mocks__` directory: `export * from "react-native-localize/mock"` (or `"react-native-localize/mock/jest"`) in `__mocks__/react-native-localize.ts`.

## Checked
Confirmed on 2026-11-08 against the react-native-localize README: install, support policy, every API function and return type, the three platform locale declarations, the SSR section and the mock path. Removed because the readable page does not state them: the FormatJS docs and Apple CoreFoundationKeys sources (not read), claims about the OS treating an undeclared app as English-only, number-format examples such as `1 000,50`, the failure-mode list (stale values after a system language change, Jest native-module crash text), a link to another localization skill, and the claim that `findBestLanguageTag` returns null (the README type is `undefined`).
Method: docs-only read of cited pages, 2026-11-08
