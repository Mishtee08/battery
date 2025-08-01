import streamlit as st
import random
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Battery Cell Management System",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        animation: fadeInDown 1s ease-out;
    }
    
    .sub-header {
        font-family: 'Roboto', sans-serif;
        color: #4a5568;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        animation: fadeIn 1.5s ease-out;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        margin: 1rem 0;
        animation: slideInUp 0.8s ease-out;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .task-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
        margin: 1rem 0;
        animation: slideInLeft 0.8s ease-out;
        transition: transform 0.3s ease;
    }
    
    .task-card:hover {
        transform: translateY(-5px);
    }
    
    .success-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f7fafc;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}
if 'tasks_data' not in st.session_state:
    st.session_state.tasks_data = {}
if 'show_success' not in st.session_state:
    st.session_state.show_success = False

def create_cell_data(cell_type, idx):
    """Create cell data based on type"""
    voltage = 3.2 if cell_type == "lfp" else 3.6
    min_voltage = 2.8 if cell_type == "lfp" else 3.2
    max_voltage = 3.6 if cell_type == "lfp" else 4.0
    current = round(random.uniform(0, 5), 2)
    temp = round(random.uniform(25, 40), 1)
    capacity = round(voltage * current, 2)
    
    return {
        "voltage": voltage,
        "current": current,
        "temp": temp,
        "capacity": capacity,
        "min_voltage": min_voltage,
        "max_voltage": max_voltage
    }

