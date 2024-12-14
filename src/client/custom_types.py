from typing import Callable, Literal

type Writer = Callable[[str], None]

type Reader = Callable[[str], str]

type MenuOption = Literal["os", "compute", "default", "quit"]
