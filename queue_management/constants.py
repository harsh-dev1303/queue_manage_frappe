import frappe
from frappe import _
import jwt



SECRET_KEY = "  beginbe_secret_key"

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["user"]
    except jwt.ExpiredSignatureError:
        frappe.throw(_("Token expired, please login again"))
    except jwt.InvalidTokenError:
        frappe.throw(_("Invalid token"))