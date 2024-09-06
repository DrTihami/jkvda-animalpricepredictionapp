
import pandas as pd
import pickle
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Load the model and scaler
with open('model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)
with open('scaler.pkl', 'rb') as file:
    loaded_scaler = pickle.load(file)

# Custom CSS
st.markdown("""
<style>
/* General styles */
body {
    font-family: 'Arial', serif;
    background-color: #f0f2f6;
    color: #333;
    margin: 0;
    padding: 0;
}

.container {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
}

.header {
    background-color: #007bff;
    color: white;
    text-align: center;
    padding: 20px;
    border-radius: 10px;
}

.header img {
    display: block;
    margin: 0 auto;
    max-width: 100%;
    height: auto;
}

.header h1 {
    margin-top: 10px;
}

.main-content {
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-top: 20px;
}

h1, h2 {
    color: #333;
    text-align: center;
}

.stButton button {
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
}

.stButton button:hover {
    background-color: #0056b3;
}

.stSelectbox, .stSlider, .stTextInput {
    margin-bottom: 20px;
}

.stSelectbox select, .stSlider input, .stTextInput input {
    border: 1px solid #ced4da;
    border-radius: 5px;
    padding: 10px;
    font-size: 16px;
    width: 100%;
}

.stSelectbox select:focus, .stSlider input:focus, .stTextInput input:focus {
    border-color: #007bff;
}

.footer {
    background-color: #007bff;
    color: white;
    text-align: center;
    padding: 10px;
    border-radius: 5px;
    margin-top: 20px;
}

.footer p {
    margin: 0;
    font-size: 16px;
}

.footer a {
    color: #f0f2f6;
    text-decoration: none;
}

.footer a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown('<div class="header"><h1>Animal Price Prediction Application</h1></div>', unsafe_allow_html=True)
st.image('IMG-jkvda.jpg.jpg', width=160)
st.markdown('<div class="container">', unsafe_allow_html=True)

st.write('This App will provide you accurate animal price based on selected parameters only')

st.markdown('<h2>Courtesy : Jammu & Kashmir Veterinary Doctors Association-Kashmir</h2>', unsafe_allow_html=True)

st.subheader('Enter the Animal details to know the Price')

# Input fields
col1, col2 = st.columns(2)
with col1:
    Animal_Breed = st.selectbox("Select the Breed of the Animal?", ("HF", "JY"))
with col2:
    Milk_Yield = st.slider("Select Milk Yield (liters)", 10, 30, value=20, step=1)

col3, col4, col5 = st.columns(3)
with col3:
    Parity_No = st.selectbox("Select Lactation No of Animal?", [0, 1, 2, 3])
with col4:
    Pregnancy_Status = st.selectbox("Select Pregnancy Status?", ("Yes", "No"))
# Conditionally set Pregnancy_Trimester
with col5:
    if Pregnancy_Status == "No":
        Pregnancy_Trimester = 0
    else:
        Pregnancy_Trimester = st.selectbox("Select Pregnancy Trimester?", [1, 2, 3])

# Map Yes/No to 1/0
Animal_Breed = 1 if Animal_Breed == 'JY' else 0
Pregnancy_Status = 1 if Pregnancy_Status == 'Yes' else 0

# Prepare the input data for prediction
input_data = {
    'Animal_Breed': [Animal_Breed],
    'Milk_Yield': [Milk_Yield],
    'Parity_No': [Parity_No],
    'Pregnancy_Status': [Pregnancy_Status],
    'Pregnancy_Trimester': [Pregnancy_Trimester]
}

# Convert input data to dataframe
input_df = pd.DataFrame(input_data)

# Scale the input data
scaled_df = loaded_scaler.transform(input_df)

# Make prediction
if st.button('Predict Animal Price'):
    predicted_price = loaded_model.predict(scaled_df)
    Animal_Price = round(predicted_price[0])
    st.write(f'The Price of selected Dairy Animal is Rupees: {Animal_Price}')
    # Display image based on Animal_Breed
    if Animal_Breed == 0:  # 'HF' is mapped to 0
        st.image('hf.jpg', width=160)
    else:  # 'JY' is mapped to 1
        st.image('jy.jpg', width=160)


    # PDF Generation Function with Colored Header and Logo Below Header
    def create_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)

        # Add Logo Below the Header (adjust path and dimensions as needed)
        logo_path = "IMG-jkvda.jpg.jpg"  # Ensure this path points to the correct image file
        logo = ImageReader(logo_path)
        c.drawImage(logo, 250, 650, width=100, height=100)  # Adjust the y-position for below header

        # Draw Colored Header Rectangle
        c.setFillColor(colors.HexColor("#007bff"))
        c.rect(50, 570, 550, 50, fill=True, stroke=False)

        # Title in White
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(100, 585, "JKVDA Animal Price Prediction Application")

        # Current Timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(200, 530, f"Report generated on: {current_time}")

        # Input Data
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 12)
        c.drawString(100, 510, "Input Details:")
        c.drawString(100, 490, f"Animal Breed: {'JY' if Animal_Breed == 1 else 'HF'}")
        c.drawString(100, 470, f"Milk Yield: {Milk_Yield} liters")
        c.drawString(100, 450, f"Parity No: {Parity_No}")
        c.drawString(100, 430, f"Pregnancy Status: {'Yes' if Pregnancy_Status == 1 else 'No'}")
        c.drawString(100, 410, f"Pregnancy Trimester: {Pregnancy_Trimester}")

        # Results

        c.drawString(100, 380, f"Predicted Price: The Price of selected Dairy Animal is Rupees: {Animal_Price}")

        c.drawString(100, 300, "Courtesy: Jammu & Kashmir Veterinary Doctors Association-Kashmir")

        c.drawString(100, 100, f"Disclaimer: This is a system generated price and may vary slightly from the actual price.")
        # Footer
        c.showPage()
        c.save()

        buffer.seek(0)
        return buffer


    # PDF Download Button
    st.download_button(
        label="Download Report as PDF",
        data=create_pdf(),
        file_name="animal_price_prediction_report.pdf",
        mime="application/pdf"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer"><p><a href="https://yourwebsite.com">jkvda.org</a></p></div>', unsafe_allow_html=True)

