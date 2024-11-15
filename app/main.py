import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import time


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    attention_message = st.empty()  # Create an empty space for the attention message

    # Animate the attention message
    for i in range(5):  # You can adjust the number of frames as needed
        attention_message.text(f"👈 Please go to the sidebar for instructions 👈")
        time.sleep(0.75)  # Adjust the sleep duration for the desired speed

    # Clear the animated attention message
    attention_message.empty()



    # Add instructions and project details to the sidebar
    with st.sidebar:
        
        st.markdown("<h2 style='color: #3366ff;'>Welcome to Cold Mail Generator! 📧</h2>", unsafe_allow_html=True)

        st.write("This tool is built using Groq, Langchain, and Streamlit, and it’s designed to help businesses reach out to potential clients or partners with personalized cold emails."
                 "Here’s how it works: 🔍 The tool extracts job listings from a company’s careers page using the URL. ✉️ It then generates personalized cold emails, complete with relevant portfolio links pulled from a vector database based on the job descriptions.   "
                 " Imagine this : Nike is hiring for a Principal Software Engineer. Atliq, a software development company, can offer a dedicated software engineer. Using the Cold Mail Generator, Atliq’s business development executive, Mohan, can craft a personalized cold email to reach out to Nike.")

        st.markdown("<h3 style='color: #3366ff;'>How to Use:</h3>", unsafe_allow_html=True)
        st.write("1. Copy and paste the URL of the job listing from the company's careers page into the input field.")
        st.write("2. Press the 'Submit' button to start the process.")
        st.write("3. The tool will extract relevant details from the job listing, including job title and description.")
        st.write("4. Based on the extracted information, a personalized cold email will be generated, including links to relevant portfolio items.")
        st.write("4. Review the generated email, make any necessary edits, and send it to the target company.")

        # Add contact information at the end
        st.markdown("---")
        st.subheader("Contact Information:")
        st.write("For any inquiries or feedback, feel free to reach out:")
        st.write("📧 Email: [gokuldas127199544@gmail.com](mailto:gokuldas127199544@gmail.com)")
        st.write("📷 Instagram: [gokul_mundott](https://www.instagram.com/gokul_mundott/)")

    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)