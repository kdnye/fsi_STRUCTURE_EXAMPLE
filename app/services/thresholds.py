from enum import Enum
from dataclasses import dataclass
from typing import Union, Tuple

class ThresholdStatus(Enum):
    SAFE = "SAFE"
    WARNING = "WARNING"
    BLOCKED = "BLOCKED"

@dataclass
class ValidationResult:
    status: ThresholdStatus
    message: str = ""
    value: float = 0.0

class LogisticsThresholds:
    # Standard FSI operational constants
    MAX_LTL_WEIGHT = 10000.0  # lbs
    MAX_EXPENDITURE_LIMIT = 5000.00  # USD
    WARNING_BUFFER = 0.90  # 90% of limit triggers a warning

    @classmethod
    def validate_shipment_weight(cls, weight: float) -> ValidationResult:
        """Evaluates weight against LTL (Less Than Truckload) standards."""
        if weight >= cls.MAX_LTL_WEIGHT:
            return ValidationResult(
                ThresholdStatus.BLOCKED, 
                f"Weight exceeds LTL maximum of {cls.MAX_LTL_WEIGHT} lbs."
            )
        
        if weight >= (cls.MAX_LTL_WEIGHT * cls.WARNING_BUFFER):
            return ValidationResult(
                ThresholdStatus.WARNING, 
                "Shipment is nearing maximum LTL capacity."
            )
            
        return ValidationResult(ThresholdStatus.SAFE)

    @classmethod
    def validate_budget(cls, amount: float, user_role: str) -> ValidationResult:
        """Evaluates spending based on RBAC authority."""
        # Supervisors have higher thresholds than Employees
        limit = cls.MAX_EXPENDITURE_LIMIT
        if user_role == "SUPERVISOR":
            limit *= 2.0  # Double limit for supervisors

        if amount > limit:
            return ValidationResult(
                ThresholdStatus.BLOCKED, 
                f"Amount exceeds individual spending limit of ${limit:,.2f}."
            )
            
        return ValidationResult(ThresholdStatus.SAFE)
