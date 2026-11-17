---
id: computing-software.software-engineering.swift.swift-package-plugins
name: swift-package-plugins
category: computing-software
field: software-engineering
product: swift
tags: [swift, swift-spm, package-plugins]
level: advanced
status: docs-checked
description: "Declare and run SwiftPM build tool and command plugins, including permissions and the plugin-to-tool relationship."
sources: ["https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/Plugins.md", "https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/Plugins/EnableBuildPlugin.md", "https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/Plugins/EnableCommandPlugin.md", "https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/Plugins/WritingBuildToolPlugin.md", "https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/Plugins/WritingCommandPlugin.md", "https://github.com/swiftlang/swift-package-manager/blob/main/Sources/PackageManagerDocs/Documentation.docc/Package/PackagePlugin.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package plugins
Plugins, available since Swift 5.6, extend SwiftPM and are written in Swift against the `PackagePlugin` module (a plugin script can import Foundation and standard libraries but not other packages' libraries). There are two extension points:

- Build tool plugins: construct commands that run before or during a build (code generation, for example). The plugin does not do the work; it forms the commands the build runs later.
- Command plugins: custom `swift package <verb>` commands run on demand, unrelated to the build graph.

A plugin is a `.plugin` target whose `capability` (`.buildTool()` or `.command(intent:permissions:)`) selects the entry point (`BuildToolPlugin` or `CommandPlugin`). Add a `.plugin` product to make it available to packages that depend on yours. Sources normally live in a directory named after the plugin under `Plugins`.

```swift
.plugin(
  name: "MyCommandPlugin",
  capability: .command(
    intent: .sourceCodeFormatting(),
    permissions: [.writeToPackageDirectory(reason: "This command reformats source files")]),
  dependencies: [.product(name: "SomeTool", package: "sometool")])

.executableTarget(name: "MyExample",
  plugins: [.plugin(name: "OpenAPIGenerator", package: "swift-openapi-generator")])
```

Use and run:
- Add a package dependency, list command plugins with `swift package plugin --list`, and invoke one as `swift package <verb> [arguments]`; everything after the verb goes to the plugin (for example `--target MyTarget`).
- To use a build tool plugin, list it in the `plugins:` of each target it should apply to.

Build commands vs prebuild commands:
- Prefer a build command when all input and output paths are known beforehand; the build system runs it only when outputs are missing or inputs changed.
- Use a prebuild command only when output names are unknown until the tool runs. It runs before every build, so do your own caching, and its tool dependencies must be binary targets.

Gotchas:
- Every plugin runs as a separate process. Where sandboxing is supported it blocks network access and writes outside a temporary directory. Command plugins can declare a need to write to the package directory; `swift package` then asks for approval at a console and denies the request otherwise. Pass `--allow-writing-to-package-directory` (or `--allow-network-connections`) to allow without a prompt, which suits CI. Build tool plugins cannot modify package sources.
- Tool dependencies are an `executableTarget` or `binaryTarget` in the same package or an executable product from another package, looked up with `PluginContext.tool(named:)`. Build tool plugins do not search the user's `PATH`, so provide the tool as a dependency.
- Generated outputs: Swift sources and resources are supported; non-Swift source files are not.
- SwiftPM has no specific support for debugging or testing plugins; factor non-trivial code into separate files that unit tests can include.

Verify: `swift package plugin --list` shows the command plugin, and the plugin's `Diagnostics` or thrown errors appear when it fails.

## Checked
2026-11-08: read in full the SwiftPM docs pages Plugins, Enable a build plugin, Enable a command plugin, Writing a build tool plugin, Writing a command plugin and `swift package plugin` (swift-package-manager repository, PackageManagerDocs source). Removed: SE-0303 and SE-0332 references and that proposal source (not read), the `.custom(verb:description:)` intent and `swiftlint-binary` example, the claim Linux has no sandbox, `--disable-sandbox` and Xcode `-skipPackagePluginValidation` advice, the trust-prompt claim for dependency plugins, and `swift build -v` verification.
Method: documentation only; no commands were run.
