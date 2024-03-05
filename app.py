import streamlit as st
import google.generativeai as genai
import os 
from dotenv import load_dotenv
from PIL import Image as PILImage
import google.api_core.exceptions


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


def main():
    st.set_page_config(page_title="Nutrition from Food", page_icon=":apple:")

    st.title("Nutrition from Food")

    uploaded_file = st.file_uploader("Upload your food image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        food_image = PILImage.open(uploaded_file)
        st.image(food_image, caption="Uploaded Image of Food", use_column_width=True)
        submit = st.button("Tell me about Food Nutrition")

        if submit:
            try:
                input_prompt = """
                I have given you a Food dish tell me the following accurately
                Name of Dish: [Input the name of the dish here]

Description of Dish: [Provide any additional details or ingredients if necessary]

Portion Size: [Specify the portion size, e.g., 100 grams or 100 ml if it's a drink]

Healthiness Assessment:

Is the dish generally considered healthy? [Yes/No/Neutral]

Nutritional Values (per specified portion size):

Calories: [Provide the number of calories per portion]

Fat: [Specify the amount of fat in grams per portion]

Carbohydrates: [Specify the amount of carbohydrates in grams per portion]

Protein: [If applicable, specify the amount of protein in grams per portion]

Sugar: [If applicable, specify the amount of sugar in grams per portion]

Fiber: [If applicable, specify the amount of fiber in grams per portion]

Sodium: [If applicable, specify the amount of sodium in milligrams per portion]

Other Key Nutrients: [Any other important nutrients present in significant amounts]

Additional Notes:

if the given image is not in category of food  or not related to any of the food item response me "This is not the image of Food"

[Provide any further insights or information regarding the dish's nutritional value, ingredients, or health implications.]
                """
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data)
                st.header("The Response is")
                st.write(response)
            except google.api_core.exceptions.InvalidArgument:
                st.error("Please upload an image of food or drink.")


if __name__ == "__main__":
    main()