def main():
    # Header
    st.markdown('<h1 class="main-header">🔋 Battery Cell Management System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Monitor and manage your battery cells with advanced task scheduling</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")
        page = st.selectbox("Select Page", ["Cell Configuration", "Task Management", "Dashboard", "Data Visualization"])
    
    if page == "Cell Configuration":
        cell_configuration_page()
    elif page == "Task Management":
        task_management_page()
    elif page == "Dashboard":
        dashboard_page()
    elif page == "Data Visualization":
        data_visualization_page()

def cell_configuration_page():
    st.header("⚡ Cell Configuration")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("Add New Cells")
        
        with st.form("cell_form"):
            number_of_cells = st.number_input("Number of Cells", min_value=1, max_value=20, value=1)
            
            cell_configs = []
            for i in range(number_of_cells):
                st.write(f"**Cell {i+1}**")
                cell_type = st.selectbox(f"Cell Type {i+1}", ["lfp", "li-ion"], key=f"cell_type_{i}")
                cell_configs.append(cell_type)
            
            submitted = st.form_submit_button("🚀 Create Cells", type="primary")
            
            if submitted:
                # Clear existing data
                st.session_state.cells_data = {}
                
                # Create new cells
                for idx, cell_type in enumerate(cell_configs, start=1):
                    cell_key = f"cell_{idx}_{cell_type}"
                    st.session_state.cells_data[cell_key] = create_cell_data(cell_type, idx)
                
                st.session_state.show_success = True
                st.success("✅ Cells created successfully!")
                time.sleep(0.5)
                st.rerun()
    
    with col2:
        st.subheader("Current Cells")
        
        if st.session_state.cells_data:
            for cell_key, cell_data in st.session_state.cells_data.items():
                with st.container():
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🔋 {cell_key.replace('_', ' ').title()}</h3>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                            <div><strong>Voltage:</strong> {cell_data['voltage']}V</div>
                            <div><strong>Current:</strong> {cell_data['current']}A</div>
                            <div><strong>Temperature:</strong> {cell_data['temp']}°C</div>
                            <div><strong>Capacity:</strong> {cell_data['capacity']}Wh</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No cells configured yet. Please add some cells using the form on the left.")

def task_management_page():
    st.header("📋 Task Management")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("Create New Task")
        
        with st.form("task_form"):
            task_type = st.selectbox("Task Type", ["CC_CV", "IDLE", "CC_CD"])
            
            task_data = {"task_type": task_type}
            
            if task_type == "CC_CV":
                st.write("**CC_CV Parameters**")
                cc_input = st.text_input("CC/CP Value (e.g., '5A' or '10W')", value="5A")
                cv_voltage = st.number_input("CV Voltage (V)", value=3.6, step=0.1)
                current = st.number_input("Current (A)", value=2.0, step=0.1)
                capacity = st.number_input("Capacity", value=100.0, step=1.0)
                time_seconds = st.number_input("Time (seconds)", value=3600, step=1)
                
                task_data.update({
                    "cc_cp": cc_input,
                    "cv_voltage": cv_voltage,
                    "current": current,
                    "capacity": capacity,
                    "time_seconds": time_seconds
                })
                
            elif task_type == "IDLE":
                st.write("**IDLE Parameters**")
                time_seconds = st.number_input("Time (seconds)", value=1800, step=1)
                task_data["time_seconds"] = time_seconds
                
            elif task_type == "CC_CD":
                st.write("**CC_CD Parameters**")
                cc_input = st.text_input("CC/CP Value (e.g., '5A' or '10W')", value="5A")
                voltage = st.number_input("Voltage (V)", value=3.6, step=0.1)
                capacity = st.number_input("Capacity", value=100.0, step=1.0)
                time_seconds = st.number_input("Time (seconds)", value=3600, step=1)
                
                task_data.update({
                    "cc_cp": cc_input,
                    "voltage": voltage,
                    "capacity": capacity,
                    "time_seconds": time_seconds
                })
            
            submitted = st.form_submit_button("➕ Add Task", type="primary")
            
            if submitted:
                task_key = f"task_{len(st.session_state.tasks_data) + 1}"
                st.session_state.tasks_data[task_key] = task_data
                st.success(f"✅ Task {task_key} added successfully!")
                time.sleep(0.5)
                st.rerun()
    
    with col2:
        st.subheader("Active Tasks")
        
        if st.session_state.tasks_data:
            for task_key, task_data in st.session_state.tasks_data.items():
                with st.container():
                    task_type = task_data.get("task_type", "Unknown")
                    
                    # Create task card content
                    task_content = f"<h3>📋 {task_key.replace('_', ' ').title()}</h3>"
                    task_content += f"<div><strong>Type:</strong> {task_type}</div>"
                    
                    if task_type == "CC_CV":
                        task_content += f"""
                        <div style="margin-top: 1rem;">
                            <strong>CC/CP:</strong> {task_data.get('cc_cp', 'N/A')}<br>
                            <strong>CV Voltage:</strong> {task_data.get('cv_voltage', 'N/A')}V<br>
                            <strong>Current:</strong> {task_data.get('current', 'N/A')}A<br>
                            <strong>Time:</strong> {task_data.get('time_seconds', 'N/A')}s
                        </div>
                        """
                    elif task_type == "IDLE":
                        task_content += f"""
                        <div style="margin-top: 1rem;">
                            <strong>Time:</strong> {task_data.get('time_seconds', 'N/A')}s
                        </div>
                        """
                    elif task_type == "CC_CD":
                        task_content += f"""
                        <div style="margin-top: 1rem;">
                            <strong>CC/CP:</strong> {task_data.get('cc_cp', 'N/A')}<br>
                            <strong>Voltage:</strong> {task_data.get('voltage', 'N/A')}V<br>
                            <strong>Capacity:</strong> {task_data.get('capacity', 'N/A')}<br>
                            <strong>Time:</strong> {task_data.get('time_seconds', 'N/A')}s
                        </div>
                        """
                    
                    st.markdown(f'<div class="task-card">{task_content}</div>', unsafe_allow_html=True)
                    
                    # Delete button
                    if st.button(f"🗑️ Delete {task_key}", key=f"delete_{task_key}"):
                        del st.session_state.tasks_data[task_key]
                        st.rerun()
        else:
            st.info("No tasks created yet. Please add some tasks using the form on the left.")

def dashboard_page():
    st.header("📊 System Dashboard")
    
    if not st.session_state.cells_data and not st.session_state.tasks_data:
        st.warning("Please configure cells and tasks first to view the dashboard.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cells", len(st.session_state.cells_data))
    
    with col2:
        st.metric("Active Tasks", len(st.session_state.tasks_data))
    
    with col3:
        if st.session_state.cells_data:
            avg_temp = sum(cell['temp'] for cell in st.session_state.cells_data.values()) / len(st.session_state.cells_data)
            st.metric("Avg Temperature", f"{avg_temp:.1f}°C")
    
    with col4:
        if st.session_state.cells_data:
            total_capacity = sum(cell['capacity'] for cell in st.session_state.cells_data.values())
            st.metric("Total Capacity", f"{total_capacity:.2f}Wh")
    
    # Cell status table
    if st.session_state.cells_data:
        st.subheader("🔋 Cell Status Overview")
        
        cell_df = pd.DataFrame.from_dict(st.session_state.cells_data, orient='index')
        cell_df.index.name = 'Cell ID'
        st.dataframe(cell_df, use_container_width=True)
    
    # Task summary
    if st.session_state.tasks_data:
        st.subheader("📋 Task Summary")
        
        task_types = [task['task_type'] for task in st.session_state.tasks_data.values()]
        task_counts = pd.Series(task_types).value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.bar_chart(task_counts)
        
        with col2:
            st.write("**Task Distribution:**")
            for task_type, count in task_counts.items():
                st.write(f"- {task_type}: {count} tasks")

def data_visualization_page():
    st.header("📈 Data Visualization")
    
    if not st.session_state.cells_data:
        st.warning("Please configure cells first to view visualizations.")
        return
    
    # Cell data visualization
    cell_df = pd.DataFrame.from_dict(st.session_state.cells_data, orient='index')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌡️ Temperature Distribution")
        fig_temp = px.bar(
            x=cell_df.index,
            y=cell_df['temp'],
            title="Cell Temperature",
            labels={'x': 'Cell ID', 'y': 'Temperature (°C)'},
            color=cell_df['temp'],
            color_continuous_scale='viridis'
        )
        fig_temp.update_layout(showlegend=False)
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Voltage vs Current")
        fig_scatter = px.scatter(
            cell_df,
            x='voltage',
            y='current',
            size='capacity',
            hover_name=cell_df.index,
            title="Voltage vs Current (Size: Capacity)",
            labels={'voltage': 'Voltage (V)', 'current': 'Current (A)'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Multi-metric comparison
    st.subheader("📊 Multi-Metric Comparison")
    
    metrics = st.multiselect(
        "Select metrics to compare:",
        ['voltage', 'current', 'temp', 'capacity'],
        default=['voltage', 'current']
    )
    
    if metrics:
        fig_multi = make_subplots(
            rows=len(metrics), cols=1,
            subplot_titles=metrics,
            vertical_spacing=0.1
        )
        
        for i, metric in enumerate(metrics, 1):
            fig_multi.add_trace(
                go.Bar(x=cell_df.index, y=cell_df[metric], name=metric),
                row=i, col=1
            )
        
        fig_multi.update_layout(height=200*len(metrics), showlegend=False)
        st.plotly_chart(fig_multi, use_container_width=True)

if __name__ == "__main__":
    main()
