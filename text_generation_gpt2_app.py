import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import random
from datetime import datetime

# Set page config with creative theme
st.set_page_config(
    page_title="✨ Magic Text Generator",
    page_icon="🧙‍♂️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load GPT-2 Model and Tokenizer with progress indication
@st.cache_resource(show_spinner=False)
def load_model():
    with st.spinner("🔮 Summoning the AI wizard..."):
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        model = GPT2LMHeadModel.from_pretrained("gpt2")
        model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# Define Text Generation Function with enhanced completion
def generate_text(prompt, max_length=150, writing_style="creative"):
    try:
        # Create style-specific prompts with clear instructions
        style_instructions = {
            "creative": "Write a creative and imaginative continuation that completes the thought:",
            "formal": "Write a formal and well-structured completion of:",
            "humorous": "Write a funny and entertaining completion of:",
            "poetic": "Write a poetic and lyrical completion of:",
            "technical": "Write a precise and technical completion of:"
        }
        
        instruction = style_instructions.get(writing_style.lower(), "Write a completion of:")
        full_prompt = f"{instruction} {prompt}\n\nCompletion:"
        
        inputs = tokenizer.encode(full_prompt, return_tensors="pt")
        
        # Generate text with attention to completion
        outputs = model.generate(
            inputs,
            max_length=max_length,
            min_length=max(50, int(max_length * 0.7)),  # Ensure substantial completion
            do_sample=True,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,  # Reduce repetition
            early_stopping=True  # Stop at natural conclusion
        )
        
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the prompt part and ensure completion
        if prompt in generated_text:
            generated_text = generated_text.replace(full_prompt, "").strip()
        
        # Ensure the text ends with proper punctuation
        if generated_text and generated_text[-1] not in {'.', '!', '?', '"', "'"}:
            generated_text += "."
            
        return generated_text
    except Exception as e:
        st.error(f"✨ The magic spell failed! Error: {str(e)}")
        return None

# Creative prompt suggestions
PROMPT_SUGGESTIONS = [
    "A dragon who loves baking cookies",
    "The secret diary of a time traveler",
    "What if the moon was made of cheese?",
    "A conversation between two AI assistants",
    "The most unusual superhero origin story",
    "A detective story set in 3023",
    "A poem about quantum physics",
    "Instructions for taming a unicorn"
]

# Custom CSS for styling
st.markdown("""
<style>
    .stTextArea textarea {
        min-height: 120px;
    }
    .stButton>button {
        background-color: #9c27b0;
        color: white;
        border-radius: 20px;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #7b1fa2;
        transform: scale(1.05);
    }
    .stDownloadButton>button {
        background-color: #2196f3;
        color: white;
        border-radius: 20px;
    }
    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #9c27b0, #2196f3);
    }
    .css-1aumxhk {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 20px;
    }
    .css-1v0mbdj {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with additional features
with st.sidebar:
    st.markdown("### 🔮 Magic Settings")
    
    # Theme selector
    theme = st.radio(
        "Choose your theme:",
        ("Default", "Dark", "Light", "Wizard"),
        index=0,
        help="Change the visual theme of the app"
    )
    
    # Prompt helper
    if st.button("🎲 Random Prompt"):
        random_prompt = random.choice(PROMPT_SUGGESTIONS)
        st.session_state.random_prompt = random_prompt
    
    st.markdown("---")
    st.markdown("### 📜 Writing Styles")
    writing_style = st.selectbox(
        "Select a style:",
        ("Creative", "Formal", "Humorous", "Poetic", "Technical"),
        index=0
    )
    
    st.markdown("---")

# Main app interface
st.title("✨ Magic Text Generator")
st.markdown("""
<div style="background-color:#f0f2f6;padding:20px;border-radius:10px;margin-bottom:20px;">
    <h3 style="color:#9c27b0;">🧙‍♂️ Conjure creative text with AI magic!</h3>
    <p>Enter a prompt below and the AI will generate a complete response in your selected style.</p>
</div>
""", unsafe_allow_html=True)

# Prompt input with random suggestion
if 'random_prompt' in st.session_state:
    prompt = st.text_area(
        "📝 Enter your prompt or story starter:",
        value=st.session_state.random_prompt,
        help="The AI will generate a complete response based on your input"
    )
else:
    prompt = st.text_area(
        "📝 Enter your prompt or story starter:",
        value="The future of artificial intelligence",
        help="The AI will generate a complete response based on your input"
    )

# Generation settings
with st.expander("⚙️ Generation Settings", expanded=True):
    max_len = st.slider(
        "📏 Response Length",
        50, 500, 150, step=10,
        help="Approximate length of the generated response"
    )

# Generate button with animation
generate = st.button(
    "✨ Cast the Spell (Generate Text)",
    help="Click to generate your magical text"
)

if generate and prompt.strip():
    with st.spinner("🌀 The AI wizard is conjuring your text..."):
        output = generate_text(
            prompt,
            max_length=max_len,
            writing_style=writing_style.lower()
        )
    
    if output:
        st.balloons()
        st.subheader("📖 Your Magical Creation")
        
        # Display output in a nice container
        st.markdown(f"""
        <div style="
            background-color:#black;
            padding:20px;
            border-radius:10px;
            border-left:5px solid #9c27b0;
            margin-bottom:20px;
        ">
            {output.replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        # Download and copy buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            st.download_button(
                "💾 Download as TXT",
                output,
                file_name=f"magic_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                help="Save your generated text to a file"
            )
        with col2:
            if st.button("📋 Copy to Clipboard"):
                st.session_state.clipboard = output
                st.success("Text copied to clipboard!")
        
        # Feedback mechanism
        st.markdown("---")
        feedback = st.radio(
            "How do you like this generated text?",
            ("🤩 Amazing!", "😊 Good", "😐 Okay", "👎 Not great"),
            horizontal=True
        )
        
        if st.button("Submit Feedback"):
            st.success("Thanks for your feedback! It helps improve the magic.")
            
elif generate:
    st.warning("🪄 The wizard needs a prompt to work his magic! Please enter some text.")

# Add footer
st.markdown("---")
st.markdown("""

""", unsafe_allow_html=True)
