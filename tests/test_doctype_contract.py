"""Validate shipped DocType JSON artifacts parse and name expected types."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCTYPE_ROOT = REPO_ROOT / "erpnext_amazon_business_buying" / "amazon_business_buying" / "doctype"

EXPECTED_DOCTYPES = {
	"Amazon Business Buying Settings",
	"Amazon Business Punch-in Storefront Secret",
	"Amazon Business Buying Company Config",
	"Amazon Business Buying Cost Center Approver",
	"Amazon Business Buying Buyer Map",
	"Amazon Business Purchase Request",
	"Amazon Business Purchase Request Item",
	"Amazon Business Punch-in Log",
}


class TestDocTypeContract(unittest.TestCase):
	def test_all_expected_doctype_json_present(self) -> None:
		found: set[str] = set()
		for path in DOCTYPE_ROOT.glob("**/*.json"):
			payload = json.loads(path.read_text(encoding="utf-8"))
			self.assertEqual(payload.get("doctype"), "DocType")
			name = payload.get("name")
			self.assertIsInstance(name, str)
			found.add(name)
			self.assertIn("fields", payload)
			self.assertIsInstance(payload["fields"], list)
		self.assertEqual(found, EXPECTED_DOCTYPES)

	def test_buying_settings_has_no_relay_pairing_fields(self) -> None:
		path = DOCTYPE_ROOT / "amazon_business_buying_settings" / "amazon_business_buying_settings.json"
		payload = json.loads(path.read_text(encoding="utf-8"))
		fieldnames = {field["fieldname"] for field in payload["fields"]}
		for forbidden in ("site_pairing_id", "pairing_secret", "relay_base_url", "relay_graphql_url"):
			self.assertNotIn(forbidden, fieldnames)


if __name__ == "__main__":
	unittest.main()
