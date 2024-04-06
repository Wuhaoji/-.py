import streamlit as st
import pyodbc
from datetime import datetime

# SQL Server 连接信息
server = '10.0.3.113'
database = 'yy'
username = 'sa'
password = 'jlq@$120606'

# 连接 SQL Server 数据库
def connect_to_sql_server():
    try:
        conn = pyodbc.connect(
            f"DRIVER=ODBC Driver 17 for SQL Server;"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )
        return conn
    except pyodbc.Error as e:
        st.error(f"Error connecting to SQL Server: {e}")
        return None

# 初始化会话状态
if 'updated_stock' not in st.session_state:
    st.session_state.updated_stock = None
    st.session_state.history = []
    st.session_state.undo_last = False

# 初始化药品库存
def load_stock():
    try:
        conn = connect_to_sql_server()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT medicine, quantity FROM medicine_stock")
            stock = {row.medicine: row.quantity for row in cursor.fetchall()}
            conn.close()
            return stock
    except pyodbc.Error as e:
        st.error(f"Error loading stock from SQL Server: {e}")
        return {}

# 加载历史记录
def load_history():
    try:
        conn = connect_to_sql_server()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history")
            history = [f"登记人: {row.registrant}, 病人: {row.name}, 药品: {row.medicine}, 数量: {row.quantity}, 时间: {row.date}" for row in cursor.fetchall()]
            conn.close()
            return history
    except pyodbc.Error as e:
        st.error(f"Error loading history from SQL Server: {e}")
        return []

# 保存药品库存信息
def save_stock(stock):
    try:
        conn = connect_to_sql_server()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicine_stock")
            for medicine, quantity in stock.items():
                cursor.execute("INSERT INTO medicine_stock (medicine, quantity) VALUES (?, ?)", (medicine, quantity))
            conn.commit()
            conn.close()
    except pyodbc.Error as e:
        st.error(f"Error saving stock to SQL Server: {e}")

# 保存历史记录
def save_history(history):
    try:
        conn = connect_to_sql_server()
        if conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history")
            for action in history:
                parts = action.split(', ')
                registrant = parts[0].split(': ')[1]
                name = parts[1].split(': ')[1]
                medicine = parts[2].split(': ')[1]
                quantity = int(parts[3].split(': ')[1])
                date_str = parts[4].split(': ')[1]
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO history (registrant, name, medicine, quantity, date) VALUES (?, ?, ?, ?, ?)", (registrant, name, medicine, quantity, date))
            conn.commit()
            conn.close()
    except pyodbc.Error as e:
        st.error(f"Error saving history to SQL Server: {e}")

# 其余部分保持不变

# 标题
st.title("综合药房临购药品登记表")

# 显示当前库存
st.write("当前库存:")
for medicine, quantity in st.session_state.updated_stock.items():
    st.write(f"{medicine}: {quantity}")

# 后台管理
with st.sidebar:
    if st.text_input("输入后台密码", type="password") == ADMIN_PASSWORD:
        st.subheader("后台管理")
        # 更新库存表单
        update_medicine = st.selectbox("更新药品名称", list(st.session_state.updated_stock.keys()))
        update_quantity = st.number_input("更新数量", min_value=1)

        if st.button("更新库存"):
            update_stock(update_medicine, update_quantity)

        # 新增药品表单
        new_medicine = st.text_input("新增药品名称")
        new_quantity = st.number_input("初始库存数量", min_value=1)

        if st.button("新增药品"):
            add_new_medicine(new_medicine, new_quantity)

        # 删除药品表单
        delete_medicine_name = st.selectbox("删除药品名称", list(st.session_state.updated_stock.keys()))

        if st.button("删除药品"):
            delete_medicine(delete_medicine_name)

        # 删除历史记录表单
        max_delete_history_index = len(st.session_state.history) - 1 if st.session_state.history else 0
        delete_history_index = st.number_input("删除历史记录索引", min_value=0, max_value=max_delete_history_index)

        if st.button("删除历史记录"):
            delete_history_record(delete_history_index)

# 登记表单
st.subheader("登记表")
name = st.text_input("病人姓名")
medicine = st.selectbox("药品名称", list(st.session_state.updated_stock.keys()))
quantity = st.number_input("领取数量", min_value=1)
registrant = st.text_input("登记人")

if st.button("保存"):
    save_info(name, medicine, quantity, registrant)

# 撤销上一步操作
if not st.session_state.undo_last:
    if st.button("撤销上一步操作"):
        undo_last_action()

# 历史记录
st.sidebar.subheader("历史记录")
selected_date = st.date_input("选择查询日期")
for action in st.session_state.history:
    parts = action.split(', ')
    date_str = parts[-1].split(': ')[1]
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
    if selected_date is None or date == selected_date:
        if not action.startswith("已撤销上一步操作"):
            st.sidebar.write(action)

# 实时更新药品信息和数量
st.write("实时更新药品信息和数量:")
for medicine, quantity in st.session_state.updated_stock.items():
    st.write(f"{medicine}: {quantity}")


