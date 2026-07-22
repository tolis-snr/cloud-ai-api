import streamlit as st
import requests

# The exact URL of your LIVE Azure API (with https:// included)
API_URL = "https://tolis-ai-api-fubqb5e0euacgcae.italynorth-01.azurewebsites.net"

# Page configuration
st.set_page_config(page_title="RAG AI Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Cloud-Native RAG Assistant")
st.markdown("Upload your own data and ask questions!")

# --- SIDEBAR: Upload Knowledge ---
with st.sidebar:
    st.header("📚 Upload Knowledge")
    source_name = st.text_input("Source Name (e.g., 'Company Rules')")
    knowledge_text = st.text_area("Paste your text here...", height=250)

    if st.button("Upload to AI Memory"):
        if source_name and knowledge_text:
            with st.spinner("Saving to Vector Database..."):
                try:
                    # POST request to /upload-knowledge
                    response = requests.post(
                        f"{API_URL}/upload-knowledge", 
                        json={"text": knowledge_text, "source_name": source_name}
                    )
                    
                    if response.status_code == 200:
                        st.success("Knowledge uploaded successfully!")
                    else:
                        st.error(f"Error uploading knowledge: {response.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
            st.warning("Please provide both a Source Name and Text.")


# --- MAIN AREA: Chat Interface ---
# Initialize chat history in session state (so messages don't disappear on refresh)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_question := st.chat_input("Ask a question about the uploaded text..."):
    
    # 1. Display user message in chat container
    st.chat_message("user").markdown(user_question)
    
    # 2. Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_question})

    # 3. AI Response generation
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # POST request to /ask
                response = requests.post(
                    f"{API_URL}/ask", 
                    json={"question": user_question}
                )
                
                if response.status_code == 200:
                    json_resp = response.json()
                    answer = json_resp.get("answer", "No answer found in response.")
                    context_used = json_resp.get("context_used", "") # ΠΑΙΡΝΟΥΜΕ ΤΟ CONTEXT
                    
                    # --- CLEANUP LOGIC ---
                    if isinstance(answer, list) and len(answer) > 0 and "text" in answer[0]:
                        answer = answer[0]["text"]
                    elif isinstance(answer, str) and answer.startswith("[{") and "'text':" in answer:
                        import ast
                        try:
                            parsed_answer = ast.literal_eval(answer)
                            answer = parsed_answer[0]["text"]
                        except Exception:
                            pass
                    # ---------------------

                    st.markdown(answer)
                    
                    # --- DEBUGGING MENU (Βλέπουμε τι διάβασε το AI) ---
                    with st.expander("🔍 See what the AI read (Context)"):
                        if context_used:
                            st.write(context_used)
                        else:
                            st.warning("The Database returned nothing! It's empty or search failed.")
                    # ---------------------------------------------------
                    
                    # Add AI message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"API Error ({response.status_code}): {response.text}")
                    
            except Exception as e:
                st.error(f"Connection failed: {e}")