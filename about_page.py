import streamlit as st

def show_about_page():
    st.title("About This App")

    st.markdown("""
    ## Alzheimer's Disease Data Visualization App
    
    This app provides insights into the prevalence of Alzheimer's disease across the U.S., 
    along with health-related factors that may be associated with Alzheimer's disease.
    
    ### Pages Overview:
    
    - **Overall:** Presents an overview of Alzheimer's disease prevalence across U.S. states and health-related factors among different regions
    - **Compare Topics:** Allows users to compare various health-related factors between different topics (smoking, cognitive decline, mental health, caregiving).
    - **Compare States:** Provides the ability to compare specific factors across two U.S. states.
    
    ### Data Source:
    
    The data used in this app is obtained from publicly available sources:
    
    - Alzheimer's Disease prevalence data: [Prevalence Dataset URL](https://www.alz.org/media/Documents/alzheimers-facts-and-figures.pdf)
    - Alzheimer's Disease related data from CDC's Behavioral Risk Factor Surveillance System (BRFSS): [CDC BRFSS Dataset](https://data.cdc.gov/Healthy-Aging/Alzheimer-s-Disease-and-Healthy-Aging-Data/hfr9-rurv/about_data/)
    
    ### About the Developers:
    
    This app was developed as part of the BMI706 Layperson project to provide accessible, 
    interactive visualizations on Alzheimer's disease statistics and associated factors.
                
    ### Our GitHub Page:
    [GitHub](https://github.com/m1ma0314/BMI706_Layperson/tree/main)
    """)
