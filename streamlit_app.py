import streamlit as st
import requests

st.set_page_config(page_title="FastAPI Code Generator", layout="centered")

st.title("🚀 FastAPI Code Generator for Organizations")

# Step 1: User input
org_name = st.text_input("Enter your organization name")

if st.button("Generate API Code"):
    if not org_name.strip():
        st.error("Please enter a valid organization name")
    else:
        with st.spinner("Generating..."):
            # Step 2: Call /generate_org
            response = requests.get(
                "http://127.0.0.1:8000/generate_org", params={"name": org_name}
            )

            if response.status_code == 200:
                org_data = response.json()

                org_id = org_data["org_id"]
                api_key = org_data["api_key"]
                base_url = org_data["base_url"]

                # Step 3: Call /generate_sample_code
                code_res = requests.get(
                    "http://127.0.0.1:8000/generate_sample_code",
                    params={"org_id": org_id, "org_name": org_name},
                )

                if code_res.status_code == 200:
                    code_data = code_res.json()
                    code = code_data["generated_code"]

                    # Step 4: Display info
                    st.success("✅ API generated successfully!")

                    st.subheader("📌 Organization Details")
                    st.write(f"**Org Name:** {org_name}")
                    st.write(f"**Org ID:** `{org_id}`")
                    st.write(f"**API Key:** `{api_key}`")
                    st.write(f"**Base API URL:** `/api/org/{org_id}/users/`")

                    st.subheader("📄 Auto-Generated FastAPI Code")
                    st.code(code, language="python")

                    # Step 5: Download button
                    st.download_button(
                        label="⬇ Download Python API Code",
                        data=code,
                        file_name=f"{org_name.lower()}_api.py",
                        mime="text/plain",
                    )
                else:
                    st.error("❌ Failed to generate sample code.")
            else:
                st.error("❌ Failed to create organization.")
