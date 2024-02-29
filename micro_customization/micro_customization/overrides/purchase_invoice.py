from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
import frappe
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import (
	get_party_tax_withholding_details,
)

class CustomPurchaseInvoice(PurchaseInvoice):
    def validate(self):
        taxes = self.get("taxes")
        tax_dict = {tax.name: tax.rate for tax in taxes if tax.charge_type == 'Actual'}
        super(CustomPurchaseInvoice, self).validate()
        for tax in self.taxes:
            if tax.charge_type == 'Actual':
                if tax.name:
                    tax.rate = tax_dict[tax.name]
    
    def set_tax_withholding(self):
        if not self.apply_tds:
            return

        if self.apply_tds and not self.get("tax_withholding_category"):
            self.tax_withholding_category = frappe.db.get_value(
                "Supplier", self.supplier, "tax_withholding_category"
            )
        supplie_tds = frappe.get_doc("Supplier",self.supplier)

        if supplie_tds.cnp_tds_details:
            return
        
        if not self.tax_withholding_category :
            return

        tax_withholding_details, advance_taxes, voucher_wise_amount = get_party_tax_withholding_details(
            self, self.tax_withholding_category
        )

        # Adjust TDS paid on advances
        self.allocate_advance_tds(tax_withholding_details, advance_taxes)

        if not tax_withholding_details:
            return

        accounts = []
        for d in self.taxes:
            if d.account_head == tax_withholding_details.get("account_head"):
                d.update(tax_withholding_details)

            accounts.append(d.account_head)

        if not accounts or tax_withholding_details.get("account_head") not in accounts:
            self.append("taxes", tax_withholding_details)

        to_remove = [
            d
            for d in self.taxes
            if not d.tax_amount and d.account_head == tax_withholding_details.get("account_head")
        ]

        for d in to_remove:
            self.remove(d)

        ## Add pending vouchers on which tax was withheld
        self.set("tax_withheld_vouchers", [])

        for voucher_no, voucher_details in voucher_wise_amount.items():
            self.append(
                "tax_withheld_vouchers",
                {
                    "voucher_name": voucher_no,
                    "voucher_type": voucher_details.get("voucher_type"),
                    "taxable_amount": voucher_details.get("amount"),
                },
            )

        # calculate totals again after applying TDS
        self.calculate_taxes_and_totals()


@frappe.whitelist()
def get_supplier_tds_details(supplier):
    records = []
    supplier_tds = frappe.get_doc("Supplier", supplier)
    if not supplier_tds.cnp_tds_details:
        return None
    
    for tax in supplier_tds.cnp_tds_details:
        tax_withholding_cat = frappe.get_doc("Tax Withholding Category", tax.tax_withholding_category)
        if tax_withholding_cat.accounts:
            for account in tax_withholding_cat.accounts:
                data = {}
                data["charge_type"] = tax.tax_withholding_category
                data["account_head"] = account.account
                records.append(data)
    return records