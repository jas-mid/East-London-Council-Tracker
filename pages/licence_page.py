"""Page covering the app's licence and where its data comes from"""

#the code is MIT licensed, the data belongs to its publishers

import streamlit as st

#---links to other pages---
col1, col2, col3, col4 = st.columns(4)
col1.page_link("app.py", label="Home", icon="🏠")
col2.page_link("pages/statistics_page.py", label="Statistics Comparison Tool", icon="📊")
col3.page_link("pages/contacts_page.py", label="Contacting Your Council", icon="📱")
col4.page_link("pages/licence_page.py", label="Licence & Data Sources", icon="📄", disabled=True)
st.divider()

st.header("Licence & Data Sources")

#licensing is still being checked, so make that clear before anything else
st.warning(
    "**Work in progress:** this page was drafted with the help of Claude, an AI assistant, and "
    "has not yet been fully checked against each data source's terms. Some details may be "
    "inaccurate or incomplete. Please check the original sources before relying on it."
)

#---licence for the app's code---
st.subheader("App Licence")
st.markdown(
    "The code for this app is released under the **MIT Licence**. You are free to use, copy, "
    "change and share it, as long as you keep the copyright notice and licence text with it. "
    "The software is provided as is, without any warranty."
)
st.page_link(
    "https://github.com/jas-mid/East-London-Council-Tracker/blob/main/LICENSE",
    label="Read the full licence on GitHub",
    icon="🔗",
)
st.write("")

#---where the data comes from---
st.subheader("Data Sources")
st.markdown(
    "The MIT Licence covers the app's code only. The data shown in the app belongs to the "
    "organisations that publish it, and is used under their own terms."
)
st.markdown(
    "- **Office for National Statistics (ONS):** population estimates and local statistics. "
    "Contains public sector information licensed under the Open Government Licence v3.0.\n"
    "- **London Datastore (Greater London Authority):** safe streets, council employee and debt "
    "data. Used under the licence shown on each dataset's page, which for most London Datastore "
    "data is the Open Government Licence v3.0.\n"
    "- **Council websites:** contact and voting pages are linked to, not copied. Their content "
    "belongs to each council."
)
st.page_link(
    "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
    label="Open Government Licence v3.0",
    icon="🔗",
)
st.page_link("https://www.ons.gov.uk/", label="Office for National Statistics", icon="🔗")
st.page_link("https://data.london.gov.uk/", label="London Datastore", icon="🔗")
st.write("")

#---disclaimer---
st.subheader("Disclaimer")
st.markdown(
    "This is an independent project. It is not affiliated with or endorsed by the ONS, the "
    "Greater London Authority or any council. Figures may be out of date, so check the original source before relying on them."
)
