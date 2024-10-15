import base64

import streamlit as st
from functions import create_vectorstore_from_texts, get_pdf_text, query_document

# Initialize the API key in session state if it doesn't exist
if "api_key" not in st.session_state:
    st.session_state.api_key = ""


def display_pdf(uploaded_file):
    """
    Display a PDF file that has been uploaded to Streamlit.

    The PDF will be displayed in an iframe, with the width and height set to 700x1000 pixels.

    Parameters
    ----------
    uploaded_file : UploadedFile
        The uploaded PDF file to display.

    Returns
    -------
    None
    """
    try:
        # Código potencialmente problemático
        # Read file as bytes:
        bytes_data = uploaded_file.getvalue()

        # Convert to Base64
        base64_pdf = base64.b64encode(bytes_data).decode("utf-8")

        # Embed PDF in HTML
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="350" height="500" type="application/pdf"></iframe>'

        # Display file
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
        print(e)


if __name__ == "__main__":
    with st.sidebar:
        st.header("Input your OpenAI API key")
        st.text_input(
            "OpenAI API key",
            type="password",
            key="api_key",
            label_visibility="collapsed",
            disabled=False,
        )
        st.header("Upload file")
        uploaded_file = st.file_uploader("Please upload your PDF document:", type="pdf")

    col1, col2 = st.columns(2)
    with col1:
        if uploaded_file is not None:
            try:
                display_pdf(uploaded_file)

                # Load in the documents
                documents = get_pdf_text(uploaded_file)
                st.session_state.vector_store = create_vectorstore_from_texts(
                    documents,
                    api_key=st.session_state.api_key,
                    file_name=uploaded_file.name,
                )
                st.write("Input Processed")
            # Código potencialmente problemático
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
                print(e)

    with col2:
        try:
            # Código potencialmente problemático
            if st.button("Generate table"):
                with st.spinner("Generating answer"):
                    # Load vectorstore:

                    answer = query_document(
                        vectorstore=st.session_state.vector_store,
                        query="Give me the title, summary, publication date, and authors of the research paper.",
                        api_key=st.session_state.api_key,
                    )

                    placeholder = st.empty()
                    placeholder = st.write(answer)
        except Exception as e:
            st.error(f"Ocurrió un error generando la respuesta: {e}")
            print(e)
