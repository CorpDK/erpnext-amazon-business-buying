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
		if not self.is_new() and not _user_may_change_buyer_identity(frappe.session.user):
			before = self.get_doc_before_save()
			if before:
				if self.buyer_user != before.buyer_user:
					frappe.throw("Only System Manager may change Buyer User.")
				if self.buyer_email != before.buyer_email:
					frappe.throw("Only System Manager may change Buyer Email.")
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


def _user_may_change_buyer_identity(user: str) -> bool:
	if user == "Administrator":
		return True
	return "System Manager" in frappe.get_roles(user)


def _buyer_list_scope_applies(user: str) -> bool:
	if user == "Administrator":
		return False
	roles = set(frappe.get_roles(user))
	if "Amazon Business Buyer" not in roles:
		return False
	return not roles.intersection(_ELEVATED_ROLES)


def get_permission_query_conditions(user: str) -> str:
	if not _buyer_list_scope_applies(user):
		return ""
	escaped_user = frappe.db.escape(user)
	return f"`tabAmazon Business Purchase Request`.buyer_user = {escaped_user}"


def has_permission(doc, ptype: str, user: str) -> bool:
	if not _buyer_list_scope_applies(user):
		return True
	if ptype == "create" or doc.get("__islocal"):
		return True
	buyer_user = doc.get("buyer_user")
	return bool(buyer_user and buyer_user == user)
