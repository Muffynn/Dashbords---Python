import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.write("Testing Mode - Super Store Dashboard")

# Define a function to load and cache the data
@st.cache_data
def load_data():
    data = pd.read_csv("./dataset/Super_Store_data.csv", encoding='ISO-8859-1', on_bad_lines='skip')
    data['Order Date'] = pd.to_datetime(data['Order Date'])
    data['Ship Date'] = pd.to_datetime(data['Ship Date'])
    return data

# Call the function to load data
data_load_state= st.text('Loading data...')
data = load_data()
data_load_state.text("Data Loaded!✅ (using st.cache_data)")

st.subheader('Super Store Data')
st.write(data)


# Create a 'Year' column from 'Order Date'
data['Year'] = data['Order Date'].dt.year
# Group by year and sum sales
sales_by_year = data.groupby('Year')['Sales'].sum().reset_index()

# Bar chart
fig = px.bar(sales_by_year, x='Year', y='Sales', title='Total Sales by Year',
             text_auto='.2s', color='Sales', color_continuous_scale='Oranges')


# Scatter plot of Sales vs Profit
fig2 = px.scatter(data, x='Sales', y='Profit', color='Category', title='Sales vs Profit',
                   hover_data=['Sub-Category'])


#map dictionary for state abbreviations
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

#Map sales by state
sales_by_state = data.groupby('State')['Sales'].sum().reset_index()
sales_by_state['Code'] = sales_by_state['State'].map(state_abbrev)
fig3 = px.choropleth(
    sales_by_state,
    locations='Code',
    locationmode='USA-states',
    color='Sales',
    hover_name='State',  # shows full name on hover
    scope='usa',
    color_continuous_scale='Reds',
    title='Total Sales by State'
)



# --- Custom CSS for Cards ---
st.markdown("""
<style>
.card {
    background-color: #f9f9f9;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    border: 1px solid #ddd;
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
</style>
""", unsafe_allow_html=True)

# --- Container 1: Cards ---
with st.container():
    st.subheader("📊 Business Overview")

    col1, col2, col3 = st.columns(3)

    # Card 1
    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">Total Sales</div>
            <div class="metric-value">${data['Sales'].sum():,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 2
    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">Average Profit</div>
            <div class="metric-value">${data['Profit'].mean():,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Card 3
    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">Total Orders</div>
            <div class="metric-value">{data['Order ID'].nunique():,}</div>
        </div>
        """, unsafe_allow_html=True)

# --- Container 2: Visual Dashboards ---
with st.container():
    st.subheader("📈 Sales Trends")
    #figure order by columns
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.plotly_chart(fig2, use_container_width=True)
