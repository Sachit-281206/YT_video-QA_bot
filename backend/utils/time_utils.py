def seconds_to_mmss(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)

    return f"{minutes:02}:{seconds:02}"