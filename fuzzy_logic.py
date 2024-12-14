import math


# Triangular Membership Function
def triangular_mf(x, a, b, c):
    # 0 if x<=a || c<=x
    # 1 if x==b
    if b == c:  # Avoid division by zero
        return max(0, min((x - a) / (b - a), 0))
    return max(0, min((x - a) / (b - a), (c - x) / (c - b)))


# Trapezoidal Membership Function
# 0 if x<=a || x>=d
# 1 if b<=x<=c
def trapezoidal_mf(x, a, b, c, d):
    return max(0, min((x - a) / (b - a), 1, (d - x) / (d - c)))


# Gaussian Membership Function
def gaussian_mf(x, mean, sigma):
    return math.exp(-((x - mean) ** 2) / (2 * sigma**2))


# Evaluate Dish Based on Selected Logic
def evaluate_dish(taste, spiciness, sweetness, texture, logic_choice):
    """
    Evaluates dish suitability based on the selected logic.

    Parameters:
        taste: float (0-20)
        spiciness: float (0-10)
        sweetness: float (0-10)
        texture: float (0-10)
        logic_choice: int (1, 2, or 3)

    Returns:
        Suitability score (0.0 to 1.0) with reasoning details.
    """
    if logic_choice == 1:  # Logic 1: Triangular
        taste_score = triangular_mf(taste, 5, 10, 20)
        spiciness_score = triangular_mf(spiciness, 0, 3, 6)
        sweetness_score = triangular_mf(sweetness, 0, 5, 7)
        texture_score = triangular_mf(texture, 2, 3, 7)
        method = "Triangular Membership Functions"

    elif logic_choice == 2:  # Logic 2: Trapezoidal
        taste_score = trapezoidal_mf(taste, 0, 1, 19, 20)
        spiciness_score = trapezoidal_mf(spiciness, 0, 1, 6, 10)
        sweetness_score = trapezoidal_mf(sweetness, 0, 2, 7, 10)
        texture_score = trapezoidal_mf(texture, 0, 2, 7, 10)
        method = "Trapezoidal Membership Functions"

    elif logic_choice == 3:  # Logic 3: Gaussian
        taste_score = gaussian_mf(taste, 10, 2)
        spiciness_score = gaussian_mf(spiciness, 3, 3.5)
        sweetness_score = gaussian_mf(sweetness, 5.5, 3.8)
        texture_score = gaussian_mf(texture, 6, 2.2)
        method = "Gaussian Membership Functions"

    else:
        raise ValueError("Invalid logic choice! Must be 1, 2, or 3.")

    # Combine scores using an average
    suitability = (taste_score + spiciness_score + sweetness_score + texture_score) / 4
    details = (
        f"\nMethod: {method}\n"
        f"Taste = {taste_score:.2f}\nSpiciness = {spiciness_score:.2f}\n"
        f"Sweetness = {sweetness_score:.2f}\nTexture = {texture_score:.2f}\n"
        f"Suitability Score = {suitability:.2f}"
    )
    return details
