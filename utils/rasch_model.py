"""
Rasch Model implementation for test scoring
Based on international methodology used in Uzbekistan National Certificate exams
"""
import math


def calculate_rasch_score(raw_score: float, max_score: float) -> float:
    """
    Calculate Rasch model score from raw score.

    The Rasch model converts raw scores to ability estimates using logit transformation:
    1. Calculate proportion correct (p)
    2. Calculate odds ratio: p / (1 - p)
    3. Apply natural log to get logit (ability estimate)
    4. Scale to 0-78 range

    Args:
        raw_score: Total points earned
        max_score: Maximum possible points

    Returns:
        Rasch score in 0-78 range
    """
    if max_score == 0:
        return 0.0

    # Calculate proportion correct
    proportion = raw_score / max_score

    # Handle edge cases (0% and 100%)
    if proportion <= 0.0001:
        proportion = 0.0001
    elif proportion >= 0.9999:
        proportion = 0.9999

    # Calculate odds ratio: p / (1-p)
    odds = proportion / (1 - proportion)

    # Calculate logit (natural log of odds)
    logit = math.log(odds)

    # Scale logit to 0-78 range
    # Logit typically ranges from about -7 to +7
    # We'll map -7 to 0 and +7 to 78
    rasch_score = ((logit + 7) / 14) * 78

    # Ensure within 0-78 bounds
    rasch_score = max(0, min(78, rasch_score))

    return round(rasch_score, 2)


def get_score_level(rasch_score: float) -> tuple:
    """
    Get score level based on Rasch score.

    Based on Uzbekistan National Certificate levels (78 ball tizimi):
    - 54.6+: A+ level (70% dan yuqori)
    - 50.7-54.59: A level (65-69.9%)
    - 46.8-50.69: B+ level (60-64.9%)
    - 42.9-46.79: B level (55-59.9%)
    - 39-42.89: C+ level (50-54.9%)
    - 35.88-38.99: C level (46-49.9%)
    - Below 35.88: Not passed

    Args:
        rasch_score: Rasch model score (0-78)

    Returns:
        Tuple of (level, description)
    """
    if rasch_score >= 54.6:
        return ("A+", "A'lo (maksimal ball)")
    elif rasch_score >= 50.7:
        return ("A", "A'lo")
    elif rasch_score >= 46.8:
        return ("B+", "Yaxshi (yuqori)")
    elif rasch_score >= 42.9:
        return ("B", "Yaxshi")
    elif rasch_score >= 39:
        return ("C+", "Qoniqarli (yuqori)")
    elif rasch_score >= 35.88:
        return ("C", "Qoniqarli")
    else:
        return ("F", "O'tmadi")


def calculate_logistic_probability(ability: float, difficulty: float) -> float:
    """
    Calculate probability of correct response using Rasch model logistic function.

    P(θ, b) = 1 / (1 + exp(-(θ - b)))

    Args:
        ability: Person's ability level (theta)
        difficulty: Item's difficulty level (b)

    Returns:
        Probability of correct response (0-1)
    """
    try:
        return 1.0 / (1.0 + math.exp(-(ability - difficulty)))
    except OverflowError:
        # Handle extreme values
        if ability > difficulty:
            return 1.0
        else:
            return 0.0


def estimate_item_difficulty(correct_count: int, total_count: int) -> float:
    """
    Estimate item difficulty from response data.

    Difficulty is calculated as the negative logit of proportion correct:
    difficulty = -ln(p / (1-p))

    Args:
        correct_count: Number of correct responses
        total_count: Total number of responses

    Returns:
        Item difficulty estimate
    """
    if total_count == 0:
        return 0.0

    proportion = correct_count / total_count

    # Handle edge cases
    if proportion <= 0.0001:
        proportion = 0.0001
    elif proportion >= 0.9999:
        proportion = 0.9999

    # Difficulty is negative logit of proportion correct
    odds = proportion / (1 - proportion)
    difficulty = -math.log(odds)

    return round(difficulty, 3)
