---
id: computing-software.software-engineering.groovy.extension-module-descriptor
name: extension-module-descriptor
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, extension-module-descriptor, groovy-extension-modules]
level: advanced
status: docs-checked
description: "Package extra instance and static methods as a Groovy extension module using META-INF/groovy/org.codehaus.groovy.runtime.ExtensionModule."
sources:
  - https://groovy-lang.org/metaprogramming.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-metaprogramming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extension module descriptor
- Create a class with static methods whose first parameter is the receiver type: `static String shout(String self)`.
- Descriptor file `META-INF/groovy/org.codehaus.groovy.runtime.ExtensionModule` (properties format):
```
moduleName=my-ext
moduleVersion=1.0
extensionClasses=com.acme.StringExt
staticExtensionClasses=com.acme.StaticStringExt
```
- `moduleVersion` is only used to check you do not load the same module in two versions; several comma-separated classes may be listed per key, and a module need not define both kinds.
- Extension modules are compatible with type checking (`@TypeChecked`/`@CompileStatic`), unlike categories.

## Gotchas
- Static and instance extension methods cannot be in the same class; the first parameter of a static extension method is the extended class and is unused.

## Checked

2026-11-02. Confirmed against the Metaprogramming chapter (Extension modules: module descriptor, static methods, compatibility with type checking). Removed: IDE visibility and Groovy 4 package claims.

Method: documentation only; no commands were run.

## Self-check
Jar the class and descriptor, put it on the classpath, and call `'a'.shout()` from a script.
