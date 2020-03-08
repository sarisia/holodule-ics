class HoloduleException(Exception):
    pass

class HTTPStatusError(HoloduleException):
    def __init__(self, status:int) -> None:
        super().__init__(f"http status is not success: {status}")
    