"""Tests for the pure data-cleaning helpers."""
from pathlib import Path

import pandas as pd

from council_tracker.cleaning import (
    clean_columns,
    convert_percentage_to_numeric,
    filter_by_boroughs,
    load_and_clean_data,
    population_to_numeric,
)

SAMPLE_CSV = Path(__file__).parent / "fixtures" / "sample.csv"


def test_clean_columns_replaces_underscores_and_titlecases():
    df = pd.DataFrame(columns=["number_of_employees", "debt_in_gbp"])
    assert list(clean_columns(df).columns) == ["Number Of Employees", "Debt In Gbp"]


def test_convert_percentage_to_numeric_strips_sign_and_scales():
    df = pd.DataFrame({"Rate": ["50%", "75%", "100%"]})
    assert convert_percentage_to_numeric(df, "Rate")["Rate"].tolist() == [0.5, 0.75, 1.0]


def test_convert_percentage_to_numeric_leaves_numeric_columns_untouched():
    df = pd.DataFrame({"Rate": [0.5, 0.75]})
    assert convert_percentage_to_numeric(df, "Rate")["Rate"].tolist() == [0.5, 0.75]


def test_population_to_numeric_removes_thousands_separators():
    df = pd.DataFrame({"Population": ["1,000", "2,500"]})
    assert population_to_numeric(df, "Population")["Population"].tolist() == [1000.0, 2500.0]


def test_load_and_clean_data_converts_percentage_columns():
    df = load_and_clean_data(SAMPLE_CSV)
    assert df["Percentage Column"].tolist() == [0.5, 0.75, 1.0]


def test_filter_by_boroughs_keeps_only_requested_rows():
    df = pd.DataFrame({"Borough": ["Hackney", "Newham", "Havering"], "Value": [1, 2, 3]})
    assert filter_by_boroughs(df, ["Hackney", "Havering"])["Borough"].tolist() == ["Hackney", "Havering"]


def test_filter_by_boroughs_with_no_matches_returns_empty():
    df = pd.DataFrame({"Borough": ["Hackney"], "Value": [1]})
    assert filter_by_boroughs(df, ["Westminster"]).empty
