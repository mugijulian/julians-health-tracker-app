import requests
import streamlit as st
import pandas as pd
import numpy as np
import json


st.markdown('<h1 style="color: sandybrown;">Easy Jotting 📝', unsafe_allow_html=True)
st.markdown('<h2 style="color: sienna;">Julian\'s simple note taking app',unsafe_allow_html=True)

if st.button('Need a random piece of advice today? Click here.'):
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)
    advice_data = response.json()
    advice_text = advice_data['slip']['advice']
    st.write(advice_text)

if "notes" not in st.session_state:
    st.session_state["notes"] = {}
if "current_note" not in st.session_state:
    st.session_state["current_note"] = ""
if "creating_new_note" not in st.session_state:
    st.session_state["creating_new_note"] = False
if 'delete_error_shown' not in st.session_state:
    st.session_state['delete_error_shown'] = False

with st.sidebar:
    st.header("Manage your notes")

    if st.button("Create New Note"):
        st.session_state["creating_new_note"] = True
        st.session_state["new_note_title"] = ""

    if st.session_state["creating_new_note"]:
        new_note_title = st.text_input("New note title:", key="new_note_title")
        if st.button("Open New Note"):
            if new_note_title and new_note_title not in st.session_state["notes"]:
                st.session_state["notes"][new_note_title] = ""
                st.session_state["current_note"] = new_note_title
                st.session_state["creating_new_note"] = False
                st.success("New note created!")
            else:
                st.error("Please enter a unique title for the new note.")

    if not st.session_state["creating_new_note"]:
        if st.session_state["notes"]:
            note_titles = list(st.session_state["notes"].keys())
            if st.session_state["current_note"] not in note_titles:
                st.session_state["current_note"] = note_titles[0] if note_titles else ""
            selected_note = st.selectbox("Select a note to view/edit:", note_titles, key="note_select",
                                             index=note_titles.index(st.session_state["current_note"]) if
                                             st.session_state["current_note"] in note_titles else 0)

            if selected_note:
                st.session_state["current_note"] = selected_note

if st.session_state["current_note"]:
    st.subheader(f"Current Note: {st.session_state['current_note']}")
    note_content = st.text_area("Write here:", st.session_state["notes"][st.session_state["current_note"]])

    if st.button("Save Note"):
        st.session_state["notes"][st.session_state["current_note"]] = note_content
        st.success("Note saved successfully!")

    col1, col2 = st.columns(2)

    with col2:
        if st.checkbox("Confirm delete note", key="delete_confirm"):
            if st.button("Confirm Delete"):
                if st.session_state["delete_confirm"]:
                    if not st.session_state['delete_error_shown']:
                        st.error("Please click again to confirm. Otherwise, click save to cancel.")
                        st.session_state['delete_error_shown'] = True
                    else:
                        del st.session_state["notes"][st.session_state["current_note"]]
                        st.session_state["current_note"] = ""
                        st.session_state['delete_error_shown'] = False
                        st.success("Note is being deleted! Click any button to move on.")
