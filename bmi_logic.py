import math


def bmi_guidance(bmi):
    if bmi < 18.5:
        return {
            "label": "體重過輕",
            "tone": "low",
            "advice": "留意是否攝取足夠且均衡的營養，規律進食並搭配適度肌力活動；若體重持續下降，建議諮詢醫師或營養師。",
        }
    if bmi < 24:
        return {
            "label": "健康體位",
            "tone": "healthy",
            "advice": "維持均衡飲食與規律運動，並持續留意睡眠及生活習慣，幫助保持健康體位。",
        }
    if bmi < 27:
        return {
            "label": "體重過重",
            "tone": "high",
            "advice": "可從減少含糖飲料、增加蔬菜與日常活動量開始，循序建立適合自己的健康習慣。",
        }
    return {
        "label": "肥胖",
        "tone": "high",
        "advice": "建議與醫師或營養師討論適合自己的飲食及運動計畫，並留意血壓、血糖等健康指標。",
    }


def parse_positive_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) and number > 0 else None


def bmi_gauge_position(bmi):
    gauge_min = 10
    gauge_max = 35
    position = (bmi - gauge_min) / (gauge_max - gauge_min) * 100
    return max(0, min(100, round(position, 1)))


def parse_bmi_inputs(form):
    height_input = form.get("height", "").strip()
    weight_input = form.get("weight", "").strip()
    height = parse_positive_number(height_input)
    weight = parse_positive_number(weight_input)
    errors = {}

    if height is None:
        errors["height"] = "請輸入大於 0 的有效身高（公分）。"
    if weight is None:
        errors["weight"] = "請輸入大於 0 的有效體重（公斤）。"

    if errors:
        return height_input, weight_input, None, errors

    height_meters = height / 100
    height_squared = height_meters * height_meters
    if not math.isfinite(height_squared) or height_squared <= 0:
        errors["height"] = "無法使用這組數值計算 BMI，請檢查身高與體重。"
        return height_input, weight_input, None, errors
    bmi = weight / height_squared
    if not math.isfinite(bmi) or bmi <= 0:
        errors["weight"] = "無法使用這組數值計算 BMI，請檢查身高與體重。"
        return height_input, weight_input, None, errors

    return height_input, weight_input, bmi, errors


def military_guidance(height, bmi):
    """Return a BMI-based preliminary military classification.

    This is only an information aid. The official classification depends on
    the applicable regulation and the conscription medical examination.
    """
    if height <= 154 or bmi < 15 or bmi > 35:
        return {
            "label": "免役體位（初步篩選）",
            "tone": "low",
            "advice": "身高或 BMI 落在免役初步篩選範圍，仍須依徵兵檢查及最新體位區分標準確認。",
        }
    if bmi < 16.5 or bmi > 32:
        return {
            "label": "替代役體位（初步篩選）",
            "tone": "high",
            "advice": "BMI 落在替代役初步篩選範圍，仍須依徵兵檢查及最新體位區分標準確認。",
        }
    return {
        "label": "常備役體位（初步篩選）",
        "tone": "healthy",
        "advice": "BMI 落在常備役初步篩選範圍，實際結果仍須以徵兵檢查判定為準。",
    }
