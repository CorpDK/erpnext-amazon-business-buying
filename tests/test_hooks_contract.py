"""Hooks module exposes required_apps dependency on core Amazon Business app."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path

HOOKS_PATH = (
	Path(__file__).resolve().parents[1] / "erpnext_amazon_business_buying" / "hooks.py"
)


class TestHooksContract(unittest.TestCase):
	def test_required_apps_lists_core_amazon_business(self) -> None:
		tree = ast.parse(HOOKS_PATH.read_text(encoding="utf-8"))
		required: list[str] | None = None
		for node in tree.body:
			if isinstance(node, ast.Assign):
				for target in node.targets:
					if isinstance(target, ast.Name) and target.id == "required_apps":
						required = ast.literal_eval(node.value)
		self.assertEqual(required, ["erpnext_amazon_business"])


if __name__ == "__main__":
	unittest.main()
