def calculate_grade(score: float) -> str:
    """Ballga qarab bahoni aniqlash (78 ball tizimi)"""
    if score >= 70:
        return "A+"
    elif score >= 65:
        return "A"
    elif score >= 60:
        return "B+"
    elif score >= 55:
        return "B"
    elif score >= 50:
        return "C+"
    elif score >= 46:
        return "C"
    else:
        return "NC"

def calculate_percent(score: float, max_score: float = 78) -> float:
    """Ballni foizga o'girish"""
    if max_score == 0:
        return 0.0
    return round((score / max_score) * 100, 2)

# Test qilish
test_scores = [82.1, 70.5, 65.0, 60.0, 55.0, 50.0, 46.0, 45.0]

print("Ball -> Daraja testi:\n")
for score in test_scores:
    grade = calculate_grade(score)
    percent = calculate_percent(score)
    print(f"{score:.2f} ball -> {percent:.2f}% -> {grade}")
