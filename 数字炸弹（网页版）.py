import random
import streamlit as st

# 初始化炸弹的数字
if 'bomb' not in st.session_state:
    st.session_state.bomb = random.randint(1, 99)

# 初始化范围
if 'start' not in st.session_state:
    st.session_state.start = 0
if 'end' not in st.session_state:
    st.session_state.end = 99

# 初始化记录
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("数字炸弹游戏")

# 显示当前范围和输入框
st.write(f'请输入 {st.session_state.start} 到 {st.session_state.end} 之间的数:')
people_input = st.text_input('你的输入:', '')

# 按钮提交
if st.button('提交'):
    try:
        people = int(people_input)
        if st.session_state.start < people < st.session_state.end:
            st.session_state.history.append(f'你输入: {people}')
            if people > st.session_state.bomb:
                st.write('大了')
                st.session_state.end = people
            elif people < st.session_state.bomb:
                st.write('小了')
                st.session_state.start = people
            else:
                st.write('BOOM!!! 靓女赢了!')
                st.session_state.history.append('靓女赢了!')
                st.stop()  # 结束游戏

            # 电脑输入
            if st.session_state.start + 1 < st.session_state.end:
                st.write(f'等待靓女输入 {st.session_state.start} 到 {st.session_state.end} 之间的数...')
                com = random.randint(st.session_state.start + 1, st.session_state.end - 1)
                st.write(f'靓女输入：{com}')
                st.session_state.history.append(f'电脑输入: {com}')
                if com > st.session_state.bomb:
                    st.write('大了')
                    st.session_state.end = com
                elif com < st.session_state.bomb:
                    st.write('小了')
                    st.session_state.start = com
                else:
                    st.write('BOOM!!! you赢了!')
                    st.session_state.history.append('you赢了!')
                    st.stop()  # 结束游戏

            st.write(f'请输入 {st.session_state.start} 到 {st.session_state.end} 之间的数:')        
        else:
            st.write(f'请输入一个在 {st.session_state.start} 到 {st.session_state.end} 范围内的数')
    except ValueError:
        st.write('请输入有效的数字')

# 显示历史记录
st.write("历史记录:")
for record in st.session_state.history:
    st.write(record)
