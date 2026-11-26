
import json
from pathlib import Path


def export_camp_statistics(
    statistics: list[dict],
    output_path: Path,
    observation_date: str,
    satellite: str = "Sentinel-2",
    vegetation_threshold: float = 0.3,
) -> Path:
    """
    Export statistics for all camps into one JSON file.
    """

    if not statistics:
        raise ValueError("No camp statistics provided.")

    if not 0 <= vegetation_threshold <= 1:
        raise ValueError(
            "Vegetation threshold must be between 0 and 1."
        )

    output = {
        "observation_date": observation_date,
        "satellite": satellite,
        "vegetation_threshold": vegetation_threshold,
        "camp_count": len(statistics),
        "camps": statistics,
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(output, file, indent=4, allow_nan=False)

    return output_path
