app_name = "erpnext_amazon_business_buying"
app_title = "ERPNext Amazon Business Buying"
app_publisher = "CorpDK"
app_description = "Amazon Business Punch-in purchase request approval"
app_email = "ops@corpdk.local"
app_license = "GPL-3.0-or-later"

required_apps = ["erpnext_amazon_business"]

add_to_apps_screen = [
	{
		"name": app_name,
		"title": app_title,
		"route": "/app/amazon-business-buying",
		"has_permission": "erpnext_amazon_business_buying.permissions.has_app_permission",
	},
]

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
