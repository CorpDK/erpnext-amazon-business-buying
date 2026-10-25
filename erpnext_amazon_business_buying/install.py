import frappe


def after_install() -> None:
	_ensure_buying_settings_defaults()


def after_migrate() -> None:
	_ensure_buying_settings_defaults()


def _ensure_buying_settings_defaults() -> None:
	if not frappe.db.exists("DocType", "Amazon Business Buying Settings"):
		return
	settings = frappe.get_single("Amazon Business Buying Settings")
	changed = False
	if not settings.punchin_path_prefix:
		settings.punchin_path_prefix = "/punchin"
		changed = True
	if not settings.company_resolution_mode:
		settings.company_resolution_mode = "By buyer email map"
		changed = True
	if settings.enable_buyer_portal is None:
		settings.enable_buyer_portal = 0
		changed = True
	if changed:
		settings.save(ignore_permissions=True)
