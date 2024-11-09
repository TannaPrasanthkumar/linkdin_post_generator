import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

def main():
    
    st.title("Linkdin Post Generator")
    
    fs = FewShotPosts()
    
    col1, col2, col3 = st.columns(3)
    
    length_options = ["Short", "Medium", "Long"]
    language_options = ["English", "Hinglish"]
    
    with col1:
        choosed_tag = st.selectbox("Title", options = fs.get_tags())
        
    with col2:
        choosed_length = st.selectbox("Length", options = length_options)
    
    with col3:
        choosed_language = st.selectbox("Language", options = language_options)

    if st.button("Generate"):
        
        post = generate_post(choosed_length, choosed_language, choosed_tag)
        st.write(post)
    
if __name__ == "__main__":
    main()