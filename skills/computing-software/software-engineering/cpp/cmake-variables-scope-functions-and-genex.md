---
id: computing-software.software-engineering.cpp.cmake-variables-scope-functions-and-genex
name: cmake-variables-scope-functions-and-genex
category: computing-software
field: software-engineering
product: cpp
tags: [cmake, cmake-language, cmake-lang-scope, cmake-lang-functions, cmake-lang-genex, generator-expressions, cmake-function, cmake-macro, cache-variables, cmake-variables-scope, cmake-generator-expressions, cmake-functions-macros]
level: practitioner
status: docs-checked
description: "Write correct CMake language: variable scopes, cache lookup order, cmake_parse_arguments in functions and macros, and generator expressions."
sources:
  - https://cmake.org/cmake/help/latest/manual/cmake-language.7.html
  - https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html
  - https://cmake.org/cmake/help/latest/command/cmake_parse_arguments.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMake variables, scope, functions and generator expressions

## Scope
- Variables have dynamic scope. A `function()` runs in a new binding scope: variables set there are visible to the function and anything it calls, but not after it returns. `block()` can also create a scope.
- Each directory has its own bindings. Before processing a directory's `CMakeLists.txt`, CMake copies the parent directory's current bindings into the new scope.
- Cache entries are a separate set that persists across runs in a build tree and changes only on explicit request, such as the `CACHE` option of `set()` and `unset()`.
- Lookup order for `${VAR}`: function call stack, then the current directory scope; if unset or not found, the cache; otherwise the empty string. `$CACHE{VAR}` reads the cache directly.
- `$ENV{VAR}` reads an environment variable.

## Functions and macros with cmake_parse_arguments
```cmake
function(add_checked_test name)
  cmake_parse_arguments(PARSE_ARGV 1 arg "SLOW" "TIMEOUT" "SOURCES;LIBS")
  # sets arg_SLOW (TRUE/FALSE), arg_TIMEOUT, arg_SOURCES, arg_LIBS (unset if absent)
  if(arg_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "unknown arguments: ${arg_UNPARSED_ARGUMENTS}")
  endif()
  add_executable(${name} ${arg_SOURCES})
  target_link_libraries(${name} PRIVATE ${arg_LIBS})
endfunction()
```
- Option keywords always get a variable (`TRUE` or `FALSE`). One-value and multi-value keywords are undefined if not given.
- Anything unrecognised lands in `<prefix>_UNPARSED_ARGUMENTS`; keywords given without values land in `<prefix>_KEYWORDS_MISSING_VALUES` (3.15+).
- `PARSE_ARGV <N>` (3.7+) is for functions only. It parses the `ARGV#` variables from the N-th argument and lets values contain `;`. The docs advise avoiding `ARGV` and `ARGN` in functions.
- The docs suggest prefix `arg` inside functions. In a macro, which acts on the calling scope, use something unique from the macro name (for example `arg_my_macro`) so two macros with common keywords do not overwrite each other's variables.
- Keywords must be unique across the three keyword lists, and by convention are all uppercase.

## Generator expressions
They are evaluated during build system generation, not while `CMakeLists.txt` is processed, so `message()` cannot show their result.
```cmake
target_compile_definitions(app PRIVATE $<$<CONFIG:Debug>:DEBUG_LOG=1>)
target_compile_options(app PRIVATE $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall> $<$<CXX_COMPILER_ID:MSVC>:/W4>)
target_include_directories(lib PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:include>)
add_custom_command(TARGET app POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:dep> $<TARGET_FILE_DIR:app>)
```
- `$<condition:text>` gives the text if condition is `1`, empty if `0`; any other value is an error. `$<IF:cond,a,b>` picks between two strings (3.8+).
- `$<CONFIG:cfgs>` takes a comma-separated list (3.19+) and compares case-insensitively. `$<CXX_COMPILER_ID:ids>` also takes a comma-separated list.
- `$<BUILD_INTERFACE:...>` applies when the property is exported with `export()` or used by another target in the same build; `$<INSTALL_INTERFACE:...>` applies when exported with `install(EXPORT)`.
- Not every property accepts generator expressions: check the property's own documentation.
- Debug by writing the value out: `file(GENERATE OUTPUT out.txt CONTENT "$<TARGET_FILE:app>")`, or add a custom target that runs `${CMAKE_COMMAND} -E echo "$<...>"` and build it.

## Verify
- [ ] Build the debug custom target or inspect the `file(GENERATE)` output to confirm each expression expands as intended.

## Checked
Method: docs-checked 2026-11-09 against the cmake-language(7), cmake-generator-expressions(7) and cmake_parse_arguments pages on cmake.org (latest). Dropped unconfirmed claims about PARENT_SCOPE, CACHE FORCE, CMP0126, multi-config CMAKE_BUILD_TYPE, genex in if() and string(JSON).
