import math

# PDF'dan ko'proq nuqtalar
targets = [
    (47, 82.10),
    (46, 80.77),
    (40, 71.25),
    (39, 69.90),
    (37, 68.69),
    (34, 64.87),
    (32, 60.61),
    (30, 58.59),
    (28, 55.00),
    (26, 54.94),
    (24, 52.45),
    (23, 49.22),
    (20, 45.95),
]

# Turli max_score va koeffitsientlarni sinab ko'ramiz
best_error = float('inf')
best_params = None

for max_score in range(48, 52):
    for scale_factor in [9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5]:
        for offset in [48.0, 49.0, 50.0, 51.0, 52.0]:
            error = 0
            for correct, target_ball in targets:
                p = min(0.999, correct / max_score)
                logit = math.log(p/(1-p))
                predicted = offset + scale_factor * logit
                error += abs(predicted - target_ball)
            
            if error < best_error:
                best_error = error
                best_params = (max_score, scale_factor, offset)

max_s, scale, off = best_params
print(f"Eng yaxshi parametrlar:")
print(f"  max_score = {max_s}")
print(f"  formula: ball = {off:.2f} + {scale:.2f} * logit")
print(f"  o'rtacha xatolik: {best_error/len(targets):.3f}")

print("\nTest:")
for correct, target in targets[:8]:
    p = min(0.999, correct / max_s)
    logit = math.log(p/(1-p))
    predicted = off + scale * logit
    error = abs(predicted - target)
    print(f"{correct} -> {predicted:.2f} (target: {target}, error: {error:.2f})")
