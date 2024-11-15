import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import networkx as nx
from PIL import Image, ImageDraw

# Define ROOM_CLASS and ID_COLOR for room type mappings
ROOM_CLASS = {"living_room": 1, "kitchen": 2, "bedroom": 3, "bathroom": 4, "balcony": 5, "entrance": 6, "dining room": 7, "study room": 8,
            "storage": 10 , "front door": 11, "unknown": 13, "interior_door": 12}
ID_COLOR = {1: '#EE4D4D', 2: '#C67C7B', 3: '#FFD274', 4: '#BEBEBE', 5: '#BFE3E8',
                6: '#7BA779', 7: '#E87A90', 8: '#FF8C69', 10: '#1F849B', 11: '#727171',
                13: '#785A67', 12: '#D3A2C7'}

# Streamlit UI for input
st.title("Generative Design Visualization")

# Initialize session state for room data if not already present
if 'room_data' not in st.session_state:
    st.session_state.room_data = []

# Room Input Form
with st.form("room_form"):
    room_type = st.selectbox("Select Room Type", list(ROOM_CLASS.keys()))
    room_num = st.number_input("Enter Room Number", min_value=1, step=1)
    room_size = st.number_input("Enter Room Size", min_value=0.0, step=1.0)

    if st.form_submit_button("Add Room"):
        room_exists = any(room['number'] == room_num for room in st.session_state.room_data)
        if not room_exists:
            st.session_state.room_data.append({
                'type': room_type,
                'number': room_num,
                'size': room_size
            })
            st.success(f"Room {room_num} added.")
        else:
            st.error(f"Room {room_num} already exists. Please use a different room number.")

# Display added rooms
if st.session_state.room_data:
    st.subheader("Added Rooms")
    for room in st.session_state.room_data:
        st.text(f"Room {room['number']} - {room['type'].capitalize()} - {room['size']}")

# Connectivity Input
connections = st.text_area("Enter Room Connections (format: room_num1,connectivity,room_num2)",
                           placeholder="Example: 1,1,2\n2,-1,4")

# Boundary Input
boundary_coords = st.text_area("Enter Boundary Coordinates (format: x1,y1 x2,y2 ...)",
                               placeholder="Example: 0,0 10,0 10,10 0,10")