import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import tempfile
import os
import dtale

# 🌟 Page config
st.set_page_config(page_title="DataSpark", layout="centered")

# 🎨 Title
st.markdown("<h1 style='text-align: center;'>🚀 DataSpark </h1>", unsafe_allow_html=True)

# 📁 File uploader
uploaded_file = st.file_uploader("📤 Upload your CSV file (Max size: 200 MB)", type=["csv"])

# ➤ Analyze button aligned to the right
col1, col2, col3 = st.columns([1, 1, 1.5])
with col3:
    analyze_clicked = st.button("🔍 Analyze", use_container_width=True)

# 🧠 Run analysis and cache results in session_state
if uploaded_file is not None and analyze_clicked:
    with st.spinner("Generating profiling report and launching D-Tale... please wait ⏳"):
        df = pd.read_csv(uploaded_file)
        profile = ProfileReport(df, title="DataSpark Report", explorative=True)

        # Save report to session state
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
            profile.to_file(tmp_file.name)
            st.session_state["report_html_path"] = tmp_file.name

        with open(st.session_state["report_html_path"], 'rb') as f:
            st.session_state["report_html_bytes"] = f.read()

        # Start D-Tale and store URL
        d = dtale.show(df, subprocess=False)
        st.session_state["d_tale_url"] = d._main_url

        st.session_state["analysis_complete"] = True

# ✅ Show buttons if analysis already done
if st.session_state.get("analysis_complete", False):
    st.success("✅ Analysis complete!")
    st.markdown("### 🔗 Explore Your Dataset:")

    # col_left, col_right = st.columns([1, 1])

    # with col_left:
    #     st.download_button(
    #         label="📥 Download Profiling Report",
    #         data=st.session_state["report_html_bytes"],
    #         file_name="Report.html",
    #         mime="text/html",
    #         use_container_width=True
    #     )

    # with col_right:
    #     st.markdown(
    #         f"""
    #         <a href="{st.session_state['d_tale_url']}" target="_blank">
    #             <button style="background-color: #1c1f26; color: white; padding: 0.6rem 1.2rem;
    #                            border: 1px solid #444; border-radius: 8px; width: 100%; margin-top: 0.25rem;">
    #                 📈 Launch D-Tale Dashboard
    #             </button>
    #         </a>
    #         """,
    #         unsafe_allow_html=True
    #     )
    
    col_left, col_right = st.columns(2)

    with col_left:
        st.download_button(
        label="📥 Download Profiling Report",
        data=st.session_state["report_html_bytes"],
        file_name="Report.html",
        mime="text/html",
        use_container_width=True
    )

    with col_right:
        st.markdown(
        f"""
        <a href="{st.session_state['d_tale_url']}" target="_blank" style="text-decoration: none;">
            <div style="display: flex; align-items: center; justify-content: center;
                        background-color: #1c1f26; color: white; padding: 0.6rem 1.2rem;
                        border: 1px solid #444; border-radius: 8px; width: 100%; height: 2.7rem;">
                📈 Launch D-Tale Dashboard
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )


# In Packages.txt
# | 📦 Package Name   | 🔍 Description                                                                                                          |
# | ----------------- | ----------------------------------------------------------------------------------------------------------------------- |
# | `libgl1-mesa-glx` | This is a **Linux system library** that provides **OpenGL** rendering support through the **Mesa 3D Graphics Library**. |
