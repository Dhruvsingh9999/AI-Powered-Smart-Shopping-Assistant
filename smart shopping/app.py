import streamlit as st
import requests
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.express as px


# Apply Orange Background Using Custom CSS

# FastAPI Backend URL
BASE_URL = "http://127.0.0.1:8000"
API_URL = "http://127.0.0.1:8000/calculate_emi/"

# Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "signup"  # Start with the signup page

# Auto-fill session state for signup details
for key in ["signup_name", "signup_username", "signup_password"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# Signup Page
if st.session_state.page == "signup":
    st.title("📝 Signup for AI Shopping Assistant")
    
    name = st.text_input("Enter Your Name", value=st.session_state.signup_name)
    new_username = st.text_input("Create Username", value=st.session_state.signup_username)
    new_password = st.text_input("Create Password", type="password", value=st.session_state.signup_password)

    if st.button("Signup"):
        if name and new_username and new_password:
            # Store signup details in session state
            st.session_state.signup_name = name
            st.session_state.signup_username = new_username
            st.session_state.signup_password = new_password
            st.success("Signup successful! Redirecting to Login...")
            
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error("Please fill out all fields.")

# Login Page
elif st.session_state.page == "login":
    st.title("🔑 Login to AI Shopping Assistant")

    # Autofill the username and password from signup
    username = st.text_input("Username", value=st.session_state.signup_username)
    password = st.text_input("Password", type="password", value=st.session_state.signup_password)

    if st.button("Login"):
        if username == st.session_state.signup_username and password == st.session_state.signup_password:
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Invalid credentials.")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"
        st.rerun()

# Home Page
elif st.session_state.page == "home":
    st.title("🛍️ AI-Powered Smart Shopping Assistant")

    st.subheader("🔹 Select a Feature")
    
    if st.button("🤖 Chatbot"):
        st.session_state.page = "chatbot"
        st.rerun()

    if st.button("🔍 Product Comparison"):
        st.session_state.page = "comparison"
        st.rerun()

    if st.button("💰 EMI Calculator"):
        st.session_state.page = "emi"
        st.rerun()

# Chatbot Page
elif st.session_state.page == "chatbot":
    st.title("🤖 AI Shopping Chatbot")

    categories = ["Mobile", "Laptop", "Smartwatches", "Soundbar", "Television", "Air Conditioner", "Washing Machine", "Freeze"]
    selected_category = st.selectbox("Select Product Category", categories)
    budget = st.number_input("Enter Your Budget (₹)", min_value=1000, step=500)
    user_query = st.text_input("Ask about shopping (e.g., 'Suggest best phone with 5000mAh battery')")

    if st.button("Send"):
        if selected_category and budget and user_query:
            try:
                response = requests.get(f"{BASE_URL}/chatbot", params={"category": selected_category, "budget": budget, "query": user_query})
                if response.status_code == 200:
                    response_data = response.json()
                    response_text = response_data.get("response", {}).get("response", "No response received.")
                    st.markdown("💬 **AI:**\n\n" + response_text)

                else:
                    st.write("⚠️ Error:", response.text)
            except requests.exceptions.RequestException as e:
                st.write("🚨 Connection Error:", str(e))
        else:
            st.warning("Please select a category, enter a budget, and type a query.")

    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# Comparison Page
elif st.session_state.page == "comparison":
    st.title("🔍 Compare Products")

    product1 = st.text_input("Enter First Product Name")
    product2 = st.text_input("Enter Second Product Name")

    if st.button("Compare"):
        if product1 and product2:
            try:
                response = requests.get(f"{BASE_URL}/compare", params={"product1": product1, "product2": product2})
                if response.status_code == 200:
                    st.write("📊 AI:", response.json().get("response", "No response received."))
                else:
                    st.write("⚠️ Error:", response.text)
            except requests.exceptions.RequestException as e:
                st.write("🚨 Connection Error:", str(e))
        else:
            st.warning("Please enter both product names for comparison.")

    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# EMI Calculator Page
elif st.session_state.page == "emi":
    st.title("💰 EMI Calculator")

    price = st.number_input("Enter Product Price (INR)", min_value=1, step=100)
    down_payment = st.number_input("Enter Down Payment (INR)", min_value=0, step=100, value=0)
    tenure = st.number_input("Enter Loan Tenure (Months)", min_value=1, step=1)
    interest_rate = st.number_input("Enter Annual Interest Rate (%)", min_value=0.0, step=0.1)

    if st.button("Calculate EMI"):
        if down_payment > price:
            st.error("Down payment cannot be greater than the product price.")
        else:
            data = {"price": price, "down_payment": down_payment, "tenure": tenure, "interest_rate": interest_rate}
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                result = response.json()
                emi = result['emi']
                total_payment = result['total_payment']
                total_interest = result['total_interest']
                loan_amount = price - down_payment

                st.success(f"Monthly EMI: ₹{emi}")
                st.write(f"Total Payment (including interest): ₹{total_payment}")
                st.write(f"Total Interest Paid: ₹{total_interest}")
                # Pie Chart for EMI Breakdown
                labels = ["Loan Amount", "Total Interest Paid"]
                values = [loan_amount, total_interest]

                fig = px.pie(
                names=labels,
                values=values,
                title="EMI Breakdown: Loan vs Interest",
                color=labels,
                color_discrete_map={"Loan Amount": "blue", "Total Interest Paid": "red"}
                )

                st.plotly_chart(fig)
            else:
                st.error("Error calculating EMI. Please try again.")

    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()

def main():
    pass  # main logic is managed by session state above

if __name__ == "__main__":
    main()