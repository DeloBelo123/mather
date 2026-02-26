# AGENTS.md

## Cursor Cloud specific instructions

This is a small Python 3.12 math library ("Kurvendiskussion" / curve analysis) with German naming conventions. It has no web UI, no services, no database — it is a pure Python library.

### Project structure

- `src/mather.py` — Data models (`Term`, `AbsolutesGlied`, `Punkt`, etc.) using Pydantic
- `src/regex.py` — Parses function strings (e.g. `"-2x^3 +15x^2 -24x +10"`) into `Term` objects
- `src/funktion.py` — Main `Funktion` class with all math operations (derivatives, roots, extrema, etc.)
- `test.py` — Manual test script exercising the library

### Running

```bash
python3 test.py
```

### Dependencies

Only external dependency is `pydantic`. No `requirements.txt` exists in the repo; install with `pip install pydantic`.

### Notes

- There is no test framework (pytest, unittest, etc.) — `test.py` is a simple script, not a test suite.
- There is no linter, formatter, or type checker configured.
- There is no build step — this is a pure Python library run directly.
