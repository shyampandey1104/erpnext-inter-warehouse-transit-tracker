"""Inter-Warehouse Stock Transfer, Virtual In-Transit Warehouse & Breakage Reconciliation Engine."""

import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class TransitTransferOrder(BaseModel):
    transfer_id: str
    source_warehouse: str
    target_warehouse: str
    transit_warehouse: str = "Virtual In-Transit Warehouse"
    transporter_name: str
    lorry_receipt_lr_number: str
    vehicle_number: str
    sku: str
    dispatched_quantity: int
    unit_cost_price: float
    freight_shipping_charge: float
    dispatched_at: str
    status: str = "IN_TRANSIT"  # IN_TRANSIT, RECEIVED_FULL, RECEIVED_WITH_LOSS


class DestinationReceiptAudit(BaseModel):
    receipt_id: str
    transfer_id: str
    sku: str
    dispatched_qty: int
    received_sound_qty: int
    transit_loss_or_damaged_qty: int
    total_transit_loss_value: float
    adjusted_unit_landed_cost: float
    claim_against_transporter_eligible: bool
    status: str


class InterWarehouseTransitEngine:
    """Manages multi-state inter-warehouse transfers, freight capitalisation, and transit loss accounting."""

    def __init__(self):
        self.transfers: Dict[str, TransitTransferOrder] = {}
        self.receipts: Dict[str, DestinationReceiptAudit] = {}

    def dispatch_stock_transfer(
        self,
        source_wh: str,
        target_wh: str,
        sku: str,
        qty: int,
        unit_cost: float,
        transporter: str,
        lr_no: str,
        vehicle_no: str,
        freight_charge: float,
        dispatch_date: str
    ) -> TransitTransferOrder:
        transfer_id = f"TRF-{uuid.uuid4().hex[:8].upper()}"
        order = TransitTransferOrder(
            transfer_id=transfer_id,
            source_warehouse=source_wh,
            target_warehouse=target_wh,
            transporter_name=transporter,
            lorry_receipt_lr_number=lr_no,
            vehicle_number=vehicle_no,
            sku=sku,
            dispatched_quantity=qty,
            unit_cost_price=unit_cost,
            freight_shipping_charge=freight_charge,
            dispatched_at=dispatch_date,
            status="IN_TRANSIT"
        )
        self.transfers[transfer_id] = order
        return order

    def receive_and_reconcile_at_destination(
        self,
        transfer_id: str,
        received_sound_qty: int,
        damaged_or_lost_qty: int
    ) -> DestinationReceiptAudit:
        order = self.transfers.get(transfer_id)
        if not order:
            raise ValueError(f"Transfer {transfer_id} not found.")

        if (received_sound_qty + damaged_or_lost_qty) != order.dispatched_quantity:
            raise ValueError("Sum of sound received and lost quantity must match dispatched total.")

        loss_val = damaged_or_lost_qty * order.unit_cost_price

        # Adjusted Landed Cost per unit at destination:
        # (Total Sound Base Value + Freight) / Received Sound Qty
        if received_sound_qty > 0:
            total_landed = (received_sound_qty * order.unit_cost_price) + order.freight_shipping_charge
            adjusted_unit_cost = round(total_landed / received_sound_qty, 2)
        else:
            adjusted_unit_cost = order.unit_cost_price

        # Claim eligibility: if loss > 0 and transporter liability active
        claim_eligible = damaged_or_lost_qty > 0

        status = "RECEIVED_FULL" if damaged_or_lost_qty == 0 else "RECEIVED_WITH_LOSS"
        order.status = status

        receipt_id = f"REC-{uuid.uuid4().hex[:8].upper()}"
        audit = DestinationReceiptAudit(
            receipt_id=receipt_id,
            transfer_id=transfer_id,
            sku=order.sku,
            dispatched_qty=order.dispatched_quantity,
            received_sound_qty=received_sound_qty,
            transit_loss_or_damaged_qty=damaged_or_lost_qty,
            total_transit_loss_value=round(loss_val, 2),
            adjusted_unit_landed_cost=adjusted_unit_cost,
            claim_against_transporter_eligible=claim_eligible,
            status=status
        )
        self.receipts[receipt_id] = audit
        return audit
