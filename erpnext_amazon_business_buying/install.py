import frappe

WORKFLOW_ROLES = ("Amazon Business Buyer", "Amazon Business Approver")


def after_install() -> None:
	_ensure_workflow_roles()
	_ensure_buying_settings_defaults()


def after_migrate() -> None:
	_ensure_workflow_roles()
	_ensure_buying_settings_defaults()


def _ensure_workflow_roles() -> None:
	for role_name in WORKFLOW_ROLES:
		if frappe.db.exists("Role", role_name):
			continue
		frappe.get_doc({"doctype": "Role", "role_name": role_name, "desk_access": 1}).insert(
			ignore_permissions=True
		)


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
