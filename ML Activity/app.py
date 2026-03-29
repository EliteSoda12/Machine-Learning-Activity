import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load the model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("ML Activity/converted_savedmodel/model.savedmodel")

model = load_model()

# Load class labels and strip numeric prefixes
with open("ML Activity/converted_savedmodel/labels.txt", "r") as f:
    raw_labels = f.read().splitlines()
    class_names = [line.split(" ", 1)[1] if " " in line else line for line in raw_labels]

st.title("Bass Classifier")
st.write("Upload an image to check if it's Bass, Not Bass, or Fish Bass.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess image
    img = image.resize((224, 224))  # Teachable Machine default size
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction[0])
    confidence = np.max(prediction[0])

    label = class_names[predicted_class]
    confidence_pct = confidence * 100  # convert to percentage

    # Color-coded border
    if "BASS" in label.upper() and "NOT" not in label.upper():
        border_color = "green"
    elif "NOT" in label.upper():
        border_color = "red"
    else:
        border_color = "blue"

    st.markdown(
        f"""
        <div style='border: 3px solid {border_color}; padding: 15px; border-radius: 10px;'>
            <h3 style='margin:0;'>Prediction: {label}</h3>
            <p style='margin:0;'>Confidence: {confidence_pct:.1f}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )
