import streamlit as st


def init():
    if "selected_objects" not in st.session_state:
        st.session_state.selected_objects = {}
