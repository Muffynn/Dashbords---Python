import streamlit as st
import pandas as pd
import plotly.express as px

st.write("Testing Mode - Super Store Dashboard")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    data = pd.read_csv("./dataset/Super_Store_data.csv", encoding='ISO-8859-1', on_bad_lines='skip')
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Ship Date'] = pd.to_datetime(data['Ship Date'])
    return data

data_load_state = st.text("Loading data...")
data = load_data()
data_load_state.text("Data Loaded! ✅ (using st.cache_data)")

# Create Year column
data['Year'] = data['Order Date'].dt.year

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

# YEAR FILTER (for Sub-Category only)
years = sorted(data['Year'].unique())
selected_years = st.sidebar.multiselect("Filter by Year (Sub-Category only)", years, default=years)

# Sub-Category FILTER (applied globally)
categories = sorted(data['Sub-Category'].unique())
selected_categories = st.sidebar.multiselect("Filter by Category", categories, default=categories)

# Apply global filters (exclude Year)
df = data[data['Sub-Category'].isin(selected_categories)]

st.subheader("Super Store Data")
st.write(df)

# =========================
# BUSINESS OVERVIEW CARDS
# =========================
st.markdown("""
<style>
.card { background-color: #f9f9f9; border-radius: 15px; padding: 20px;
       box-shadow: 2px 2px 8px rgba(0,0,0,0.1); border: 1px solid #ddd; text-align: center; }
.metric-label { font-size: 16px; color: #666; }
.metric-value { font-size: 26px; font-weight: bold; color: #333; }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.subheader("📊 Business Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='card'><div class='metric-label'>Total Sales</div><div class='metric-value'>${df['Sales'].sum():,.2f}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='card'><div class='metric-label'>Average Profit</div><div class='metric-value'>${df['Profit'].mean():,.2f}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='card'><div class='metric-label'>Total Orders</div><div class='metric-value'>{df['Order ID'].nunique():,}</div></div>", unsafe_allow_html=True)

# =========================
# SALES BY YEAR (global)
# =========================
sales_by_year = df.groupby('Year')['Sales'].sum().reset_index()
fig_year = px.bar(sales_by_year, x='Year', y='Sales', text_auto='.2s', color='Sales',
                  color_continuous_scale='Oranges', title='Total Sales by Year')

# =========================
# Sub-Category TREND (Pie Chart) filtered by Year AND Category
# =========================
df_subcategory = data[
    (data['Sub-Category'].isin(selected_categories)) &
    (data['Year'].isin(selected_years))
]

# Aggregate total sales by Sub-Category
subcategory_sales = df_subcategory.groupby('Sub-Category')['Sales'].sum().reset_index()

# Create Pie chart
fig_cat_trend = px.pie(
    subcategory_sales,
    names='Sub-Category',
    values='Sales',
    title="Sales Distribution by Sub-Category",
    hole=0  # set >0 for donut chart if desired
)

# Add data labels (show percentage + label + value)
fig_cat_trend.update_traces(textposition='inside', textinfo='percent+label+value')

# =========================
# SCATTER (SALES VS PROFIT) - global
# =========================
fig_scatter = px.scatter(df, x='Sales', y='Profit', color='Category',
                         hover_data=['Sub-Category'], title='Sales vs Profit')

# =========================
# MAP (global)
# =========================
state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
    'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

sales_by_state = df.groupby('State')['Sales'].sum().reset_index()
sales_by_state['Code'] = sales_by_state['State'].map(state_abbrev)

fig_map = px.choropleth(sales_by_state, locations='Code', locationmode='USA-states',
                        color='Sales', hover_name='State', scope='usa',
                        color_continuous_scale='Reds', title='Total Sales by State')

# =========================
# VISUALIZATION LAYOUT
# =========================
with st.container():
    st.subheader("📈 Sales Trends")
    colA, colB = st.columns(2)
    with colA:
        st.plotly_chart(fig_year, use_container_width=True)
    with colB:
        st.plotly_chart(fig_map, use_container_width=True)
        # st.plotly_chart(fig_scatter, use_container_width=True)

# =========================
# Full-width Sub-Category Trend (Pie Chart)
# =========================
with st.container():
    st.subheader("📊 Sub-Category Trend (Pie Chart)")
    st.plotly_chart(fig_cat_trend, use_container_width=True)
