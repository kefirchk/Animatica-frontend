import streamlit as st
from core.api_config import APIConfig
from services.auth import AuthService
from services.resource import ResourceService

# st.set_page_config(page_title="Pricing - Animatica", layout="centered")

# plans = ResourceService.load_json("subscription_plans.json")

response = AuthService.make_authenticated_request("GET", f"{APIConfig().BASE_URL}/api/v0/subscriptions/suggested")
subscriptions_data = response.json().get("subscriptions", [])
plans = {
    sub["subscription_type_name"].capitalize(): {
        "Price": f"${sub['pricing']['price']}",
        "Discount": f"Discount {sub['pricing']['discount']}%",
        "Features": sub["features"],
        "Credits": sub.get("total_credits", "Unlimited"),
        "Duration": f"{sub.get('duration_days', '')} days" if sub.get("duration_days") else "Unlimited",
        "StripeLink": sub["stripe_link"],
    }
    for sub in subscriptions_data
}

# Load styles and templates
ResourceService.load_styles("pricing.css")
header_template = ResourceService.load_template("pricing/header.html")
plan_card_template = ResourceService.load_template("pricing/plan_card.html")
selection_template = ResourceService.load_template("pricing/selection_message.html")

# Header
st.markdown(header_template, unsafe_allow_html=True)

# Check if plans exist
if not plans:
    st.warning("No subscription plans available at the moment.")
    # st.stop()
    st.switch_page("views/auth.py")

# Init selected plan
if "selected_plan" not in st.session_state:
    st.session_state.selected_plan = list(plans.keys())[0]


# Select Plan Handler
def select_plan(plan_name):
    st.session_state.selected_plan = plan_name


# Container for Plan Cards
with st.container():
    num_columns = min(3, len(plans))
    cols = st.columns(num_columns)
    plan_names = list(plans.keys())

    for i in range(num_columns):
        with cols[i]:
            if i < len(plan_names):
                plan_name = plan_names[i]
                plan = plans[plan_name]
                is_selected = st.session_state.selected_plan == plan_name

                # Plan Select Button
                if st.button(
                    plan_name,
                    key=f"plan_btn_{plan_name}",
                    type="primary" if is_selected else "secondary",
                    use_container_width=True,
                    on_click=select_plan,
                    args=(plan_name,),
                ):
                    pass

                # Show Plan Card
                features_html = "".join(f'<li class="plan-feature">{feature}</li>' for feature in plan["Features"])

                card_html = plan_card_template.format(
                    card_class="plan-card selected" if is_selected else "plan-card",
                    plan_name=plan_name,
                    price=plan["Price"],
                    discount=plan["Discount"],
                    features=features_html,
                )
                st.markdown(card_html, unsafe_allow_html=True)

# Select Message and Subscribe Button
if st.session_state.selected_plan:
    st.markdown(selection_template.format(selected_plan=st.session_state.selected_plan), unsafe_allow_html=True)

    stripe_link = plans[st.session_state.selected_plan]["StripeLink"]
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin: 20px 0;">
            <form action="{stripe_link}" method="GET" target="_self">
                <button type="submit" class="button">
                    Subscribe Now
                </button>
            </form>
        </div>
        """,
        unsafe_allow_html=True,
    )
