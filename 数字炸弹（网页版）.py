import random
import streamlit as st

# 初始化全局变量
if 'bomb' not in st.session_state:
    st.session_state.bomb = random.randint(1, 99)
if 'start' not in st.session_state:
    st.session_state.start = 0
if 'end' not in st.session_state:
    st.session_state.end = 99
if 'message' not in st.session_state:
    st.session_state.message = ''

st.title("猜数字游戏")

st.write("请输入一个数字在{}到{}之间:".format(st.session_state.start, st.session_state.end))

# 玩家输入
people = st.number_input("Waoji的数字", min_value=st.session_state.start, max_value=st.session_state.end, step=1)

if st.button('提交'):
    if people > st.session_state.bomb:
        st.session_state.message = '大了'
        st.session_state.end = people
    elif people < st.session_state.bomb:
        st.session_state.message = '小了'
        st.session_state.start = people
    else:
        st.session_state.message = 'BOOM!!!'
        st.session_state.bomb = random.randint(1, 99)
        st.session_state.start = 0
        st.session_state.end = 99
    st.experimental_rerun()

st.write(st.session_state.message)

# 电脑输入
if st.session_state.message != 'BOOM!!!':
    st.write('等待靓女输入{}到{}之间的数...'.format(st.session_state.start, st.session_state.end))
    com = random.randint(st.session_state.start + 1, st.session_state.end - 1)
    st.write('靓女：{}'.format(com))
    if com > st.session_state.bomb:
        st.write('大了')
        st.session_state.end = com
    elif com < st.session_state.bomb:
        st.write('小了')
        st.session_state.start = com
    else:
        st.write('BOOM!!!')
        st.session_state.bomb = random.randint(1, 99)
        st.session_state.start = 0
        st.session_state.end = 99

