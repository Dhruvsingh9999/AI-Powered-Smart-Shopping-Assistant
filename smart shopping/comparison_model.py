import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyDHdIhHV_dWFibpPua9uWnKvkPmhz3zTdY")

def compare_products(product1, product2):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp")

        # Optimized prompt for a **shorter, to-the-point** response
        prompt = (
            f"Compare these two products: \n\n"
            f"1. {product1}\n2. {product2}\n\n"
            "Give a **short answer** mentioning the **better product** and 3-4 key reasons why it's better."
        )

        response = model.generate_content(prompt)

        if not response or not hasattr(response, "text"):
            return "Sorry, I couldn't compare these products. Try again."

        return response.text.strip()

    except Exception as e:
        return f"Error: {str(e)}"
