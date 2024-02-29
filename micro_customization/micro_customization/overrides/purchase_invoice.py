from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice


class CustomPurchaseInvoice(PurchaseInvoice):
    def validate(self):
        taxes = self.get("taxes")
        tax_dict = {tax.name: tax.rate for tax in taxes if tax.charge_type == 'Actual'}
        super(CustomPurchaseInvoice, self).validate()
        for tax in self.taxes:
            if tax.charge_type == 'Actual':
                tax.rate = tax_dict[tax.name]