---
id: computing-software.software-engineering.mobile-development.hilt-dependency-injection-on-android
name: hilt-dependency-injection-on-android
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, android, hilt, dagger, dependency-injection, hiltviewmodel, entrypoint, scopes, ksp]
level: practitioner
status: docs-checked
description: "Set up Hilt on Android: Application and entry point annotations, modules with @Provides and @Binds, component scopes, @HiltViewModel and test replacements."
sources: ["https://developer.android.com/training/dependency-injection/hilt-android", "https://developer.android.com/training/dependency-injection/hilt-testing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hilt dependency injection

Hilt provides containers for Android classes and manages their lifecycles. It is built on
Dagger and keeps its compile-time correctness.

## Gradle
Apply the Hilt plugin and KSP as the Android guide shows (the page used version 2.57.1 when
read; check it for the current number):
```kotlin
plugins {
    id("com.google.devtools.ksp")
    id("com.google.dagger.hilt.android")
}
dependencies {
    implementation("com.google.dagger:hilt-android:<version>")
    ksp("com.google.dagger:hilt-android-compiler:<version>")
}
```
The root build file declares the plugin `com.google.dagger.hilt.android` with `apply false`.

## Code
- Every app needs an `Application` annotated `@HiltAndroidApp`; it triggers code generation
  and creates the application-level container.
- `@AndroidEntryPoint` makes an Android class receive dependencies, with field injection via
  `@Inject lateinit var`. In Compose, annotate the root `ComponentActivity` rather than each
  composable. `@HiltViewModel` covers ViewModels.
- Constructor injection: `@Inject` on a class constructor tells Hilt how to build it.
- Modules (`@Module`) provide types that constructor injection cannot (interfaces, third-party
  classes) and need `@InstallIn(<component>)`. Use an abstract `@Binds` function to pick an
  implementation for an interface; use a `@Provides` function for a class you do not own.
- Same-type bindings can be told apart with qualifiers.
```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class DataModule {
    @Binds abstract fun repo(impl: FeedRepositoryImpl): FeedRepository
}
```

## Scopes
By default all bindings are unscoped: Hilt creates a new instance at every request. Scope
annotations by component: `@Singleton` (`SingletonComponent`, Application),
`@ActivityRetainedScoped` (`ActivityRetainedComponent`), `@ViewModelScoped`
(`ViewModelComponent`), `@ActivityScoped` (`ActivityComponent`). A binding's scope must
match the scope of the component where it is installed (for example a `@Singleton`
binding is installed in `SingletonComponent`). Scope only what needs the same instance.
Hilt injects broadcast receivers directly from `SingletonComponent`.

## Testing
Add the `hilt-android-testing` dependency. Annotate UI tests with `@HiltAndroidTest` and add
`HiltAndroidRule`; run instrumented tests in an `Application` that supports Hilt, such as
`HiltTestApplication`. To replace a binding for all tests in a folder, add a module there
annotated `@TestInstallIn(..., replaces = [ProductionModule::class])`; to replace it in one test,
use `@UninstallModules` and a test module inside the test.

## Checked
Confirmed in the Hilt Android and Hilt testing pages: setup, annotations, @Binds/@Provides,
scopes table, unscoped default, test rule, `HiltTestApplication`, `@TestInstallIn` and
`@UninstallModules`. Removed as not stated there: the claim that `@Binds` is cheaper than
`@Provides`, that a missing `@AndroidEntryPoint` crashes at runtime, the
`[Dagger/MissingBinding]` text, the sample OkHttp provider and the KSP-versus-kapt speed claim.
The `@HiltViewModel` constructor-injection detail and `hiltViewModel()` are described on the
Android ViewModel guide, not re-confirmed here beyond the Hilt page's annotation list.
Method: docs-only read of cited pages, 2026-11-08
