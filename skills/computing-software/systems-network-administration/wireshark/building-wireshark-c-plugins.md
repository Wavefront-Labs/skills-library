---
id: computing-software.systems-network-administration.wireshark.building-wireshark-c-plugins
name: building-wireshark-c-plugins
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wireshark-plugin-c, dissector, plugin, cmake]
level: practitioner
status: docs-checked
description: "Build a C dissector plugin for Wireshark in the source tree with CMake: support files, CMakeListsCustom.txt, registration and handoff routines."
sources:
  - https://www.wireshark.org/docs/wsdg_html_chunked/ChDissectAdd.html
  - https://www.wireshark.org/docs/wsdg_html_chunked/ChSrcBuildFirstTime.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building C plugins

Lua is fine for prototypes; C plugins are faster and suit heavy traffic or complex reassembly.
The Wireshark Developer's Guide notes plugins are easier to write at first, and with care a plugin can
later be converted into a built-in dissector.

## In-tree build
1. Build Wireshark itself first and test the build environment before changing anything (the guide's
   advice). Follow the platform build procedure for Unix or Windows.
2. Create the plugin directory under the source tree (plugins/epan). The guide's sample support files
   live in the gryphon plugin directory (plugins/epan/gryphon): copy them and update
   `CMakeLists.txt` with your plugin name and version. Support files are `CMakeLists.txt` (CMake file
   and version info) and optionally `plugin.rc.in` (Windows DLL resource template).
3. In the top-level source directory copy `CMakeListsCustom.txt.example` to `CMakeListsCustom.txt` and
   add your plugin path to the `CUSTOM_PLUGIN_SRC_DIR` list.
4. Re-run CMake and build. Run your build from the build directory, or copy the plugin binary into the
   plugin directory of an installed Wireshark and run that.

CMake build type is set with `CMAKE_BUILD_TYPE` (for example `cmake .. -DCMAKE_BUILD_TYPE=Debug`);
Debug is the usual choice for development.

## Minimal registration
Register the protocol in `proto_register_foo()` with `proto_register_protocol()` (name, short name,
filter name), register fields with `proto_register_field_array()`, and register the dissector by name
with `register_dissector()` (preferred over unnamed `create_dissector_handle()`, whose handle cannot
be called from other dissectors). Then associate traffic in the handoff routine:
```c
void proto_reg_handoff_foo(void)
{
    dissector_add_uint("udp.port", FOO_PORT, foo_handle);
}
```
By convention `proto_register_foo()` and `proto_reg_handoff_foo()` are the last two functions in the
dissector source. Use the same short dissector name as the protocol in simple cases, or names such as
`foo.udp` and `foo.tcp` if dissection differs per transport.

## Gotchas
- Plugins are built against the Wireshark source version in use; rebuild when you move to a new
  release.

## Verify
- [ ] The dissector decodes traffic on the registered port in your built Wireshark or tshark.

## Checked
Method: docs-checked 2026-11-09 against the Wireshark Developer's Guide pages "Adding a basic dissector" (read in the plugin-support-file, registration and handoff sections) and "Building Wireshark for the first time" (build type section). The gitlab README.plugins source returned 404 and was dropped. Dropped unconfirmed claims: out-of-tree find_package build, plugin.c/plugin_version details, install folder paths, version-ABI specifics, tshark -G plugins.
