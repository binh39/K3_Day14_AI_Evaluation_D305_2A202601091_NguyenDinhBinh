"""Completed Part 2 solution.

The implementation lives in the repository-level template so it remains easy
to compare with the exercise starter; this module exposes the same public API
for the test suite and submission folder.
"""

import importlib.util
import sys
from pathlib import Path


_template_path = Path(__file__).resolve().parents[1] / "template.py"
_spec = importlib.util.spec_from_file_location("day14_template", _template_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Không thể nạp template từ {_template_path}")
_template = importlib.util.module_from_spec(_spec)
sys.modules["day14_template"] = _template
_spec.loader.exec_module(_template)

for _name in dir(_template):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_template, _name)
