import streamlit as st
from app.parser import parse_whatsapp_chat
from app.utils import filter_by_date
from app.summarizer import summarize_chats

def run_ui():
    st.title("📱 WhatsApp Chat Summarizer (GenAI Powered)")

    uploaded_file = st.file_uploader("Upload WhatsApp .txt file", type=["txt"])
    
    if uploaded_file:
        file_content = uploaded_file.read().decode("utf-8")
        messages = parse_whatsapp_chat(file_content)
        
        if not messages:
            st.warning("Could not parse the file correctly. Make sure it's a valid exported chat.")
            return
        
        # Debugging: Show first 5 parsed messages with timestamps
        st.write("### Sample Parsed Messages")
        for msg in messages[:5]:
            st.write(f"{msg['timestamp']} - {msg['sender']}: {msg['message']}")

        st.success(f"Parsed {len(messages)} messages.")

        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        custom_prompt = st.text_area("Enter your custom summarization prompt", 
                                     value="Summarize the assignment deadlines and important updates from the chat.")
        
        if st.button("Summarize"):
            filtered_df = filter_by_date(messages, start_date, end_date)
            
            if filtered_df.empty:
                st.warning("No messages in the selected date range.")
            else:
                with st.spinner("Summarizing with GenAI..."):
                    summary = summarize_chats(filtered_df, custom_prompt)
                    st.subheader("📝 Summary")
                    st.write(summary)
