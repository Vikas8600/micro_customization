
frappe.ui.form.on('Purchase Invoice', {
    refresh: frm => {
        if (frm.doc.items) {
            if (frm.doc.items[0].purchase_receipt) {
                frappe.call({
                    method: 'micro_customization.api.purchase_invoice.get_due_date_based_on_condition',
                    args: { pr: frm.doc.items[0].purchase_receipt },
                    freeze: true,
                    callback: r => {
                        if (r.message.due_date) {
                            frm.set_df_property('cnp_section_break_wob2z', 'hidden', true);
                        }
                        else if (r.message.status) {
                            frm.set_df_property('cnp_section_break_wob2z', 'hidden', false);
                        }
                    }
                })

            }
        }
    },
    before_save: frm => {
        if (frm.doc.items) {
            if (frm.doc.items[0].purchase_receipt) {
                frappe.call({
                    method: 'micro_customization.api.purchase_invoice.get_due_date_based_on_condition',
                    args: { pr: frm.doc.items[0].purchase_receipt },
                    freeze: true,
                    callback: r => {
                        if (r.message.due_date) {
                            frm.doc.payment_schedule[0].due_date = r.message.due_date;
                            frm.doc.due_date = r.message.due_date;
                        }
                        else if (r.message.status) {
                            let installation_date = frm.doc.cnp_installation_date
                            let expected_installation_date = frm.doc.cnp_expected_installation_date
                            if (frm.doc.cnp_is_installed && installation_date) {
                                frm.doc.payment_schedule[0].due_date = installation_date;
                                frm.doc.due_date = installation_date;
                            }
                            else if (!frm.doc.cnp_is_installed && expected_installation_date) {
                                frm.doc.payment_schedule[0].due_date = expected_installation_date;
                                frm.doc.due_date = expected_installation_date;
                            }
                        }

                    }
                })
            }

        }
        if(frm.doc.taxes){
            frm.doc.taxes.forEach(element=>{
                if(element.rate!=0 && element.add_deduct_tax=="Deduct"){
                    element.tax_amount = (element.rate *element.total)/100
                    element.total = element.total - element.tax_amount
                }
            })
            frm.refresh_field('taxes');
        }

    },
    cnp_expected_installation_date: frm => {
        update_due_date(frm)
    },
    cnp_installation_date: frm => {
        update_due_date(frm)
    },
    on_update: frm =>{
        

    },
    supplier: frm =>{
        if(frm.doc.supplier){            
        frappe.call({
            method: 'micro_customization.micro_customization.overrides.purchase_invoice.get_supplier_tds_details',
            args: { supplier: frm.doc.supplier },
            freeze: true,
            callback: r => {
                if (r.message) {
                    r.message.forEach(element => {
                        let existingRow ;
                        if(frm.doc.taxes){
                            existingRow = frm.doc.taxes.find(row => row.account_head === element.account_head);   
                        }
                        else{
                            existingRow = false;
                        }
                        if (!existingRow) {
                            const row = frm.add_child('taxes');
                            row.charge_type = "Actual";
                            row.account_head = element.account_head;
                            row.add_deduct_tax = "Deduct";
                            row.description = element.charge_type;
                            row.total = 0.0;
                            row.rate = 0.0;
                        }
                    });
                    frm.refresh_field('taxes');
                }
            }
        })
    }
    }


})


function update_due_date(frm) {
    let installation_date = frm.doc.cnp_installation_date
    let expected_installation_date = frm.doc.cnp_expected_installation_date
    if (frm.doc.cnp_is_installed && installation_date) {
        frm.doc.payment_schedule[0].due_date = installation_date;
        frm.doc.due_date = installation_date;
    }
    else if (!frm.doc.cnp_is_installed && expected_installation_date) {
        frm.doc.payment_schedule[0].due_date = expected_installation_date;
        frm.doc.due_date = expected_installation_date;
    }
}
erpnext.taxes.set_conditional_mandatory_rate_or_amount = function(grid_row) {
	if(grid_row) {
		if(grid_row.doc.charge_type==="Actual") {
			grid_row.toggle_editable("tax_amount", true);
			grid_row.toggle_reqd("tax_amount", true);
			grid_row.toggle_editable("rate", true);
			grid_row.toggle_reqd("rate", false);
		} else {
			grid_row.toggle_editable("rate", true);
			grid_row.toggle_reqd("rate", true);
			grid_row.toggle_editable("tax_amount", false);
			grid_row.toggle_reqd("tax_amount", false);
		}
	}
}

erpnext.taxes_and_totals.prototype.set_cumulative_total= function(row_idx, tax) {
    if(tax.add_deduct_tax=="Deduct" && this.frm.doc.apply_tds && this.frm.doc.cnp_multi_tsd){
        tax.total = this.frm.doc.items[row_idx].amount
    }
    else{
        var tax_amount = tax.tax_amount_after_discount_amount;
		if (tax.category == 'Valuation') {
			tax_amount = 0;
		}

		if (tax.add_deduct_tax == "Deduct") { tax_amount = -1*tax_amount; }
        if(row_idx==0) {
			tax.total = flt(this.frm.doc.net_total + tax_amount, precision("total", tax));
		} else {
			tax.total = flt(this.frm.doc["taxes"][row_idx-1].total + tax_amount, precision("total", tax));
		}
    }
}