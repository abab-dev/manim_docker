import streamlit as st
import requests
import google.generativeai as genai

# Replace with your Gemini API key
GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)

# Replace with the URL of your FastAPI endpoint
FASTAPI_URL = "http://localhost:8000/convert/"

def generate_code(prompt):
    """
    Generates Python code using the Gemini API based on the given prompt.
    """
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Generate Manim code based on this description: {prompt}")
    return response.text

def main():
    st.title("Manim Code Generator")

    # Chat input
    prompt = st.text_input("Enter your animation description:")

    # Scene name input
    scene_name = st.text_input("Enter the scene name:", value="MyScene")

    if st.button("Generate Code"):
        if not GOOGLE_API_KEY or GOOGLE_API_KEY == "YOUR_GEMINI_API_KEY":
            st.error("Please set your Gemini API key in the code.")
            return

        if prompt:
            # Generate code using Gemini
            generated_code = generate_code(prompt)
            st.code(generated_code, language="python")

            # Send code to FastAPI endpoint
            if st.button("Run Animation"):
                data = {"scene_name": scene_name, "code": generated_code}
                response = requests.post(FASTAPI_URL, data=data)

                # Display the streaming response
                if response.status_code == 200:
                    st.subheader("Rendering Log:")
                    for line in response.iter_content(chunk_size=None, decode_unicode=True):
                        st.text(line)  # Display each line of the stream

                    # Extract the download link
                    if "::done::" in response.text:
                        download_link = response.text.split("::done::")[1].strip()
                        st.markdown(f"Download video: [link]({download_link})")
                    elif "::error::" in response.text:
                        st.error("Rendering failed. Check the logs for errors.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
        else:
            st.warning("Please enter a description.")

if __name__ == "__main__":
    main()
