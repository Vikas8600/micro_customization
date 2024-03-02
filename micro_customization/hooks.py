app_name = "micro_customization"
app_title = "Micro Customization"
app_publisher = "micro_customization"
app_description = "micro_customization"
app_email = "author@email.com"
app_license = "apache-2.0"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/micro_customization/css/micro_customization.css"
# app_include_js = "/assets/micro_customization/js/micro_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/micro_customization/css/micro_customization.css"
# web_include_js = "/assets/micro_customization/js/micro_customization.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "micro_customization/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Purchase Invoice" : "public/js/purchase_invoice.js" 
}
doctype_list_js = {
    "Asset" : "public/js/list/asset.js"
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "micro_customization/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "micro_customization.utils.jinja_methods",
# 	"filters": "micro_customization.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "micro_customization.install.before_install"
# after_install = "micro_customization.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "micro_customization.uninstall.before_uninstall"
# after_uninstall = "micro_customization.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "micro_customization.utils.before_app_install"
# after_app_install = "micro_customization.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "micro_customization.utils.before_app_uninstall"
# after_app_uninstall = "micro_customization.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "micro_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Purchase Invoice": "micro_customization.micro_customization.overrides.purchase_invoice.CustomPurchaseInvoice"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Supplier": {
		"before_save": "micro_customization.micro_customization.overrides.supplier.before_save",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"micro_customization.tasks.all"
# 	],
# 	"daily": [
# 		"micro_customization.tasks.daily"
# 	],
# 	"hourly": [
# 		"micro_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"micro_customization.tasks.weekly"
# 	],
# 	"monthly": [
# 		"micro_customization.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "micro_customization.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "micro_customization.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "micro_customization.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["micro_customization.utils.before_request"]
# after_request = ["micro_customization.utils.after_request"]

# Job Events
# ----------
# before_job = ["micro_customization.utils.before_job"]
# after_job = ["micro_customization.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"micro_customization.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

fixtures = [
    {"dt": "Property Setter", "filters": [["module", "in", [app_title]]]},
    {"dt": "Custom Field", "filters": [["module", "=", app_title]]},
]
