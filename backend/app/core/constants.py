# Price calculation constants
PRICE_MULTIPLIERS = {
    "horizontal": 1.0,
    "vertical": 1.2,
    "roller": 0.8,
    "panel": 1.5,
    "motorized": 2.0,
}

CONTROL_TYPE_MULTIPLIERS = {
    "manual": 1.0,
    "chain": 1.1,
    "motor": 2.5,
    "smart": 3.0,
}

# Price per square meter (base)
BASE_PRICE_PER_SQM = 500  # in currency units

# Stock warning threshold
LOW_STOCK_THRESHOLD_PERCENTAGE = 20  # warn when stock drops below 20%

# Order numbering
ORDER_NUMBER_PREFIX = "ORD"

# Production task numbering
TASK_NUMBER_PREFIX = "TASK"

# Maximum discount percentage
MAX_DISCOUNT_PERCENTAGE = 30

# Pagination defaults
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# File upload limits (in MB)
MAX_UPLOAD_SIZE_MB = 10

# Allowed file types for uploads
ALLOWED_FILE_TYPES = ["image/jpeg", "image/png", "application/pdf"]
