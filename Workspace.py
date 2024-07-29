import streamlit as st
import google.generativeai as genai
import sqlite3
import uuid
import os

# Configure your API key
GOOGLE_API_KEY = "AIzaSyCvJIjsOSsyHennTE10ooiogk7PyU_d0Zo"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Function to generate text content
def generate_text(prompt):
    response = model.generate_content(prompt)
    return response.text

# Function to initialize the database
def init_db():
    if os.path.exists('chat_history.db'):
        os.remove('chat_history.db')  # Remove the existing database file to start fresh
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chats
                 (id TEXT, persona TEXT, message TEXT)''')
    conn.commit()
    conn.close()

# Function to save chat history to the database
def save_chat_history(chat_id, persona, message):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO chats (id, persona, message) VALUES (?, ?, ?)", (chat_id, persona, message))
    conn.commit()
    conn.close()

# Function to retrieve chat history from the database
def get_chat_history(chat_id):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT message FROM chats WHERE id = ?", (chat_id,))
    messages = c.fetchall()
    conn.close()
    return [message[0] for message in messages]

# Initialize the database
init_db()

personas = {
    "Sarah Johnson": {
        "Name": "Sarah Johnson",
        "Age": 55,
        "Occupation": "Senior Executive at a Tech Company",
        "Annual Income": "$250,000",
        "Retirement Savings": "$1.5 million in 401(k), IRA, and other investments",
        "Financial Literacy": "High",
        "Goals": "Retire at 60, travel extensively, maintain current lifestyle",
        "Concerns": "Market volatility, healthcare costs",
        "Profile": "Sarah is well-versed in financial planning and has been actively managing her retirement savings for years. She has a clear understanding of her retirement goals and regularly reviews her investment portfolio. Sarah is confident but seeks professional advice to optimize her retirement strategy and ensure she’s fully prepared for any potential risks.",
        "Key Attributes": [
            "High financial awareness and literacy",
            "Proactive in managing investments",
            "Seeks advanced strategies for optimizing retirement savings",
            "Concerned with preserving wealth and ensuring a comfortable retirement"
        ],
        "Scenario Interaction": "Sarah engages with the advisor to review her current retirement plan, seeking advice on fine-tuning her investment strategy, minimizing tax liabilities, and planning for healthcare costs. She asks detailed questions and is interested in sophisticated financial products and strategies."
    },
    "John Miller": {
        "Name": "John Miller",
        "Age": 50,
        "Occupation": "Business Owner",
        "Annual Income": "$300,000",
        "Retirement Savings": "$800,000 in various accounts, but not actively managed",
        "Financial Literacy": "Moderate",
        "Goals": "Retire at 65, start a hobby business, spend more time with family",
        "Concerns": "Lack of knowledge about retirement planning, unsure about investment strategies, unaware of potential healthcare costs",
        "Profile": "John has accumulated substantial wealth but has not actively planned for retirement. He is focused on his business and personal life, leaving little time to manage or understand his retirement savings. John is aware that he needs to start planning but is unsure where to begin and what steps to take.",
        "Key Attributes": [
            "Financially strong but lacks retirement planning knowledge",
            "Passive in managing investments",
            "Seeks basic guidance and education on retirement readiness",
            "Concerned about potential gaps in his retirement plan"
        ],
        "Scenario Interaction": "John engages with the advisor to get a comprehensive overview of retirement planning. He needs education on the importance of diversifying investments, understanding retirement accounts, and planning for future healthcare costs. The advisor provides step-by-step guidance and helps John create a detailed retirement plan."
    },
    "Emily Davis": {
        "Name": "Emily Davis",
        "Age": 45,
        "Occupation": "Marketing Manager",
        "Annual Income": "$90,000",
        "Retirement Savings": "$50,000 in a 401(k)",
        "Financial Literacy": "Low",
        "Goals": "Retire at 65, downsize home, live comfortably",
        "Concerns": "Insufficient savings, debt management, lack of investment knowledge",
        "Profile": "Emily has not prioritized retirement savings and finds herself significantly behind in her retirement planning. She has some debt and limited knowledge of investment options. Emily is starting to realize the importance of planning for retirement but feels overwhelmed and unsure about how to catch up.",
        "Key Attributes": [
            "Financially unprepared for retirement",
            "Limited savings and investment knowledge",
            "Concerned about debt and insufficient savings",
            "Needs foundational advice and a catch-up strategy"
        ],
        "Scenario Interaction": "Emily engages with the advisor seeking a realistic plan to become retirement ready. The advisor helps her understand the basics of retirement planning, prioritize debt reduction, and develop a savings plan. Emily is guided through setting up automatic contributions, exploring employer match options, and understanding the importance of starting early and staying consistent."
    }
}

def main():
    st.title("Retirement Advisor Chat")
    
    if 'persona_choice' not in st.session_state:
        st.session_state.persona_choice = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if 'chat_id' not in st.session_state:
        st.session_state.chat_id = None
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("/Users/atharvabapat/Desktop/Retirement_Readiness/DALL·E 2024-07-28 15.42.16 - A close-up portrait of a woman in her 50s with fair skin, settled in the USA. She is wearing a casual, simple blouse. Her hair is shoulder-length, sli.webp", caption="Sarah Johnson", use_column_width=True)
        if st.button("Chat with Sarah"):
            st.session_state.persona_choice = "Sarah Johnson"
            st.session_state.initialized = True
            st.session_state.chat_id = str(uuid.uuid4())
            st.session_state.chat_history = [f"Chat with {personas['Sarah Johnson']['Name']} started.\n"]
    
    with col2:
        st.image("/Users/atharvabapat/Desktop/Retirement_Readiness/DALL·E 2024-07-28 16.34.12 - A portrait of a man in his 40s with a casual dress code. He has short, neatly styled hair and a friendly, approachable expression. He is wearing a sim.webp", caption="John Miller", use_column_width=True)
        if st.button("Chat with John"):
            st.session_state.persona_choice = "John Miller"
            st.session_state.initialized = True
            st.session_state.chat_id = str(uuid.uuid4())
            st.session_state.chat_history = [f"Chat with {personas['John Miller']['Name']} started.\n"]
    
    with col3:
        st.image("/Users/atharvabapat/Desktop/Retirement_Readiness/DALL·E 2024-07-28 15.43.44 - A close-up portrait of an Asian woman in her 30s with fair skin, settled in the USA. She is wearing a casual, simple blouse. Her hair is shoulder-leng.webp", caption="Emily Davis", use_column_width=True)
        if st.button("Chat with Emily"):
            st.session_state.persona_choice = "Emily Davis"
            st.session_state.initialized = True
            st.session_state.chat_id = str(uuid.uuid4())
            st.session_state.chat_history = [f"Chat with {personas['Emily Davis']['Name']} started.\n"]
        
    if st.session_state.initialized:
        persona_data = personas[st.session_state.persona_choice]
        
        st.subheader(f"Chat with {st.session_state.persona_choice}")
        
        for message in st.session_state.chat_history:
            st.markdown(message)
        
        user_input = st.text_input("You (Advisor):", key="advisor_input")
        
        if st.button("Send"):
            if user_input:
                st.session_state.chat_history.append(f"**You (Advisor):** {user_input}\n")
                save_chat_history(st.session_state.chat_id, st.session_state.persona_choice, f"You (Advisor): {user_input}")
                
                persona_prompt = (
                    f"You are {persona_data['Name']}, a {persona_data['Age']} year old {persona_data['Occupation']} "
                    f"with an annual income of {persona_data['Annual Income']}. Your retirement savings are {persona_data['Retirement Savings']} "
                    f"and your financial literacy is {persona_data['Financial Literacy']}. "
                    f"Your goals are: {persona_data['Goals']}. Your concerns are: {persona_data['Concerns']}.\n\n"
                    f"Based on this information, ask your advisor relevant questions to help you with your retirement planning.\n\n"
                    f"Profile: {persona_data['Profile']}\n\n"
                    f"Scenario Interaction: {persona_data['Scenario Interaction']}\n\n"
                    "Ask one question at a time."
                )
                
                response = generate_text(persona_prompt + "\n\n" + user_input)
                st.session_state.chat_history.append(f"**{persona_data['Name']}:** {response}\n")
                save_chat_history(st.session_state.chat_id, st.session_state.persona_choice, f"{persona_data['Name']}: {response}")
                st.experimental_rerun()
 
        if st.button("End Chat"):
            st.session_state.initialized = False
            chat_summary = get_chat_history(st.session_state.chat_id)
            st.session_state.chat_history = []
            st.session_state.chat_id = None
            
            st.subheader("Chat Summary")
            for message in chat_summary:
                st.markdown(message)

if __name__ == "__main__":
    main()
