import streamlit as st
import requests
import streamlit.components.v1 as components
from graph import generate_graph


BASE_URL = "http://localhost:8000"

st.title("Synthetic Selection Module Management System")

with st.expander("Module related functions"):
    response = requests.get(f"{BASE_URL}/get_all_users")
    st.json(response.json())


with st.expander("Module related functions"):

    # Endpoint to get all modules
    if st.button("Get All Modules") and not st.button("Clear"):
        response = requests.get(f"{BASE_URL}/get_all_modules")
        st.json(response.json())

    # Endpoint to get a specific module by ID
    st.subheader("Get a Specific Module")
    module_id = st.number_input("Enter Module ID", min_value=0, value=0, step=1)
    if st.button("Get Module"):
        response = requests.get(f"{BASE_URL}/get_module", params={"id": module_id})
        st.json(response.json())

    # Endpoint to create a module
    st.subheader("Create a Specific Module")
    module_name = st.text_input("Enter Module Name")
    owner_id = st.number_input("Enter Owner ID", min_value=0, value=0, step=1)
    if st.button("Create Module") and not st.button("Clear"):
        response = requests.post(
            f"{BASE_URL}/create_module?module_name={module_name}&owner_id={owner_id}"
        )
        st.json(response.json())


with st.expander("Linkage related functions"):
        # Endpoint to create a linkage between modules
    st.subheader("Create a Linkage Between Modules")
    parent_id = st.number_input(
        "Enter Parent Module ID", min_value=0, value=0, step=1, key="parent_id"
    )
    child_id = st.number_input(
        "Enter Child Module ID", min_value=0, value=0, step=1, key="child_id"
    )
    if st.button("Create Linkage") and not st.button("Clear"):
        response = requests.post(
            f"{BASE_URL}/create_linkage?parent_id={parent_id}&child_id={child_id}"
        )
        st.json(response.json())


st.subheader("Creating a graph!")
if st.button("Generate Graph") and not st.button("Clear"):
    # Read the HTML file

    generate_graph()

    html_file = open("graph.html", 'r', encoding='utf-8')
    source_code = html_file.read()
    html_file.close()

    # Use Streamlit's components.html to render the HTML
    components.html(source_code, height=800)
