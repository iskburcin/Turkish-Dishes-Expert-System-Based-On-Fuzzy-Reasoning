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


def get_string_score(score):
    """Returns a human-readable description of the score."""
    if score < 0.4:
        return "Low"
    elif 0.4 <= score < 0.7:
        return "Modarete"
    else:
        return "Yummy"


def print_table(data, headers):
    from tabulate import tabulate

    table = tabulate(data, headers=headers, tablefmt="grid")

    table = ""
    # Print the table header
    header_row = "| " + " | ".join(headers) + " |"
    separator = "-" * len(header_row)
    table += separator + "\n"
    table += header_row + "\n"
    table += separator + "\n"

    for row in data:
        if row[0] == "Taste":
            row_data = "| " + str(row[0]) + "\t\t"
            row_data += "| " + str(row[1]) + "\t"
            row_data += "| " + str(row[2]) + "\t"
            row_data += "| " + str(row[3]) + " |"
        else:
            row_data = "| " + "\t | ".join(map(str, row)) + " |"
        table += row_data + "\n"
        table += "-" * len(row_data) + "\n"
    return table


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

    details = calculateScores([taste, spiciness, sweetness, texture], logic_choice)

    return details


# Evaluate Dish Based on Selected Logic
def predict_suitability(
    taste, spiciness, sweetness, texture, logic_choice, ispredict=False
):
    features = calculateScores(
        [taste, spiciness, sweetness, texture], logic_choice, True
    )
    # Combine scores using an average
    suitability = (features[0] + features[1] + features[2] + features[3]) / 4
    details = calculateScores([taste, spiciness, sweetness, texture], logic_choice)
    return details if not ispredict else suitability


def calculateScores(data, logic_choice, wantValues=False):
    taste_score = evaluate_character("taste", data[0], logic_choice)
    spiciness_score = evaluate_character("spiciness", data[1], logic_choice)
    sweetness_score = evaluate_character("sweetness", data[2], logic_choice)
    texture_score = evaluate_character("texture", data[3], logic_choice)

    details = print_table(
        [
            ["Taste", data[0], round(taste_score, 2), get_string_score(taste_score)],
            [
                "Spiciness",
                data[1],
                round(spiciness_score, 2),
                get_string_score(spiciness_score),
            ],
            [
                "Sweetness",
                data[2],
                round(sweetness_score, 2),
                get_string_score(sweetness_score),
            ],
            [
                "Texture",
                data[3],
                round(texture_score, 2),
                get_string_score(texture_score),
            ],
        ],
        headers=["Feature", "User Votes", "MF Scores"],
    )

    suitability = (taste_score + spiciness_score + sweetness_score + texture_score) / 4
    isSuit = get_string_score(suitability)
    details += f"\nSuitibility value: {round(suitability,2)} so, it is {isSuit}"

    return (
        [taste_score, spiciness_score, sweetness_score, texture_score]
        if wantValues
        else details
    )
