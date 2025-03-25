import streamlit as st

st.set_page_config(page_title="DSS Enterprises Simulator", layout="centered")

# Market model (customer expectations)
MARKET_MODEL = {
    "Traditional": {
        "market_size": 7000,
        "ideal_price": (28, 32),
        "ideal_perf": 5.0,
        "ideal_size": 15.0
    },
    "Low-End": {
        "market_size": 8000,
        "ideal_price": (18, 22),
        "ideal_perf": 4.0,
        "ideal_size": 16.0
    }
}

def score_product(price, perf, size, segment):
    model = MARKET_MODEL[segment]
    pmin, pmax = model["ideal_price"]
    price_score = 1 - abs((price - ((pmin + pmax)/2)) / ((pmax - pmin)/2))
    price_score = max(0, min(price_score, 1))
    perf_score = max(0, 1 - abs(perf - model["ideal_perf"]))
    size_score = max(0, 1 - abs(size - model["ideal_size"]))
    return 0.5 * price_score + 0.25 * perf_score + 0.25 * size_score

def simulate(product_name, segment, price, perf, size, marketing, capacity):
    model = MARKET_MODEL[segment]
    satisfaction = score_product(price, perf, size, segment)
    demand_share = satisfaction * 0.3
    expected_sales = min(int(model["market_size"] * demand_share), capacity)
    revenue = expected_sales * price
    cogs = expected_sales * price * 0.6
    cm = revenue - cogs
    profit = cm - marketing
    inventory_left = capacity - expected_sales
    market_share = (expected_sales / model["market_size"]) * 100
    return expected_sales, revenue, profit, inventory_left, market_share

st.title("📊 DSS Enterprises Simulator")
st.markdown("Simulate a Capsim-style business round for two products.")

with st.form("product_form"):
    st.header("Product A (Traditional)")
    price_a = st.number_input("Price A ($)", 0.0, 100.0, 30.0)
    perf_a = st.number_input("Performance A", 0.0, 10.0, 5.0)
    size_a = st.number_input("Size A", 0.0, 20.0, 15.0)
    marketing_a = st.number_input("Marketing Budget A ($)", 0.0, 50000.0, 1500.0)
    capacity_a = st.number_input("Production Capacity A (units)", 0, 10000, 1000)

    st.header("Product B (Low-End)")
    price_b = st.number_input("Price B ($)", 0.0, 100.0, 20.0)
    perf_b = st.number_input("Performance B", 0.0, 10.0, 4.0)
    size_b = st.number_input("Size B", 0.0, 20.0, 16.0)
    marketing_b = st.number_input("Marketing Budget B ($)", 0.0, 50000.0, 1000.0)
    capacity_b = st.number_input("Production Capacity B (units)", 0, 10000, 1200)

    submitted = st.form_submit_button("Simulate Round")

if submitted:
    results = []
    for name, seg, pr, pf, sz, mk, cap in [
        ("Product A", "Traditional", price_a, perf_a, size_a, marketing_a, capacity_a),
        ("Product B", "Low-End", price_b, perf_b, size_b, marketing_b, capacity_b)
    ]:
        sales, rev, prof, inv, share = simulate(name, seg, pr, pf, sz, mk, cap)
        results.append((name, seg, sales, rev, prof, inv, share))

    st.subheader("📈 Round Results")
    for name, seg, sales, rev, prof, inv, share in results:
        st.markdown(f"**{name} ({seg})**")
        st.write(f"Units Sold: {sales}")
        st.write(f"Revenue: ${rev:,.2f}")
        st.write(f"Net Profit: ${prof:,.2f}")
        st.write(f"Inventory Remaining: {inv}")
        st.write(f"Market Share: {share:.2f}%")
