---
id: computing-software.software-engineering.python.writing-c-api-extension-modules
name: writing-c-api-extension-modules
category: computing-software
field: software-engineering
product: python
tags: [python, py-ffi, py-ffi-capi, c-api-extension-modules, extension-module, py-incref, limited-api, abi3, multi-phase-init]
level: advanced
status: docs-checked
description: "Write a CPython C-API extension: module init with PyModuleDef_Init, argument parsing, error and reference-counting conventions, borrowed references, the GIL, limited API."
sources: ["https://docs.python.org/3/extending/extending.html", "https://docs.python.org/3/c-api/stable.html", "https://docs.python.org/3/c-api/refcounting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing C-API extension modules

```c
#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;                      /* exception already set by the parser */
    sts = system(command);
    return PyLong_FromLong(sts);          /* new reference */
}
```
Register such a function with `METH_VARARGS` in `PyMethodDef.ml_flags`. For a module, the tutorial uses multi-phase initialisation:

```c
static PyModuleDef_Slot spam_module_slots[] = {
    {Py_mod_exec, spam_module_exec},
    {0, NULL}
};

static struct PyModuleDef spam_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "spam",
    .m_size = 0,  // non-negative
    .m_slots = spam_module_slots,
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModuleDef_Init(&spam_module);
}
```

## Error convention
- When a function fails it sets an exception and returns an error value, usually `NULL` for object-returning functions and `-1` for integer-status functions. `PyArg_ParseTuple()` and friends are the exception: they return a true value on success.
- Raise with `PyErr_SetString(PyExc_ImportError, "...")` or similar; pick the right built-in exception: `PyExc_ValueError` for out-of-range values, `PyExc_TypeError` when the argument list is wrong (which `PyArg_ParseTuple` already raises).
- Every failing `malloc()` becomes an exception via `PyErr_NoMemory()`.
- When returning an error, clean up objects you created with `Py_XDECREF()` or `Py_DECREF()`.
- Call `PyErr_Clear()` only when you deliberately swallow an error.
- Keyword arguments: `METH_VARARGS | METH_KEYWORDS`.

## Reference counting
- Most object-creating functions (for example `PyLong_FromLong`, and `Py_BuildValue`) return a new reference you must release or return.
- `PyObject_CallObject()` is reference-count-neutral for its arguments and returns a new reference; `Py_DECREF()` the result unless you store it. Put `Py_DECREF(arglist)` immediately after the call, before the error check.
- Borrowed references, such as the result of `PyList_GetItem()`, can become invalid if arbitrary code runs and drops the owner; the docs' example shows a `__del__` bug and a thread bug where another thread runs during `Py_BEGIN_ALLOW_THREADS ... Py_END_ALLOW_THREADS`. `Py_INCREF` before use if code may run in between.
- Do not pass `NULL` to functions that expect object references; functions returning object references return `NULL` only to indicate an exception.
- A module-level static such as `SpamError` is overwritten if the module is initialised again; the tutorial blocks repeated initialisation with an `ImportError`. State kept in the module object (`m_size`) avoids this.

## Stable ABI
- Defining `Py_LIMITED_API` exposes only the Limited API subset of `Python.h`; extensions built for it are compatible across several minor releases (`abi3`, introduced in 3.2, for non-free-threaded builds; `abi3t` arrives in 3.15 for free-threaded builds).
- `Py_LIMITED_API` can be given as a version value such as `0x03020000`; compiling with a later value does not guarantee the same source compiles with a still-later one. The macros do not guard against passing arguments that are invalid on an older Python.
- A few private declarations are exposed even with the macro defined; check the docs for whether each API is part of the Limited API.

## Verify
- [ ] Each function handles bad arguments by raising an exception rather than crashing.
- [ ] Reference counts stay stable over repeated calls in a debug build.

## Checked
Date: 2026-11-03. Confirmed against "Extending and Embedding" (extending.html), the Stable ABI page and the reference counting page: parse and error conventions, module init template, borrowed references and thread example, new-reference rules, Limited API and abi3/abi3t statements. Removed as unconfirmed in the fetched pages: the setuptools `py_limited_api` build recipe and `cp311` tag, the `Py_mod_gil` free-threading declaration, `PyTuple_GET_ITEM`, `goto fail` pattern, `sys.gettotalrefcount()`, `python -X dev`, `auditwheel`/`delocate`, comments on alternative tools, `METH_FASTCALL`/buffer-protocol advice, free-threading macro remarks.
Method: documentation only; no commands were run.
