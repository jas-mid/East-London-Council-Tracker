import streamlit as st
import plotly.express as px
import pandas as pd
from data_handling import load_and_clean_data, merge_datasets, safe_streets_cleaning
from data_handling import population_cleaning

#---links to other pages---

#using columns to make the page links go next to eachother instead of on top of each other
col1, col2, col3 = st.columns(3)
#page links
col1.page_link("app.py", label="Home", icon="🏠")
col2.page_link("pages/statistics_page.py", label="Statistics Comparison Tool", icon="📊",disabled=True)
col3.page_link("pages/contacts_page.py", label="Contacting Your Borough", icon="📱")
st.divider()

#---Title and introduction to the page---
st.header("Statistics Comparison Tool")
st.markdown("This page allows you to compare the statistics of different measures that Boroughs in East London have direct control over")

#---Load and clean the data---

#council performance data
employee_and_debt_data = load_and_clean_data("EDSP_employees_and_debt_data.csv")

#population data
population_data = load_and_clean_data("EDSP_population_data.csv")
#further clean the data
population_data = population_cleaning(population_data)

#safe streets data
safe_streets_data = load_and_clean_data("EDSP_safe_streets_data.csv")
#further clean the data
safe_streets_data = safe_streets_cleaning(safe_streets_data)

#merge the datasets together
performance_data = merge_datasets(safe_streets_data, population_data, employee_and_debt_data)


#---Select Boroughs to compare---
st.sidebar.subheader("Select Boroughs to Compare:")
boroughs = ["Barking & Dagenham", "Hackney", "Havering", "Newham", "Redbridge", "Tower Hamlets", "Waltham Forest"]
selected_boroughs = ["Greater London Average"]  # Always include Greater London Average for comparison
for borough in boroughs:
    if st.sidebar.checkbox(borough):
        selected_boroughs.append(borough)


#---Select which metrics you want to see---
metrics = [
    #as the first column is 'Borough'
    col for col in performance_data.columns[1:]
    # exclude the population column
    if col not in ["Population"]
]  
selected_metrics = st.selectbox("Select Metric to Compare", metrics)

#---Filter the data based on user selections---
plot_data = performance_data[performance_data["Borough"].isin(selected_boroughs)]

#warnings for metrics where there's no london data
if selected_metrics=="Debt In Gbp":
    st.warning("There is no wide data for the Greater London Average for this metric, so it is not included in the graph.")
elif selected_metrics =="Number Of Employees":
    st.warning("There is no wide data for the Greater London Average for this metric, so it is not included in the graph.")
elif selected_metrics =="Debt Per Capita":
    st.warning("There is no wide data for the Greater London Average for this metric, so it is not included in the graph.")
elif selected_metrics =="Percentage Of Population Employed":
    st.warning("There is no wide data for the Greater London Average for this metric, so it is not included in the graph.")

if selected_metrics:

    #assigning the metrics for the graph 
    metric = selected_metrics

    # defining the graph for plotly
    fig = px.bar(
        plot_data,
        x="Borough",
        y=metric,
        color="Borough",
        title=f"{metric} Comparison"
    )
    
    #displaying the graph
    st.plotly_chart(fig, use_container_width=True)

#default warning for when no council is selected
else:
    st.warning("Select what data you want to display.")