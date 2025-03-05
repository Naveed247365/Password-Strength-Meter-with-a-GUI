import streamlit as st
import re
import random
import string

# Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .strength-card {
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 15px 0;
    }
    
    .generated-password {
        font-size: 1.2em;
        font-weight: 600;
        letter-spacing: 1.5px;
        padding: 12px;
        background: #ffffff;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .requirement-item {
        margin: 8px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

def check_password_strength(password):
    score = 0
    feedback = []
    
    criteria = {
        "length": (len(password) >= 8, "Password should be at least 8 characters long"),
        "case": (bool(re.search(r"[A-Z]", password)) and bool(re.search(r"[a-z]", password)), 
        "Include both uppercase and lowercase letters"),
        "digit": (bool(re.search(r"\d", password)), "Add at least one number (0-9)"),
        "special": (bool(re.search(r"[!@#$%^&*]", password)), 
                "Include at least one special character (!@#$%^&*)")
    }
    
    for key, (condition, message) in criteria.items():
        if condition:
            score += 1
        else:
            feedback.append(message)
    
    return score, feedback

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(random.choice(characters) for _ in range(length))
        if all([
            re.search(r"[A-Z]", password),
            re.search(r"[a-z]", password),
            re.search(r"\d", password),
            re.search(r"[!@#$%^&*]", password)
        ]):
            return password

# Streamlit UI
st.title("🔐 Ultimate Password Strength Analyzer")
st.markdown("---")

# Initialize session state
if 'generated_password' not in st.session_state:
    st.session_state.generated_password = ''

# Password Input Section
input_col, generate_col = st.columns([3, 1])
with input_col:
    password = st.text_input("Enter your password:", 
                           type="password",
                           value=st.session_state.generated_password,
                           key="pw_input",
                           placeholder="Type or generate a password...",
                           label_visibility="collapsed")

with generate_col:
    if st.button("✨ Generate Strong Password", use_container_width=True):
        generated_pw = generate_strong_password()
        st.session_state.generated_password = generated_pw
        st.rerun()

if password:
    score, feedback = check_password_strength(password)
    
    # Strength Indicator
    strength_levels = {
        0: ("Critical", "#ff0000", "💀"),
        1: ("Very Weak", "#ff4d4d", "⚠️"),
        2: ("Weak", "#ff9999", "🔓"),
        3: ("Moderate", "#ffd699", "🔒"),
        4: ("Strong", "#85e085", "🔐")
    }
    
    level = min(score, 4)
    level_name, color, icon = strength_levels[level]
    
    with st.container():
        st.markdown(f"""
        <div class="strength-card" style="background: {color}20; border-left: 5px solid {color}">
            <h3 style="margin:0;color:{color}">{icon} {level_name} Password</h3>
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
                <div style="width: 100%; height: 8px; background: #eee; border-radius: 4px">
                    <div style="width: {score*25}%; height: 100%; background: {color}; border-radius: 4px"></div>
                </div>
                <span style="color: {color}">{score}/4</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Requirements Checklist
    st.subheader("Security Checklist")
    requirements = {
        "✅ 8+ characters": len(password) >= 8,
        "✅ Upper & lowercase letters": bool(re.search(r"[A-Z]", password) and re.search(r"[a-z]", password)),
        "✅ Contains numbers": bool(re.search(r"\d", password)),
        "✅ Special characters": bool(re.search(r"[!@#$%^&*]", password))
    }
    
    for req_text, met in requirements.items():
        icon = "✔️" if met else "❌"
        color = "#2ecc71" if met else "#e74c3c"
        st.markdown(f"""
        <div class="requirement-item">
            <span style="color: {color}; font-size: 1.2em">{icon}</span>
            <span style="color: {'#555' if met else '#777'}">{req_text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Feedback Section
    if feedback:
        st.subheader("Improvement Suggestions")
        for suggestion in feedback:
            st.error(f"🚨 {suggestion}")
    
    if score == 4:
        st.success("🎉 Excellent! Your password is fortress-strong!")
        st.markdown(f"""
        <div class="generated-password">
            {password}
            <span style="float: right; color: #2ecc71">✓ Secure</span>
        </div>
        """, unsafe_allow_html=True)

# Password Guide
with st.expander("📘 Password Creation Guidelines", expanded=True):
    st.markdown("""
    **Create strong passwords by following these rules:**
    
    - 🔐 Use at least 12 characters
    - 🔠 Mix uppercase and lowercase letters
    - 🔢 Include numbers and symbols
    - 🚫 Avoid personal information
    - 🔄 Use unique passwords for different accounts
    
    *Remember: A strong password is your first line of defense!*
    """)

# Footer
st.markdown("---")
st.markdown("""
<style>
.footer {
    text-align: center;
    padding: 15px;
    color: #666;
}
</style>
<div class="footer">
    Made with ❤️ by Muhammad Naveed | 🔒 Keep your data safe
</div>
""", unsafe_allow_html=True)