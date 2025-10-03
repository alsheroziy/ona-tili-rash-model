import math

# PDF'dan olingan ma'lumotlar
pdf_data = [
    (47, 82.10),
    (46, 80.77),
    (40, 71.25),
    (39, 70.24),
    (37, 68.69),
    (30, 58.59),
    (20, 49.24),
]

print("Analiz:")
for correct, ball in pdf_data:
    proportion = correct / 50.0  # Maksimal 50 ball deb olamiz
    percent = proportion * 100
    
    # Linear formula: ball = a * correct + b
    # 47 -> 82.1, 20 -> 49.24
    # 82.1 = a*47 + b
    # 49.24 = a*20 + b
    # a = (82.1 - 49.24) / (47 - 20) = 32.86 / 27 = 1.217
    
    print(f"{correct} to'g'ri -> {ball} ball ({percent:.1f}%)")

print("\nLinear formula topamiz:")
# y = mx + c
# (47, 82.1) va (20, 49.24) nuqtalaridan
m = (82.10 - 49.24) / (47 - 20)
c = 82.10 - m * 47

print(f"Formula: ball = {m:.4f} * correct + {c:.4f}")

print("\nTest:")
for correct in [47, 46, 40, 30, 20]:
    predicted = m * correct + c
    print(f"{correct} to'g'ri -> {predicted:.2f} ball")
