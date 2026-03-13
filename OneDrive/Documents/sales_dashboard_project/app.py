"""
Modern AI-Powered Sales Analytics Dashboard
A professional business dashboard with dark theme, similar to Power BI
Built with Streamlit, Pandas, and Plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Dark Theme Dashboard
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main Background - Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0a1628 0%, #1a2d4a 50%, #0d1f3c 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Force single page - no scrolling */
    html, body {
        max-height: 100vh !important;
        overflow: hidden !important;
    }
    
    /* Main content container */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        max-width: 100% !important;
    }
    
    /* Sidebar - Dark Theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1f3c 0%, #1a2d4a 100%) !important;
        min-width: 260px !important;
        max-width: 260px !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #e0e6ed !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #64b5f6 !important;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] label {
        color: #90caf9 !important;
        font-size: 0.8rem !important;
        font-weight: 500;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: #1a2d4a !important;
        border-color: #64b5f6 !important;
    }
    
    section[data-testid="stSidebar"] .stMultiSelect > div > div {
        background: #1a2d4a !important;
        border-color: #64b5f6 !important;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(90deg, #1565c0 0%, #0d47a1 50%, #1565c0 100%);
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(100,181,246,0.3);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.25rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.85rem !important;
        margin: 0 !important;
    }
    
    /* KPI Cards with Gradient Backgrounds */
    .kpi-card {
        border-radius: 12px;
        padding: 1rem 1.25rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        height: 100%;
    }
    
    .kpi-card-sales {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 50%, #1976d2 100%);
    }
    
    .kpi-card-profit {
        background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 50%, #388e3c 100%);
    }
    
    .kpi-card-orders {
        background: linear-gradient(135deg, #e65100 0%, #ef6c00 50%, #f57c00 100%);
    }
    
    .kpi-card-title {
        color: rgba(255,255,255,0.9) !important;
        font-size: 0.75rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .kpi-card-value {
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .kpi-card-delta {
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.7rem !important;
        margin-top: 0.25rem;
    }
    
    /* Chart Containers - Dark Theme */
    .chart-container {
        background: linear-gradient(145deg, #1a2d4a 0%, #0d1f3c 100%);
        border-radius: 12px;
        padding: 0.75rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        border: 1px solid rgba(100,181,246,0.2);
        height: 100%;
    }
    
    .chart-title {
        color: #64b5f6 !important;
        font-size: 0.9rem !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid rgba(100,181,246,0.3);
    }
    
    /* Insight Boxes */
    .insight-box {
        background: linear-gradient(135deg, #1a2d4a 0%, #0d1f3c 100%);
        border-left: 3px solid #64b5f6;
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        margin-top: 0.5rem;
        color: #90caf9;
        border: 1px solid rgba(100,181,246,0.2);
    }
    
    .insight-box h4 {
        color: #64b5f6 !important;
        font-weight: 600;
        margin-bottom: 0.25rem;
        font-size: 0.8rem !important;
    }
    
    .insight-box ul {
        margin: 0 !important;
        padding-left: 1rem !important;
        font-size: 0.7rem !important;
    }
    
    .insight-box li {
        margin-bottom: 0.1rem !important;
        color: #bbdefb;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Reduce section headers */
    h3, h4 {
        color: #64b5f6 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        background: transparent !important;
    }
    
    /* Remove scrollbars */
    ::-webkit-scrollbar {
        display: none;
    }
    
    /* Make all text more readable on dark background */
    .stMarkdown {
        color: #e0e6ed;
    }
    
    /* Vertical block spacing */
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.4rem !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the sales data"""
    df = pd.read_csv('sales_data.csv')
    
    # Convert date column
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
    
    # Convert numeric columns
    numeric_cols = ['Sales', 'Profit', 'Quantity', 'Discount']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def calculate_metrics(df):
    """Calculate key performance metrics"""
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'total_orders': total_orders
    }

