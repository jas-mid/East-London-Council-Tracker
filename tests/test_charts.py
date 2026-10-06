"""Tests for the chart builders."""
import pandas as pd
import plotly.graph_objects as go
import pytest

from council_tracker.charts import build_comparison_chart

DATA = pd.DataFrame({"Borough": ["Hackney", "Newham"], "Median Age": [32, 31]})


def test_builds_one_bar_trace_per_borough():
    figure = build_comparison_chart(DATA, "Median Age")
    assert isinstance(figure, go.Figure)
    assert len(figure.data) == 2
    assert figure.layout.title.text == "Median Age Comparison"


def test_unknown_metric_is_rejected():
    with pytest.raises(KeyError, match="Unknown metric"):
        build_comparison_chart(DATA, "Not A Column")
