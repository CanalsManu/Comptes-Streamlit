import streamlit as st

testA, testB = st.tabs(['Test A', 'Test B'], on_change='rerun')

testA.write('Hola, test A')
testB.write('Hola, test B')