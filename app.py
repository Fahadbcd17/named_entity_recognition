# Environment configuration to handle proxy issues : ensures model loading won't be blocked in restricted networks
import os
os.environ['NO_PROXY'] = '*'
os.environ['all_proxy'] = ''
os.environ['ALL_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['socks_proxy'] = ''

# Import necessary libraries
# Gradio for UI, transformers for NER model, re for cleaning text
import gradio as gr
from transformers import pipeline
import re

# Load the NER model
load_model = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")


# Analyze input text to extract entities
# The Main function responsible for executing NER and grouping results

def analyze_input(text):

    try:
        if not text.strip():
            return "Please enter some text to analyze." # Validation for empty input
        
        # Perform the analysis
        entities = load_model(text)
        
        # Group entities by type
        grouped_entities = {}
        for entity in entities:
            entity_type = entity['entity_group']
            entity_word = entity['word']
            
            # Clean word pieces
            entity_word = re.sub(r' ##', '', entity_word)
            
            if entity_type not in grouped_entities:
                grouped_entities[entity_type] = []
            
            # Avoid duplicates to keep the output cleaner
            if entity_word not in grouped_entities[entity_type]:
                grouped_entities[entity_type].append(entity_word)
        
        # Format the output nicely
        return format_entity_output(grouped_entities, text)
        
    except Exception as e:
        # Helpful error message for debugging
        return f"Error analyzing text: {str(e)}"

def format_entity_output(grouped_entities, original_text):
    #Format the NER output

    if not grouped_entities:
        return "No named entities found in the text."
    
    output = []
    output.append("<h2>🔍 Named Entities Found</h2>")
    
    # Entity type labels and emojis
    entity_labels = {
        'PER': '👤 Persons',
        'ORG': '🏢 Organizations', 
        'LOC': '📍 Locations',
        'MISC': '📌 Miscellaneous'
    }
    
    # Loop through each category and list its entities
    for entity_type, entities in grouped_entities.items():
        label = entity_labels.get(entity_type, f'📋 {entity_type}')
        output.append(f"<h3>{label}</h3>")
        for entity in entities:
            output.append(f"• {entity}<br>")
        output.append("<br>")
    
    # Display original text with highlights
    output.append("<h2>📝 Original Text with Entities</h2>")
    highlighted_text = original_text
    
    # Apply simple HTML highlight to detected words
    for entity_type, entities in grouped_entities.items():
        for entity in entities:
            pattern = r'\b' + re.escape(entity) + r'\b'
            if re.search(pattern, highlighted_text, re.IGNORECASE):
                color = get_entity_color(entity_type)
                highlighted_text = re.sub(
                    pattern, 
                    f'<span style="background-color: {color}; padding: 2px 4px; border-radius: 3px; font-weight: bold;">{entity}</span>', 
                    highlighted_text, 
                    flags=re.IGNORECASE
                )
    
    output.append(highlighted_text)
    
    return "".join(output)

def get_entity_color(entity_type):

    #Return a highlight color for each entity type

    colors = {
        'PER': "#B2C0B2",    
        'ORG': "#CDB5B5",    
        'LOC': "#88896F",    
        'MISC': "#9E98A9"     
    }
    return colors.get(entity_type, '#FFEAA7')  # Default light yellow

def process_text(text):
    # function to trigger analysis.
    return analyze_input(text)

# Create Gradio interface
with gr.Blocks(title="Named Entity Recognition") as demo:
    gr.Markdown("# 🔍 Named Entity Recognition")
    gr.Markdown("Enter text to identify persons, organizations, locations, and other entities using BERT NER model")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Input Text",
                placeholder="Enter text here to analyze for named entities...",
                lines=8,
                max_lines=15
            )
            analyze_btn = gr.Button("Analyze Entities", variant="primary")
            clear_btn = gr.Button("Clear")
        
        with gr.Column():
            analysis_output = gr.HTML(
                label="Entity Analysis"
            )
        
    # Example inputs for quick testing
    examples = [
        "Yunnan University is the best University in Yunnan Province",
        "Kunming is the capital of Yunnan",
        "Beijing is the capital of China",
        "Mao Zedong was a Chinese politician, who founded the People's Republic of China"
    ]
    
    gr.Examples(
        examples=examples,
        inputs=text_input,
        outputs=analysis_output,
        fn=process_text,
        cache_examples=False
    )
    
    # Button actions
    analyze_btn.click(
        fn=process_text,
        inputs=text_input,
        outputs=analysis_output
    )
    
    clear_btn.click(
        fn=lambda: ("", ""),
        inputs=[],
        outputs=[text_input, analysis_output]
    )

# Run the Gradio app
if __name__ == "__main__":
    demo.launch(share=True)
