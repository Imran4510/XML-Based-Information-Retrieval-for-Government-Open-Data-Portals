import streamlit as st
import xml.etree.ElementTree as ET
import os

# Configure page
st.set_page_config(
    page_title="Crop Data Retrieval",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Correct XML file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
xml_path = os.path.join(BASE_DIR, "data.xml")

# Load XML file
tree = ET.parse(xml_path)
root = tree.getroot()

# Custom CSS
st.markdown("""
<style>
    /* Full app background */
    .stApp {
        background: linear-gradient(135deg, #f5f1e8 0%, #e8dfd2 50%, #f5f1e8 100%);
        min-height: 100vh;
    }

    /* Main content area with glass effect */
    .main .block-container {
        background: rgba(255, 255, 255, 0.28);
        padding: 2rem 2rem 3rem 2rem;
        border-radius: 20px;
        backdrop-filter: blur(4px);
        box-shadow: 0 8px 30px rgba(45, 80, 22, 0.08);
    }

    /* Subtle texture overlay */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 2px,
                rgba(45, 80, 22, 0.02) 2px,
                rgba(45, 80, 22, 0.02) 4px
            );
        pointer-events: none;
        z-index: 0;
    }

    .block-container {
        position: relative;
        z-index: 1;
    }

    /* Headings */
    h1, h2, h3 {
        color: #2D5016 !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Text */
    p, label, div {
        color: #2b2b2b !important;
    }

    /* Input fields */
    .stSelectbox, .stTextInput {
        border-radius: 12px;
    }

    .stSelectbox [data-baseweb="select"] > div,
    .stTextInput input {
        background-color: #FFFFFF !important;
        border: 2px solid #D4A574 !important;
        border-radius: 10px !important;
    }

    .stSelectbox [data-baseweb="select"] > div:hover,
    .stTextInput input:hover {
        border-color: #2D5016 !important;
        box-shadow: 0 4px 12px rgba(45, 80, 22, 0.15);
    }

    /* Search button - FIXED */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-weight: 700 !important;
        font-size: 1.05em !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.25) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #43A047 0%, #1B5E20 100%) !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 125, 50, 0.35) !important;
    }

    /* Success message */
    .stSuccess {
        background-color: rgba(45, 80, 22, 0.1) !important;
        border-left: 4px solid #2D5016 !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }

    /* Error message */
    .stError {
        background-color: rgba(196, 30, 58, 0.1) !important;
        border-left: 4px solid #C41E3A !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }

    /* Info message */
    .stInfo {
        background-color: rgba(212, 165, 116, 0.12) !important;
        border-left: 4px solid #D4A574 !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E0D5C7;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(45, 80, 22, 0.08);
    }

    [data-testid="metric-container"]:hover {
        box-shadow: 0 4px 16px rgba(45, 80, 22, 0.12);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }

    /* Better spacing */
    .element-container [data-testid="stVerticalBlock"] > [style*="flex-direction"] {
        gap: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("## 🌾 Crop Data Retrieval System")
st.markdown(
    "<p style='color: #666; margin-bottom: 2rem;'>Explore agricultural production data across Indian states</p>",
    unsafe_allow_html=True
)

# Get unique states and years from XML
states = sorted(set(
    record.find("state").text
    for record in root.findall(".//record")
    if record.find("state") is not None
))

years = sorted(set(
    int(record.find("year").text)
    for record in root.findall(".//record")
    if record.find("year") is not None
))

# Crop options
crops = ["rice", "wheat", "sugarcane", "cotton", "maize", "pulses"]

# Input layout
col1, col2, col3 = st.columns(3)

with col1:
    state = st.selectbox(
        "📍 State",
        states,
        index=states.index("Maharashtra") if "Maharashtra" in states else 0
    )

with col2:
    year = st.selectbox("📅 Year", years, index=len(years) - 1)

with col3:
    crop = st.selectbox("🌱 Crop", crops)

# Search button
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 3])

with col_btn1:
    search_clicked = st.button("🔍 Search", use_container_width=True)

# Results
if search_clicked:
    results = []

    for record in root.findall(".//record"):
        state_elem = record.find("state")
        year_elem = record.find("year")

        if state_elem is not None and year_elem is not None:
            if state_elem.text == state and int(year_elem.text) == year:
                crops_elem = record.find("crops")

                if crops_elem is not None:
                    for crop_elem in crops_elem.findall("crop"):
                        if crop_elem.get("name") == crop:
                            production = crop_elem.find("production")
                            area = crop_elem.find("area")

                            if production is not None:
                                results.append({
                                    "production": production.text,
                                    "area": area.text if area is not None else "N/A",
                                    "district": record.find("district").text if record.find("district") is not None else "N/A"
                                })

    st.markdown("---")

    if results:
        st.success(f"✅ Found {len(results)} result(s) for **{crop.capitalize()}** in **{state}** ({year})")
        st.markdown("")

        for i, result in enumerate(results, 1):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("📍 District", result["district"])

            with col2:
                try:
                    st.metric("📏 Area (1000 ha)", float(result["area"]))
                except:
                    st.metric("📏 Area (1000 ha)", result["area"])

            with col3:
                try:
                    st.metric("📊 Production (1000 t)", float(result["production"]))
                except:
                    st.metric("📊 Production (1000 t)", result["production"])

            if i < len(results):
                st.divider()
    else:
        st.error(f"❌ No data found for **{crop.capitalize()}** in **{state}** ({year})")
        st.info("Try selecting a different state, year, or crop.")



# Main logic (original code - now replaced with enhanced version above)

# import streamlit as st
# import xml.etree.ElementTree as ET
 
# # Load XML file
# tree = ET.parse("data.xml")
# root = tree.getroot()
 
# st.title("🌾 Crop Data Retrieval System")
 
# # Inputs
# state = st.text_input("Enter State")
# year = st.text_input("Enter Year")
# crop = st.selectbox("Select Crop", ["rice", "wheat"])
 
# # Button
# if st.button("Search"):
#     query = f".//record[state='{state}'][year='{year}']/crops/crop[@name='{crop}']/production"
#     results = root.findall(query)
 
#     if results:
#         for r in results:
#             st.success(f"Production: {r.text}")
#     else:
#         st.error("No data found")