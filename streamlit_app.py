import streamlit as st  # type: ignore
from PIL import Image, ImageDraw  # type: ignore
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
        age_str = st.text_input("Your Age")
        guests_str = st.text_input("Number of Guests")
        nights_str = st.text_input("Number of Nights")

        # Validate and convert to int if possible
        def parse_int(val, min_val=None, max_val=None):
            try:
                num = int(val)
                if min_val is not None and num < min_val:
                    return None
                if max_val is not None and num > max_val:
                    return None
                return num
            except Exception:
                return None

        age = parse_int(age_str, 0, 120)
        guests = parse_int(guests_str, 1, 20)
        nights = parse_int(nights_str, 1, 60)

        if age_str and (age is None or age < 0 or age > 120):
            st.warning("Please enter a valid age (0-120).")
        if guests_str and (guests is None or guests < 1 or guests > 20):
            st.warning("Please enter a valid number of guests (1-20).")
        if nights_str and (nights is None or nights < 1 or nights > 60):
            st.warning("Please enter a valid number of nights (1-60).")
        if age is not None and age < 21:
            st.warning("You must be 21 or older to book a room.")
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
        previewed = st.form_submit_button("Preview Booking Summary")

        # Use session state to track preview
        if "preview_ready" not in st.session_state:
            st.session_state.preview_ready = False
        if previewed:
            errors = []
            if age is None:
                errors.append("Please enter a valid age (0-120).")
            elif age < 21:
                errors.append("You must be 21 or older to book.")
            if guests is None:
                errors.append("Please enter a valid number of guests (1-20).")
            if nights is None:
                errors.append("Please enter a valid number of nights (1-60).")
            if not first_name.strip():
                errors.append("First name is required.")
            if not last_name.strip():
                errors.append("Last name is required.")
            if not valid_email(email):
                errors.append("Please enter a valid email address.")
            if not phone.strip():
                errors.append("Phone number is required.")
            if errors:
                st.session_state.preview_ready = False
                st.error("\n".join(errors))
            else:
                st.session_state.preview_ready = True
                st.session_state.preview_data = {
                    "age": age,
                    "nights": nights,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "guests": guests,
                    "understands_policy": understands_policy,
                }

        if st.session_state.get("preview_ready", False):
            data = st.session_state.preview_data
            st.success("Booking summary preview:")
            st.markdown(
                f"""
                <div style='background:#f0f6ff; border-radius:8px; padding:1em; border:1px solid #b3d1f7;'>
                <b>Age:</b> {data['age']}<br>
                <b>Nights:</b> {data['nights']}<br>
                <b>Guest Name:</b> {data['first_name']} {data['last_name']}<br>
                <b>Email:</b> {data['email']}<br>
                <b>Phone:</b> {data['phone']}<br>
                <b>Total Guests:</b> {data['guests']}<br>
                <b>Understands Policy:</b> {data['understands_policy']}
                </div>
                <br>
                """,
                unsafe_allow_html=True,
            )
            submit_booking = st.form_submit_button("Submit Booking")
            if submit_booking:
                # Save booking to file
                booking_log = (
                    f"Age: {data['age']}\n"
                    f"Nights: {data['nights']}\n"
                    f"First Name: {data['first_name']}\n"
                    f"Last Name: {data['last_name']}\n"
                    f"Email: {data['email']}\n"
                    f"Phone: {data['phone']}\n"
                    f"Total Guests: {data['guests']}\n"
                    f"Understands Cancellation Policy: {data['understands_policy']}\n"
                    f"{'-'*40}\n"
                )
                try:
                    with open("hotel_bookings.txt", "a") as file:
                        file.write(booking_log)
                    st.success("Booking submitted and saved!")
                    st.session_state.preview_ready = False
                except Exception as e:
                    st.error(f"ERROR: Could not save booking to file. {e}")

with tab2:
    st.header("All Bookings")
    st.markdown(
        "<div style='height:200px; display:flex; align-items:center; justify-content:center; color:#205080; font-size:1.2em;'>[Bookings list coming soon]</div>",
        unsafe_allow_html=True,
    )
