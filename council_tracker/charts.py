"""Chart builders. Deliberately free of Streamlit calls so they can be unit tested."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_comparison_chart(data: pd.DataFrame, metric: str) -> go.Figure:
    """Bar chart comparing a single metric across the boroughs in `data`."""
    if metric not in data.columns:
        raise KeyError(f"Unknown metric: {metric!r}")
    return px.bar(data, x="Borough", y=metric, color="Borough", title=f"{metric} Comparison")
