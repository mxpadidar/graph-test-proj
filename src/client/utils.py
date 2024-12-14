from client.custom_types import MenuOption, Reader, Writer


def write_user(msg: str) -> None:
    """write message to the user"""
    print(msg)


def read_user(prompt: str, writer: Writer = write_user) -> str:
    """read user input and return the entered value"""
    text = input(f"{prompt}: ")
    if not text:
        writer("validation error, enter a valid value")
        return read_user(prompt, writer)
    return text


def menu(reader: Reader = read_user, writer: Writer = write_user) -> MenuOption:
    """display choices for the user and return the selected option"""

    writer("`0` -> exit; `1` -> os command; `2` -> compute command; `3` -> exec default messages, `0` to quit")
    while True:
        choice = reader("enter choice")
        match choice:
            case "1":
                return "os"
            case "2":
                return "compute"
            case "3":
                return "default"
            case "0":
                return "quit"
            case _:
                writer("Invalid choice, enter `0` to quit")