def create_kpi_cards(metrics):
    """Create modern KPI cards with gradient backgrounds"""
    
    # Create columns for KPI cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card kpi-card-sales">
            <div class="kpi-card-title">💰 Total Sales</div>
            <div class="kpi-card-value">${metrics['total_sales']:,.0f}</div>
            <div class="kpi-card-delta">📈 Revenue Generated</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card kpi-card-profit">
            <div class="kpi-card-title">💵 Total Profit</div>
            <div class="kpi-card-value">${metrics['total_profit']:,.0f}</div>
            <div class="kpi-card-delta">📊 Net Profit</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card kpi-card-orders">
            <div class="kpi-card-title">📦 Total Orders</div>
            <div class="kpi-card-value">{metrics['total_orders']:,}</div>
            <div class="kpi-card-delta">🛒 Orders Placed</div>
        </div>
        """, unsafe_allow_html=True)

def create_sales_by_category_chart(df):
    """Create sales by category bar chart"""
    category_sales = df.groupby('Category')['Sales'].sum().reset_index()
    category_sales = category_sales.sort_values('Sales', ascending=True)
    
    fig = px.bar(
        category_sales,
        x='Sales',
        y='Category',
        orientation='h',
        title='Sales by Category',
        text='Sales',
        color='Category',
        color_discrete_sequence=['#42a5f5', '#66bb6a', '#ffa726']
    )
    
    fig.update_traces(
        texttemplate='$%{text:,.0f}', 
        textposition='outside',
        marker_line_width=1,
        marker_line_color='white'
    )
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=10, color='#e0e6ed'),
        showlegend=False,
        height=180,
        margin=dict(l=10, r=60, t=30, b=10),
        xaxis=dict(showgrid=True, gridcolor='rgba(100,181,246,0.2)', tickfont_size=9, color='#90caf9'),
        yaxis=dict(tickfont_size=10, color='#90caf9')
    )
    
    return fig

def create_sales_by_region_chart(df):
    """Create sales by region bar chart"""
    region_sales = df.groupby('Region')['Sales'].sum().reset_index()
    region_sales = region_sales.sort_values('Sales', ascending=True)
    
    fig = px.bar(
        region_sales,
        x='Sales',
        y='Region',
        orientation='h',
        title='Sales by Region',
        text='Sales',
        color='Region',
        color_discrete_sequence=['#ab47bc', '#26c6da', '#ff7043', '#9ccc65']
    )
    
    fig.update_traces(
        texttemplate='$%{text:,.0f}', 
        textposition='outside',
        marker_line_width=1,
        marker_line_color='white'
    )
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=10, color='#e0e6ed'),
        showlegend=False,
        height=180,
        margin=dict(l=10, r=60, t=30, b=10),
        xaxis=dict(showgrid=True, gridcolor='rgba(100,181,246,0.2)', tickfont_size=9, color='#90caf9'),
        yaxis=dict(tickfont_size=10, color='#90caf9')
    )
    
    return fig

def create_monthly_sales_trend(df):
    """Create monthly sales trend line chart"""
    monthly_sales = df.groupby(df['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly_sales['Order Date'] = monthly_sales['Order Date'].astype(str)
    
    fig = px.line(
        monthly_sales,
        x='Order Date',
        y='Sales',
        title='Monthly Sales Trend',
        markers=True,
        line_shape='spline'
    )
    
    fig.update_traces(
        line_color='#42a5f5',
        line_width=3,
        marker=dict(size=6, color='#64b5f6', symbol='circle')
    )
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=10, color='#e0e6ed'),
        height=220,
        margin=dict(l=10, r=20, t=30, b=10),
        xaxis=dict(showgrid=False, tickfont_size=9, color='#90caf9'),
        yaxis=dict(showgrid=True, gridcolor='rgba(100,181,246,0.2)', tickfont_size=9, color='#90caf9')
    )
    
    return fig

def create_top_products_chart(df):
    """Create top 5 products by sales horizontal bar chart"""
    top_products = df.groupby('Product Name')['Sales'].sum().reset_index()
    top_products = top_products.nlargest(5, 'Sales')
    top_products = top_products.sort_values('Sales', ascending=True)
    
    # Add trophy for #1
    top_products['Product Name'] = top_products['Product Name'].apply(
        lambda x: '🏆 ' + x[:35] + '...' if len(x) > 35 else '🏆 ' + x
    )
    
    fig = px.bar(
        top_products,
        x='Sales',
        y='Product Name',
        orientation='h',
        title='Top 5 Products by Sales',
        text='Sales',
        color='Sales',
        color_continuous_scale=['#1565c0', '#42a5f5']
    )
    
    fig.update_traces(
        texttemplate='$%{text:,.0f}', 
        textposition='outside',
        marker_line_width=1,
        marker_line_color='white'
    )
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=9, color='#e0e6ed'),
        showlegend=False,
        height=200,
        margin=dict(l=10, r=70, t=30, b=10),
        xaxis=dict(showgrid=True, gridcolor='rgba(100,181,246,0.2)', tickfont_size=9, color='#90caf9'),
        yaxis=dict(tickfont_size=9, color='#90caf9')
    )
    
    return fig

def create_key_insights(df):
    """Create automatic key insights from data"""
    # Highest revenue category
    category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    top_category = category_sales.idxmax()
    
    # Best performing region
    region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    top_region = region_sales.idxmax()
    
    # Monthly trend
    monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()
    if len(monthly_sales) > 1:
        first_month = monthly_sales.iloc[0]
        last_month = monthly_sales.iloc[-1]
        trend = "📈 Upward" if last_month > first_month else "📉 Downward"
    else:
        trend = "➡️ Stable"
    
    insights = [
        f"🏆 Highest Revenue Category: {top_category} (${category_sales.max():,.0f})",
        f"🌍 Best Performing Region: {top_region} (${region_sales.max():,.0f})",
        f"📊 Monthly Sales Trend: {trend}"
    ]
    
    return insights

def main():
    """Main application function"""
    
    # Load data
    df = load_data()
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Sales Analytics Dashboard</h1>
        <p>AI-Powered Insights | Real-time Analytics | Dark Theme</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Filters
    st.sidebar.markdown("## 🔍 Filters")
    
    # Region Filter
    st.sidebar.markdown("### 🗺️ Region")
    all_regions = sorted(df['Region'].unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Select Region(s)",
        options=all_regions,
        default=all_regions
    )
    
    # Category Filter
    st.sidebar.markdown("### 🏷️ Category")
    all_categories = sorted(df['Category'].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Select Category",
        options=all_categories,
        default=all_categories
    )
    
    # Segment Filter
    st.sidebar.markdown("### 👥 Segment")
    all_segments = sorted(df['Segment'].unique().tolist())
    selected_segments = st.sidebar.multiselect(
        "Select Segment",
        options=all_segments,
        default=all_segments
    )
    
    # Date Filter - Last 12 months or custom
    st.sidebar.markdown("### 📅 Date Range")
    min_date = df['Order Date'].min().date()
    max_date = df['Order Date'].max().date()
    
    # Quick date filter options
    date_option = st.sidebar.radio(
        "Select Period",
        ["All Time", "Last 12 Months", "Custom Range"],
        index=0
    )
    
    if date_option == "Last 12 Months":
        # Calculate 12 months back from max date
        from dateutil.relativedelta import relativedelta
        start_date = (max_date - relativedelta(months=12)).replace(day=1)
    elif date_option == "Custom Range":
        col_date1, col_date2 = st.sidebar.columns(2)
        with col_date1:
            start_date = st.date_input("From", value=min_date, min_value=min_date, max_value=max_date)
        with col_date2:
            end_date = st.date_input("To", value=max_date, min_value=min_date, max_value=max_date)
    else:
        start_date = min_date
        end_date = max_date
    
    # Reset Filters button
    if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
        st.rerun()
    
    # Apply Filters
    df_filtered = df[
        (df['Region'].isin(selected_regions)) &
        (df['Category'].isin(selected_categories)) &
        (df['Segment'].isin(selected_segments)) &
        (df['Order Date'].dt.date >= start_date) &
        (df['Order Date'].dt.date <= end_date)
    ].copy()
    
    # Check if data exists after filtering
    if df_filtered.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
        st.stop()
    
    # KPI Summary Cards
    st.markdown("### 📊 KPI Summary")
    metrics = calculate_metrics(df_filtered)
    create_kpi_cards(metrics)
    
    # Sales Analysis Charts
    st.markdown("### 📈 Sales Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_category = create_sales_by_category_chart(df_filtered)
        st.plotly_chart(fig_category, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_region = create_sales_by_region_chart(df_filtered)
        st.plotly_chart(fig_region, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Trend Analysis
    st.markdown("### 📉 Trend Analysis")
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_trend = create_monthly_sales_trend(df_filtered)
    st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Product Performance
    st.markdown("### 🏆 Product Performance")
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig_top = create_top_products_chart(df_filtered)
    st.plotly_chart(fig_top, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Insights Section
    st.markdown("### 💡 Key Insights")
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    insights = create_key_insights(df_filtered)
    for insight in insights:
        st.markdown(f"• {insight}")
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
