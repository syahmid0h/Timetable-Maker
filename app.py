from flask import Flask, render_template, request, session
from timetable_logic import find_conflicts, build_timetable, DAYS

app = Flask(__name__)
app.secret_key = "SYAHMI AWESOME"

MAX_SUBJECTS = 12
INITIAL_VISIBLE = 3


@app.route("/", methods=["GET", "POST"])
def index():
    saved_form = session.get("form_data", {})

    if request.method == "POST":
        slots = []
        form_data = {}
        for i in range(1, MAX_SUBJECTS + 1):
            subject = request.form.get(f"subject{i}")
            type_ = request.form.get(f"type{i}")
            day = request.form.get(f"day{i}")
            start = request.form.get(f"start{i}")
            end = request.form.get(f"end{i}")
            if subject:
                form_data[f"subject{i}"] = subject or ""
                form_data[f"type{i}"] = type_ or ""
                form_data[f"day{i}"] = day or ""
                form_data[f"start{i}"] = start or ""
                form_data[f"end{i}"] = end or ""
            if subject and type_ and day and start and end:
                slots.append({
                    "subject": subject,
                    "type": type_,
                    "day": day,
                    "start": start,
                    "end": end
                })

        conflicts = find_conflicts(slots)
        session["form_data"] = form_data

        hours, grid = build_timetable(slots)

        return render_template(
            "result.html",
            slots=slots,
            conflicts=conflicts,
            hours=hours,
            days=DAYS,
            grid=grid,
        )
    return render_template("index.html", form_data=saved_form, max_subjects=MAX_SUBJECTS, initial_visible=INITIAL_VISIBLE)

if __name__ == "__main__":
    app.run(debug=True)
