import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Battery Cell Dashboard",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
    
    .status-charging {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-discharging {
        color: #dc3545;
        font-weight: bold;
    }
    
    .status-idle {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'charging_history' not in st.session_state:
    st.session_state.charging_history = {}
if 'cell_status' not in st.session_state:
    st.session_state.cell_status = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>🔋 Battery Cell Management Dashboard</h1>
    <p>Advanced Battery Cell Monitoring, Analysis & Control System</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for cell input
st.sidebar.header("🔧 Cell Configuration")

# Cell type mapping
cell_types = {
    "lfp": "LFP (Lithium Iron Phosphate)",
    "mnc": "MNC (Manganese Nickel Cobalt)",
    "nca": "NCA (Nickel Cobalt Aluminum)",
    "lto": "LTO (Lithium Titanate)",
    "lco": "LCO (Lithium Cobalt Oxide)"
}

def calculate_cell_params(cell_type, current):
    """Calculate cell parameters based on type and current"""
    voltage = 3.2 if cell_type == "lfp" else 3.6
    max_vol = 3.4 if cell_type == "mnc" else 4.0
    min_vol = 2.8 if cell_type == "lfp" else 3.2
    temp = round(random.uniform(25, 40), 1)
    capacity = round(voltage * current, 2)
    
    return {
        "voltage": voltage,
        "current": current,
        "temp": temp,
        "capacity": capacity,
        "max_voltage": max_vol,
        "min_voltage": min_vol,
        "soc": random.randint(20, 100),  # State of Charge
        "health": random.randint(85, 100),  # Battery Health
        "cycles": random.randint(0, 500),  # Charge cycles
        "cell_type": cell_type
    }

# Cell input form
with st.sidebar.form("cell_form"):
    st.subheader("Add New Cell")
    
    selected_type = st.selectbox(
        "Cell Type",
        options=list(cell_types.keys()),
        format_func=lambda x: cell_types[x]
    )
    
    current_input = st.number_input(
        "Current (A)",
        min_value=0.1,
        max_value=100.0,
        value=1.0,
        step=0.1
    )
    
    submitted = st.form_submit_button("➕ Add Cell")

    if submitted and len(st.session_state.cells_data) < 8:
        cell_count = len(st.session_state.cells_data) + 1
        cell_key = f"cell_{cell_count}_{selected_type}"
        
        st.session_state.cells_data[cell_key] = calculate_cell_params(selected_type, current_input)
        st.session_state.cell_status[cell_key] = "idle"
        st.session_state.charging_history[cell_key] = []
        
        st.success(f"Added {cell_key}")
        st.rerun()

# Clear all cells button
if st.sidebar.button("🗑️ Clear All Cells", type="secondary"):
    st.session_state.cells_data = {}
    st.session_state.charging_history = {}
    st.session_state.cell_status = {}
    st.rerun()

# Display current cell count
st.sidebar.info(f"Cells Added: {len(st.session_state.cells_data)}/8")

# Main dashboard
if st.session_state.cells_data:
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Analytics", "🔋 Charging Control", "📋 Data Table", "🧮 Correlation Matrix"])
    
    with tab1:
        st.header("📊 System Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_cells = len(st.session_state.cells_data)
        avg_voltage = np.mean([cell['voltage'] for cell in st.session_state.cells_data.values()])
        total_capacity = sum([cell['capacity'] for cell in st.session_state.cells_data.values()])
        avg_temp = np.mean([cell['temp'] for cell in st.session_state.cells_data.values()])
        
        col1.metric("Total Cells", total_cells, "Active")
        col2.metric("Avg Voltage", f"{avg_voltage:.2f}V", "Normal")
        col3.metric("Total Capacity", f"{total_capacity:.2f}Wh", "Good")
        col4.metric("Avg Temperature", f"{avg_temp:.1f}°C", "Optimal")
        
        # Cell status overview
        st.subheader("🔋 Cell Status Overview")
        
        cols = st.columns(min(4, len(st.session_state.cells_data)))
        for idx, (cell_key, cell_data) in enumerate(st.session_state.cells_data.items()):
            col = cols[idx % 4]
            
            status = st.session_state.cell_status.get(cell_key, "idle")
            
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{cell_key.upper()}</h4>
                    <p><strong>Type:</strong> {cell_data['cell_type'].upper()}</p>
                    <p><strong>Voltage:</strong> {cell_data['voltage']}V</p>
                    <p><strong>Current:</strong> {cell_data['current']}A</p>
                    <p><strong>SOC:</strong> {cell_data['soc']}%</p>
                    <p class="status-{status}">Status: {status.title()}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Voltage distribution
        st.subheader("⚡ Voltage Distribution")
        
       
        cell_names = list(st.session_state.cells_data.keys())
        voltages = [cell['voltage'] for cell in st.session_state.cells_data.values()]
        
            
            y=voltages,
            marker_color='lightblue',
            name='Current Voltage'
        ))
        
        # Add max voltage line
        max_voltages = [cell['max_voltage'] for cell in st.session_state.cells_data.values()]
        fig_voltage.add_trace(go.Scatter(
            x=cell_names,
            y=max_voltages,
            mode='lines+markers',
            line=dict(color='red', dash='dash'),
            name='Max Voltage'
        ))
        
        fig_voltage.update_layout(
            title="Cell Voltage Comparison",
            xaxis_title="Cell ID",
            yaxis_title="Voltage (V)",
            hovermode='x'
        )
        
        st.plotly_chart(fig_voltage, use_container_width=True)
    
    with tab2:
        st.header("📈 Advanced Analytics")
        
        # Create subplots
        fig_analytics = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Temperature vs Voltage', 'Capacity Distribution', 
                          'State of Charge', 'Battery Health'),
            specs=[[{"secondary_y": False}, {"type": "domain"}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Temperature vs Voltage scatter
        temps = [cell['temp'] for cell in st.session_state.cells_data.values()]
        voltages = [cell['voltage'] for cell in st.session_state.cells_data.values()]
        
        fig_analytics.add_trace(
            go.Scatter(x=temps, y=voltages, mode='markers', 
                      marker=dict(size=10, color='blue'),
                      name='Temp vs Voltage'),
            row=1, col=1
        )
        
        # Capacity pie chart
        cell_names = [key.split('_')[-1] for key in st.session_state.cells_data.keys()]
        capacities = [cell['capacity'] for cell in st.session_state.cells_data.values()]
        
        fig_analytics.add_trace(
            go.Pie(labels=cell_names, values=capacities, name="Capacity"),
            row=1, col=2
        )
        
        # SOC bar chart
        socs = [cell['soc'] for cell in st.session_state.cells_data.values()]
        
        fig_analytics.add_trace(
            go.Bar(x=list(range(len(cell_names))), y=socs, 
                   marker_color='green', name='SOC'),
            row=2, col=1
        )
        
        # Health indicator
        healths = [cell['health'] for cell in st.session_state.cells_data.values()]
        
        fig_analytics.add_trace(
            go.Scatter(x=list(range(len(cell_names))), y=healths,
                      mode='lines+markers', line=dict(color='orange'),
                      name='Health'),
            row=2, col=2
        )
        
        fig_analytics.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig_analytics, use_container_width=True)
        
        # Performance metrics
        st.subheader("⚡ Performance Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Efficiency radar chart
            categories = ['Voltage', 'Capacity', 'Temperature', 'SOC', 'Health']
            
            # Normalize values to 0-100 scale
            norm_voltage = np.mean(voltages) / 4.0 * 100
            norm_capacity = np.mean(capacities) / max(capacities) * 100 if capacities else 0
            norm_temp = (40 - np.mean(temps)) / 15 * 100  # Lower temp is better
            norm_soc = np.mean(socs)
            norm_health = np.mean(healths)
            
            values = [norm_voltage, norm_capacity, norm_temp, norm_soc, norm_health]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='System Performance'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="System Performance Radar"
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            # Cell type distribution
            type_counts = {}
            for cell in st.session_state.cells_data.values():
                cell_type = cell['cell_type']
                type_counts[cell_type] = type_counts.get(cell_type, 0) + 1
            
            fig_types = go.Figure(data=[
                go.Pie(labels=list(type_counts.keys()), 
                       values=list(type_counts.values()),
                       hole=0.3)
            ])
            fig_types.update_layout(title="Cell Type Distribution")
            st.plotly_chart(fig_types, use_container_width=True)
    
    with tab3:
        st.header("🔋 Charging & Discharging Control")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Individual Cell Control")
            
            for cell_key in st.session_state.cells_data.keys():
                with st.expander(f"Control {cell_key.upper()}"):
                    cols = st.columns(4)
                    
                    current_status = st.session_state.cell_status.get(cell_key, "idle")
                    
                    with cols[0]:
                        if st.button(f"🔋 Charge", key=f"charge_{cell_key}"):
                            st.session_state.cell_status[cell_key] = "charging"
                            # Simulate charging by increasing SOC
                            if st.session_state.cells_data[cell_key]['soc'] < 100:
                                st.session_state.cells_data[cell_key]['soc'] = min(100, 
                                    st.session_state.cells_data[cell_key]['soc'] + random.randint(5, 15))
                            st.rerun()
                    
                    with cols[1]:
                        if st.button(f"⚡ Discharge", key=f"discharge_{cell_key}"):
                            st.session_state.cell_status[cell_key] = "discharging"
                            # Simulate discharging by decreasing SOC
                            if st.session_state.cells_data[cell_key]['soc'] > 0:
                                st.session_state.cells_data[cell_key]['soc'] = max(0, 
                                    st.session_state.cells_data[cell_key]['soc'] - random.randint(5, 15))
                            st.rerun()
                    
                    with cols[2]:
                        if st.button(f"⏸️ Stop", key=f"stop_{cell_key}"):
                            st.session_state.cell_status[cell_key] = "idle"
                            st.rerun()
                    
                    with cols[3]:
                        st.write(f"Status: **{current_status}**")
                    
                    # Progress bar for SOC
                    soc = st.session_state.cells_data[cell_key]['soc']
                    st.progress(soc / 100, text=f"SOC: {soc}%")
        
        with col2:
            st.subheader("System Control")
            
            if st.button("🔋 Charge All Cells", type="primary"):
                for cell_key in st.session_state.cells_data.keys():
                    st.session_state.cell_status[cell_key] = "charging"
                    if st.session_state.cells_data[cell_key]['soc'] < 100:
                        st.session_state.cells_data[cell_key]['soc'] = min(100, 
                            st.session_state.cells_data[cell_key]['soc'] + random.randint(5, 15))
                st.rerun()
            
            if st.button("⚡ Discharge All Cells", type="secondary"):
                for cell_key in st.session_state.cells_data.keys():
                    st.session_state.cell_status[cell_key] = "discharging"
                    if st.session_state.cells_data[cell_key]['soc'] > 0:
                        st.session_state.cells_data[cell_key]['soc'] = max(0, 
                            st.session_state.cells_data[cell_key]['soc'] - random.randint(5, 15))
                st.rerun()
            
            if st.button("⏸️ Stop All Operations"):
                for cell_key in st.session_state.cells_data.keys():
                    st.session_state.cell_status[cell_key] = "idle"
                st.rerun()
            
            st.markdown("---")
            
            # System status summary
            st.subheader("System Status")
            charging_count = sum(1 for status in st.session_state.cell_status.values() if status == "charging")
            discharging_count = sum(1 for status in st.session_state.cell_status.values() if status == "discharging")
            idle_count = sum(1 for status in st.session_state.cell_status.values() if status == "idle")
            
            st.metric("Charging", charging_count)
            st.metric("Discharging", discharging_count)
            st.metric("Idle", idle_count)
        
        # Real-time monitoring chart
        st.subheader("📊 Real-time SOC Monitoring")
        
        fig_soc = go.Figure()
        
        for cell_key, cell_data in st.session_state.cells_data.items():
            fig_soc.add_trace(go.Bar(
                x=[cell_key],
                y=[cell_data['soc']],
                name=cell_key,
                text=f"{cell_data['soc']}%",
                textposition='auto'
            ))
        
        fig_soc.update_layout(
            title="State of Charge (SOC) by Cell",
            xaxis_title="Cell ID",
            yaxis_title="SOC (%)",
            yaxis_range=[0, 100],
            showlegend=False
        )
        
        st.plotly_chart(fig_soc, use_container_width=True)
    
    with tab4:
        st.header("📋 Detailed Data Table")
        
        # Convert to DataFrame
        df_data = []
        for cell_key, cell_data in st.session_state.cells_data.items():
            row = {
                'Cell ID': cell_key,
                'Type': cell_data['cell_type'].upper(),
                'Voltage (V)': cell_data['voltage'],
                'Current (A)': cell_data['current'],
                'Temperature (°C)': cell_data['temp'],
                'Capacity (Wh)': cell_data['capacity'],
                'Max Voltage (V)': cell_data['max_voltage'],
                'Min Voltage (V)': cell_data['min_voltage'],
                'SOC (%)': cell_data['soc'],
                'Health (%)': cell_data['health'],
                'Cycles': cell_data['cycles'],
                'Status': st.session_state.cell_status.get(cell_key, 'idle').title()
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        
        # Display table with formatting
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "SOC (%)": st.column_config.ProgressColumn(
                    "SOC (%)",
                    help="State of Charge",
                    min_value=0,
                    max_value=100,
                ),
                "Health (%)": st.column_config.ProgressColumn(
                    "Health (%)",
                    help="Battery Health",
                    min_value=0,
                    max_value=100,
                ),
            }
        )
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"battery_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        
        numeric_cols = ['Voltage (V)', 'Current (A)', 'Temperature (°C)', 
                       'Capacity (Wh)', 'SOC (%)', 'Health (%)']
        
        summary_df = df[numeric_cols].describe()
        st.dataframe(summary_df, use_container_width=True)
    
    with tab5:
        st.header("🧮 Correlation Matrix & Analysis")
        
        # Prepare numeric data for correlation
        numeric_data = []
        for cell_data in st.session_state.cells_data.values():
            numeric_data.append([
                cell_data['voltage'],
                cell_data['current'],
                cell_data['temp'],
                cell_data['capacity'],
                cell_data['soc'],
                cell_data['health'],
                cell_data['cycles']
            ])
        
        if len(numeric_data) > 1:
            # Create correlation matrix
            df_corr = pd.DataFrame(numeric_data, columns=[
                'Voltage', 'Current', 'Temperature', 'Capacity', 
                'SOC', 'Health', 'Cycles'
            ])
            
            corr_matrix = df_corr.corr()
            
            # Heatmap
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Correlation Matrix",
                color_continuous_scale="RdBu_r"
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Pair plot
            st.subheader("📈 Pairwise Relationships")
            
            col1, col2 = st.columns(2)
            
            with col1:
                x_var = st.selectbox("X Variable", df_corr.columns, index=0)
            with col2:
                y_var = st.selectbox("Y Variable", df_corr.columns, index=1)
            
            fig_scatter = px.scatter(
                df_corr, x=x_var, y=y_var,
                title=f"{x_var} vs {y_var}",
                trendline="ols"
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Correlation insights
            st.subheader("🔍 Key Insights")
            
            # Find strongest correlations
            corr_pairs = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    corr_pairs.append({
                        'Variables': f"{corr_matrix.columns[i]} - {corr_matrix.columns[j]}",
                        'Correlation': corr_val
                    })
            
            corr_df = pd.DataFrame(corr_pairs)
            corr_df = corr_df.reindex(corr_df['Correlation'].abs().sort_values(ascending=False).index)
            
            st.write("**Strongest Correlations:**")
            st.dataframe(corr_df.head(10), use_container_width=True)
        
        else:
            st.info("Add more cells to generate correlation analysis (minimum 2 cells required)")

else:
    # Welcome screen
    st.markdown("""
    ## 👋 Welcome to the Battery Cell Dashboard!
    
    This advanced dashboard allows you to:
    
    🔧 **Configure Cells**: Add up to 8 battery cells with different types and specifications
    
    📊 **Monitor Performance**: View real-time metrics, voltage distributions, and system health
    
    📈 **Analyze Data**: Explore correlations, performance metrics, and detailed analytics
    
    🔋 **Control Operations**: Manage charging and discharging operations for individual cells or the entire system
    
    📋 **Export Data**: Download comprehensive reports and data tables
    
    ---
    
    **Get started by adding your first battery cell using the sidebar! →**
    """)
    
    # Demo data button
    if st.button("🚀 Load Demo Data", type="primary"):
        demo_cells = [
            ("lfp", 2.5),
            ("mnc", 3.0),
            ("nca", 2.8),
            ("lto", 1.5),
            ("lfp", 3.2)
        ]
        
        for i, (cell_type, current) in enumerate(demo_cells, 1):
            cell_key = f"cell_{i}_{cell_type}"
            st.session_state.cells_data[cell_key] = calculate_cell_params(cell_type, current)
            st.session_state.cell_status[cell_key] = "idle"
            st.session_state.charging_history[cell_key] = []
        
        st.success("Demo data loaded successfully!")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; opacity: 0.6;'>
    Battery Cell Management Dashboard | Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
