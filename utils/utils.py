def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}:{milliseconds:03d}"

def time_to_seconds(time_str):
    h, m, s, ms = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s + ms / 1000
