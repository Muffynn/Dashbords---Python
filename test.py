import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# DASHBOARD TITLE
# =========================
st.markdown("""
<style>
.dashboard-title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #FF6F61;
    font-family: 'Trebuchet MS', sans-serif;
    margin-bottom: 30px;
}
</style>
<div class="dashboard-title">📊 Super Store Dashboard</div>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    data = pd.read_csv("./dataset/Super_Store_data.csv", encoding='ISO-8859-1', on_bad_lines='skip')
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Ship Date'] = pd.to_datetime(data['Ship Date'])
    data['Year'] = data['Order Date'].dt.year
    return data

data = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

years = sorted(data['Year'].unique())
selected_years = st.sidebar.multiselect("Filter by Year (Sub-Category only)", years, default=years)

categories = sorted(data['Sub-Category'].unique())
selected_categories = st.sidebar.multiselect("Filter by Category", categories, default=categories)

df = data[data['Sub-Category'].isin(selected_categories)]

st.subheader("⊞ Super Store Dataset")
st.write(df)

# =========================
# STYLES FOR UNIFORM CARD HEIGHTS
# =========================
with st.container(): st.subheader("📊 Business Overview")
st.markdown("""
<style>
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    height: 100px;              /* FIXED HEIGHT */
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
}
.metric-label {
    font-size: 16px;
    color: #666;
}
.metric-value {
    font-size: 26px;
    font-weight: bold;
    color: #333;
}
.row-space {
    margin-top: 20px;           /* SPACE BETWEEN ROWS */
}
</style>
""", unsafe_allow_html=True)

# =========================
# BUSINESS OVERVIEW CARDS
# =========================

# ---- Row 1 ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='card'><div class='metric-label'>Total Sales</div><div class='metric-value'>${df['Sales'].sum():,.2f}</div></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='card'><div class='metric-label'>Average Profit</div><div class='metric-value'>${df['Profit'].mean():,.2f}</div></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='card'><div class='metric-label'>Total Orders</div><div class='metric-value'>{df['Order ID'].nunique():,}</div></div>", unsafe_allow_html=True)

# ---- Space between rows ----
st.markdown("<div class='row-space'></div>", unsafe_allow_html=True)

# ---- Row 2 ----
total_profit = df['Profit'].sum()
total_quantity = df['Quantity'].sum()
avg_discount = df['Discount'].mean() * 100
profit_margin = (total_profit / df['Sales'].sum()) * 100 if df['Sales'].sum() > 0 else 0

col4, col5, col6, col7 = st.columns(4)

with col4:
    st.markdown(f"<div class='card'><div class='metric-label'>Total Profit</div><div class='metric-value'>${total_profit:,.2f}</div></div>", unsafe_allow_html=True)

with col5:
    st.markdown(f"<div class='card'><div class='metric-label'>Total Quantity Sold</div><div class='metric-value'>{total_quantity:,}</div></div>", unsafe_allow_html=True)

with col6:
    st.markdown(f"<div class='card'><div class='metric-label'>Average Discount</div><div class='metric-value'>{avg_discount:.2f}%</div></div>", unsafe_allow_html=True)

with col7:
    st.markdown(f"<div class='card'><div class='metric-label'>Profit Margin</div><div class='metric-value'>{profit_margin:.2f}%</div></div>", unsafe_allow_html=True)

# =========================
# COLOR PALETTES
# =========================
color_sequence = ['#FC4100', '#FFC55A', '#2C4E80', '#00215E']
continuous_scale = ['#00215E', '#2C4E80', '#FFC55A', '#FC4100']

# =========================
# CHARTS
# =========================

# SALES BY YEAR
sales_by_year = df.groupby('Year')['Sales'].sum().reset_index()

fig_year = px.line(
    sales_by_year,
    x='Year',
    y='Sales',
    markers=True,  # Show markers for each year
    title='Total Sales by Year',
    color_discrete_sequence=['#FC4100']  # Line color
)

# Add data labels on markers
fig_year.update_traces(
    text=sales_by_year['Sales'].apply(lambda x: f"${x:,.2f}"),  # Format as currency
    textposition='top center',
    mode='markers+text+lines',
    textfont=dict(size=12, color='#FFFFFF')  # Optional: adjust font
)

fig_year.update_layout(
    height=500,
    yaxis_title='Sales ($)',
    xaxis_title='Year'
)

# Profit BY YEAR
sales_by_profit = df.groupby('Year')['Profit'].sum().reset_index()

fig_profit = px.line(
    sales_by_profit,
    x='Year',
    y='Profit',
    markers=True,  # Show markers for each year
    title='Total Profit by Year',
    color_discrete_sequence=['#00215E']  # Line color
)

# Add data labels on markers
fig_profit.update_traces(
    text=sales_by_profit['Profit'].apply(lambda x: f"${x:,.2f}"),  # Format as currency
    textposition='top center',
    mode='markers+text+lines',
    textfont=dict(size=12, color='#FFFFFF')  # Optional: adjust font
)

fig_profit.update_layout(
    height=500,
    yaxis_title='Profit ($)',
    xaxis_title='Year'
)

# SEGMENT SALES
segment_sales = df.groupby('Segment')['Sales'].sum().reset_index()
fig_segment = px.bar(
    segment_sales,
    x='Segment',
    y='Sales',
    text_auto='.2s',
    color='Segment',
    title='Total Sales by Segment',
    color_discrete_sequence=color_sequence
)
fig_segment.update_layout(height=500)

# SUB-CATEGORY PIE
df_sub = data[
    (data['Sub-Category'].isin(selected_categories)) &
    (data['Year'].isin(selected_years))
]
subcategory_sales = df_sub.groupby('Sub-Category')['Sales'].sum().reset_index()
fig_cat_trend = px.pie(
    subcategory_sales,
    names='Sub-Category',
    values='Sales',
    title="Sales Distribution by Sub-Category",
    color_discrete_sequence=color_sequence * 10
)
fig_cat_trend.update_traces(textposition='inside', textinfo='percent+label+value')

# SCATTER
fig_scatter = px.scatter(
    df,
    x='Sales',
    y='Profit',
    color='Category',
    hover_data=['Sub-Category'],
    color_discrete_sequence=color_sequence,
    title='Sales vs Profit'
)
fig_scatter.update_layout(height=500)

# MAP
state_abbrev = {
    'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA',
    'Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','Florida': 'FL','Georgia': 'GA',
    'Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN','Iowa': 'IA','Kansas': 'KS',
    'Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA',
    'Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO','Montana': 'MT',
    'Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM',
    'New York': 'NY','North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH','Oklahoma': 'OK',
    'Oregon': 'OR','Pennsylvania': 'PA','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD',
    'Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virginia': 'VA','Washington': 'WA',
    'West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'
}
sales_by_state = df.groupby('State')['Sales'].sum().reset_index()
sales_by_state['Code'] = sales_by_state['State'].map(state_abbrev)

fig_map = px.choropleth(
    sales_by_state,
    locations='Code',
    locationmode='USA-states',
    color='Sales',
    hover_name='State',
    scope='usa',
    color_continuous_scale=continuous_scale,
    title='Total Sales by State'
)
fig_map.update_layout(height=500)

# TOP 3 MOST PROFITABLE
top_products = df.groupby('Sub-Category')['Profit'].sum().reset_index()
top_products = top_products.sort_values(by='Profit', ascending=False).head(3)
fig_top_products = px.bar(
    top_products,
    x='Sub-Category',
    y='Profit',
    text_auto='.2s',
    color='Sub-Category',
    title='Top 3 Most Profitable Sub-Categories',
    color_discrete_sequence=color_sequence[:3]
)
fig_top_products.update_layout(height=500, showlegend=False)

# TOP 10 STATES BY SALES (Heatmap Style)
top_states = df.groupby('State')['Sales'].sum().reset_index()
top_states = top_states.sort_values(by='Sales', ascending=False).head(10)

fig_top_states = px.bar(
    top_states,
    x='State',
    y='Sales',
    text=top_states['Sales'].apply(lambda x: f"${x:,.0f}"),  # Display values as labels
    color='Sales',  # Map color to Sales for heat effect
    title='Top 10 States by Sales',
    color_continuous_scale=continuous_scale,  # Use your defined heat scale
)

fig_top_states.update_layout(
    height=500,
    showlegend=False,
    yaxis_title='Sales ($)',
    xaxis_title='State'
)

# =========================
# LAYOUT
# =========================
with st.container():
    colA, colB = st.columns(2)

    with colA:
        st.plotly_chart(fig_year, use_container_width=True)
        st.plotly_chart(fig_segment, use_container_width=True)
        st.plotly_chart(fig_map, use_container_width=True)
        st.plotly_chart(fig_cat_trend, use_container_width=True)
        

    with colB:
        st.plotly_chart(fig_profit, use_container_width=True)
        st.plotly_chart(fig_top_products, use_container_width=True)
        st.plotly_chart(fig_top_states, use_container_width=True)
        
        

# # =========================
# # FULL-WIDTH PIE CHART
# # =========================
# with st.container():
    
