def analyze_risk(cmd: str):
    lower = cmd.lower()

    dangerous = [
        "rm -rf",
        "rm -r",
        ":>",
        "> ",
        "sudo ",
        "mkfs",
        "dd if=",
    ]

    for d in dangerous:
        if d in lower:
            return "HIGH"

        if "rm" in lower:
            return "MEDIUM"

    return "LOW"
