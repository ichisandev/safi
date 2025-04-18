from utils import config

def get_regex():
    names = "|".join(config.NICKNAME_LIST)
    # struct a regex string that will be used to call the bot
    regex_string = r"\s("+f"{names}" + r")\b|\b(" + f"{names}"+r")\s|\A("+f"{names}"+r")|@("+f"{names}"+r")"
    return regex_string
