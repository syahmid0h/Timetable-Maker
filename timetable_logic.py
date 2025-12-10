from datetime import datetime

def convert_to_24h(time_str):
    normalized = time_str.strip().upper()
    normalized = normalized.replace(" ", "")

    try:
        dt = datetime.strptime(normalized, "%I:%M%p")
    except ValueError:
        dt = datetime.strptime(normalized, "%H:%M")

    return dt.strftime("%H:%M")

def time_to_minutes(time_str):
    """Convert any supported time string to minutes since midnight."""
    converted = convert_to_24h(time_str)
    hours, minutes = map(int, converted.split(":"))
    return hours * 60 + minutes

def overlap(start1, end1, start2, end2):
    """Check if two time intervals overlap"""
    s1 = time_to_minutes(start1)
    e1 = time_to_minutes(end1)
    s2 = time_to_minutes(start2)
    e2 = time_to_minutes(end2)
    return s1 < e2 and s2 < e1

def find_conflicts(slots):
    """
    slots = [
        {"subject": "OOP", "type": "Lecture", "day": "Monday", "start": "10:00", "end": "12:00"},
        {"subject": "OS", "type": "Tutorial", "day": "Monday", "start": "11:00", "end": "12:30"}
    ]
    """
    conflicts = []
    for i in range(len(slots)):
        for j in range(i + 1, len(slots)):
            a = slots[i]
            b = slots[j]
            if a["day"] == b["day"] and overlap(a["start"], a["end"], b["start"], b["end"]):
                conflicts.append((a, b))
    return conflicts


# timetable result
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

def build_timetable(slots, start_hour=8, end_hour=20):
    """
    Build a simple 1-hour granularity timetable grid.
    Each slot is only placed in its starting hour, with span_hours calculated.
    """
    hours = list(range(start_hour, end_hour))
    grid = {hour: {day: [] for day in DAYS} for hour in hours}

    for slot in slots:
        start_m = time_to_minutes(slot["start"])
        end_m = time_to_minutes(slot["end"])

        slot["start_minutes"] = start_m
        slot["end_minutes"] = end_m

        # Find the starting hour for this slot
        start_hour_idx = None
        span_hours = 0

        for hour in hours:
            block_start = hour * 60
            block_end = (hour + 1) * 60

            if start_m < block_end and end_m > block_start:
                if start_hour_idx is None:
                    start_hour_idx = hour
                span_hours += 1

        # Only add the slot to its starting hour, with span info
        if start_hour_idx is not None:
            slot["start_hour"] = start_hour_idx
            slot["span_hours"] = span_hours
            day = slot["day"]
            if day in grid[start_hour_idx]:
                grid[start_hour_idx][day].append(slot)

    return hours, grid