import streamlit as st

st.set_page_config(page_title="Take Home Assignment - APM", layout="wide")
st.title("Take Home Assignment - APM")
st.caption("Prototype: Zones → Rates → Packaging → Special Features → Completion")

# ----- SESSION STATE (to share data across tabs) -----
if "rate_strategy" not in st.session_state:
    st.session_state.rate_strategy = "Flat rate"
if "handling_fee" not in st.session_state:
    st.session_state.handling_fee = 0.0

# ----- TABS -----
tab_zones, tab_rates, tab_packaging, tab_special, tab_done = st.tabs(
    ["Zones", "Rates", "Packaging & Dimensions", "Special Features", "Completion"]
)

# ===================== ZONES =====================
with tab_zones:
    st.subheader("Zones")

    left, right = st.columns([2, 1])

    with left:
        st.markdown("### How would you like to set up your zones?")
        choice = st.radio(
            "Choose setup mode",
            ["Use Smart Presets", "Build Custom Zones"],
            horizontal=True,
            label_visibility="collapsed",
        )

        if choice == "Use Smart Presets":
            st.markdown("#### Smart Presets")
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown("**Domestic Hero**")
                st.caption("Ship only within your main country.")
                st.badge("Profit grade: A")

            with c2:
                st.markdown("**North American Expansion**")
                st.caption("US + Canada with sensible defaults.")
                st.badge("Profit grade: B")

            with c3:
                st.markdown("**Global Explorer**")
                st.caption("Sell worldwide with protective margins.")
                st.badge("Profit grade: B−")

            preset = st.selectbox(
                "Select a preset to preview",
                ["Domestic Hero", "North American Expansion", "Global Explorer"],
            )

        else:
            st.markdown("#### Build Custom Zones")
            query = st.text_input(
                "Search regions, countries, or zones (e.g. “Europe”)",
                placeholder="Type “Europe”, “US West”, “Asia Pacific”…",
            )
            if query:
                st.markdown(f"Selected zone tag: `{query}`")

            optimize_profit = st.toggle(
                "Optimize for profit (exclude high‑cost remote areas)",
                value=True,
            )
            if optimize_profit:
                st.caption("Remote islands and high‑cost regions are excluded to protect margins.")

    with right:
        st.markdown("### Live feedback")
        st.caption("Updates as you configure zones.")

        # Very simple fake numbers, just for demo
        st.metric("Potential reach", "12 countries")
        st.metric("Avg. order value", "$65")
        st.metric("Net profit estimate", "Healthy")

    st.divider()
    st.button("Save & continue to Rates", type="primary", key="zones_continue")

# ===================== RATES =====================
with tab_rates:
    st.subheader("Rates")

    st.markdown("### Choose your main rate strategy")

    strategy = st.radio(
        "Rate strategy",
        ["Flat rate", "Carrier‑calculated"],
        horizontal=True,
    )
    st.session_state.rate_strategy = strategy

    if strategy == "Flat rate":
        st.info("Flat rate: You set fixed prices customers pay at checkout.")

        view = st.radio(
            "How do you want to structure your flat rates?",
            ["By transit time", "By price", "By weight"],
            horizontal=True,
        )

        if view == "By transit time":
            st.markdown("#### By transit time")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                express = st.number_input("Express (1–2 days)", min_value=0.0, value=20.0)
            with col_b:
                economy = st.number_input("Economy (5–7 days)", min_value=0.0, value=10.0)
            with col_c:
                value = st.number_input("Value (7–14 days)", min_value=0.0, value=6.0)

        elif view == "By price":
            st.markdown("#### By cart price")
            threshold = st.number_input("If cart price is over…", min_value=0.0, value=75.0)
            charge = st.number_input("…then charge this shipping price", min_value=0.0, value=0.0)
            st.caption("Example: Free shipping over $75, flat rate below that.")

        else:
            st.markdown("#### By weight")
            weight_limit = st.number_input("If total weight (kg) is over…", min_value=0.0, value=5.0)
            charge_weight = st.number_input("…then charge this shipping price", min_value=0.0, value=25.0)

        st.caption("With Flat rate, Packaging & Dimensions becomes optional for a simple setup.")

    else:
        st.info("Carrier‑calculated: Real‑time rates from carriers like UPS and FedEx (simulated here).")
        st.markdown("#### Carrier‑calculated (placeholder)")
        st.caption("In a real build, this is where merchants connect UPS/FedEx accounts.")
        st.selectbox("Preferred carrier", ["UPS", "FedEx", "USPS"])

    st.divider()
    st.button("Save & continue to Packaging", type="primary", key="rates_continue")

