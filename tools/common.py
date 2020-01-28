def highlight(text, color=32):
    return f"\033[1;{color};20m {text} \033[0m"