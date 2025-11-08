# Copyright (c) 2025, BeginBe and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document


class ServiceCenter(Document):
	def autoname(self):
		initials = ''.join([word[0].upper() for word in self.name1.split()[:3]])
		last = frappe.db.count("Service Center") + 1
		self.name = f"{initials}-{last:03d}"
