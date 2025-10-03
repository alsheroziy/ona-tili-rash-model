import math

# 49 ball maksimal
data = [
    (47, 82.10),
    (40, 71.25),
    (30, 58.59),
    (20, 45.95),
]

print("49 maksimal bilan:")
for correct, ball in data:
    p = correct / 49.0
    if p > 0.999:
        p = 0.999
    logit = math.log(p/(1-p))
    print(f"{correct}/49 -> p={p:.3f}, logit={logit:.3f}, ball={ball}")

# Formula: ball = a + b*logit
p1 = 47/49
logit1 = math.log(p1/(1-p1))
ball1 = 82.10

p2 = 20/49
logit2 = math.log(p2/(1-p2))
ball2 = 45.95

b = (ball1 - ball2) / (logit1 - logit2)
a = ball1 - b * logit1

print(f"\nFormula: ball = {a:.4f} + {b:.4f} * logit")

print("\nTest:")
for correct in [47, 46, 40, 30, 20]:
    p = min(0.999, correct / 49)
    logit = math.log(p/(1-p))
    predicted = a + b * logit
    print(f"{correct} to'g'ri -> {predicted:.2f} ball")
