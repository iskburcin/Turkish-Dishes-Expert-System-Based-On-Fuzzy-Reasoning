import math

import pandas as pd


# Triangular Membership Function
def triangular_mf(x, a, b, c):
    # 0 if x<=a || c<=x
    # 1 if x==b
    if b == c:  # Avoid division by zero
        return max(0, min((x - a) / (b - a), 0))
    return float(max(0, min((x - a) / (b - a), (c - x) / (c - b))))


# Trapezoidal Membership Function
# 0 if x<=a || x>=d
# 1 if b<=x<=c
def trapezoidal_mf(x, a, b, c, d):
    return float(max(0, min((x - a) / (b - a), 1, (d - x) / (d - c))))


# Gaussian Membership Function
def gaussian_mf(x, mean, sigma):
    return float(math.exp(-((x - mean) ** 2) / (2 * sigma**2)))


def evaluate_character(character, value, logic_choice):
    """
    Parameters:
        taste: float (0-20)
        spiciness: float (0-10)
        sweetness: float (0-10)
        texture: float (0-10)
        logic_choice: int (1, 2, or 3)
    """
    value = float(value)
    result = 0
    match (logic_choice):
        case 1:
            match character:
                case "taste":
                    result = triangular_mf(value, 5, 10, 20)
                case "spiciness":
                    result = triangular_mf(value, 0, 3, 6)
                case "sweetness":
                    result = triangular_mf(value, 0, 5, 7)
                case "texture":
                    result = triangular_mf(value, 2, 3, 7)
        case 2:
            match character:
                case "taste":
                    result = trapezoidal_mf(value, 0, 1, 19, 20)
                case "spiciness":
                    result = trapezoidal_mf(value, 0, 1, 6, 10)
                case "sweetness":
                    result = trapezoidal_mf(value, 0, 2, 7, 10)
                case "texture":
                    result = trapezoidal_mf(value, 0, 2, 7, 10)
        case 3:
            match character:
                case "taste":
                    result = gaussian_mf(value, 10, 2)
                case "spiciness":
                    result = gaussian_mf(value, 3, 3.5)
                case "sweetness":
                    result = gaussian_mf(value, 5.5, 3.8)
                case "texture":
                    result = gaussian_mf(value, 6, 2.2)
        case _:
            raise ValueError("Invalid logic choice! Must be 1, 2, or 3.")

    return result


def evaluate_dish_from_dataset(file_path, dish_name, logic_choice):
    # Load dataset
    df = (
        pd.read_excel(file_path)
        if file_path.endswith(".xlsx")
        else pd.read_csv(file_path)
    )

    # Find the selected dish
    dish = df[df["Name"] == dish_name].iloc[0]

    # Extract characteristics
    taste = dish["Taste"]
    spiciness = dish["Spiciness"]
    sweetness = dish["Sweetness"]
    texture = dish["Texture"]
    print(taste, spiciness, sweetness, texture)

    taste_score = evaluate_character("taste", taste, logic_choice)
    spiciness_score = evaluate_character("spiciness", spiciness, logic_choice)
    sweetness_score = evaluate_character("sweetness", sweetness, logic_choice)
    texture_score = evaluate_character("texture", texture, logic_choice)

    return taste_score, spiciness_score, sweetness_score, texture_score


# Evaluate Dish Based on Selected Logic
def predict_suitability(
    taste, spiciness, sweetness, texture, logic_choice, ispredict=False
):
    """
    Evaluates dish suitability based on the selected logic.
    Returns:
        Suitability score (0.0 to 1.0) with reasoning details.
    """
    match logic_choice:
        case 1:
            method = "Triangular Membership Function"
        case 2:
            method = "Trapezoidal Membership Function"
        case 3:
            method = "Gaussian Membership Function"
    taste_score = evaluate_character("taste", taste, logic_choice)
    spiciness_score = evaluate_character("spiciness", spiciness, logic_choice)
    sweetness_score = evaluate_character("sweetness", sweetness, logic_choice)
    texture_score = evaluate_character("texture", texture, logic_choice)

    # Combine scores using an average
    suitability = (taste_score + spiciness_score + sweetness_score + texture_score) / 4
    details = (
        f"\nMethod: {method}\n"
        f"Taste = {taste_score:.2f}\nSpiciness = {spiciness_score:.2f}\n"
        f"Sweetness = {sweetness_score:.2f}\nTexture = {texture_score:.2f}\n"
        f"Suitability Score = {suitability:.2f}"
    )
    return details if not ispredict else suitability
