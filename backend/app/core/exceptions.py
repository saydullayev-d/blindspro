from fastapi import HTTPException, status


class BlindSProException(Exception):
    """Base exception for BlindsPro"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(BlindSProException):
    """Resource not found"""
    def __init__(self, resource: str, resource_id: int):
        super().__init__(f"{resource} with id {resource_id} not found", 404)


class ValidationError(BlindSProException):
    """Validation error"""
    def __init__(self, message: str):
        super().__init__(f"Validation error: {message}", 422)


class UnauthorizedError(BlindSProException):
    """Unauthorized access"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)


class ForbiddenError(BlindSProException):
    """Forbidden access"""
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, 403)


class ConflictError(BlindSProException):
    """Resource already exists"""
    def __init__(self, message: str):
        super().__init__(message, 409)


class LowStockError(BlindSProException):
    """Insufficient stock"""
    def __init__(self, material: str, available: int, required: int):
        super().__init__(
            f"Insufficient stock for {material}. Available: {available}, Required: {required}",
            400
        )


def to_http_exception(exc: BlindSProException) -> HTTPException:
    """Convert BlindSProException to HTTPException"""
    return HTTPException(status_code=exc.status_code, detail=exc.message)
