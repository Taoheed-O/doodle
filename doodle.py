import streamlit as st
import pandas as pd
from io import BytesIO

# Function to load uploaded Excel file
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            return df
        except FileNotFoundError:
            st.error("File not found.")
        except ValueError:
            st.error("The file format is incorrect. Please upload a valid Excel file.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
        return None
    else: 
        return None

# Streamlit app layout and functionality
def main():
    st.title("Streamlit Q&A with Note-Taking App")

    # File upload section
    uploaded_file = st.file_uploader("Upload Excel File", type="xlsx")

    # Load data based on uploaded file
    df = load_data(uploaded_file)

    # Check if the file has been successfully uploaded and loaded
    if df is not None:
        # Check if the file contains a 'Question' column
        if "Question" not in df.columns:
            st.warning("The Excel file must contain a 'Question' column.")
        elif df.empty:
            st.warning("Your uploaded spreadsheet is empty. Please add questions and notes.")
        else:
            # Random question button
            if st.button("Get Random Question"):
                random_question = df["Question"].sample(1).values[0]
                st.subheader("Question:")
                st.write(random_question)

                # Note-taking section
                note_input = st.text_input("Add Note (Optional)", key="note")

                # Button to save the note
                if st.button("Save Note"):
                    if note_input:
                        # Add the note as a new row
                        new_row = pd.DataFrame({"Question": [random_question], "Note": [note_input]})
                        df = pd.concat([df, new_row], ignore_index=True)

                        # Save updated DataFrame to an in-memory buffer
                        buffer = BytesIO()
                        df.to_excel(buffer, index=False, engine='xlsxwriter')

                        # Provide download option for the updated file
                        st.download_button(
                            label="Download updated file",
                            data=buffer,
                            file_name='updated_file.xlsx',
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
                        st.success("Note saved successfully!")
                    else:
                        st.warning("Please enter a note before saving.")
    else:
        st.info("Please upload an Excel file to get started.")

if __name__ == "__main__":
    main()
