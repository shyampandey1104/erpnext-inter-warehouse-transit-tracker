# ERPNext Inter-Warehouse In-Transit Tracker 🚚🛣️

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise multi-state inter-warehouse stock transfer, virtual in-transit warehouse custody, Lorry Receipt (LR) tracking, transit shrinkage loss, and freight landed cost adjustment engine for **ERPNext Inventory & Supply Chain**.

---

## 🚀 Key Features

- **Virtual In-Transit Stock Custody**: Transfers stock from origin warehouse into a dedicated in-transit virtual account to maintain balance sheet accuracy during multi-day highway transit.
- **Transporter LR & Vehicle Audit**: Captures Lorry Receipt numbers, driver phone contacts, vehicle GPS tracking, and delivery timelines.
- **Transit Loss & Breakage Ledger**: Distinguishes between sound accepted quantities and transit damages to automatically generate transporter liability claims.
- **Landed Freight Capitalisation**: Proportionally distributes transport freight charges across accepted destination units to re-value local inventory costs.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/erpnext-inter-warehouse-transit-tracker.git
cd erpnext-inter-warehouse-transit-tracker
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from transit.engine import InterWarehouseTransitEngine

engine = InterWarehouseTransitEngine()

# Dispatch from Mother Hub to Regional DC
transfer = engine.dispatch_stock_transfer(
    source_wh="Mother Hub Bhiwandi",
    target_wh="Regional DC Kolkata",
    sku="SOLAR-INVERTER-5KW",
    qty=50,
    unit_cost=32000.0,
    transporter="TCI Express",
    lr_no="TCI-99021",
    vehicle_no="MH-04-AB-1234",
    freight_charge=18000.0,
    dispatch_date="2026-09-10"
)

# Inward and reconcile at destination
receipt = engine.receive_and_reconcile_at_destination(
    transfer_id=transfer.transfer_id,
    received_sound_qty=49,
    damaged_or_lost_qty=1
)
print(f"Status: {receipt.status} | Adjusted Landed Cost: ₹{receipt.adjusted_unit_landed_cost} | Transporter Claim: {receipt.claim_against_transporter_eligible}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
