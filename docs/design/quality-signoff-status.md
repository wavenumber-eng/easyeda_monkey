# Quality Signoff Status

EasyEDA Monkey uses the same public-package signoff shape planned for the
larger Wavenumber EDA tooling:

- pytest for executable behavior
- Rack strata for test organization
- `scripts/py_signoff.py` for source quality checks
- ruff for lint checks
- pyright for type checking public source and tests
- build, `twine check`, and installed-wheel smoke tests before release

The initial public split carries some inherited parser complexity from the
pre-public package. Those findings are recorded in
`scripts/py_signoff_baseline.json`. New code should not add to that baseline.

Future work should reduce the baseline by splitting high-complexity parsers
behind typed helper functions without changing EasyEDA format semantics.
