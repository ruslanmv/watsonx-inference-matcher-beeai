import difflib
from typing import Union


def calculate_similarity(inference: str, target: Union[str, dict]) -> float:
    """
    Calculate a similarity score between a generated inference and a target output.

    Parameters:
    - inference (str): The generated inference text.
    - target (str | dict): The target criteria. If dict, it's stringified for comparison.

    Returns:
    - float: Similarity score between 0 and 1.
    """
    if isinstance(target, dict):
        target_str = "\n".join([f"{k}: {v}" for k, v in target.items()])
    else:
        target_str = target

    sequence_matcher = difflib.SequenceMatcher(None, inference, target_str)
    score = sequence_matcher.ratio()
    return round(score, 4)


def meets_criteria(inference: str, criteria: dict) -> bool:
    """
    Check if the generated inference includes all required keywords or patterns.

    Parameters:
    - inference (str): The generated output.
    - criteria (dict): A dict of conditions the output must contain.

    Returns:
    - bool: True if all criteria are met.
    """
    for key, value in criteria.items():
        if value.lower() not in inference.lower():
            return False
    return True


if __name__ == "__main__":
    # Example testing
    generated = "This configuration sets max_latency to 50ms and supports TLS security."
    target_data = {
        "max_latency": "50ms",
        "security_protocols": "TLS"
    }

    print("Similarity Score:", calculate_similarity(generated, target_data))
    print("Meets Criteria:", meets_criteria(generated, target_data))
