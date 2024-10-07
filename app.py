import numpy as np
import streamlit as st
import easyocr
from PIL import Image, ImageDraw, ImageFont

st.title("Text Recognition EasyOCR with Streamlit")
st.text("This application helps detect text in multiple languages from uploaded images.")
st.logo("data/myself.jpg")

file_uploaded = st.file_uploader("Upload your file here", type=["png", "jpg", "jpeg"], accept_multiple_files=False)

language = st.multiselect("Choose language", ["vi", "es", "en"])

rectangle_width = 2


# Container for displaying the result
result_container = st.container()
with st.sidebar:
    font_size = st.select_slider("Choose font size", options = range(1,20))
    font = ImageFont.truetype("./data/JetBrainsMono-Medium.ttf", size=font_size)


def start_predict():
    if file_uploaded and language:
        # Convert the uploaded file to an image
        image = Image.open(file_uploaded)
        image_np = np.array(image)  # Convert the image to a NumPy array

        reader = easyocr.Reader(lang_list=language)
        result = reader.readtext(image_np)

        # Optional: Draw the bounding boxes on the image
        draw = ImageDraw.Draw(image)
        for (bbox, text, prob) in result:
            # Extract the bounding box points
            top_left, top_right, bottom_right, bottom_left = bbox

            # Find the minimum and maximum coordinates to create the bounding box
            min_x = min(top_left[0], bottom_right[0], top_right[0], bottom_left[0])
            min_y = min(top_left[1], bottom_right[1], top_right[1], bottom_left[1])
            max_x = max(top_left[0], bottom_right[0], top_right[0], bottom_left[0])
            max_y = max(top_left[1], bottom_right[1], top_right[1], bottom_left[1])

            # Draw the rectangle using the min and max coordinates
            draw.rectangle([min_x, min_y, max_x, max_y], outline="green", width=rectangle_width)

            text_pos = (top_left[0], top_left[1] - font_size - rectangle_width)
            draw.text(text_pos, text, fill="blue", font=font)


        # Display the processed image in the result container
        with result_container:
            st.image(image, caption="Processed Image")
    else:
        st.write("Please fill all the options")

st.button("Start predict", on_click=start_predict)
