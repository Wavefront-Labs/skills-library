---
id: computing-software.ai-ml-engineering.llama-cpp.build-blas-backends
name: build-blas-backends
category: computing-software
field: ai-ml-engineering
product: llama-cpp
tags: [llama-cpp, blas, openblas, blis, onemkl]
level: advanced
status: docs-checked
description: "Enable BLAS with GGML_BLAS and a vendor, plus the BLIS runtime environment variables."
sources: ["https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md", "https://github.com/ggml-org/llama.cpp/blob/master/docs/backend/BLIS.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BLAS builds

Enable with `-DGGML_BLAS=ON` and pick the library with `-DGGML_BLAS_VENDOR=...`. Per the build guide, BLAS may improve prompt processing for batch sizes higher than 32 (the default is 512) and does not affect generation speed.

```bash
cmake -B build -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS
cmake --build build --config Release
```

Variants in the guide:

- Accelerate Framework: macOS only, enabled by default; build normally.
- `OpenBLAS`: CPU-only BLAS; install OpenBLAS first.
- BLIS: vendor `FLAME`, see below.
- AMD AOCL-BLAS: the guide recommends the ZenDNN backend for AMD CPU inference, with AOCL as a vendor option of the generic BLAS backend. Source `amd-libs.cfg` from the AOCL install, then `cmake -B build -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=AOCL_mt -DBLAS_INCLUDE_DIRS="${AOCL_ROOT}/include" -DGGML_NATIVE=ON`. CMake 3.27+ is recommended for the AOCL / AOCL_mt vendors.
- Intel oneMKL: source `/opt/intel/oneapi/setvars.sh`, then `cmake -B build -DGGML_BLAS=ON -DGGML_BLAS_VENDOR=Intel10_64lp -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx -DGGML_NATIVE=ON`. This makes `avx_vnni` available on Intel CPUs without avx512; it does not support Intel GPU (use SYCL for that). `GGML_BLAS_VENDOR` defaults to `Generic`, so with the Intel environment already sourced `-DGGML_BLAS=ON` selects MKL.
- Any other BLAS library: set `GGML_BLAS_VENDOR` to a vendor value listed in the CMake FindBLAS documentation.

BLIS (docs/backend/BLIS.md): build BLIS with `./configure --enable-cblas -t openmp,pthreads auto` and `make -j`, install it, then configure llama.cpp with `-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=FLAME`. The doc recommends OpenMP because it is easier to change the cores used. At run time the example sets:

- `GOMP_CPU_AFFINITY="0-19"`
- `BLIS_NUM_THREADS=14`

(values are the page's example; adjust to your cores), then run the binaries as normal.

## Checked

Date: 2026-11-08. Confirmed against docs/build.md (BLAS Build) and docs/backend/BLIS.md. Removed: the wrong default batch size (2048; the page says 512), the "BLAS = 1" system-info claim, the advice about rebuilding from a clean directory, the "run with matching -t" claim, and 64-core example values not on the page.

Method: docs-only read of cited pages, 2026-11-08
