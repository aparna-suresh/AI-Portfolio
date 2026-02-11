def operator_replace_string(left: str, right: str) -> str:
    if left is None or len(left) == 0:
        return right
    else:
        return left


def operator_replace_int(left: int, right: int) -> int:
    if left <= 0 < right:
        return right
    else:
        return left