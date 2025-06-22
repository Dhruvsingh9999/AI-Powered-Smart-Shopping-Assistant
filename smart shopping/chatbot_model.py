import google.generativeai as genai 
import json
import logging
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure Gemini API
API_KEY = "AIzaSyDHdIhHV_dWFibpPua9uWnKvkPmhz3zTdY"
genai.configure(api_key=API_KEY)

# Define model
model = genai.GenerativeModel("gemini-1.5-flash")

# Define product specifications for different categories
CATEGORY_SPECS = {
    "Mobile": "Price, Battery, Display, Processor, RAM/Storage, Camera, Key Features",
    "Laptop": "Price, Processor, RAM/Storage, Display, Battery, Graphics Card, Key Features",
    "Smartwatch": "Price, Battery, Display, Features (Heart Rate Monitoring, GPS, Connectivity)",
    "Television": "Price, Display Type, Screen Size, Resolution, Refresh Rate, Smart Features, Connectivity",
    "Air Conditioner": "Price, Capacity (Tonnage), Energy Efficiency (Star Rating), Cooling Technology, Key Features",
    "Washing Machine": "Price, Capacity, Type (Front Load/Top Load), Wash Programs, Energy Rating, Key Features",
    "Soundbar": "Price, Power Output, Connectivity (Bluetooth, HDMI, AUX), Features like Dolby Audio, Key Features",
}

# ✅ Updated chatbot_response function
def chatbot_response(category, budget, query):
    try:
        logging.debug(f"Generating response for: Category={category}, Budget={budget}, Query={query}")

        if category not in CATEGORY_SPECS:
            return {"error": "Invalid category. Please choose a valid category."}

        specs = CATEGORY_SPECS[category]

        prompt = (
            f"Suggest 3 best {category} products under ₹{budget} for the query: {query}.\n"
            f"For each product, include:\n"
            f"- Name\n"
            f"- Price\n"
            f"- Features (each one as a key-value pair): {specs}\n"
            f"Format the response exactly in this JSON:\n\n"
            f"""{{
  "products": [
    {{
      "name": "Product Name",
      "price": "₹xxxxx",
      "features": {{
        "Battery": "xxxx mAh",
        "Display": "xxxx",
        "Processor": "xxxx",
        "RAM/Storage": "xxxx",
        "Camera": "xxxx",
        "Key Features": "xxxx"
      }}
    }},
    ...
  ]
}}"""
        )

        # Call Gemini
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            raw_text = response.text.strip()
            logging.debug(f"Raw AI Response: {raw_text}")

            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group())
                    formatted_response = f"📦 **AI Suggests: Here are the top 3 {category} options for you!**\n\n"

                    if "products" in data:
                        for idx, product in enumerate(data["products"], 1):
                            formatted_response += f"🟠 **Product {idx}: {product.get('name', 'N/A')}**\n"
                            formatted_response += f"💰 **Price:** {product.get('price', 'Not available')}\n"
                            features = product.get('features', {})

                            for key in specs.split(", "):
                                emoji = {
                                    "Battery": "🔋", "Display": "📱", "Processor": "⚙️",
                                    "RAM/Storage": "💾", "Camera": "📷", "Key Features": "⭐",
                                    "Graphics Card": "🎮", "Price": "💰", "Smart Features": "📡",
                                    "Resolution": "🖼️", "Screen Size": "📏", "Capacity": "🏷️",
                                    "Type (Front Load/Top Load)": "🧺", "Energy Rating": "🔋",
                                    "Wash Programs": "🌀", "Power Output": "🔊",
                                    "Connectivity (Bluetooth, HDMI, AUX)": "🔌",
                                    "Features (Heart Rate Monitoring, GPS, Connectivity)": "❤️📍📶"
                                }.get(key.strip(), "•")
                                formatted_response += f"{emoji} **{key}**: {features.get(key.strip(), 'Not available')}\n"

                            formatted_response += "\n"
                    else:
                        return {"error": "No products found in AI response."}

                    return {"response": formatted_response.strip()}
                except json.JSONDecodeError as e:
                    logging.error(f"JSON decode failed: {e}")
                    return {"error": "AI response is not valid JSON. Please try again."}
            else:
                logging.error("No JSON found in AI response")
                return {"error": "Invalid response format from AI"}
        else:
            return {"error": "No response from AI."}

    except Exception as e:
        logging.error(f"Error in chatbot_response: {str(e)}")
        return {"error": str(e)}
