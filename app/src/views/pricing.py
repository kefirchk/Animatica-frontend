import streamlit as st
from utils.resource_loader import ResourceLoader

st.set_page_config(page_title="Pricing - Animatica", layout="centered")

# Load resources
ResourceLoader.load_styles("pricing.css")
plans = ResourceLoader.load_json("subscription_plans.json")

# Load templates
header_template = ResourceLoader.load_template("pricing/header.html")
plan_card_template = ResourceLoader.load_template("pricing/plan_card.html")
selection_template = ResourceLoader.load_template("pricing/selection_message.html")

# Header
st.markdown(header_template, unsafe_allow_html=True)


# Init of Selected Plan in session_state
if "selected_plan" not in st.session_state:
    st.session_state.selected_plan = list(plans.keys())[0]


# Select Plan Handler
def select_plan(plan_name):
    st.session_state.selected_plan = plan_name


# Container for Plan Cards
with st.container():
    cols = st.columns(len(plans))
    for col, plan_name in zip(cols, plans.keys()):
        with col:
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


# Select Message
if st.session_state.selected_plan:
    st.markdown(selection_template.format(selected_plan=st.session_state.selected_plan), unsafe_allow_html=True)

    # Subscription Button
    if st.button(
        "Subscribe Now",
        type="primary",
        help=f"Subscribe to {st.session_state.selected_plan} plan",
        use_container_width=True,
    ):
        st.success(f"You have successfully subscribed to {st.session_state.selected_plan}!")
