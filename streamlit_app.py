import streamlit as st
import requests

st.title("Practice with Streamlit and FastAPI")
st.write("This is a simple app to demonstrate integration of Streamlit and FastAPI.")
st.write("You can submit your name, age, and favorite color below:")

name = st.text_input("Enter your name")
color = st.text_input("Enter your favorite color")
age = st.number_input("Enter your age", min_value=0, max_value=120, step=1)

if st.button("Submit"):
    if not name or not color:
        st.warning("Please fill in all fields before submitting.")
    else:
        try:
            response = requests.post(
                "http://localhost:8000/submit",
                data={"name": name, "age": age, "color": color}
            )
            if response.status_code == 200:
                st.success("Data submitted successfully!")
            else:
                st.error(f"Failed to submit data. Status code: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server. Make sure it's running.")
