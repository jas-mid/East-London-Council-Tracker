"""Page compiling all the councils and contacts"""

#features links to their contacts page and voting information page

import streamlit as st

from council_tracker.health_checker import Health, LinkCheck, check_councils
from council_tracker.repository import get_repository

repository = get_repository()

#---links to other pages---
col1, col2, col3, col4 = st.columns(4)
col1.page_link("app.py", label="Home", icon="🏠")
col2.page_link("pages/statistics_page.py", label="Statistics Comparison Tool", icon="📊")
col3.page_link("pages/contacts_page.py", label="Contacting Your Council", icon="📱", disabled=True)
col4.page_link("pages/licence_page.py", label="Licence & Data Sources", icon="📄")
st.divider()

st.header("Getting Your Voice Heard")

#checking links are active
@st.cache_data(ttl=60 * 60, show_spinner="Checking councils' page status...")
def link_health() -> dict[str, LinkCheck]:
    return {check.url: check for check in check_councils(repository.councils())}

#---choose a group, only when there is more than one to choose from---
groups = repository.groups()
if len(groups) > 1:
    group = st.sidebar.selectbox("Area", groups, format_func=lambda g: g.label)
else:
    group = groups[0]

#choose a council within that group
st.sidebar.subheader("Select Your Council")
council = st.sidebar.radio(
    "Your council",
    repository.members(group.key),
    index=None,
    format_func=lambda c: c.name,
    label_visibility="collapsed",
)

#default load when no council is selected
if council is None:
    st.info("Select your council in the sidebar to see how to contact them and how to vote.")
    st.stop()

st.subheader(f"{council.name} Council")

#one column per kind of page this council publishes
available = [kind for kind in repository.link_kinds() if council.link(kind.key)]
if not available:
    st.warning(f"We don't have any pages recorded for {council.name} yet.")
    st.stop()

for column, kind in zip(st.columns(len(available)), available):
    with column:
        st.markdown(f"### {kind.label}")
        if kind.blurb:
            st.markdown(kind.blurb)
        url = council.link(kind.key).url
        check = link_health().get(url)

        if check and check.health is Health.BROKEN:
            st.warning(f"{council.name}'s {kind.lable.lower()} page seems to be offline. Tray again later.")
            continue
        if check and check.health is Health.MOVED:
            url = check.final_url

        st.page_link(url, label=f"{kind.label} for {council.name}", icon = kind.icon )

#bottom of page information
st.divider()
st.markdown(
    "To find out when the next local elections are in your area, visit the "
    "[Electoral Commission](https://www.electoralcommission.org.uk/i-am-a/voter)."
)
