import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import requests

SERVER_URL = "http://localhost:8000"

# Initialize session state for canvas clearing
if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = 0

def predict_digit(image_data: list) -> dict:
    """Predict the digit from the image data using the server."""
    # Convert the image data to a list
    image_list = image_data.flatten().tolist()
    payload = {"image_data": image_list}
    
    try:
        response = requests.post(f"{SERVER_URL}/predict/", json=payload)
        response.raise_for_status()  # Raise error for 4xx/5xx
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to server. Is it running?")
        return {"error": "Connection failed"}
    except requests.exceptions.JSONDecodeError:
        st.error(f"❌ Server returned non-JSON: {response.text[:200]}")
        return {"error": "Invalid response"}
    except Exception as e:
        st.error(f"❌ Request failed: {str(e)}")
        return {"error": str(e)}

st.set_page_config(page_title="Digits Recognition App")
st.header("Digits Recognition App")
st.subheader("Draw a Digit (28×28)")

# Set up the canvas with dynamic key
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0.0)",
    stroke_width=30,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key=f"canvas_{st.session_state.canvas_key}",  # Dynamic key
)

# Display controls
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Save Drawing", use_container_width=True):
        if canvas_result.image_data is not None:
            # Convert canvas to PIL Image
            img = Image.fromarray((canvas_result.image_data[:, :, :3]).astype('uint8'))
            
            # Convert to grayscale
            img_gray = img.convert('L')
            
            # Resize to 28x28
            img_28 = img_gray.resize((28, 28), Image.Resampling.LANCZOS)
            
            # Save the image
            img_28.save("src/digits_recognition/ui/digit.png")
            
            st.success("✓ Drawing saved as digit.png")
            st.image(img_28, caption="28x28 Digit", width=150)
        else:
            st.error("Please draw something first")

with col2:
    if st.button("Clear Canvas", use_container_width=True):
        st.session_state.canvas_key += 1  # Increment to reset canvas
        st.rerun()

with col3:
    pass

# File uploader as alternative
st.divider()
st.subheader("Or Upload a Digit Image")

uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg", "bmp"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert('L')
    img_resized = img.resize((28, 28), Image.Resampling.LANCZOS)
    
    st.subheader("28x28 Preview")
    st.image(img_resized, caption="Your Digit (28x28)", width=150)
    
    if st.button("Save Uploaded Image", key="save_upload_btn"):
        img_resized.save("digit.png")
        st.success("✓ Image saved as digit.png")

# Prediction
st.divider()
st.subheader("Predict the Digit")
predict_button = st.button("Predict Digit")
if predict_button:
    if canvas_result.image_data is not None:
        # Process canvas image
        img = Image.fromarray((canvas_result.image_data[:, :, :3]).astype('uint8'))
        img_gray = img.convert('L')
        img_28 = img_gray.resize((28, 28))
        img_array = np.array(img_28).reshape(28, 28)
        normalized_img = 255 - img_array  # Invert colors if necessary
        
        prediction = predict_digit(normalized_img)
        st.image(normalized_img, caption="28x28 Digit", width=150)
        if "error" not in prediction and "predictions" in prediction:
            st.success(f"Predicted Digit: {prediction['predictions']}")
        elif "error" in prediction:
            st.error(f"Prediction failed: {prediction['error']}")
        else:
            st.error("Unexpected response format")
    elif uploaded_file is not None:
        # Process uploaded image
        img_array = np.array(img_resized).reshape(28, 28)
        
        prediction = predict_digit(img_array)
        if "error" not in prediction and "predictions" in prediction:
            st.success(f"Predicted Digit: {prediction['predictions']}")
        elif "error" in prediction:
            st.error(f"Prediction failed: {prediction['error']}")
        else:
            st.error("Unexpected response format")
    else:
        st.error("Please draw or upload an image first")