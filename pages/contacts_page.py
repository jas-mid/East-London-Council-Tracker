import streamlit as st
import pandas as pd
from data_handling import load_and_clean_data

#---links to other pages---

#using columns to make the page links go next to eachother instead of on top of each other
col1, col2, col3 = st.columns(3)
#page links
col1.page_link("app.py", label="Home", icon="🏠")
col2.page_link("pages/statistics_page.py", label="Statistics Comparison Tool", icon="📊")
col3.page_link("pages/contacts_page.py", label="Contacting Your Council", icon="📱", disabled =True)
st.divider()

#---Load and clean the data---
data = load_and_clean_data("EDSP_employees_and_debt_data.csv")
#gaining boroughs
boroughs = sorted(
    [b for b in data["Borough"].unique() if b != "Greater London Average"]
)

#---Laying out varaibles for the page---
selected_borough = "Select your"

#---Title and introduction to the page---
st.header("Getting Your Voice Heard")

#---Selecting your council in the sidebar---
st.sidebar.subheader("Select Your Council")
for borough in boroughs:
    if st.sidebar.button(borough):
        selected_borough = borough




#---Displaying the contact information and voting for the selected council---
#displays the council name
st.subheader(f"{selected_borough} Council")
st.write("")

#using columns to display contact info and voting info
contacts, voting = st.columns(2)



with contacts:
    st.markdown("### Contact Information")

    #function to display the contact information for the selected council
    def display_contact_info(selected_borough):
        

        #initialising link to the website and determining what it will be based on the selected borough
        link=""
        if selected_borough == "Barking & Dagenham":
            link = "https://www.lbbd.gov.uk/contact-us/"
        elif selected_borough == "Hackney":
            link = "https://hackney.gov.uk/contact-us"
        elif selected_borough == "Havering":
            link = "https://www.havering.gov.uk/contactus"
        elif selected_borough == "Newham":
            link = "https://www.newham.gov.uk/contact-information"
        elif selected_borough == "Redbridge":
            link = "https://www.redbridge.gov.uk/contact-us/"
        elif selected_borough == "Tower Hamlets":
            link = "https://www.towerhamlets.gov.uk/content_pages/contact_us/contact-us.aspx"
        elif selected_borough == "Waltham Forest":
            link = "https://www.walthamforest.gov.uk/contact-us"
    
        #button to redirect to the contact us page
        st.page_link(link, label= selected_borough + " Contact Us Page", icon="📱")
    
    #Page logic to display the contact information or a message initially
    if selected_borough == "Select your":
        st.warning("Select your council to see how you can get your opinion to them")
    else:
        display_contact_info(selected_borough)


with voting:
    st.markdown("### Voting Information")
    st.markdown("Voting is one of the most important ways to get your voice heard by your council. By voting in local elections, you can help to elect representatives who will advocate for the issues that are important to you. Local elections typically take place every four years, and they allow you to vote for your local councillors, who are responsible for making decisions about local services and policies.")

    def display_voting_info(selected_borough):

        #initialising link to the website and determining what it will be based on the selected borough
        link=""
        if selected_borough == "Barking & Dagenham":
            link = "https://www.lbbd.gov.uk/council-and-democracy/voting-and-elections/how-vote"
        elif selected_borough == "Hackney":
            link = "https://www.hackney.gov.uk/council-and-elections/elections-and-voting/register-vote"
        elif selected_borough == "Havering":
            link = "https://www.havering.gov.uk/elections-voting"
        elif selected_borough == "Newham":
            link = "https://www.newham.gov.uk/council/register-vote-1/3"
        elif selected_borough == "Redbridge":
            link = "https://www.redbridge.gov.uk/voting-and-elections/register-to-vote/"
        elif selected_borough == "Tower Hamlets":
            link = "https://www.towerhamlets.gov.uk/lgnl/council_and_democracy/elections__voting/elections__voting.aspx"
        elif selected_borough == "Waltham Forest":
            link = "https://www.walthamforest.gov.uk/voting-and-elections"
    
        #button to redirect to the voting page
        st.page_link(link, label="Learn about voting in " + selected_borough, icon="✉️")

    if selected_borough == "Select your":
        st.warning("Select your council to see their voting information")
    else:
        st.divider()
        display_voting_info(selected_borough)
        st.divider()
    
    st.markdown("To find out when the next local elections are taking place in your area, you can visit the [Electoral Commission](https://www.electoralcommission.org.uk/i-am-a/voter) website.")