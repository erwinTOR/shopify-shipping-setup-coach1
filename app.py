import streamlit as st
import re

st.set_page_config(page_title="Take Home Assignment - APM", layout="wide")
st.title("Take Home Assignment - APM")
st.caption("Prototype: Zones → Rates → Packaging → Special Features → Completion")

# ----- SESSION STATE (to share data across tabs) -----
if "rate_strategy" not in st.session_state:
    st.session_state.rate_strategy = "Flat rate"
if "handling_fee" not in st.session_state:
    st.session_state.handling_fee = 0.0
if "zone_mode" not in st.session_state:
    st.session_state.zone_mode = "Use Smart Presets"
if "zone_preset" not in st.session_state:
    st.session_state.zone_preset = "Domestic Hero"
if "custom_zones" not in st.session_state:
    # list of dicts: {"name": ..., "query": ...}
    st.session_state.custom_zones = []

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
        st.session_state.zone_mode = choice

        if choice == "Use Smart Presets":
            st.markdown("#### Smart Presets")
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown("**Domestic Hero**")
                st.caption("Ship only within your main country.")
                st.markdown("Profit grade: **A**")

            with c2:
                st.markdown("**North American Expansion**")
                st.caption("US + Canada with sensible defaults.")
                st.markdown("Profit grade: **B**")

            with c3:
                st.markdown("**Global Explorer**")
                st.caption("Sell worldwide with protective margins.")
                st.markdown("Profit grade: **B−**")

            preset = st.selectbox(
                "Select a preset to preview",
                ["Domestic Hero", "North American Expansion", "Global Explorer"],
            )
            st.session_state.zone_preset = preset

        else:
            st.markdown("#### Build Custom Zones")
            query = st.text_input(
                "Search regions, countries, or zones (e.g. “Europe”)",
                placeholder="Type “Europe”, “US West”, “Asia Pacific”…",
                key="custom_zone_query",
            )

            zone_name = st.text_input(
                "Name this zone (e.g. 'EU Core', 'US West')",
                placeholder="Give your custom zone a name",
                key="custom_zone_name",
            )

            if st.button("Save custom zone", type="primary"):
                if zone_name and query:
                    st.session_state.custom_zones.append(
                        {"name": zone_name, "query": query}
                    )
                    st.success(f"Saved zone: {zone_name}")
                else:
                    st.warning("Please enter both a zone name and at least one region/country before saving.")

            if query:
                st.markdown(f"Current selection (not yet saved): `{query}`")

            optimize_profit = st.toggle(
                "Optimize for profit (exclude high‑cost remote areas)",
                value=True,
            )
            if optimize_profit:
                st.caption("Remote islands and high‑cost regions are excluded to protect margins.")

    with right:
        st.markdown("### Live feedback")
        st.caption("Updates as you configure zones.")

        # Simple fake numbers, just for demo
        if st.session_state.zone_mode == "Use Smart Presets":
            if st.session_state.zone_preset == "Domestic Hero":
                reach = "1 country"
            elif st.session_state.zone_preset == "North American Expansion":
                reach = "2 countries"
            else:
                reach = "40+ countries"
        else:
            # rough idea: number of saved zones = reach hint
            count = len(st.session_state.custom_zones)
            reach = f"{count} custom zone(s)" if count > 0 else "Custom (not yet saved)"

        st.metric("Potential reach", reach)

        with st.expander("What does profit grade mean?"):
            st.write(
                "- **Domestic Hero (A)** – Focused on your primary country with strong margin protection.\n"
                "- **North American Expansion (B)** – Balanced reach across US and Canada with healthy margins.\n"
                "- **Global Explorer (B−)** – Maximum reach worldwide with protective but tighter margin assumptions."
            )

        if st.session_state.custom_zones:
            with st.expander("Saved custom zones (click to view/edit)"):
                for idx, z in enumerate(st.session_state.custom_zones):
                    st.markdown(f"**Zone {idx + 1}**")
                    new_name = st.text_input(
                        f"Name for zone {idx + 1}",
                        value=z["name"],
                        key=f"zone_name_{idx}",
                    )
                    new_query = st.text_input(
                        f"Regions/countries for zone {idx + 1}",
                        value=z["query"],
                        key=f"zone_query_{idx}",
                    )
                    # Update the stored values with edits
                    st.session_state.custom_zones[idx]["name"] = new_name
                    st.session_state.custom_zones[idx]["query"] = new_query
                    st.markdown("---")

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
    st.button("Save & continue to Special Features", type="primary", key="rates_continue")

