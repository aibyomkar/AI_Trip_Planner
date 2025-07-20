# frontend

import streamlit as st
import requests
import datetime

BASE_URL = 'https://ai-trip-planner-backend-jrdl.onrender.com'

st.set_page_config(
    page_title="Roamio",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state='expanded'
)

# Simple session state for download counter
if 'download_counter' not in st.session_state:
    st.session_state.download_counter = 0

# Luxury Header
st.markdown("""
<div style='
   text-align: center; 
   padding: 25px 15px; 
   background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); 
   border-radius: 15px; 
   margin-bottom: 30px; 
   border: 1px solid #333;
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
'>
   <h1 style='
       font-size: clamp(2rem, 5vw, 3.2rem); 
       margin: 0;
       font-weight: 300;
       letter-spacing: clamp(1px, 2vw, 3px);
       color: #fff;
       font-family: "Times New Roman", serif;
       text-align: center;
       width: 100%;
   '>✈️ ROAMIO <span style='
       background: linear-gradient(45deg, #d4af37, #ffd700, #ffed4e);
       -webkit-background-clip: text;
       -webkit-text-fill-color: transparent;
       font-weight: 600;
   '>AI</span></h1>
   <p style='
       color: #b8860b;
       margin: 10px 0 0 0;
       font-size: clamp(0.9rem, 3vw, 1.1rem);
       font-style: italic;
       letter-spacing: clamp(0.5px, 1vw, 1px);
       text-align: center;
       width: 100%;
       max-width: 90%;
   '>AI Trip Planner by Omkar · Guided by Krish Naik & Sunny Sir</p>
</div>
""", unsafe_allow_html=True)

with st.expander("🧠 What Can Roamio Do? Click to discover"):
   st.markdown("""   
   - 🧳 Understands your preferences: destination, dates, budget, group type
   - 🧠 Intelligently reasons and takes actions based on your input
   - 🧭 Generates personalized day-wise itineraries instantly
   - 🏙️ Suggests real places: landmarks, cafes, hidden gems, museums
   - 🗺️ Organizes intelligently with timing and proximity-based suggestions
   - ✨ Discovers offbeat locations using real-time APIs
   - 🔍 Backed by Google Map's 200M+ verified places dataset
   - 📆 Auto-balances activities: cultural, relaxing, adventurous
   - 🌐 Fetches weather, travel tips, and exchange rates
   - 💡 Perfect for solo, couples, family, or group adventures
   - 🌟 Live 24 X 7
   """)

