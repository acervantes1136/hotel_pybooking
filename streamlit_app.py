import streamlit as st # type: ignore
from PIL import Image, ImageDraw # type: ignore
import os

# --- App Config ---
st.set_page_config(
    page_title="Hotel Booking System",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="auto",
)


# --- Airplane Logo Placeholder ---
def draw_airplane_logo():
    img = Image.new("RGBA", (120, 60), (230, 245, 255, 0))
    draw = ImageDraw.Draw(img)
    # Simple airplane shape (stylized)
    draw.polygon([(10, 30), (110, 30), (60, 10)], fill=(30, 90, 200, 255))
    draw.rectangle([55, 30, 65, 55], fill=(30, 90, 200, 255))
    draw.line([(60, 10), (60, 55)], fill=(0, 60, 180, 255), width=3)
    return img


st.markdown(
    """
	<style>
	.main {background-color: #e6f0fa;}
	.stApp {background-color: #e6f0fa;}
	</style>
	""",
    unsafe_allow_html=True,
)

col1, col2 = st.columns([1, 6])
with col1:
    st.image(draw_airplane_logo(), width=80)
with col2:
    st.markdown(
        "<h1 style='color:#205080; font-family:sans-serif;'>Hotel Booking System</h1>",
        unsafe_allow_html=True,
    )

st.markdown(
    """
	<hr style='border:1px solid #205080; margin-top:0; margin-bottom:1em;'>
	""",
    unsafe_allow_html=True,
)

# --- Layout: Tabs for Booking and Bookings List ---
tab1, tab2 = st.tabs(["Book a Room", "All Bookings"])

with tab1:
    st.header("Book a Room")
    st.info("Fill out the form below to book your stay.")

    with st.form("booking_form", clear_on_submit=False):
        age = st.number_input("Your Age", min_value=0, max_value=120, step=1)
        if age and age < 21:
            st.warning("You must be 21 or older to book a room.")
        guests = st.number_input("Number of Guests", min_value=1, max_value=20, step=1)
        nights = st.number_input("Number of Nights", min_value=1, max_value=60, step=1)
        st.markdown("---")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        st.markdown("---")
        understands_policy = st.radio(
            "Have you read and understood our Cancellation Policy?", ("Yes", "No")
        )
        st.caption(
            "You must cancel 72 hours before check-in or you will be charged for the first night."
        )

        # Validate email (simple check)
        import re

        def valid_email(e):
            return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e)

        # Preview summary before submission
        submitted = st.form_submit_button("Preview Booking Summary")

        if submitted:
            errors = []
            if age < 21:
                errors.append("You must be 21 or older to book.")
            if not first_name.strip():
                errors.append("First name is required.")
            if not last_name.strip():
                errors.append("Last name is required.")
            if not valid_email(email):
                errors.append("Please enter a valid email address.")
            if not phone.strip():
                errors.append("Phone number is required.")
            if errors:
                st.error("\n".join(errors))
            else:
                st.success("Booking summary preview:")
                st.markdown(
                    f"""
				<div style='background:#f0f6ff; border-radius:8px; padding:1em; border:1px solid #b3d1f7;'>
				<b>Age:</b> {age}<br>
				<b>Nights:</b> {nights}<br>
				<b>Guest Name:</b> {first_name} {last_name}<br>
				<b>Email:</b> {email}<br>
				<b>Phone:</b> {phone}<br>
				<b>Total Guests:</b> {guests}<br>
				<b>Understands Policy:</b> {understands_policy}
				</div>
				<br>
				<form method='post'>
				<button type='submit' disabled style='background:#205080; color:white; border:none; padding:0.5em 1.5em; border-radius:5px; font-size:1em; opacity:0.6;'>Submit Booking (coming next)</button>
				</form>
				""",
                    unsafe_allow_html=True,
                )

with tab2:
    st.header("All Bookings")
    st.markdown(
        "<div style='height:200px; display:flex; align-items:center; justify-content:center; color:#205080; font-size:1.2em;'>[Bookings list coming soon]</div>",
        unsafe_allow_html=True,
    )
