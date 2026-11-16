# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "transit"
app_title = "Erpnext Inter Warehouse Transit Tracker"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Inter Warehouse Transit Tracker for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/transit/css/transit.bundle.css"
app_include_js = "/assets/transit/js/transit.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "transit.engine.on_document_submit",
        "on_cancel": "transit.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "transit.engine.daily_scheduled_sync"
    ]
}
