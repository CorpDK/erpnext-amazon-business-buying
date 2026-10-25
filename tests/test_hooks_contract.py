"""Hooks module exposes required_apps dependency on core Amazon Business app."""

from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
	sys.path.insert(0, str(REPO_ROOT))


class TestHooksContract(unittest.TestCase):
	def test_required_apps_lists_core_amazon_business(self) -> None:
		hooks = importlib.import_module("erpnext_amazon_business_buying.hooks")
		self.assertEqual(hooks.required_apps, ["erpnext_amazon_business"])


if __name__ == "__main__":
	unittest.main()
