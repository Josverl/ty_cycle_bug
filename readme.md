
Reproduction steps:

```pwsh
uv tool install ty
uv pip install -r pyproject.toml --extra stubs --target typings
$env:RUST_BACKTRACE=1
ty check
```

### expected result: 

`ty check` should complete without panicking

### actual result:

```
error[panic]: Panicked at C:\Users\runneradmin\.cargo\git\checkouts\salsa-e6f3bb7c2a062968\53421c2\src\function\fetch.rs:178:21 when checking `D:\mypython\!-stubtestprojects\ty_cycle_bug\src\report.py`: `dependency graph cycle when querying Type < 'db >::try_call_dunder_get_(Id(8c00)), set cycle_fn/cycle_initial to fixpoint iterate.
```

Both mypy and pyright complete without errors on the same codebase, so this seems to be a ty specific issue.
likely the ty configuration in pyproject.toml could be adjusted to avoid this by not including the `typing folder`,
but that results in ty not being able to find several stubs in the `typings` folder, and that is the issue I was trying to solve.

without the `typings` folder, ty reports a lot of errors about missing stubs, and that is not ideal either.
```
(ty_cycle_bug) PS D:\mypython\!-stubtestprojects\ty_cycle_bug> ty check
error[unresolved-import]: Cannot resolve imported module `uasyncio`
 --> src\report.py:1:6
  |
1 | from uasyncio import sleep_ms
  |      ^^^^^^^^
2 | from usys import print_exception
3 | from uos import mount, umount, statvfs
  |
info: Searched in the following paths during module resolution:
info:   1. D:\mypython\!-stubtestprojects\ty_cycle_bug\src\lib (extra search path specified on the CLI or in your config file)
info:   2. D:\mypython\!-stubtestprojects\ty_cycle_bug\src (first-party code)
info:   3. D:\mypython\!-stubtestprojects\ty_cycle_bug (first-party code)
info:   4. D:\mypython\!-stubtestprojects\ty_cycle_bug\typings\stdlib (custom stdlib stubs specified on the CLI or in your config file)
info:   5. D:\mypython\!-stubtestprojects\ty_cycle_bug\.venv\Lib\site-packages (site-packages)
info: make sure your Python environment is properly configured: https://docs.astral.sh/ty/modules/#python-environment
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Cannot resolve imported module `usys`
 --> src\report.py:2:6
  |
1 | from uasyncio import sleep_ms
2 | from usys import print_exception
  |      ^^^^
3 | from uos import mount, umount, statvfs
  |
info: Searched in the following paths during module resolution:
info:   1. D:\mypython\!-stubtestprojects\ty_cycle_bug\src\lib (extra search path specified on the CLI or in your config file)
info:   2. D:\mypython\!-stubtestprojects\ty_cycle_bug\src (first-party code)
info:   3. D:\mypython\!-stubtestprojects\ty_cycle_bug (first-party code)
info:   4. D:\mypython\!-stubtestprojects\ty_cycle_bug\typings\stdlib (custom stdlib stubs specified on the CLI or in your config file)
info:   5. D:\mypython\!-stubtestprojects\ty_cycle_bug\.venv\Lib\site-packages (site-packages)
info: make sure your Python environment is properly configured: https://docs.astral.sh/ty/modules/#python-environment
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Cannot resolve imported module `uos`
 --> src\report.py:3:6
  |
1 | from uasyncio import sleep_ms
2 | from usys import print_exception
3 | from uos import mount, umount, statvfs
  |      ^^^
4 |
5 | mount("/sd", "/sdcard")
  |
