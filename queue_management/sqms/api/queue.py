import frappe
import jwt
from frappe import _
from queue_management.constants import verify_token



@frappe.whitelist()
def join_queue(service_center):
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Please Login to join the queue"))

    customer = frappe.db.get_value("Customer",{"user" : user},"name")
    frappe.logger().info(f" Customer fetched: {customer}")
    if not customer:
        frappe.throw(_("No Customer record linked to this user"))

    if not frappe.db.exists("Service Center",service_center):
        frappe.throw(_("Service Center not found"))

    queue_token = frappe.get_doc({
        "doctype" : "Queue Token",
        "service_center" : service_center,
        "customer" : customer,
        "status" : "Created",
        "priority" : 0,
        "created_at" : frappe.utils.now_datetime()
    }).insert(ignore_permissions=True)
    frappe.logger().info(f" Queue Token created: {queue_token.name}")

    frappe.db.commit()
    return{
        "message" : _("Token Created Successfully"),
        "token_id" : queue_token.name
    }


@frappe.whitelist(allow_guest=True)
def service_center_list():
    centers = frappe.get_all("Service Center",fields=["name1","address","latitude","longitude","time_zone",
    "open_time","close_time"])

    return{
        "centers" : centers
    }

@frappe.whitelist()
def my_active_tokens():
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Please Login to view your active tokens"))

    customer = frappe.db.get_value("Customer",{"user" : user},"name1")
    if not customer:
        frappe.throw(_("No Customer record linked to this user"))

    active_tokens = frappe.get_all("Queue Token",filters={"customer" : customer},
    fields=["name","service_center","counter","status","created_at","estimated_wait"]
    )

    return{
        "active_tokens" : active_tokens
    }


