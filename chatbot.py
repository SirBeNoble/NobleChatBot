import streamlit as st 
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq


st.title("Chat with Agent Noble!")
st.write("Hello! I'm your friendly Gro/Ollama Chatbot, named NOBLE. I can help answer your questions, provide information on any topic, or just chat. Let's start a conversation!")

conversatoinal_memory_length = 18

memory = ConversationBufferWindowMemory(k=conversatoinal_memory_length)


# session state variable
if 'chat_history' not in st.session_state:
    st.session_state.chat_history=[]
else:
    for message in st.session_state.chat_history:
        memory.save_context(
            {'input':message['human']},
            {'output':message['AI']}
                )


# Initialize Groq Langchain chat object and conversation
groq_chat = ChatGroq(
    groq_api_key=("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"), 
    model_name="llama3-70b-8192"
    )

# Create a conversation chain using the LangChain LLM (Language Learning Model)
conversation = ConversationChain(
    llm=groq_chat,  # The Groq LangChain chat object initialized earlier.
    memory=memory,  # The conversational memory object that stores and manages the conversation history.
    )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("Ask a question..."):
    # Display user message in chat message container
    with st.chat_message("User:"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    response = conversation(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("NOBLE:"):
        st.markdown(response["response"])
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response["response"]})