info: Searched in the following paths during module resolution:
info:   1. D:\mypython\!-stubtestprojects\ty_cycle_bug\src\lib (extra search path specified on the CLI or in your config file)
info:   2. D:\mypython\!-stubtestprojects\ty_cycle_bug\src (first-party code)
info:   3. D:\mypython\!-stubtestprojects\ty_cycle_bug (first-party code)
info:   4. D:\mypython\!-stubtestprojects\ty_cycle_bug\typings\stdlib (custom stdlib stubs specified on the CLI or in your config file)
info:   5. D:\mypython\!-stubtestprojects\ty_cycle_bug\.venv\Lib\site-packages (site-packages)
info: make sure your Python environment is properly configured: https://docs.astral.sh/ty/modules/#python-environment
info: rule `unresolved-import` is enabled by default
```

If i install the stubs into the .venv, ty can find the stubs and does not report any errors, but the cycle panic still occurs.

It may be that the cycle is caused by some of the stubs in the `typings` folder, but I have not been able to narrow it down yet.
If you have a suggestion for that that does not break pyright or mypy, im happy to try it out and update/improve the stubs.




Environment:
OS: Windows_NT x64 10.0.26200
- no .venv folder, ty is installed globally with uv tool install ty
- Python 3.11.9
- Same error occurs when using a uv created .venv with Python 3.11.9
- 

Error report

```
D:\mypython\!-stubtestprojects\ty_cycle_bug> ty check
error[panic]: Panicked at C:\Users\runneradmin\.cargo\git\checkouts\salsa-e6f3bb7c2a062968\53421c2\src\function\fetch.rs:178:21 when checking `D:\mypython\!-stubtestprojects\ty_cycle_bug\src\report.py`: `dependency graph cycle when querying Type < 'db >::try_call_dunder_get_(Id(8c00)), set cycle_fn/cycle_initial to fixpoint iterate.
Query stack:
[
    check_file_impl(Id(c00)),
    infer_scope_types_impl(Id(1000)),
    infer_definition_types(Id(1400)),
    Type < 'db >::member_lookup_with_policy_(Id(2800)),
    place_by_id(Id(3000)),
    dunder_all_names(Id(c40)),
    dunder_all_names(Id(c56)),
    infer_expression_types_impl(Id(3408)),
    Type < 'db >::member_lookup_with_policy_(Id(2801)),
    place_by_id(Id(3001)),
    infer_definition_types(Id(38e4)),
    infer_definition_types(Id(38e3)),
    FunctionType < 'db >::signature_(Id(4800)),
    infer_deferred_types(Id(39cb)),
    infer_definition_types(Id(3a96)),
    Type < 'db >::member_lookup_with_policy_(Id(2803)),
    Type < 'db >::class_member_with_policy_(Id(7c00)),
    enum_metadata(Id(5802)),
    enum_metadata(Id(5805)),
    infer_definition_types(Id(7071)),
    StaticClassLiteral < 'db >::explicit_bases_(Id(5807)),
    infer_deferred_types(Id(6410)),
    StaticClassLiteral < 'db >::explicit_bases_(Id(5808)),
    infer_deferred_types(Id(3b68)),
    infer_definition_types(Id(3ae4)),
    FunctionType < 'db >::signature_(Id(4802)),
    infer_deferred_types(Id(3abb)),
    infer_definition_types(Id(3a9d)),
    Type < 'db >::try_call_dunder_get_(Id(8c00)),
    Type < 'db >::class_member_with_policy_(Id(7c01)),
    place_by_id(Id(300d)),
    infer_definition_types(Id(3ded)),
    overloads_and_implementation_inner(Id(4404)),
    infer_definition_types(Id(3de9)),
    FunctionType < 'db >::signature_(Id(4803)),
    infer_deferred_types(Id(3a9f)),
    infer_definition_types(Id(3a94)),
]`
info: This indicates a bug in ty.
info: If you could open an issue at https://github.com/astral-sh/ty/issues/new?title=%5Bpanic%5D, we'd be very appreciative!
info: Platform: windows x86_64
info: Version: 0.0.17 (8cec85718 2026-02-13)
info: Args: ["c:\\users\\josverl\\.local\\bin\\ty.exe", "check"]
info: Backtrace:
   0: <unknown>
   1: <unknown>
   2: <unknown>
   3: <unknown>
   4: <unknown>
   5: <unknown>
   6: <unknown>
   7: <unknown>
   8: <unknown>
   9: <unknown>
  10: <unknown>
  11: <unknown>
  12: <unknown>
  13: <unknown>
  14: <unknown>
  15: <unknown>
  16: <unknown>
  17: <unknown>
  18: <unknown>
  19: <unknown>
  20: <unknown>
  21: <unknown>
  22: <unknown>
  23: <unknown>
  24: <unknown>
  25: <unknown>
  26: <unknown>
  27: <unknown>
  28: <unknown>
  29: <unknown>
  30: <unknown>
  31: <unknown>
  32: <unknown>
  33: <unknown>
  34: <unknown>
  35: <unknown>
  36: <unknown>
  37: <unknown>
  38: <unknown>
  39: <unknown>
  40: <unknown>
  41: <unknown>
  42: <unknown>
  43: <unknown>
  44: <unknown>
  45: <unknown>
  46: <unknown>
  47: <unknown>
  48: <unknown>
  49: <unknown>
  50: <unknown>
  51: <unknown>
  52: <unknown>
  53: <unknown>
  54: <unknown>
  55: <unknown>
  56: <unknown>
  57: <unknown>
  58: <unknown>
  59: <unknown>
  60: <unknown>
  61: <unknown>
  62: <unknown>
  63: <unknown>
  64: <unknown>
  65: <unknown>
  66: <unknown>
  67: <unknown>
  68: <unknown>
  69: <unknown>
  70: <unknown>
  71: <unknown>
  72: <unknown>
  73: <unknown>
  74: <unknown>
  75: <unknown>
  76: <unknown>
  77: <unknown>
  78: <unknown>
  79: <unknown>
  80: <unknown>
  81: <unknown>
  82: <unknown>
  83: <unknown>
  84: <unknown>
  85: <unknown>
  86: <unknown>
  87: <unknown>
  88: <unknown>
  89: <unknown>
  90: <unknown>
  91: <unknown>
  92: <unknown>
  93: <unknown>
  94: <unknown>
  95: <unknown>
  96: <unknown>
  97: <unknown>
  98: <unknown>
  99: <unknown>
 100: <unknown>
 101: <unknown>
 102: <unknown>
 103: <unknown>
 104: <unknown>
 105: <unknown>
 106: <unknown>
 107: <unknown>
 108: <unknown>
 109: <unknown>
 110: <unknown>
 111: <unknown>
 112: <unknown>
 113: <unknown>
 114: <unknown>
 115: <unknown>
 116: <unknown>
 117: <unknown>
 118: <unknown>
 119: <unknown>
 120: <unknown>
 121: <unknown>
 122: <unknown>
 123: <unknown>
 124: <unknown>
 125: <unknown>
 126: <unknown>
 127: <unknown>
 128: <unknown>
 129: <unknown>
 130: <unknown>
 131: <unknown>
 132: <unknown>
 133: <unknown>
 134: <unknown>
 135: <unknown>
 136: <unknown>
 137: <unknown>
 138: <unknown>
 139: <unknown>
 140: <unknown>
 141: <unknown>
 142: <unknown>
 143: <unknown>
 144: <unknown>
 145: <unknown>
 146: <unknown>
 147: <unknown>
 148: <unknown>
 149: <unknown>
 150: <unknown>
 151: <unknown>
 152: <unknown>
 153: <unknown>
 154: <unknown>
 155: <unknown>
 156: <unknown>
 157: <unknown>
 158: <unknown>
 159: <unknown>
 160: <unknown>
 161: <unknown>
 162: <unknown>
 163: <unknown>
 164: <unknown>
 165: <unknown>
 166: <unknown>
 167: <unknown>
 168: <unknown>
 169: <unknown>
 170: <unknown>
 171: <unknown>
 172: <unknown>
 173: <unknown>
 174: <unknown>
 175: <unknown>
 176: <unknown>
 177: <unknown>
 178: <unknown>
 179: <unknown>
 180: <unknown>
 181: <unknown>
 182: <unknown>
 183: <unknown>
 184: <unknown>
 185: <unknown>
 186: <unknown>
 187: <unknown>
 188: <unknown>
 189: <unknown>
 190: <unknown>
 191: <unknown>
 192: <unknown>
 193: <unknown>
 194: <unknown>
 195: <unknown>
 196: <unknown>
 197: <unknown>
 198: <unknown>
 199: <unknown>
 200: <unknown>
 201: <unknown>
 202: <unknown>
 203: <unknown>
 204: <unknown>
 205: <unknown>
 206: <unknown>
 207: <unknown>
 208: <unknown>
 209: <unknown>
 210: <unknown>
 211: <unknown>
 212: <unknown>
 213: <unknown>
 214: <unknown>
 215: <unknown>
 216: <unknown>
 217: <unknown>
 218: <unknown>
 219: <unknown>
 220: <unknown>
 221: <unknown>
 222: <unknown>
 223: <unknown>
 224: <unknown>
 225: <unknown>
 226: <unknown>
 227: <unknown>
 228: <unknown>
 229: <unknown>
 230: <unknown>
 231: <unknown>
 232: <unknown>
 233: <unknown>
 234: <unknown>
 235: <unknown>
 236: <unknown>
 237: <unknown>
 238: <unknown>
 239: <unknown>
 240: <unknown>
 241: <unknown>
 242: <unknown>
 243: <unknown>
 244: <unknown>
 245: <unknown>
 246: BaseThreadInitThunk
 247: RtlUserThreadStart

