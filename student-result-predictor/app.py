from flask import Flask, render_template, request
import joblib

app = Flask(__name__)
MODEL_VERSION = "1.0"
MODEL_PATH = "student_model.joblib"
model = joblib.load(MODEL_PATH)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            study_hours = float(request.form["study_hours"])
            attendance = float(request.form["attendance"])
            internal_marks = float(request.form["internal_marks"])

            if not 0 <= study_hours <= 24:
                raise ValueError("Study hours must be between 0 and 24.")
            if not 0 <= attendance <= 100:
                raise ValueError("Attendance must be between 0 and 100.")
            if not 0 <= internal_marks <= 100:
                raise ValueError("Internal marks must be between 0 and 100.")

            result = model.predict([[study_hours, attendance, internal_marks]])[0]
            prediction = "Pass" if int(result) == 1 else "Fail"
        except (ValueError, KeyError) as exc:
            error = str(exc) or "Please enter valid numbers."

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        version=MODEL_VERSION
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
