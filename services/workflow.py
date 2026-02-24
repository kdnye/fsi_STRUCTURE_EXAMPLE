# app/services/workflow.py
from app.services.thresholds import LogisticsThresholds, ThresholdStatus

def process_new_quote(user, weight, cost):
    # 1. Check Weight Safety
    weight_check = LogisticsThresholds.validate_shipment_weight(weight)
    if weight_check.status == ThresholdStatus.BLOCKED:
        return {"success": False, "error": weight_check.message}
        
    # 2. Check Financial Authority
    budget_check = LogisticsThresholds.validate_budget(cost, user.role.value)
    if budget_check.status == ThresholdStatus.BLOCKED:
        return {"success": False, "error": budget_check.message}
    
    # 3. Proceed with Persistence if checks pass
    # ... database logic here ...
    return {"success": True, "warning": weight_check.message if weight_check.status == ThresholdStatus.WARNING else None}