info: query stacktrace:
   0: infer_definition_types(Id(3a94))
             at crates\ty_python_semantic\src\types\infer.rs:68
             cycle heads: FunctionType < 'db >::signature_(Id(4800)) -> iteration = 0, Type < 'db >::member_lookup_with_policy_(Id(2803)) -> iteration = 0
   1: infer_deferred_types(Id(3a9f))
             at crates\ty_python_semantic\src\types\infer.rs:107
   2: FunctionType < 'db >::signature_(Id(4803))
             at crates\ty_python_semantic\src\types\function.rs:923
   3: infer_definition_types(Id(3de9))
             at crates\ty_python_semantic\src\types\infer.rs:68
   4: overloads_and_implementation_inner(Id(4404))
             at crates\ty_python_semantic\src\types\function.rs:702
   5: infer_definition_types(Id(3ded))
             at crates\ty_python_semantic\src\types\infer.rs:68
   6: place_by_id(Id(300d))
             at crates\ty_python_semantic\src\place.rs:860
   7: Type < 'db >::class_member_with_policy_(Id(7c01))
             at crates\ty_python_semantic\src\types.rs:834
             cycle heads: FunctionType < 'db >::signature_(Id(4800)) -> iteration = 0
   8: Type < 'db >::try_call_dunder_get_(Id(8c00))
             at crates\ty_python_semantic\src\types.rs:834
   9: infer_definition_types(Id(3a9d))
             at crates\ty_python_semantic\src\types\infer.rs:68
             cycle heads: FunctionType < 'db >::signature_(Id(4800)) -> iteration = 0, Type < 'db >::member_lookup_with_policy_(Id(2803)) -> iteration = 0
  10: infer_deferred_types(Id(3abb))
             at crates\ty_python_semantic\src\types\infer.rs:107
  11: FunctionType < 'db >::signature_(Id(4802))
             at crates\ty_python_semantic\src\types\function.rs:923
  12: infer_definition_types(Id(3ae4))
             at crates\ty_python_semantic\src\types\infer.rs:68
  13: infer_deferred_types(Id(3b68))
             at crates\ty_python_semantic\src\types\infer.rs:107
  14: StaticClassLiteral < 'db >::explicit_bases_(Id(5808))
             at crates\ty_python_semantic\src\types\class.rs:2146
  15: infer_deferred_types(Id(6410))
             at crates\ty_python_semantic\src\types\infer.rs:107
  16: StaticClassLiteral < 'db >::explicit_bases_(Id(5807))
             at crates\ty_python_semantic\src\types\class.rs:2146
  17: infer_definition_types(Id(7071))
             at crates\ty_python_semantic\src\types\infer.rs:68
  18: enum_metadata(Id(5805))
             at crates\ty_python_semantic\src\types\enums.rs:44
             cycle heads: enum_metadata(Id(5805)) -> iteration = 0
  19: enum_metadata(Id(5802))
             at crates\ty_python_semantic\src\types\enums.rs:44
  20: Type < 'db >::class_member_with_policy_(Id(7c00))
             at crates\ty_python_semantic\src\types.rs:834
             cycle heads: FunctionType < 'db >::signature_(Id(4800)) -> iteration = 0
  21: Type < 'db >::member_lookup_with_policy_(Id(2803))
             at crates\ty_python_semantic\src\types.rs:834
  22: infer_definition_types(Id(3a96))
             at crates\ty_python_semantic\src\types\infer.rs:68
             cycle heads: FunctionType < 'db >::signature_(Id(4800)) -> iteration = 0
  23: infer_deferred_types(Id(39cb))
             at crates\ty_python_semantic\src\types\infer.rs:107
  24: FunctionType < 'db >::signature_(Id(4800))
             at crates\ty_python_semantic\src\types\function.rs:923
  25: infer_definition_types(Id(38e3))
             at crates\ty_python_semantic\src\types\infer.rs:68
  26: infer_definition_types(Id(38e4))
             at crates\ty_python_semantic\src\types\infer.rs:68
  27: place_by_id(Id(3001))
             at crates\ty_python_semantic\src\place.rs:860
  28: Type < 'db >::member_lookup_with_policy_(Id(2801))
             at crates\ty_python_semantic\src\types.rs:834
  29: infer_expression_types_impl(Id(3408))
             at crates\ty_python_semantic\src\types\infer.rs:222
  30: dunder_all_names(Id(c56))
             at crates\ty_python_semantic\src\dunder_all.rs:16
  31: dunder_all_names(Id(c40))
             at crates\ty_python_semantic\src\dunder_all.rs:16
  32: place_by_id(Id(3000))
             at crates\ty_python_semantic\src\place.rs:860
  33: Type < 'db >::member_lookup_with_policy_(Id(2800))
             at crates\ty_python_semantic\src\types.rs:834
  34: infer_definition_types(Id(1400))
             at crates\ty_python_semantic\src\types\infer.rs:68
  35: infer_scope_types_impl(Id(1000))
             at crates\ty_python_semantic\src\types\infer.rs:185
  36: check_file_impl(Id(c00))
             at crates\ty_project\src\lib.rs:569
