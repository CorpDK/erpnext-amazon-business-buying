import frappe
from frappe.model.document import Document

_ELEVATED_ROLES = frozenset(
	{
		"Amazon Business Approver",
		"Accounts Manager",
		"System Manager",
	}
)


class AmazonBusinessPurchaseRequest(Document):
	pass


def _buyer_list_scope_applies(user: str) -> bool:
	if user == "Administrator":
		return False
	roles = set(frappe.get_roles(user))
	if "Amazon Business Buyer" not in roles:
		return False
	return not roles.intersection(_ELEVATED_ROLES)


def _buyer_owns_request(user: str, buyer_user: str | None, buyer_email: str | None) -> bool:
	if buyer_user:
		return buyer_user == user
	user_email = frappe.db.get_value("User", user, "email")
	return bool(user_email and buyer_email and buyer_email == user_email)


def get_permission_query_conditions(user: str) -> str:
	if not _buyer_list_scope_applies(user):
		return ""
	user_email = frappe.db.get_value("User", user, "email") or ""
	escaped_user = frappe.db.escape(user)
	escaped_email = frappe.db.escape(user_email)
	return f"""(
		`tabAmazon Business Purchase Request`.buyer_user = {escaped_user}
		OR (
			IFNULL(`tabAmazon Business Purchase Request`.buyer_user, '') = ''
			AND `tabAmazon Business Purchase Request`.buyer_email = {escaped_email}
		)
	)"""


def has_permission(doc, ptype: str, user: str) -> bool:
	if not _buyer_list_scope_applies(user):
		return True
	return _buyer_owns_request(user, doc.get("buyer_user"), doc.get("buyer_email"))
