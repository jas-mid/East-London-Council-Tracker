import streamlit as st

#---Title and page links---#
#title
st.markdown("<h1 style='text-align: center; color: white;'>East London Council Comparison App</h1>", unsafe_allow_html=True)

#links to other pages divided clearly
st.divider()
st.subheader("Click one of the options below to navigate:")
st.page_link("pages/statistics_page.py", label="Statistics Comparison Tool", icon="📊")
st.page_link("pages/contacts_page.py", label="Contacting Your Council", icon="📱")
st.page_link("pages/licence_page.py", label="Licence & Data Sources", icon="📄")
st.divider()


#---Introduction to the app and what it does---

#using markdown to make the text bigger and centered
st.title("How to Use The App")
st.markdown("Select one of the options above to move to each section. ")

# expaining the comparison tool
st.subheader("Statistics Comparison Tool")
st.markdown("This page allows you to compare the statistics of different measures that Boroughs in East London have direct control over. This is important as it allows you to see how your borough is performing compared to others, and to the Greater London Average. This can help you to identify areas where your borough is doing well, and areas where it may be struggling. It can also help you to identify trends and patterns in the data, and to make informed decisions about how to advocate for change in your borough.")
st.markdown("To use the tool, select the councils you want to see in the sidebar, and then select the metric you want to compare from the dropdown menu. The graph will update to show you the data for the selected councils and metric. You can also hover over the graph to see more detailed information about each data point.")
st.write("")

# expaining the contact page
st.subheader("Contacting Your Council")
st.markdown("This page provides you with the contact details for your local council, as well as some tips on how to effectively contact them. This is important as it allows you to hold your council accountable for their actions, and to advocate for change in your borough. By contacting your council, you can raise awareness of issues that are important to you, and you can also provide feedback on the services that they provide. This can help to improve the quality of life in your borough, and it can also help to build a stronger community.")
st.markdown("To use the page, select your council in the sidebar, then click the button marked with the phone icon to be redirected to the contact us page.")
st.write("")

#explaining why you should contact your council
st.subheader("Why Contact Your Council?")
st.markdown("Councils in the UK are often felt to not represent their constituents very well. In a time where only 34% of people trust their local government, it is more important than ever to bring clarity.")
st.page_link("https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/bulletins/trustingovernmentuk/2023", label="ONS Survey on Trust in Government", icon="🔗")

