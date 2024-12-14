import json


class BaseErr(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        super().__init__(*args)
        self.msg = msg

    def to_json(self) -> str:
        return json.dumps({"status": "error", "message": self.msg})


class MissingTypeError(BaseErr):
    def __init__(self) -> None:
        super().__init__("missing_type")


class InvalidCmdTypeError(BaseErr):
    def __init__(self) -> None:
        super().__init__("invalid_cmd_type")


class MissingCmdError(BaseErr):
    def __init__(self) -> None:
        super().__init__("missing_cmd")


class InvalidExpressionError(BaseErr):
    def __init__(self) -> None:
        super().__init__("invalid_expression")


class InvalidCmdError(BaseErr):
    def __init__(self) -> None:
        super().__init__("invalid_cmd")


class InvalidMsgError(BaseErr):
    def __init__(self) -> None:
        super().__init__("invalid_msg")


class ServerError(BaseErr):
    def __init__(self) -> None:
        super().__init__("server_error")
