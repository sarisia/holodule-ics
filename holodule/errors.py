class HoloduleException(Exception):
    pass

class HTTPStatusError(HoloduleException):
    def __init__(self, status:int, target:str="") -> None:
        super().__init__(f"http status is not success: {status}")
        self.target = target
    