app_name = "erpnext_amazon_business_buying"
app_title = "ERPNext Amazon Business Buying"
app_publisher = "CorpDK"
app_description = "Amazon Business Punch-in purchase request approval"
app_email = "ops@corpdk.local"
app_license = "GPL-3.0-or-later"

required_apps = ["erpnext_amazon_business"]

permission_query_conditions = {
	"Amazon Business Purchase Request": (
		"erpnext_amazon_business_buying.amazon_business_buying.doctype."
		"amazon_business_purchase_request.amazon_business_purchase_request."
		"get_permission_query_conditions"
	),
}

has_permission = {
	"Amazon Business Purchase Request": (
		"erpnext_amazon_business_buying.amazon_business_buying.doctype."
		"amazon_business_purchase_request.amazon_business_purchase_request."
		"has_permission"
	),
}

before_install = "erpnext_amazon_business_buying.patches.check_version_compatibility.execute"
before_migrate = "erpnext_amazon_business_buying.patches.check_version_compatibility.execute"

after_install = "erpnext_amazon_business_buying.install.after_install"
after_migrate = "erpnext_amazon_business_buying.install.after_migrate"

fixtures = [
	{
		"dt": "Workflow",
		"filters": [["name", "in", ["Amazon Business Purchase Request Approval"]]],
	},
]