```


### pyright and mypy

reports are not identical, due to a slightly different configuration, but both report no errors on the same codebase



```
(ty_cycle_bug) PS D:\mypython\!-stubtestprojects\ty_cycle_bug> mypy .\src\report.py
Success: no issues found in 1 source file
(ty_cycle_bug) PS D:\mypython\!-stubtestprojects\ty_cycle_bug> mypy
Success: no issues found in 1 source file
(ty_cycle_bug) PS D:\mypython\!-stubtestprojects\ty_cycle_bug> pyright
Defined constant "sys" must be associated with a boolean or string value.
d:\mypython\!-stubtestprojects\ty_cycle_bug\src\report.py
  d:\mypython\!-stubtestprojects\ty_cycle_bug\src\report.py:3:17 - warning: The function "mount" is deprecated
    The `mount` function is deprecated, use `vfs.mount` instead. (reportDeprecated)
  d:\mypython\!-stubtestprojects\ty_cycle_bug\src\report.py:3:24 - warning: The function "umount" is deprecated
    The `umount` function is deprecated, use `vfs.umount` instead. (reportDeprecated)
  d:\mypython\!-stubtestprojects\ty_cycle_bug\src\report.py:5:1 - warning: The function "mount" is deprecated
    The `mount` function is deprecated, use `vfs.mount` instead. (reportDeprecated)
0 errors, 3 warnings, 0 informations
```