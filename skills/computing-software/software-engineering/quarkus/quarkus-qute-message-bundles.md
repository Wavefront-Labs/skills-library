---
id: computing-software.software-engineering.quarkus.quarkus-qute-message-bundles
name: quarkus-qute-message-bundles
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, qute, i18n, message-bundle, localization, templates]
level: advanced
status: docs-checked
description: "Create type-safe Qute message bundles in Quarkus: @MessageBundle interfaces, localized files and interfaces, locale selection, @LocaleAware and enum messages."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/qute-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Qute type-safe message bundles

Each message is a tiny template defined as a method on an interface; Quarkus generates the implementation at build time. Not supported in standalone Qute.

## Define a bundle

```java
import io.quarkus.qute.i18n.Message;
import io.quarkus.qute.i18n.MessageBundle;

@MessageBundle
public interface AppMessages {
    @Message("Hello {name}!")
    String hello_name(String name);
}
```

- Default bundle name is `msg` (top-level interface), used as the template namespace: `{msg:hello_name('Lucie')}`. A nested interface gets enclosing names joined by underscores, e.g. `Controller_index`.
- Use it via `MessageBundles.get(AppMessages.class).hello_name("Lucie")`, `@Inject AppMessages`, or in templates. `{msg:message(myKey,'Lu')}` resolves a key at runtime but skips validation.
- Build validation: namespace-less expressions must map to method parameters, are checked against parameter types, and unused parameters log a warning.
- Key strategy can be hyphenated (`helloName` becomes `hello-name`) or underscored (`hello_name`); `@Message` can override with a custom key.

## Localize

The default locale is `quarkus.default-locale`. Two ways to add a locale:

1. Interface extending the bundle, annotated `@Localized("de")` (IETF tag), with `@Override @Message("Hallo {name}!")`.
2. UTF-8 file in `src/main/resources/messages`, named `<bundle>_<tag>.properties`, e.g. `msg_de.properties`: `hello_name=Hallo {name}!`. Lines are `key=value`; `#` starts a comment; escape the line end with `\` to continue a value. The suffix is ignored.

If a file has no tag, the default bundle locale is assumed (`msg.properties` is `msg_en.properties` when the default is `en`). Duplicates at the same priority fail the build; files in the app root beat files from dependencies. A generated example lives in `target/qute-i18n-examples/msg.properties`.

`@Message` with no value takes the text from a localized file; `@Message(defaultValue = "Goodbye {name}!")` is the last-resort fallback. `Message#value()` always wins over a file.

## Select the locale at runtime

- Template: `hello.instance().setLocale("cs").render()`.
- Injection: `@Localized("cs") AppMessages msg;`.
- Follow the current request: inject with `@LocaleAware`. Locale comes from a `CurrentLocaleProvider` bean; with `quarkus-vertx-http` the default reads `Accept-Language`. A custom provider bean takes precedence. Missing locale falls back to the default.
- `quarkus-rest-qute` derives the template `locale` from `Accept-Language` if unset.

## Enum messages

A method with one enum parameter and a bare `@Message` gets a generated `{#when}` template plus one message per constant. Localized files must define `methodName_CONSTANT1=...` for every constant. If any constant name contains `_` or `$`, use the `_$` separator for all keys: `methodName_$CONSTANT_1=Value 1`.

## Checked

2026-11-07. Matched against the text (with includes) of: qute-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.
