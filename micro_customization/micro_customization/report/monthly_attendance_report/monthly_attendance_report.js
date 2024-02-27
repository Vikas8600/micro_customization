// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


frappe.query_reports["Monthly Attendance Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.str_to_obj(frappe.datetime.get_today()).getFullYear() + "-01-01"
		},
		{
			"fieldname": "to_date",
			"label": __("To"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.datetime.str_to_obj(frappe.datetime.get_today()).getFullYear() + "-01-31"
		},
		{
			"fieldname":"employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			get_query: () => {
				var company = frappe.query_report.get_filter_value('company');
				return {
					filters: {
						'company': company
					}
				};
			}
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"group_by",
			"label": __("Group By"),
			"fieldtype": "Select",
			"options": ["","Branch","Grade","Department","Designation"]
		},
		{
			"fieldname":"summarized_view",
			"label": __("Summarized View"),
			"fieldtype": "Check",
			"Default": 0,
		}
	],
	formatter: function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		const summarized_view = frappe.query_report.get_filter_value('summarized_view');
		const group_by = frappe.query_report.get_filter_value('group_by');

		if (!summarized_view) {
			if ((group_by && column.colIndex > 3) || (!group_by && column.colIndex > 2)) {
				if (value == 'P' || value == 'WFH')
					value = "<span style='color:green'>" + value + "</span>";
				else if (value == 'A')
					value = "<span style='color:red'>" + value + "</span>";
				else if (value == 'HD')
					value = "<span style='color:orange'>" + value + "</span>";
				else if (value == 'L')
					value = "<span style='color:#318AD8'>" + value + "</span>";
			}
		}

		return value;
	}
}
