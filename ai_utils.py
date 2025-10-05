# ai_utils.py
import os
import google.generativeai as genai

# Configure Gemini API if available
API_KEY = os.getenv("AIzaSyCXLiUxdW3vsFGA0Z5bwaUgcZNSfRf0BHE")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-pro")
else:
    model = None  # AI won't be used

# Placeholder AI function (offline, fallback)
def placeholder_ai(description: str) -> str:
    description = description.lower()
    if any(word in description for word in ["food", "restaurant", "lunch", "dinner"]):
        return "Food"
    elif any(word in description for word in ["taxi", "uber", "flight", "train"]):
        return "Travel"
    elif any(word in description for word in ["pen", "paper", "notebook", "supplies"]):
        return "Supplies"
    else:
        return "Other"

# Combined AI function
def ai_predict_category(description: str) -> str:
    """
    Uses Gemini AI if available, otherwise falls back to placeholder.
    """
    if not description:
        return "Other"

    # Try Gemini AI
    if model:
        try:
            prompt = f"""You are a smart expense tracker.
            Categorize this expense into one of these: Food, Travel, Supplies, Other.
            Description: '{description}'
            Return only one category name."""
            
            response = model.generate_content(prompt)
            category = response.text.strip()

            # Normalize response
            valid = ["Food", "Travel", "Supplies", "Other"]
            for v in valid:
                if v.lower() in category.lower():
                    return v
            return "Other"
        except Exception as e:
            print("Gemini AI error:", e)

    # Fallback
    return placeholder_ai(description)
