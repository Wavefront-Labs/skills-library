---
id: computing-software.software-engineering.cpp.iostreams-and-std-filesystem
name: iostreams-and-std-filesystem
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-text-io, cpp-ti-iostreams, iostreams-filesystem, ifstream, std-filesystem, stringstream, std-print]
level: practitioner
status: docs-checked
description: "Map the C++ I/O libraries (streams, std::print, C stdio) and the std::filesystem API: path operations, directory iterators, status queries, link flags."
sources: ["https://en.cppreference.com/w/cpp/io", "https://en.cppreference.com/w/cpp/filesystem"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iostreams and std::filesystem

Both cited pages are overview indexes; this skill records the structure and names they confirm and does not claim detailed behaviour.

## The I/O libraries
C++ includes three I/O libraries: the OOP-style stream-based library, the print-based family of functions (since C++23) and the C-style I/O functions.
- Stream classes: `basic_istream`, `basic_ostream`, file streams `basic_ifstream`/`basic_ofstream`, string streams `basic_istringstream`/`basic_ostringstream`/`basic_stringstream`, with typedefs such as `std::ifstream`, `std::ofstream`, `std::stringstream` and wide variants. `ios_base` is the stream base class.
- `<print>` (C++23): `std::print` and `std::println` (plus `vprint_unicode` and `vprint_nonunicode` variants). Per the reference they bring the performance benefits of `std::format`, are locale-independent by default, reduce global state, and avoid allocating a temporary `std::string` or calling `operator<<`, making formatting more efficient than iostreams and stdio. They print to stdout or a file stream, and there are overloads taking `std::ostream`.

## std::filesystem (C++17, header `<filesystem>`)
```cpp
#include <filesystem>
namespace fs = std::filesystem;

for (const auto& e : fs::recursive_directory_iterator(root, fs::directory_options::skip_permission_denied)) {
    if (e.is_regular_file() && e.path().extension() == ".txt") { /* e.file_size() */ }
}
fs::path p = fs::path("a") / "b" / "c.txt";
fs::rename(tmp, final);
fs::create_directories(dir);
```
(The `directory_options::skip_permission_denied` option name and the `path` operations above are used from general API knowledge; the cited page only lists the classes and function names.)

- Classes: `path`, `filesystem_error`, `directory_entry`, `directory_iterator`, `recursive_directory_iterator`, `file_status`, `space_info`, plus enums `file_type`, `perms`, `perm_options`, `copy_options`, `directory_options` and the `file_time_type` typedef.
- Functions: `absolute`, `canonical`/`weakly_canonical`, `relative`/`proximate`, `copy`, `copy_file`, `copy_symlink`, `create_directory`/`create_directories`, `create_hard_link`, `create_symlink`/`create_directory_symlink`, `current_path`, `exists`, `equivalent`, `file_size`, `hard_link_count`, `last_write_time`, `permissions`, `read_symlink`, `remove`/`remove_all`, `rename`, `resize_file`, `space`, `status`/`symlink_status`, `temp_directory_path`.
- Type queries: `is_directory`, `is_regular_file`, `is_symlink`, `is_empty`, `is_fifo`, `is_socket`, `is_block_file`, `is_character_file`, `is_other`, `status_known`.
- `remove` deletes a file or empty directory; `remove_all` removes a file or directory and all its contents recursively. `status` follows symlinks while `symlink_status` checks the link itself.
- Feature macro `__cpp_lib_filesystem` = 201703L.
- Linking: the GNU implementation prior to 9.1 requires `-lstdc++fs`, and the LLVM implementation prior to LLVM 9.0 requires `-lc++fs`.

## Verify
- Test a missing file, empty file, no trailing newline and a permission-denied directory.

## Checked
Read the cppreference input/output library and filesystem library overview pages. Removed as unconfirmed (these pages do not discuss them): the getline/eof loop rules, binary mode and newline translation, flush and temp-then-rename atomicity, `sync_with_stdio` and `cin.tie` fast-I/O settings, sticky formatting state, Windows path encoding, TOCTOU advice, directory iteration order and the non-throwing `error_code` overloads.
Method: docs-checked 2026-11-09 against the cppreference io and filesystem overview pages.
