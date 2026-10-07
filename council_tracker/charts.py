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

#colour-blind friendly palettes
BOROUGH_COLOUR = "#2a78d6"
REFERENCE_COLOUR = "#8c8b87"


def build_indicator_chart(
        boroughs: pd.DataFrame,
        references: pd.DataFrame,
        label: str,
        unit: str,
        format_value,
) -> go.Figure:
    """Horizontal bars for each borough"""

    ordered = boroughs.sort_values("value")
    figure = go.Figure(
        go.Bar(
            x=ordered["value"],
            y=ordered["area"],
            orientation="h",
            marker={"color": BOROUGH_COLOUR, "cornerradius": 4},
            customdata=[format_value(value) for value in ordered["value"]],
            hovertemplate="%{y}: %{customdata}<extra></extra>",
        )
    )
    #building datapoints
    for _, reference in references.iterrows():
        figure.add_vline(
            x=reference["value"],
            line = {"color": REFERENCE_COLOUR, "width": 2, "dash": "dash"},
             annotation_text=f"{reference['area']} {format_value(reference['value'])}",
            annotation_position="top",
        )
    #layout of graph
    figure.update_layout(
        title=label,
        xaxis_title=f"{label} ({unit})" if unit else label,
        bargap=0.35,
        showlegend=False,
        margin={"t": 80},
    )
    return figure