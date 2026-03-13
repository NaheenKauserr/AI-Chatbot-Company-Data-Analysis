
"""
Sales Analytics Dashboard
A professional analytics dashboard for sales data visualization and insights
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

# Custom CSS for Professional Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem !important;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .kpi-card-title {
        color: #666;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .kpi-card-value {
        color: #1e3c72;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .kpi-card-delta {
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    
    /* Chart Containers */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        color: #1e3c72;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    /* Insight Boxes */
    .insight-box {
        background: linear-gradient(135deg, #e8f4fd 0%, #d4e9f7 100%);
        border-left: 4px solid #2a5298;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        color: #1e3c72;
    }
    
    .insight-box h4 {
        color: #1e3c72;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Data Table */
    .data-table-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Sidebar */
    .sidebar-title {
        color: #1e3c72;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Metrics Colors */
    .metric-sales { border-left-color: #28a745 !important; }
    .metric-profit { border-left-color: #17a2b8 !important; }
    .metric-orders { border-left-color: #ffc107 !important; }
    .metric-aov { border-left-color: #6f42c1 !important; }
    
    /* Positive/Negative Deltas */
    .delta-positive { color: #28a745; }
    .delta-negative { color: #dc3545; }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    return {
        'total_sales': total_sales,
        'total_profit': total_profit,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value
    }

def create_kpi_cards(metrics, prev_metrics=None):
    """Create professional KPI cards"""
    
    # Calculate deltas if previous period data available
    if prev_metrics:
        sales_delta = ((metrics['total_sales'] - prev_metrics['total_sales']) / prev_metrics['total_sales']) * 100
        profit_delta = ((metrics['total_profit'] - prev_metrics['total_profit']) / prev_metrics['total_profit']) * 100
        orders_delta = ((metrics['total_orders'] - prev_metrics['total_orders']) / prev_metrics['total_orders']) * 100
        aov_delta = ((metrics['avg_order_value'] - prev_metrics['avg_order_value']) / prev_metrics['avg_order_value']) * 100
    else:
        sales_delta = profit_delta = orders_delta = aov_delta = 0
    
    # Create columns for KPI cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card metric-sales">
            <div class="kpi-card-title">💰 Total Sales</div>
            <div class="kpi-card-value">${metrics['total_sales']:,.0f}</div>
            <div class="kpi-card-delta delta-positive">📈 +{sales_delta:.1f}% vs last period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card metric-profit">
            <div class="kpi-card-title">💵 Total Profit</div>
            <div class="kpi-card-value">${metrics['total_profit']:,.0f}</div>
            <div class="kpi-card-delta {'delta-positive' if profit_delta >= 0 else 'delta-negative'}">
                {'📈 +' if profit_delta >= 0 else '📉 '}{profit_delta:.1f}% vs last period
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card metric-orders">
            <div class="kpi-card-title">📦 Total Orders</div>
            <div class="kpi-card-value">{metrics['total_orders']:,}</div>
            <div class="kpi-card-delta delta-positive">📈 +{orders_delta:.1f}% vs last period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card metric-aov">
            <div class="kpi-card-title">📊 Avg Order Value</div>
            <div class="kpi-card-value">${metrics['avg_order_value']:,.2f}</div>
            <div class="kpi-card-delta {'delta-positive' if aov_delta >= 0 else 'delta-negative'}">
                {'📈 +' if aov_delta >= 0 else '📉 '}{aov_delta:.1f}% vs last period
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_sales_trend_chart(df):
    """Create sales trend over time line chart"""
    # Aggregate by month
    monthly_sales = df.groupby(df['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly_sales['Order Date'] = monthly_sales['Order Date'].astype(str)
    
    # Create line chart
    fig = px.line(
        monthly_sales,
        x='Order Date',
        y='Sales',
        title='📈 Sales Trend Over Time',
        markers=True,
        line_shape='spline'
    )
    
    fig.update_traces(
        line_color='#1e3c72',
        line_width=3,
        marker=dict(size=8, color='#2a5298', symbol='diamond')
    )
    
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Sales ($)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter'),
        hovermode='x unified',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
    )
    
    return fig

def create_sales_by_region_chart(df):
    """Create sales by region bar chart"""
    region_sales = df.groupby('Region')['Sales'].sum().reset_index()
    region_sales = region_sales.sort_values('Sales', ascending=True)
    
    # Color mapping for regions
    colors = {'North': '#1e3c72', 'South': '#28a745', 'East': '#ffc107', 'West': '#dc3545'}
    
    fig = px.bar(
        region_sales,
        x='Sales',
        y='Region',
        orientation='h',
        title='🏢 Sales by Region',
        text='Sales',
        color='Region',
        color_discrete_map=colors
    )
    
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    
    fig.update_layout(
        xaxis_title='Sales ($)',
        yaxis_title='Region',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter'),
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=False)
    )
    
    return fig

def create_sales_by_category_chart(df):
    """Create sales by category donut chart"""
    category_sales = df.groupby('Category')['Sales'].sum().reset_index()
    
    fig = px.pie(
        category_sales,
        values='Sales',
        names='Category',
        title='🍩 Sales by Category',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        paper_bgcolor='white',
        font=dict(family='Inter'),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2)
    )
    
    return fig

def create_profit_by_region_chart(df):
    """Create profit by region bar chart"""
    region_profit = df.groupby('Region')['Profit'].sum().reset_index()
    region_profit = region_profit.sort_values('Profit', ascending=True)
    
    # Color based on profit (green for positive, red for negative)
    colors = ['#dc3545' if x < 0 else '#28a745' for x in region_profit['Profit']]
    
    fig = px.bar(
        region_profit,
        x='Profit',
        y='Region',
        orientation='h',
        title='💰 Profit by Region',
        text='Profit',
        color='Profit',
        color_continuous_scale=['#dc3545', '#28a745']
    )
    
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    
    fig.update_layout(
        xaxis_title='Profit ($)',
        yaxis_title='Region',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter'),
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=False)
    )
    
    return fig

def create_top_products_chart(df):
    """Create top 10 products by sales horizontal bar chart"""
    top_products = df.groupby('Product Name')['Sales'].sum().reset_index()
    top_products = top_products.nlargest(10, 'Sales')
    top_products = top_products.sort_values('Sales', ascending=True)
    
    # Truncate long product names
    top_products['Product Name'] = top_products['Product Name'].apply(
        lambda x: x[:40] + '...' if len(x) > 40 else x
    )
    
    fig = px.bar(
        top_products,
        x='Sales',
        y='Product Name',
        orientation='h',
        title='🏆 Top 10 Products by Sales',
        text='Sales',
        color='Sales',
        color_continuous_scale='Viridis'
    )
    
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    
    fig.update_layout(
        xaxis_title='Sales ($)',
        yaxis_title='Product',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=10),
        showlegend=False,
        height=400,
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=False)
    )
    
    return fig

def create_top_products_table(df):
    """Create data table for top products"""
    top_products = df.groupby(['Product Name', 'Category', 'Region']).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    top_products = top_products.nlargest(15, 'Sales')
    top_products = top_products.sort_values('Sales', ascending=False)
    
    # Format columns
    top_products['Sales'] = top_products['Sales'].apply(lambda x: f"${x:,.2f}")
    top_products['Profit'] = top_products['Profit'].apply(lambda x: f"${x:,.2f}")
    
    return top_products

def create_insight_box(title, insights):
    """Create styled insight box"""
    insight_html = f"""
    <div class="insight-box">
        <h4>💡 {title}</h4>
        <ul>
    """
    for insight in insights:
        insight_html += f"<li>{insight}</li>"
    insight_html += "</ul></div>"
    
    return insight_html

def main():
    """Main application function"""
    
    # Load data
    df = load_data()
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Sales Analytics Dashboard</h1>
        <p>Comprehensive insights into sales performance, regional analysis, and product trends</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Filters
    st.sidebar.markdown('<div class="sidebar-title">🔍 Interactive Filters</div>', unsafe_allow_html=True)
    
    # Make sidebar wider
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        min-width: 350px;
        max-width: 350px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Region Filter
    st.sidebar.markdown("### 🗺️ Region Filter")
    all_regions = sorted(df['Region'].unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Select Region(s)",
        options=all_regions,
        default=all_regions,
        help="Filter by geographic region"
    )
    
    # Category Filter
    st.sidebar.markdown("### 🏷️ Category Filter")
    all_categories = sorted(df['Category'].unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Select Category",
        options=all_categories,
        default=all_categories,
        help="Filter by product category"
    )
    
    # Date Filter
    st.sidebar.markdown("### 📅 Date Range Filter")
    min_date = df['Order Date'].min().date()
    max_date = df['Order Date'].max().date()
    
    col_date1, col_date2 = st.sidebar.columns(2)
    with col_date1:
        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            help="Filter orders from this date"
        )
    with col_date2:
        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            help="Filter orders until this date"
        )
    
    # Apply Filters
    df_filtered = df[
        (df['Region'].isin(selected_regions)) &
        (df['Category'].isin(selected_categories)) &
        (df['Order Date'].dt.date >= start_date) &
        (df['Order Date'].dt.date <= end_date)
    ].copy()
    
    # Check if data exists after filtering
    if df_filtered.empty:
        st.warning("⚠️ No data matches the selected filters. Please adjust your filter criteria.")
        st.stop()
    
    # Calculate and Display KPI Cards
    st.markdown("### 📊 Key Performance Indicators")
    metrics = calculate_metrics(df_filtered)
    create_kpi_cards(metrics)
    
    # Sales Trend and Region Analysis Row
    st.markdown("### 📈 Sales Analysis")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_trend = create_sales_trend_chart(df_filtered)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Insight for Sales Trend
        monthly_sales = df_filtered.groupby(df_filtered['Order Date'].dt.to_period('M'))['Sales'].sum()
        if len(monthly_sales) > 1:
            first_month = monthly_sales.iloc[0]
            last_month = monthly_sales.iloc[-1]
            trend_direction = "upward" if last_month > first_month else "downward"
            growth_rate = ((last_month - first_month) / first_month) * 100
            
            insights = [
                f"Sales show a {trend_direction} trend over the selected period",
                f"Growth rate: {abs(growth_rate):.1f}% from first to last month",
                f"Average monthly sales: ${monthly_sales.mean():,.0f}"
            ]
            st.markdown(create_insight_box("Sales Trend Insights", insights), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_region = create_sales_by_region_chart(df_filtered)
        st.plotly_chart(fig_region, use_container_width=True)
        
        # Insight for Sales by Region
        region_sales = df_filtered.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        best_region = region_sales.idxmax()
        worst_region = region_sales.idxmin()
        
        insights = [
            f"Top performing region: {best_region} (${region_sales[best_region]:,.0f})",
            f"Region needing attention: {worst_region} (${region_sales[worst_region]:,.0f})",
            f"Performance gap: ${region_sales[best_region] - region_sales[worst_region]:,.0f}"
        ]
        st.markdown(create_insight_box("Regional Insights", insights), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Category and Profit Analysis Row
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_category = create_sales_by_category_chart(df_filtered)
        st.plotly_chart(fig_category, use_container_width=True)
        
        # Insight for Category
        category_sales = df_filtered.groupby('Category')['Sales'].sum().sort_values(ascending=False)
        
        insights = [
            f"Highest revenue category: {category_sales.idxmax()} (${category_sales.max():,.0f})",
            f"Revenue distribution shows category preferences",
            f"Consider focusing marketing on top categories"
        ]
        st.markdown(create_insight_box("Category Insights", insights), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_profit = create_profit_by_region_chart(df_filtered)
        st.plotly_chart(fig_profit, use_container_width=True)
        
        # Insight for Profit by Region
        region_profit = df_filtered.groupby('Region')['Profit'].sum()
        profitable_regions = region_profit[region_profit > 0]
        unprofitable_regions = region_profit[region_profit <= 0]
        
        insights = []
        profitable_profit_val = 0
        if len(profitable_regions) > 0:
            profitable_profit_val = profitable_regions.max()
            insights.append(f"Most profitable region: {profitable_regions.idxmax()} (${profitable_profit_val:,.0f})")
        if len(unprofitable_regions) > 0:
            insights.append(f"Regions with losses: {', '.join(unprofitable_regions.index.tolist())}")
            insights.append(f"Total loss: ${abs(unprofitable_regions.sum()):,.0f}")
        insights.append(f"Overall profit margin: {(region_profit.sum() / df_filtered['Sales'].sum() * 100):.1f}%")
        
        st.markdown(create_insight_box("Profitability Insights", insights), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Top Products Section
    st.markdown("### 🏆 Top Products Analysis")
    
    col5, col6 = st.columns([2, 1])
    
    with col5:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_top = create_top_products_chart(df_filtered)
        st.plotly_chart(fig_top, use_container_width=True)
        
        # Insight for Top Products
        top_products = df_filtered.groupby('Product Name')['Sales'].sum().nlargest(3)
        
        insights = [
            f"Best selling product: {list(top_products.index)[0][:30]}...",
            f"Top 3 products generate {top_products.sum():,.0f} in sales",
            f"Consider cross-selling opportunities with top products"
        ]
        st.markdown(create_insight_box("Product Performance Insights", insights), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col6:
        st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📋 Top Products Data Table</div>', unsafe_allow_html=True)
        
        top_table = create_top_products_table(df_filtered)
        
        # Display table with formatting
        st.dataframe(
            top_table,
            column_config={
                "Product Name": st.column_config.TextColumn("Product Name", width="medium"),
                "Category": st.column_config.TextColumn("Category", width="small"),
                "Region": st.column_config.TextColumn("Region", width="small"),
                "Sales": st.column_config.TextColumn("Sales", width="small"),
                "Profit": st.column_config.TextColumn("Profit", width="small")
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Summary Statistics
    st.markdown("### 📊 Summary Statistics")
    
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Category breakdown
        cat_stats = df_filtered.groupby('Category').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Quantity': 'sum'
        }).round(2)
        
        fig_cat_summary = px.bar(
            cat_stats.reset_index(),
            x='Category',
            y='Sales',
            title='Sales by Category',
            color='Category',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig_cat_summary.update_layout(
            xaxis_title='Category',
            yaxis_title='Sales ($)',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=10),
            showlegend=False
        )
        
        st.plotly_chart(fig_cat_summary, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col8:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Regional breakdown
        reg_stats = df_filtered.groupby('Region').agg({
            'Sales': 'sum',
            'Profit': 'sum',
            'Order ID': 'nunique'
        }).reset_index()
        reg_stats.columns = ['Region', 'Sales', 'Profit', 'Orders']
        
        fig_reg_summary = px.scatter(
            reg_stats,
            x='Sales',
            y='Profit',
            size='Orders',
            color='Region',
            title='Sales vs Profit by Region',
            color_discrete_sequence=['#1e3c72', '#28a745', '#ffc107', '#dc3545']
        )
        
        fig_reg_summary.update_layout(
            xaxis_title='Sales ($)',
            yaxis_title='Profit ($)',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=10)
        )
        
        st.plotly_chart(fig_reg_summary, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col9:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Monthly profit trend
        monthly_profit = df_filtered.groupby(df_filtered['Order Date'].dt.to_period('M')).agg({
            'Profit': 'sum'
        }).reset_index()
        monthly_profit['Order Date'] = monthly_profit['Order Date'].astype(str)
        
        fig_profit_trend = px.bar(
            monthly_profit,
            x='Order Date',
            y='Profit',
            title='Monthly Profit Trend',
            color='Profit',
            color_continuous_scale=['#dc3545', '#ffc107', '#28a745']
        )
        
        fig_profit_trend.update_layout(
            xaxis_title='Month',
            yaxis_title='Profit ($)',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=10),
            showlegend=False
        )
        
        st.plotly_chart(fig_profit_trend, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>📊 Sales Analytics Dashboard | Built with Streamlit, Pandas, and Plotly</p>
        <p style="font-size: 0.8rem;">Data covers period from {} to {}</p>
    </div>
    """.format(min_date.strftime('%B %d, %Y'), max_date.strftime('%B %d, %Y')), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
