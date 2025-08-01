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
        st.header("🎛️ Quick Stats")
        
        # Display quick stats in sidebar
        if st.session_state.cells_data:
            st.metric("Total Cells", len(st.session_state.cells_data))
            avg_temp = sum(cell['temp'] for cell in st.session_state.cells_data.values()) / len(st.session_state.cells_data)
            st.metric("Avg Temperature", f"{avg_temp:.1f}°C")
            total_capacity = sum(cell['capacity'] for cell in st.session_state.cells_data.values())
            st.metric("Total Capacity", f"{total_capacity:.2f}Wh")
        
        if st.session_state.tasks_data:
            st.metric("Active Tasks", len(st.session_state.tasks_data))
        
        st.markdown("---")
        st.markdown("### 🔄 System Status")
        if st.session_state.cells_data or st.session_state.tasks_data:
            st.success("System Active")
        else:
            st.info("System Ready")
    
    # Initialize page state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    
    # Main navigation based on current page
    if st.session_state.current_page == "home":
        home_page()
    elif st.session_state.current_page == "cell_config":
        cell_configuration_page()
    elif st.session_state.current_page == "task_management":
        task_management_page()
    elif st.session_state.current_page == "dashboard":
        dashboard_page()
    elif st.session_state.current_page == "data_viz":
        data_visualization_page()

def home_page():
    """Main home page with navigation cards"""
    
    # Welcome section
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #4a5568; margin-bottom: 1rem;">Welcome to Battery Management System</h2>
        <p style="font-size: 1.1rem; color: #718096;">Choose an option below to get started with your battery management tasks</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation cards
    col1, col2 = st.columns(2)
    
    with col1:
        # Cell Configuration Card
        st.markdown("""
        <div class="nav-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; text-align: center; box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);">
            <h3 style="margin-bottom: 1rem;">⚡ Cell Configuration</h3>
            <p style="margin-bottom: 1.5rem; opacity: 0.9;">Set up and configure your battery cells with different types and parameters</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔋 Configure Cells", key="nav_cells", use_container_width=True, type="primary"):
            st.session_state.current_page = "cell_config"
            st.rerun()
        
        # Task Management Card
        st.markdown("""
        <div class="nav-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; text-align: center; box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);">
            <h3 style="margin-bottom: 1rem;">📋 Task Management</h3>
            <p style="margin-bottom: 1.5rem; opacity: 0.9;">Create and manage tasks like CC_CV, IDLE, and CC_CD operations</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Manage Tasks", key="nav_tasks", use_container_width=True, type="primary"):
            st.session_state.current_page = "task_management"
            st.rerun()
    
    with col2:
        # Dashboard Card
        st.markdown("""
        <div class="nav-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; text-align: center; box-shadow: 0 8px 32px rgba(79, 172, 254, 0.3);">
            <h3 style="margin-bottom: 1rem;">📊 System Dashboard</h3>
            <p style="margin-bottom: 1.5rem; opacity: 0.9;">View system overview, metrics, and monitor your battery cells</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📈 View Dashboard", key="nav_dashboard", use_container_width=True, type="primary"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        # Data Visualization Card
        st.markdown("""
        <div class="nav-card" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; text-align: center; box-shadow: 0 8px 32px rgba(250, 112, 154, 0.3);">
            <h3 style="margin-bottom: 1rem;">📈 Data Visualization</h3>
            <p style="margin-bottom: 1.5rem; opacity: 0.9;">Analyze data with interactive charts and visual representations</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Visualize Data", key="nav_dataviz", use_container_width=True, type="primary"):
            st.session_state.current_page = "data_viz"
            st.rerun()
    
    # Quick Actions Section
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    action_col1, action_col2, action_col3, action_col4 = st.columns(4)
    
    with action_col1:
        if st.button("⚡ Quick Cell Setup", use_container_width=True):
            # Quick setup with default values
            st.session_state.cells_data = {}
            for i in range(3):
                cell_type = "lfp" if i % 2 == 0 else "li-ion"
                cell_key = f"cell_{i+1}_{cell_type}"
                st.session_state.cells_data[cell_key] = create_cell_data(cell_type, i+1)
            st.success("✅ 3 cells created with default settings!")
            time.sleep(1)
            st.rerun()
    
    with action_col2:
        if st.button("📋 Sample Tasks", use_container_width=True):
            # Create sample tasks
            st.session_state.tasks_data = {
                "task_1": {"task_type": "CC_CV", "cc_cp": "5A", "cv_voltage": 3.6, "current": 2.0, "capacity": 100.0, "time_seconds": 3600},
                "task_2": {"task_type": "IDLE", "time_seconds": 1800},
                "task_3": {"task_type": "CC_CD", "cc_cp": "3A", "voltage": 3.2, "capacity": 80.0, "time_seconds": 2400}
            }
            st.success("✅ 3 sample tasks created!")
            time.sleep(1)
            st.rerun()
    
    with action_col3:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            st.session_state.cells_data = {}
            st.session_state.tasks_data = {}
            st.success("✅ All data cleared!")
            time.sleep(1)
            st.rerun()
    
    with action_col4:
        if st.button("🔄 Refresh Data", use_container_width=True):
            # Refresh cell data with new random values
            for cell_key, cell_data in st.session_state.cells_data.items():
                cell_type = "lfp" if "lfp" in cell_key else "li-ion"
                idx = int(cell_key.split('_')[1])
                st.session_state.cells_data[cell_key] = create_cell_data(cell_type, idx)
            st.success("✅ Cell data refreshed!")
            time.sleep(1)
            st.rerun()
    
    # System Status Overview
    if st.session_state.cells_data or st.session_state.tasks_data:
        st.markdown("---")
        st.subheader("🎯 Current System Status")
        
        status_col1, status_col2, status_col3 = st.columns(3)
        
        with status_col1:
            st.info(f"🔋 **Cells:** {len(st.session_state.cells_data)} configured")
        
        with status_col2:
            st.info(f"📋 **Tasks:** {len(st.session_state.tasks_data)} active")
        
        with status_col3:
            if st.session_state.cells_data and st.session_state.tasks_data:
                st.success("✅ **System:** Ready for operation")
            elif st.session_state.cells_data or st.session_state.tasks_data:
                st.warning("⚠️ **System:** Partially configured")
            else:
                st.info("ℹ️ **System:** Awaiting configuration")
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
    # Back to home button
    if st.button("🏠 Back to Home", key="back_from_tasks"):
        st.session_state.current_page = "home"
        st.rerun()
    
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
    # Back to home button
    if st.button("🏠 Back to Home", key="back_from_dashboard"):
        st.session_state.current_page = "home"
        st.rerun()
    
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
    # Back to home button
    if st.button("🏠 Back to Home", key="back_from_dataviz"):
        st.session_state.current_page = "home"
        st.rerun()
    
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
