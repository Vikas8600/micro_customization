import frappe
from frappe.utils import now_datetime, add_days, formatdate

_status_after_pr = {
    "7 days after PR is created": 7,
    "15 days after PR is created": 15,
    "30 days after PR is created": 30,
    "30-45 days after PR is created": 30,
    "45 days after PR is created": 45,
    "60 days after PR is created": 60,
    "100 days after PR is created": 100
}

_status_after_invoice = {
    "7 days after invoice creation": 7,
    "45 days after invoice creation": 45,
    "60 days after invoice creation": 60,
    "90 days after invoice creation": 90,
    "135 days after invoice creation": 135
}


@frappe.whitelist()
def get_due_date_based_on_condition(pr):
    purchase_receipt = frappe.get_doc("Purchase Receipt", pr)
    purchase_order = frappe.get_doc("Purchase Order", purchase_receipt.items[0].purchase_order)
    
    payment_term = None
    if purchase_order.payment_schedule:
        payment_term = purchase_order.payment_schedule[0].payment_term
    
    if payment_term:
        due_date_based_on = frappe.get_value("Payment Term", payment_term, "due_date_based_on")
        
        if due_date_based_on in _status_after_invoice:
            days_to_add = _status_after_invoice[due_date_based_on]
            today_datetime = now_datetime()
            new_date = add_days(today_datetime, days_to_add)
            return {"due_date":frappe.utils.formatdate(new_date.date(), "yyyy-mm-dd")}
        elif due_date_based_on in _status_after_pr:
            days_to_add = _status_after_pr[due_date_based_on]
            today_datetime = purchase_receipt.posting_date
        else:
            # Handle the case when due_date_based_on is not in either dictionary
            if due_date_based_on in ["Completion of Work","On Installation"]:
                return {"status":True}
            return None
        
        new_date = add_days(today_datetime, days_to_add)
        return {"due_date":new_date}

    # Handle the case when payment_term is not found
    return None
