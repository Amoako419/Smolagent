import gradio as gr
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

def process_query(query, history):
    # Initialize the model and agent
    model = HfApiModel()
    agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)
    
    # Run the agent with the query
    response = agent.run(query)
    
    # Return the response and update history
    history.append((query, response))
    return "", history

# Create a Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Smart Agent Interface")
    gr.Markdown("Ask anything and the agent will use code and search tools to help you.")
    
    chatbot = gr.Chatbot(height=500)
    with gr.Row():
        query_input = gr.Textbox(placeholder="What would you like to know?", label="Query", scale=8)
        submit_btn = gr.Button("Submit", variant="primary", scale=1)
    
    # Clear button to reset the conversation
    clear_btn = gr.Button("Clear Conversation")
    
    # Set up event handlers
    submit_btn.click(process_query, inputs=[query_input, chatbot], outputs=[query_input, chatbot])
    query_input.submit(process_query, inputs=[query_input, chatbot], outputs=[query_input, chatbot])
    clear_btn.click(lambda: None, None, chatbot, queue=False)

# Launch the interface
if __name__ == "__main__":
    demo.launch()