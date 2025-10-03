import math

def calculate_rasch_score(raw_score: float, max_score: float) -> float:
    if max_score == 0:
        return 0.0
    
    proportion = raw_score / max_score
    
    if proportion <= 0.0001:
        proportion = 0.0001
    elif proportion >= 0.9999:
        proportion = 0.9999
    
    odds = proportion / (1 - proportion)
    logit = math.log(odds)
    
    base_score = ((logit + 6) / 12) * 78
    
    if proportion > 0.7:
        bonus_factor = (proportion - 0.7) / 0.3
        bonus = bonus_factor * 10
        base_score += bonus
    
    rasch_score = max(0, min(85, base_score))
    return round(rasch_score, 2)

# Test (50 ball maksimal)
test_cases = [
    (47, 50, "PDF: 82.1"),
    (46, 50, "PDF: 80.77"),
    (40, 50, "PDF: 71.25"),
    (30, 50, "PDF: ~58"),
    (25, 50, ""),
    (20, 50, ""),
]

print("To'g'ri javoblar -> Rasch ball:\n")
for correct, max_score, expected in test_cases:
    score = calculate_rasch_score(correct, max_score)
    print(f"{correct}/{max_score} ({correct/max_score*100:.1f}%) -> {score:.2f} ball  {expected}")