# ===================== PACKAGING & DIMENSIONS =====================
with tab_packaging:
    st.subheader("Packaging & Dimensions")

    if st.session_state.rate_strategy == "Flat rate":
        st.caption("Optional: For simple flat-rate setups, you can skip detailed packaging for now.")

    mode = st.radio(
        "Packaging type",
        ["Carrier packaging", "Custom / oversized"],
        horizontal=True,
    )

    if mode == "Carrier packaging":
        st.markdown("#### Carrier packaging")
        option = st.selectbox(
            "Choose a carrier box",
            [
                "UPS – Small Box (12 x 9 x 2 in)",
                "UPS – Medium Box (16 x 12 x 3 in)",
                "FedEx – Envelope",
                "FedEx – Tube",
                "USPS – Flat Rate Box (Medium)"
            ],
        )
        st.markdown(f"**Box preview:** {option}")
        st.info("Recommendation: Merchants with similar products often choose this packaging option.")

    else:
        st.markdown("#### Custom / oversized packaging")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            length = st.number_input("Length (in)", min_value=0.0, value=40.0)
        with c2:
            width = st.number_input("Width (in)", min_value=0.0, value=20.0)
        with c3:
            height = st.number_input("Height (in)", min_value=0.0, value=20.0)
        with c4:
            weight = st.number_input("Box weight (lb)", min_value=0.0, value=10.0)

        # Simple oversize rule (not exact freight logic, just a warning)
        if length + width + height > 108:
            st.warning("This may require freight shipping.")

        st.toggle("Freight / large item", value=False)

    st.divider()
    st.button("Save & test rates", type="primary", key="packaging_continue")
    st.button("I'll do this later", key="packaging_later")

# ===================== SPECIAL FEATURES =====================
with tab_special:
    st.subheader("Special Features")

    st.markdown("#### Local pickup")
    lp = st.toggle("Allow customers to pick up orders in person")
    if lp:
        st.text_input("Pickup instructions", placeholder="e.g., Ring the side doorbell, pickup between 10–5")

    st.markdown("#### Handling fee")
    hf = st.toggle("Add a small flat fee to every order to cover packaging labor")
    if hf:
        st.session_state.handling_fee = st.number_input(
            "Handling fee per order",
            min_value=0.0,
            value=float(st.session_state.handling_fee),
        )
    else:
        st.session_state.handling_fee = 0.0

    st.markdown("#### Shipping insurance")
    si = st.toggle("Offer package protection at checkout")
    if si:
        st.caption("Customers can opt in to added protection during checkout.")

    st.divider()
    st.button("Save & continue to Confirmation", type="primary", key="special_continue")

# ===================== COMPLETION =====================
with tab_done:
    st.subheader("Completion")

    st.warning(
        "Using tentative metrics? Make sure you return to add exact weights later to protect your profit margins."
    )

    st.markdown("### Test your checkout")

    left, right = st.columns(2)

    with left:
        product = st.selectbox(
            "Mock product",
            [
                "Heavy Oak Chair – $200",
                "Silk Scarf – $40"
            ],
        )
        base_price = 200.0 if "Chair" in product else 40.0

        # Super simple "rate" just for demo
        if st.session_state.rate_strategy == "Flat rate":
            shipping = 10.0
        else:
            shipping = 12.34

    with right:
        st.markdown("#### Customer receipt")
        st.write(f"Product: ${base_price:.2f}")
        st.write(f"Shipping: ${shipping:.2f}")
        st.write(f"Handling fee: ${st.session_state.handling_fee:.2f}")
        total = base_price + shipping + st.session_state.handling_fee
        st.markdown(f"**Total: ${total:.2f}**")

    st.divider()
    if st.button("Activate shipping", type="primary"):
        st.success("Shipping is live!")
        st.balloons()
