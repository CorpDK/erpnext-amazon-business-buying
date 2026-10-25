import frappe

WORKFLOW_ROLES = ("Amazon Business Buyer", "Amazon Business Approver")


def after_install() -> None:
	_ensure_workflow_roles()


def after_migrate() -> None:
	_ensure_workflow_roles()


def _ensure_workflow_roles() -> None:
	for role_name in WORKFLOW_ROLES:
		if frappe.db.exists("Role", role_name):
			continue
		frappe.get_doc({"doctype": "Role", "role_name": role_name, "desk_access": 1}).insert(
			ignore_permissions=True
		)
