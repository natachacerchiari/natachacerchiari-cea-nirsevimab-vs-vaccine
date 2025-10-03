import pandas as pd
from pathlib import Path

__all__ = ["load_age_groups", "load_scalar_data", "load_ageband_data"]


_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

_AGE_GROUPS_FILE_PATH = _DATA_DIR / "age_groups.csv"
_COHORT_FILE_PATH = _DATA_DIR / "cohort.csv"
_DIRECT_MEDICAL_COSTS_FILE_PATH = _DATA_DIR / "direct_medical_costs.csv"
_DIRECT_NON_MEDICAL_COSTS_FILE_PATH = _DATA_DIR / "direct_non_medical_costs.csv"
_DW_FILE_PATH = _DATA_DIR / "dw.csv"
_EPIDEMIOLOGIC_DATA_FILE_PATH = _DATA_DIR / "epidemiologic_data.csv"
_ILLNESS_DURATION_FILE_PATH = _DATA_DIR / "illness_duration.csv"
_INDIRECT_COSTS_FILE_PATH = _DATA_DIR / "indirect_costs.csv"
_NIRSEVIMAB_EFFECTIVENESS_FILE_PATH = _DATA_DIR / "nirsevimab_effectiveness.csv"
_NIRSEVIMAB_PARAMETERS_FILE_PATH = _DATA_DIR / "nirsevimab_parameters.csv"
_VACCINE_EFFECTIVENESS_FILE_PATH = _DATA_DIR / "vaccine_effectiveness.csv"
_VACCINE_PARAMETERS_FILE_PATH = _DATA_DIR / "vaccine_parameters.csv"
_YLL_FILE_PATH = _DATA_DIR / "yll.csv"

single_row_files_paths = [
    _COHORT_FILE_PATH,
    _DW_FILE_PATH,
    _ILLNESS_DURATION_FILE_PATH,
    _NIRSEVIMAB_PARAMETERS_FILE_PATH,
    _VACCINE_PARAMETERS_FILE_PATH,
    _YLL_FILE_PATH,
]

multi_row_files_paths = [
    _DIRECT_MEDICAL_COSTS_FILE_PATH,
    _DIRECT_NON_MEDICAL_COSTS_FILE_PATH,
    _EPIDEMIOLOGIC_DATA_FILE_PATH,
    _INDIRECT_COSTS_FILE_PATH,
    _NIRSEVIMAB_EFFECTIVENESS_FILE_PATH,
    _VACCINE_EFFECTIVENESS_FILE_PATH,
]


def load_age_groups() -> pd.DataFrame:
    """
    Load age group data from age_groups.csv as a pandas DataFrame.
    """
    path = _AGE_GROUPS_FILE_PATH
    filename = _AGE_GROUPS_FILE_PATH.name
    if not path.exists():
        raise FileNotFoundError(f"Missing {filename}")
    df = pd.read_csv(path, sep=";")
    if "age_group" not in df.columns:
        raise ValueError(f"{filename} must contain 'age_group' column.")
    return df


def load_scalar_data() -> pd.DataFrame:
    """
    Load scalar data from predefined single-row CSV files into a pandas DataFrame.
    """
    scalar_data = {}
    for file_path in single_row_files_paths:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing {file_path.name}")
        df = pd.read_csv(file_path, sep=";")
        if len(df) != 1:
            raise ValueError(f"{file_path.name} must contain exactly one row.")
        for column in df.columns:
            if column in scalar_data:
                raise ValueError(
                    f"Duplicate column name '{column}' found in {file_path.name}.")
            scalar_data[column] = df.iloc[0][column]
    return pd.DataFrame([scalar_data])


def load_agegroup_data() -> pd.DataFrame:
    """
    Load age grouped data from predefined multi-row CSV files into a pandas DataFrame.
    """
    grouped_data = {}
    for file_path in multi_row_files_paths:
        if not file_path.exists():
            raise FileNotFoundError(f"Missing {file_path.name}")
        df = pd.read_csv(file_path, sep=";")
        if "age_group" not in df.columns:
            raise ValueError(
                f"{file_path.name} must contain 'age_group' column.")
        for column in df.columns:
            if column == "age_group":
                continue
            if column in grouped_data:
                raise ValueError(
                    f"Duplicate column name '{column}' found in {file_path.name}.")
            grouped_data[column] = df.set_index("age_group")[column].to_dict()
    return pd.DataFrame(grouped_data)
