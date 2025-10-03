import sys
sys.path.insert(0, '.')

from utils.pdf_generator import calculate_grade, calculate_percent

# Test qilish
test_scores = [82.1, 70.5, 65.0, 60.0, 55.0, 50.0, 46.0, 45.0]

print("Ball -> Daraja testi:\n")
for score in test_scores:
    grade = calculate_grade(score)
    percent = calculate_percent(score)
    print(f"{score:.2f} ball -> {percent:.2f}% -> {grade}")
