import hashlib

import streamlit as st

from config import APP_NAME
from database import init_database, get_predictions, save_prediction
from utils import authenticate
from model import predict_image


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_database()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "last_saved_prediction" not in st.session_state:
    st.session_state.last_saved_prediction = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.dashboard-card {
    padding: 22px;
    border-radius: 16px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    min-height: 125px;
}

.metric-title {
    color: #64748b !important;
    font-size: 14px;
    margin-bottom: 8px;
}

.metric-value {
    color: #111827 !important;
    font-size: 27px;
    font-weight: 700;
}

.result-card {
    padding: 24px;
    border-radius: 16px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    min-height: 130px;
}

.result-title {
    color: #64748b !important;
    font-size: 15px;
    margin-bottom: 8px;
}

.result-value {
    color: #111827 !important;
    font-size: 27px;
    font-weight: 700;
}

.model-card {
    padding: 20px;
    border-radius: 15px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 15px;
}

.login-container {
    max-width: 430px;
    margin: 80px auto;
    padding: 35px;
    border-radius: 18px;
    background: white;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

.login-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 5px;
}

.login-subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 30px;
}

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 50px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGIN
# ============================================================

def login_page():

    st.markdown(
        '<div class="login-container">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">🧠 Alzheimer AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">'
        'AI-Powered Alzheimer Disease Detection'
        '</div>',
        unsafe_allow_html=True
    )

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True,
        type="primary"
    ):

        if authenticate(username, password):

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("Login successful!")
            st.rerun()

        else:

            st.error("Invalid username or password.")

    st.markdown(
        '<div class="footer">'
        'For research and educational purposes only'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    # --------------------------------------------------------
    # SIDEBAR
    # --------------------------------------------------------

    with st.sidebar:

        st.markdown("## 🧠 Alzheimer AI")

        st.caption(
            f"Logged in as: **{st.session_state.username}**"
        )

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "🔬 Alzheimer Detection",
                "📊 Prediction History",
                "📈 Analytics"
            ]
        )

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.last_saved_prediction = None

            st.rerun()


    # ========================================================
    # HOME DASHBOARD
    # ========================================================

    if page == "🏠 Dashboard":

        st.title("🧠 Alzheimer AI Dashboard")

        st.write(
            f"Welcome back, **{st.session_state.username}** 👋"
        )

        records = get_predictions(
            st.session_state.username
        )

        total_predictions = len(records)

        st.markdown("### 📊 System Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f"""
                <div class="dashboard-card">
                    <div class="metric-title">
                        Total Predictions
                    </div>
                    <div class="metric-value">
                        {total_predictions}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                """
                <div class="dashboard-card">
                    <div class="metric-title">
                        AI Model
                    </div>
                    <div class="metric-value">
                        EfficientNetB0
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                """
                <div class="dashboard-card">
                    <div class="metric-title">
                        Classes
                    </div>
                    <div class="metric-value">
                        4
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:

            st.markdown(
                """
                <div class="dashboard-card">
                    <div class="metric-title">
                        System Status
                    </div>
                    <div class="metric-value">
                        Ready
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### 🔬 Detection System")

        st.info(
            "Upload a brain MRI image and use the trained "
            "EfficientNetB0 model to generate a four-class "
            "classification result."
        )

        st.markdown("### ⚙️ Model Information")

        model_col1, model_col2, model_col3 = st.columns(3)

        with model_col1:

            st.markdown(
                """
                <div class="model-card">
                    <b>Architecture</b><br>
                    EfficientNetB0
                </div>
                """,
                unsafe_allow_html=True
            )

        with model_col2:

            st.markdown(
                """
                <div class="model-card">
                    <b>Approach</b><br>
                    Transfer Learning + Fine-tuning
                </div>
                """,
                unsafe_allow_html=True
            )

        with model_col3:

            st.markdown(
                """
                <div class="model-card">
                    <b>Input Size</b><br>
                    224 × 224 RGB
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### ⚠️ Important Notice")

        st.warning(
            "This application is developed for research and "
            "educational purposes only. AI predictions should "
            "not be interpreted as a medical diagnosis."
        )


    # ========================================================
    # DETECTION
    # ========================================================

    elif page == "🔬 Alzheimer Detection":

        st.title("🔬 Alzheimer Disease Detection")

        st.write(
            "Upload a brain MRI image for AI-based analysis."
        )

        uploaded_file = st.file_uploader(
            "📤 Upload Brain MRI Image",
            type=["jpg", "jpeg", "png"],
            help="Supported formats: JPG, JPEG and PNG"
        )

        if uploaded_file:

            # ------------------------------------------------
            # File signature
            # Prevent duplicate DB entries
            # ------------------------------------------------

            file_bytes = uploaded_file.getvalue()

            file_signature = hashlib.md5(
                file_bytes
            ).hexdigest()

            st.markdown(
                "### 🧠 MRI Image Preview"
            )

            col1, col2 = st.columns([1.25, 1])

            with col1:

                st.image(
                    uploaded_file,
                    caption="Uploaded Brain MRI",
                    use_container_width=True
                )

            with col2:

                st.markdown(
                    """
                    <div class="model-card">
                        <h4>📄 Image Information</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write(
                    f"**File Name:** {uploaded_file.name}"
                )

                st.write(
                    f"**File Type:** {uploaded_file.type}"
                )

                st.write(
                    f"**File Size:** "
                    f"{uploaded_file.size / 1024:.2f} KB"
                )

                st.write(
                    "**Input Resolution:** 224 × 224"
                )

                st.write(
                    "**Model:** EfficientNetB0"
                )

            st.divider()

            analyze_button = st.button(
                "🔍 Analyze MRI Image",
                use_container_width=True,
                type="primary"
            )

            if analyze_button:

                with st.spinner(
                    "🧠 AI model is analyzing the MRI..."
                ):

                    try:

                        prediction, confidence, probabilities = (
                            predict_image(uploaded_file)
                        )

                        confidence_percent = confidence * 100

                        # ------------------------------------
                        # Result
                        # ------------------------------------

                        st.markdown(
                            "### 🧠 AI Prediction Result"
                        )

                        result_col1, result_col2 = st.columns(2)

                        with result_col1:

                            st.markdown(
                                f"""
                                <div class="result-card">
                                    <div class="result-title">
                                        Predicted Class
                                    </div>
                                    <div class="result-value">
                                        {prediction}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with result_col2:

                            st.markdown(
                                f"""
                                <div class="result-card">
                                    <div class="result-title">
                                        Model Confidence
                                    </div>
                                    <div class="result-value">
                                        {confidence_percent:.2f}%
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        # ------------------------------------
                        # Probability
                        # ------------------------------------

                        st.markdown(
                            "### 📊 Class Probabilities"
                        )

                        probability_data = {
                            class_name: round(
                                probability * 100,
                                2
                            )
                            for class_name, probability
                            in probabilities.items()
                        }

                        st.bar_chart(
                            probability_data,
                            y_label="Probability (%)"
                        )

                        # ------------------------------------
                        # Probability Table
                        # ------------------------------------

                        st.markdown(
                            "### 📋 Probability Details"
                        )

                        for class_name, probability in (
                            probability_data.items()
                        ):

                            st.write(
                                f"**{class_name}** — "
                                f"{probability:.2f}%"
                            )

                            st.progress(
                                min(
                                    int(probability),
                                    100
                                )
                            )

                        # ------------------------------------
                        # Save only once
                        # ------------------------------------

                        current_key = (
                            f"{file_signature}_"
                            f"{prediction}_"
                            f"{confidence_percent:.4f}"
                        )

                        if (
                            st.session_state
                            .last_saved_prediction
                            != current_key
                        ):

                            save_prediction(
                                st.session_state.username,
                                uploaded_file.name,
                                prediction,
                                confidence_percent
                            )

                            st.session_state.last_saved_prediction = (
                                current_key
                            )

                            st.success(
                                "✅ Prediction completed and "
                                "saved to prediction history."
                            )

                        else:

                            st.info(
                                "This prediction is already saved "
                                "in your current session."
                            )

                        # ------------------------------------
                        # Model Information
                        # ------------------------------------

                        st.markdown(
                            "### ⚙️ Model Information"
                        )

                        info1, info2, info3 = st.columns(3)

                        with info1:

                            st.markdown(
                                """
                                <div class="model-card">
                                    <b>Model</b><br>
                                    EfficientNetB0
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with info2:

                            st.markdown(
                                """
                                <div class="model-card">
                                    <b>Technique</b><br>
                                    Transfer Learning
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with info3:

                            st.markdown(
                                """
                                <div class="model-card">
                                    <b>Classes</b><br>
                                    4
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        st.warning(
                            "⚠️ This AI prediction is intended "
                            "for research and educational purposes "
                            "only and must not be used as a "
                            "medical diagnosis."
                        )

                    except Exception as e:

                        st.error(
                            f"❌ Prediction failed: {str(e)}"
                        )


    # ========================================================
    # HISTORY
    # ========================================================

    elif page == "📊 Prediction History":

        st.title("📊 Prediction History")

        records = get_predictions(
            st.session_state.username
        )

        if records:

            st.write(
                f"Total saved predictions: **{len(records)}**"
            )

            st.divider()

            for record in records:

                image_name, prediction, confidence, created_at = record

                with st.container(border=True):

                    col1, col2, col3, col4 = st.columns(
                        [2.2, 1.5, 1.2, 1.8]
                    )

                    with col1:

                        st.write("**🖼️ Image**")
                        st.write(image_name)

                    with col2:

                        st.write("**🧠 Prediction**")
                        st.write(prediction)

                    with col3:

                        st.write("**📊 Confidence**")
                        st.write(
                            f"{confidence:.2f}%"
                        )

                    with col4:

                        st.write("**🕒 Date**")
                        st.write(created_at)

        else:

            st.info(
                "No prediction history available yet."
            )


    # ========================================================
    # ANALYTICS
    # ========================================================

    elif page == "📈 Analytics":

        st.title("📈 Analytics")

        records = get_predictions(
            st.session_state.username
        )

        if records:

            total = len(records)

            st.markdown(
                f"### Total analyses performed: **{total}**"
            )

            prediction_counts = {}

            for record in records:

                prediction = record[1]

                prediction_counts[prediction] = (
                    prediction_counts.get(
                        prediction,
                        0
                    ) + 1
                )

            st.markdown(
                "### 📊 Prediction Distribution"
            )

            st.bar_chart(
                prediction_counts,
                y_label="Number of Predictions"
            )

            st.markdown(
                "### 📋 Summary"
            )

            for class_name, count in (
                prediction_counts.items()
            ):

                percentage = (
                    count / total
                ) * 100

                st.write(
                    f"**{class_name}:** "
                    f"{count} prediction(s) "
                    f"({percentage:.1f}%)"
                )

        else:

            st.info(
                "Analytics will appear after predictions "
                "are performed."
            )


# ============================================================
# APPLICATION ROUTER
# ============================================================

if not st.session_state.logged_in:

    login_page()

else:

    dashboard()