# ===================== PACKAGING & DIMENSIONS =====================
with tab_packaging:
    st.subheader("Packaging & Dimensions")

    # Only show the full packaging setup if Carrier‑calculated is chosen
    if st.session_state.rate_strategy != "Carrier‑calculated":
        st.info("This step is only for Carrier-calculated rates.")
    else:
        st.caption("Required when using carrier‑calculated rates to avoid surprises at checkout.")

        mode = st.radio(
            "Packaging type",
            ["Carrier packaging", "Custom / oversized"],
            horizontal=True,
        )

        if mode == "Carrier packaging":
            st.markdown("#### Carrier packaging")

            # Extended list of mock carrier boxes
            box_options = [
                "UPS – Small Box (12 x 9 x 2 in)",
                "UPS – Medium Box (16 x 12 x 3 in)",
                "UPS – Large Box (18 x 18 x 8 in)",
                "FedEx – Pak (13 x 11 x 2 in) [Recommended for your product]",
                "FedEx – Large Box (17 x 13 x 3 in)",
                "FedEx – Tube (38 x 6 x 6 in)",
                "USPS – Flat Rate Box (Medium, 14 x 12 x 3 in)",
                "USPS – Flat Rate Box (Large, 24 x 12 x 6 in)",
            ]

            option = st.selectbox(
                "Choose a carrier box",
                box_options,
            )

            st.markdown(f"**Box preview:** {option}")

            # Highlight a subtle recommendation based on the option text
            if "Recommended for your product" in option:
                st.markdown("*:green[Recommended for your product]*")

            # Parse dimensions from option for display
            dims_match = re.search(r"\(([\dx\s]+in)\)", option)
            dims_text = dims_match.group(1) if dims_match else "N/A"

            dims_numbers = re.findall(r"(\d+)", dims_text)
            if len(dims_numbers) >= 3:
                L, W, H = dims_numbers[0], dims_numbers[1], dims_numbers[2]
            else:
                L, W, H = "L", "W", "H"

            st.markdown("##### Box dimensions guidance")
            # If you add a real image file named 'box_dimensions.png' in the repo, uncomment the next line:
            # st.image("box_dimensions.png", caption="Example box showing length, width, and height.")
            st.markdown(
                f"""
                - Length: **{L} in**  
                - Width: **{W} in**  
                - Height: **{H} in**  
                """
            )
            st.caption("Visual guidance: merchants see how each dimension maps onto the box they select.")

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
    st.button("Save & continue to Special Features", type="primary", key="packaging_continue")

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
    st.button("Save & continue to Completion", type="primary", key="special_continue")

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

        mock_city = st.text_input("Mock city", placeholder="e.g., Toronto, New York, London")

        # Very simple mock logic: if city name looks like "domestic" vs "international"
        city_lower = mock_city.lower()
        if city_lower.strip() == "":
            shipping = 10.0 if st.session_state.rate_strategy == "Flat rate" else 12.34
        elif any(c in city_lower for c in ["toronto", "montreal", "vancouver", "ottawa"]):
            shipping = 8.0  # domestic Canada – cheaper
        elif any(c in city_lower for c in ["new york", "la", "los angeles", "chicago", "seattle"]):
            shipping = 10.0  # North American zone
        else:
            shipping = 18.0  # treat as international / global explorer

    with right:
        st.markdown("#### Customer receipt")
        st.write(f"Product: ${base_price:.2f}")
        st.write(f"Shipping ({mock_city or 'default'}): ${shipping:.2f}")
        st.write(f"Handling fee: ${st.session_state.handling_fee:.2f}")
        total = base_price + shipping + st.session_state.handling_fee
        st.markdown(f"**Total: ${total:.2f}**")

    st.divider()
    if st.button("Activate shipping", type="primary"):
        st.success("Shipping is live!")
        st.balloons()
