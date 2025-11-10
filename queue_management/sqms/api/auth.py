import frappe
import jwt
import datetime
from frappe import _
from frappe.auth import LoginManager


SECRET_KEY = "  beginbe_secret_key"

@frappe.whitelist(allow_guest=True)
def signup(full_name,email,password,phone):
    if frappe.db.exists("User",email):
        frappe.throw(_("User already exists"))

    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,
        "enabled" : 1,
        "user_type" : "Website user",
        "new_password" : password,
    }).insert(ignore_permissions=True)

       # Assign roles manually
    user.append("roles", {"role": "Customer"})
    user.append("roles", {"role": "Website User"})
    user.save(ignore_permissions=True)

    customer = frappe.get_doc({
        "doctype": "Customer",
        "user": user.name,
        "name1" : full_name,
        "email" : email,
        "phone" : phone,
        "vip" : 0
    }).insert(ignore_permissions=True)
    


    frappe.db.commit()
    return{
        "message" : _("Signup successful"),
        "user_id" : user.name
    }

@frappe.whitelist(allow_guest=True)
def login(email,password):
    login_manager = frappe.auth.LoginManager()
    login_manager.authenticate(email,password)
    login_manager.post_login()  


    # # create session manually
    # frappe.local.login_manager = login_manager
    # frappe.local.cookie_manager = frappe.auth.CookieManager()
    # frappe.local.cookie_manager.init_cookies()


    return{
        "message" : _("Login Successfull"),
        "User" : login_manager.user,
        "sid" : frappe.session.sid
    }

@frappe.whitelist()
def logout():
    login_manager = LoginManager()
    login_manager.logout()
    # frappe.local.login_manager.logout()
    return{
        "message" : _("Logout Successfull")
    }


