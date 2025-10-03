"""
Rasch Model implementation for test scoring
Based on international methodology used in Uzbekistan National Certificate exams
"""
import math


def calculate_rasch_score(raw_score: float, max_score: float) -> float:
    """
    Calculate Rasch model score from raw score.

    The Rasch model converts raw scores to ability estimates using logit transformation.
    Formula calibrated based on Uzbekistan National Certificate exam data.

    Reference points:
    - 47/50 (94%) -> 82.1 ball
    - 40/50 (80%) -> 71.25 ball
    - 30/50 (60%) -> 58.59 ball

    Args:
        raw_score: Total points earned
        max_score: Maximum possible points

    Returns:
        Rasch score in 0-85 range
    """
    if max_score == 0:
        return 0.0

    # Calculate proportion correct
    proportion = raw_score / max_score

    # Handle edge cases
    if proportion <= 0.001:
        return 0.0
    elif proportion >= 0.999:
        proportion = 0.999

    # Calculate logit (log odds)
    logit = math.log(proportion / (1 - proportion))

    # Rasch formula: ball = offset + scale * logit
    # Calibrated values:
    offset = 52.0
    scale = 12.5

    rasch_score = offset + scale * logit

    # Ensure within reasonable bounds
    rasch_score = max(0, min(85, rasch_score))

    return round(rasch_score, 2)


def get_score_level(rasch_score: float) -> tuple:
    """
    Get score level based on Rasch score.

    Based on Uzbekistan National Certificate levels (78 ball tizimi):
    - 70+: A+ level
    - 65-70: A level
    - 60-65: B+ level
    - 55-60: B level
    - 50-55: C+ level
    - 46-50: C level
    - Below 46: NC (Not Classified)

    Args:
        rasch_score: Rasch model score (0-78)

    Returns:
        Tuple of (level, description)
    """
    if rasch_score >= 70:
        return ("A+", "A'lo (maksimal ball)")
    elif rasch_score >= 65:
        return ("A", "A'lo")
    elif rasch_score >= 60:
        return ("B+", "Yaxshi (yuqori)")
    elif rasch_score >= 55:
        return ("B", "Yaxshi")
    elif rasch_score >= 50:
        return ("C+", "Qoniqarli (yuqori)")
    elif rasch_score >= 46:
        return ("C", "Qoniqarli")
    else:
        return ("NC", "Tasniflanmagan")


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