# Elegant Input Section
st.markdown("""
<div style='
   background: linear-gradient(135deg, #2c2c54 0%, #40407a 100%); 
   padding: 20px 15px; 
   border-radius: 12px; 
   margin: 20px 0; 
   border: 1px solid #555;
   display: flex;
   align-items: center;
   justify-content: center;
'>
   <h3 style='
       color: #d4af37; 
       text-align: center; 
       margin: 0; 
       font-weight: 300; 
       letter-spacing: clamp(1px, 2vw, 2px);
       font-size: clamp(1.2rem, 4vw, 1.5rem);
       width: 100%;
   '>🌍 DESTINATION INQUIRY</h3>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style='
    text-align: center; 
    padding: 5px 10px; 
    background: linear-gradient(135deg, #2c2c54 0%, #40407a 100%); 
    border-radius: 10px; 
    margin-bottom: 20px; 
    border: 1px solid #444;
    display: flex;
    align-items: center;
    justify-content: center;
    '>
    <h4 style='
        color: #d4af37; 
        margin: 0; 
        letter-spacing: clamp(0.5px, 1.5vw, 1px);
        font-size: clamp(1rem, 3.5vw, 1.25rem);
        text-align: center;
        width: 100%;
    '>CONCIERGE SERVICES ✨</h4>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 Some Recommendations")
    st.markdown("""
    **For premium itineraries, include:**
    - Destination preferences & duration
    - Group size & luxury tier
    - Budget range in preferred currency
    - Special experiences desired
    """)
    
    st.divider()
    
    st.markdown("### 💎 Exclusive Insights")
    luxury_facts = [
    "🏰 Dubai has the world's only 7-star hotel",
    "🍾 Monaco has more millionaires per capita than anywhere",
    "🌸 Japan's cherry blossom season lasts only 2 weeks",
    "💎 The Ritz Paris has a $18,000 per night Imperial Suite",
    "🛥️ Superyachts over 100m cost $275 million+ to build",
    "🏔️ Switzerland's Zermatt bans all cars except electric vehicles",
    "🍸 The world's most expensive cocktail costs $12,970",
    "✈️ Private jets can cost $90 million for ultra-long range models",
    "🏖️ The Bahamas has 365 islands, one for each day",
    "🌊 The Maldives has overwater villas costing $50,000+ per night",
    "🎭 Venice receives 30 million tourists annually in just 5 square km",
    "🍷 A bottle of 1945 Romanée-Conti sold for $558,000",
    "🏨 Tokyo has more Michelin stars than Paris and London combined",
    "🚁 Helicopter tours in NYC cost $200+ per person for 15 minutes",
    "🌺 Bora Bora's overwater bungalows were invented in 1967",
    "🎪 Monaco's casino generates 4% of the country's revenue",
    "🏛️ The Vatican is the smallest country at 0.17 square miles",
    "🦅 Dubai's Burj Al Arab uses 22-carat gold leaf on interiors",
    "🌴 Seychelles has beaches with naturally pink sand",
    "❄️ Antarctica luxury cruises cost $15,000+ per person"
    ]
    
    import random
    st.info(random.choice(luxury_facts))

    st.markdown("### 🌐 Connect With Me")
    st.markdown("""
    <div style='text-align: center;'>
        <a href='https://github.com/aibyomkar' target='_blank' style='text-decoration: none; margin: 0 10px;'>
            <span style='font-size: 15px;'>GitHub</span>
        </a>
        <a href='https://instagram.com/omkar_raps' target='_blank' style='text-decoration: none; margin: 0 10px;'>
            <span style='font-size: 15px;'>Instagram</span>
        </a>
    </div>
    """, unsafe_allow_html=True)


# Premium Input Form
with st.form(key='concierge_form', clear_on_submit=True):
    user_input = st.text_area('Share your travel aspirations...', height=100, placeholder="Describe your dream journey...")
    submit_button = st.form_submit_button('✨ Consult Roamio', use_container_width=True)

if submit_button and user_input.strip():
    try:
        with st.spinner('🔮 Crafting your bespoke itinerary...'):
            response = requests.post(f'{BASE_URL}/query', json={'query': user_input})

        if response.status_code == 200:
            answer = response.json().get('answer', 'No recommendations available.')
            answer = answer.strip()

            # Elegant Results Display
            st.markdown("""
            <div style='
            background: linear-gradient(135deg, #1a1a2e 0%, #2c2c54 100%); 
            padding: 20px 15px; 
            border-radius: 12px; 
            margin: 20px 0; 
            border: 1px solid #333;
            display: flex;
            align-items: center;
            justify-content: center;
            '>
            <h3 style='
                color: #d4af37; 
                text-align: center; 
                margin: 0; 
                letter-spacing: clamp(1px, 2vw, 2px);
                font-size: clamp(1.2rem, 4vw, 1.5rem);
                width: 100%;
            '>📋 CURATED ITINERARY</h3>
            </div>
            """, unsafe_allow_html=True)
            
            current_time = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M")
            st.markdown(f'**Crafted:** {current_time}')
            st.markdown(f'**By:** Roamio')

            st.markdown(answer)
            
            # 🔥 SIMPLE DOWNLOAD FEATURE
            # Create downloadable content
            current_time = datetime.datetime.now().strftime("%Y-%m-%d at %H:%M")
            download_content = f"""🌏 Roamio AI - Travel Plan

Generated: {current_time}  
Created by: Roamio AI Trip Planner (Built by Omkar under complete guidance of Krish Naik & Sunny Sir)

Your Travel Query:
{user_input}

Roamio's Travel Plan:
{answer}



This trip plan was generated by AI. Please verify all information, especially prices, operating hours, and travel requirements before your trip.
"""
            
            # Simple download button
            st.session_state.download_counter += 1
            filename = f'Roamio_Travel_Plan_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            
            st.download_button(
                label="📥 Download Travel Plan",
                data=download_content,
                file_name=filename,
                mime='text/markdown',
                key=f"download_{st.session_state.download_counter}",
                use_container_width=True
            )
            
            st.success('💼 **Roamio\'s Note:** Please verify all arrangements with official sources before travel.')
            
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; background: linear-gradient(135deg, #1a1a2e 0%, #2c2c54 100%); padding: 15px; border-radius: 8px; border: 1px solid #333;'>
                <span style='color: #d4af37; font-style: italic;'>Crafted with Excellence | Roamio | By Omkar · Guided by Krish Naik & Sunny Sir</span>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error('⚠️ Concierge service temporarily unavailable')

    except Exception as e:
        st.error(f'🚨 Service interruption: {e}')