import math

# PDF'dan ko'proq ma'lumotlar
data = [
    (47, 82.10),
    (40, 71.25),
    (34, 64.87),
    (30, 58.59),
    (26, 54.94),
    (23, 49.22),
    (20, 45.95),
]

# Rasch model: ball = a + b * logit(p/(1-p))
# Bu yerda p = correct/total

print("Logit hisoblash:")
for correct, ball in data:
    p = correct / 50.0  # 44-50 oralig'ida bo'lishi mumkin
    if p > 0.99:
        p = 0.99
    logit = math.log(p / (1 - p))
    print(f"{correct} -> p={p:.3f}, logit={logit:.3f}, ball={ball}")

# Regression qilish: ball = a + b*logit
# 2 ta nuqta bilan:
p1 = 47/50
logit1 = math.log(p1/(1-p1))
ball1 = 82.10

p2 = 20/50
logit2 = math.log(p2/(1-p2))
ball2 = 45.95

b = (ball1 - ball2) / (logit1 - logit2)
a = ball1 - b * logit1

print(f"\nFormula: ball = {a:.4f} + {b:.4f} * logit")

print("\nTest:")
for correct in [47, 40, 34, 30, 26, 23, 20]:
    p = correct / 50
    if p > 0.99:
        p = 0.99
    logit = math.log(p/(1-p))
    predicted = a + b * logit
    print(f"{correct} to'g'ri -> {predicted:.2f} ball")
