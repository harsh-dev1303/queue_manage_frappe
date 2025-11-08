import frappe

def execute():
    frappe.db.add_index("Queue Token",["service_center","status","created_at"],index_name="service_center_status_created_at")
    