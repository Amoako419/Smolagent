import gradio as gr
from smolagents import CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, HfApiModel, Tool, tool, VisitWebpageTool

@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion: The type of occasion for the party.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."

@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.
    
    Args:
        query: A search term for finding catering services.
    """
    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }
    
    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)
    
    return best_service

class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""
    
    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }
    
    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic Gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }
        
        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")

def process_query(query, history):
    try:
        # Initialize the agent with all tools
        agent = CodeAgent(
            tools=[
                DuckDuckGoSearchTool(), 
                VisitWebpageTool(),
                suggest_menu,
                catering_service_tool,
                SuperheroPartyThemeTool()
            ], 
            model=HfApiModel(),
            max_steps=10,
            verbosity_level=2
        )
        
        # Run the agent with the query
        response = agent.run(query)
        
        # Return the response and update history
        history.append((query, response))
        return "", history
    except Exception as e:
        error_message = f"Error: {str(e)}"
        history.append((query, error_message))
        return "", history

# Define theme options for the dropdown
theme_options = ["classic heroes", "villain masquerade", "futuristic Gotham"]

# Create a Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Wayne Manor Party Planner")
    gr.Markdown("Alfred's AI assistant for planning the perfect superhero-themed events")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Party Settings")
            theme_dropdown = gr.Dropdown(
                choices=theme_options,
                label="Party Theme",
                value="villain masquerade"
            )
            
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=500, label="Alfred's Responses")
            with gr.Row():
                query_input = gr.Textbox(
                    placeholder="What would you like to know about planning your superhero party?", 
                    label="Your Question", 
                    scale=8
                )
                submit_btn = gr.Button("Ask Alfred", variant="primary", scale=1)
            
            # Example queries
            gr.Examples(
                examples=[
                    ["Give me the best playlist for a party at Wayne Manor with a villain masquerade theme"],
                    ["What food should I serve at a classic heroes themed party?"],
                    ["Suggest decorations for a futuristic Gotham party"],
                    ["Who are the best caterers in Gotham City?"],
                    ["Create an invitation for a superhero costume party"]
                ],
                inputs=[query_input]
            )
            
            # Add theme suggestion to query
            def add_theme_to_query(query, theme):
                if theme and not theme.lower() in query.lower():
                    return f"{query} with a {theme} theme"
                return query
                
            # Clear button to reset the conversation
            clear_btn = gr.Button("Clear Conversation")
    
    # Set up event handlers
    combined_input = submit_btn.click(
        add_theme_to_query, 
        inputs=[query_input, theme_dropdown], 
        outputs=query_input
    ).then(
        process_query, 
        inputs=[query_input, chatbot], 
        outputs=[query_input, chatbot]
    )
    
    query_input.submit(
        add_theme_to_query, 
        inputs=[query_input, theme_dropdown], 
        outputs=query_input
    ).then(
        process_query, 
        inputs=[query_input, chatbot], 
        outputs=[query_input, chatbot]
    )
    
    clear_btn.click(lambda: None, None, chatbot, queue=False)

# Launch the interface
if __name__ == "__main__":
    demo.launch(share=True)