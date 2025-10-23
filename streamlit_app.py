import streamlit as st
import requests
import json

st.set_page_config(page_title="API Code Generator", layout="centered")

st.title("🚀 API Code Generator")

# Step 1: Upload Postman Collection
st.subheader("📂 Upload your Postman Collection")
uploaded_file = st.file_uploader("Choose a Postman collection (.json)", type=["json"])

# Step 2: Language Selection
st.subheader("💻 Select target language")
language = st.selectbox("Choose a language for generated code:", ["Python (FastAPI)", "Node.js (Express)", "Go", "Java (Spring Boot)"])

# Step 3: Generate Code
if uploaded_file and language:
    if st.button("⚡ Generate API Code"):
        try:
            # Read Postman JSON content
            postman_data = json.load(uploaded_file)

            with st.spinner("Generating code..."):

                # Send to FastAPI backend
                response = requests.post(
                    "http://127.0.0.1:8000/generate_from_postman",
                    json={
                        "postman": postman_data,
                        "language": language
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    code = result.get("generated_code", "")

                    st.success("✅ API code generated successfully!")

                    st.subheader("📄 Generated Code")
                    if language == "Python (FastAPI)":
                        st.code(code, language="python")
                    elif language == "Node.js (Express)":
                        st.code(code, language="javascript")
                    elif language == "Go":
                        st.code(code, language="go")
                    elif language == "Java (Spring Boot)":
                        st.code(code, language="java")
                    else:
                        st.code(code)

                    # Download button
                    st.download_button(
                        label="⬇ Download Generated Code",
                        data=code,
                        file_name=f"generated_api_{language.lower().replace(' ', '_')}.txt",
                        mime="text/plain",
                    )
                else:
                    st.error(f"❌ Failed to generate code. {response.text}")

        except Exception as e:
            st.error(f"Error: {str(e)}")
else:
    st.info("📌 Please upload a Postman collection and choose a language to proceed.")
