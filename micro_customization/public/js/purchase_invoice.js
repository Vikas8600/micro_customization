frappe.ui.form.on('Purchase Invoice', {
    refresh: frm => {
        if(frm.doc.items){
            if(frm.doc.items[0].purchase_receipt){
                frappe.call({
                    method: 'micro_customization.api.purchase_invoice.get_due_date_based_on_condition',
                    args: { pr: frm.doc.items[0].purchase_receipt},
                    freeze: true,
                    callback: r => {
                        if(r.message.due_date){
                            frm.doc.payment_schedule[0].due_date = r.message.due_date;
                            frm.doc.due_date = r.message.due_date;
                            frm.set_df_property('cnp_section_break_wob2z', 'hidden', true);
                        }
                        else if(r.message.status){
                            frm.set_df_property('cnp_section_break_wob2z', 'hidden', false);
                        }

                    }})
                }
        
        }
        
    },
    before_save: frm => {
        let installation_date = frm.doc.cnp_installation_date
        let expected_installation_date = frm.doc.cnp_expected_installation_date
        if(frm.doc.cnp_is_installed && installation_date){
            frm.doc.payment_schedule[0].due_date = installation_date;
            frm.doc.due_date = installation_date;
        }
        else if(!frm.doc.cnp_is_installed && expected_installation_date){
            frm.doc.payment_schedule[0].due_date = expected_installation_date;
            frm.doc.due_date = expected_installation_date;
        }
    },
    cnp_expected_installation_date: frm => {
        update_due_date(frm)
    },
    cnp_installation_date: frm => {
        update_due_date(frm)
    }

    
})
function update_due_date(frm){
    let installation_date = frm.doc.cnp_installation_date
    let expected_installation_date = frm.doc.cnp_expected_installation_date
    if(frm.doc.cnp_is_installed && installation_date){
        frm.doc.payment_schedule[0].due_date = installation_date;
        frm.doc.due_date = installation_date;
    }
    else if(!frm.doc.cnp_is_installed && expected_installation_date){
        frm.doc.payment_schedule[0].due_date = expected_installation_date;
        frm.doc.due_date = expected_installation_date;
    }
}