from flask import Flask, render_template, request

from bmi_logic import (
    bmi_gauge_position,
    bmi_guidance,
    military_guidance,
    parse_bmi_inputs,
    parse_positive_number,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    height_input = ""
    weight_input = ""
    target_bmi_input = ""
    errors = {}
    military_errors = {}
    target_errors = {}
    result = None
    military_result = None
    target_result = None

    if request.method == "POST":
        feature = request.form.get("feature", "bmi")
        if feature == "target":
            height_input, weight_input, bmi, target_errors = parse_bmi_inputs(request.form)
            target_bmi_input = request.form.get("target_bmi", "").strip()
            target_bmi = parse_positive_number(target_bmi_input)
            if target_bmi is None or not 10 <= target_bmi <= 60:
                target_errors["target_bmi"] = "請輸入 10 到 60 之間的有效目標 BMI。"
            if not target_errors:
                height = float(height_input)
                weight = float(weight_input)
                height_meters = height / 100
                target_weight = target_bmi * height_meters * height_meters
                target_result = {
                    "current_bmi": f"{bmi:.1f}",
                    "target_bmi": f"{target_bmi:.1f}",
                    "target_weight": f"{target_weight:.1f}",
                    "weight_change": f"{target_weight - weight:+.1f}",
                }
        elif feature == "military":
            height_input, weight_input, bmi, military_errors = parse_bmi_inputs(request.form)
            if not military_errors:
                military_result = {
                    "bmi": f"{bmi:.1f}",
                    **military_guidance(float(height_input), bmi),
                }
        else:
            height_input, weight_input, bmi, errors = parse_bmi_inputs(request.form)
            if not errors:
                displayed_bmi = round(bmi, 1)
                result = {
                    "bmi": f"{displayed_bmi:.1f}",
                    "gauge_position": bmi_gauge_position(displayed_bmi),
                    **bmi_guidance(displayed_bmi),
                }

    return render_template(
        "index.html",
        height_input=height_input,
        weight_input=weight_input,
        target_bmi_input=target_bmi_input,
        errors=errors,
        military_errors=military_errors,
        target_errors=target_errors,
        result=result,
        military_result=military_result,
        target_result=target_result,
    )


if __name__ == "__main__":
    app.run(debug=True)
