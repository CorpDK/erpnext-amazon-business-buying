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
	def before_insert(self) -> None:
		if not _buyer_list_scope_applies(frappe.session.user):
			return
		if not self.buyer_user:
			self.buyer_user = frappe.session.user
		if not self.buyer_email:
			email = frappe.db.get_value("User", frappe.session.user, "email")
			if email:
				self.buyer_email = email

	def validate(self) -> None:
		if not _buyer_list_scope_applies(frappe.session.user):
			return
		user = frappe.session.user
		if not self.buyer_user:
			self.buyer_user = user
		elif self.buyer_user != user:
			frappe.throw("Amazon Business Buyers cannot change Buyer User.")
		user_email = frappe.db.get_value("User", user, "email")
		if not self.buyer_email and user_email:
			self.buyer_email = user_email
		elif self.buyer_email and user_email and self.buyer_email != user_email:
			frappe.throw("Amazon Business Buyers cannot change Buyer Email.")


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
	escaped_user = frappe.db.escape(user)
	return f"`tabAmazon Business Purchase Request`.buyer_user = {escaped_user}"


def has_permission(doc, ptype: str, user: str) -> bool:
	if not _buyer_list_scope_applies(user):
		return True
	return _buyer_owns_request(user, doc.get("buyer_user"), doc.get("buyer_email"))
