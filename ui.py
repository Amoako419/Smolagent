import streamlit as st
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

# Initialize the agent
model = HfApiModel()
agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)

# Streamlit app
st.title("Chatbot UI")

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []



# Input for the agent prompt
query = st.text_input("You:")

# Button to run the agent
if st.button("Send"):
    with st.spinner('Thinking...'):
        response = agent.run(query)
        st.session_state.history.append(("User", query))
        st.session_state.history.append(("Assistant", response))
        
        
# Display the conversation history
for role, message in st.session_state.history:
    st.markdown(f"**{role}:** {message}")