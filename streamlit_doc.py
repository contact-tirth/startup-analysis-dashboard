st.title('Startup Dashboard')


st.header('Jay Swaminarayan')

st.markdown(""""
### This is Markdown.
- Point 1
""")

st.code('SELECT * FROM Application A')

a = st.latex('X^2 + Y^2 = Z^2')

st.sidebar.latex('X^2 + Y^2 = Z^2')

a1,a2 = st.columns(2)
with a1:
    st.code('SELECT * FROM Application A')
with a2:
    st.header('Jay Swaminarayan')

st.progress(100)

st.selectbox('Select Gender',['Male','Female'])

st.file_uploader('Upload File')