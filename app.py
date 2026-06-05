import streamlit as st
import json
import os
from llm import get_recipe
from prompts import build_recipe_prompt

FAVORITES_FILE = "favorites.json"

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r") as f:
            return json.load(f)
    return []

def save_favorite(craving, cuisine, recipe):
    saved = load_favorites()
    saved.append({"craving": craving, "cuisine": cuisine, "recipe": recipe})
    with open(FAVORITES_FILE, "w") as f:
        json.dump(saved, f, indent=2)

st.set_page_config(page_title="Chef's Helper", page_icon="🍲", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Lato', sans-serif; }
    .stApp { background: linear-gradient(135deg, #1a0a00 0%, #3b1a08 50%, #1a0a00 100%); min-height: 100vh; }
    .main-header { text-align: center; padding: 2rem 0 1rem 0; }
    .main-header h1 { font-family: 'Playfair Display', serif; font-size: 3rem; color: #f5c842; text-shadow: 2px 2px 8px rgba(0,0,0,0.5); margin-bottom: 0.2rem; }
    .main-header p { color: #f0e6d3; font-size: 1.1rem; letter-spacing: 1px; }
    .recipe-card { background: rgba(255, 248, 235, 0.95); border-left: 5px solid #f5c842; border-radius: 12px; padding: 2rem; margin-top: 2rem; color: #1a0a00; line-height: 1.8; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }
    .recipe-card h3 { font-family: 'Playfair Display', serif; color: #8b1a1a; font-size: 1.5rem; margin-bottom: 1rem; }
    .stTextInput > label, .stSelectbox > label { color: #f0e6d3 !important; font-weight: 600; }
    .stTextInput > div > div > input { background: rgba(255,255,255,0.95) !important; border: 1px solid rgba(245,200,66,0.4) !important; border-radius: 8px !important; color: #1a0a00 !important; }
    .stSelectbox > div > div { background: rgba(255,255,255,0.1) !important; border: 1px solid rgba(245,200,66,0.4) !important; border-radius: 8px !important; color: #f0e6d3 !important; }
    .stButton > button { background: linear-gradient(135deg, #8b1a1a, #c0392b) !important; color: #f5c842 !important; font-family: 'Playfair Display', serif !important; font-size: 1.1rem !important; font-weight: 700 !important; border: 2px solid #f5c842 !important; border-radius: 50px !important; padding: 0.6rem 3rem !important; width: 100% !important; }
    .divider { border: none; border-top: 1px solid rgba(245,200,66,0.2); margin: 1.5rem 0; }
    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <h1>🍲 Chef's Helper</h1>
        <p>Authentic recipes crafted by AI, inspired by the world's finest kitchens</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# Initialize session state
if "recipe" not in st.session_state:
    st.session_state.recipe = None
if "craving" not in st.session_state:
    st.session_state.craving = ""
if "cuisine" not in st.session_state:
    st.session_state.cuisine = ""

# Sidebar
with st.sidebar:
    st.markdown("### 📖 Saved Recipes")
    favorites = load_favorites()
    if favorites:
        for item in favorites:
            with st.expander(f"🍽️ {item['craving']}"):
                st.write(item["recipe"])
    else:
        st.write("No saved recipes yet.")

# Main inputs
craving = st.text_input("🥘 What are you craving, or what ingredients do you have?")
cuisine = st.selectbox(
    "🌍 Cuisine preference",
    ["West African", "Caribbean", "Mediterranean", "Asian", "Latin American", "Any"]
)
dietary = st.text_input("🥗 Any dietary notes? (e.g. halal, vegetarian, nut-free, dairy-free)")

if st.button("✨ Get My Recipe"):
    if craving:
        with st.spinner("Chef is crafting your recipe..."):
            prompt = build_recipe_prompt(craving, cuisine, dietary)
            st.session_state.recipe = get_recipe(prompt)
            st.session_state.craving = craving
            st.session_state.cuisine = cuisine
    else:
        st.warning("Please tell the chef what you are craving first!")

# Show recipe and save button if recipe exists
if st.session_state.recipe:
    st.markdown(f"""
        <div class="recipe-card">
            <h3>🍽️ Your Recipe</h3>
            {st.session_state.recipe.replace(chr(10), '<br>').replace('**', '<b>').replace('*', '•')}
        </div>
    """, unsafe_allow_html=True)
    if st.button("💾 Save this recipe"):
        save_favorite(st.session_state.craving, st.session_state.cuisine, st.session_state.recipe)
        st.success("✅ Recipe saved! Check the sidebar.")
        st.rerun()