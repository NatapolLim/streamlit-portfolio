"""Frameworks for running multiple Streamlit applications as a single app.
"""
from streamlit_option_menu import option_menu
from utils import html_display_img_with_href
import streamlit as st
import base64
import os
class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        # self.apps = []
        self.apps = {}

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        # self.apps.append({
        #     "title": title,
        #     "function": func
        # })
        self.apps[title] = func

    def run(self):
        with open("src/profile/style.css", 'r') as file:
            st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

        contents = list(self.apps.keys())

        with st.sidebar:
            choose = option_menu("Contents", contents,
                            icons=['person square',None,'kanban'],
                            menu_icon="app-indicator", default_index=0,
                            styles={
            "container": {"padding": "10!important", "background-color": "#7a7a7a"},
            "icon": {"color": "white", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#dddddd30"},
            "nav-link-selected": {"background-color": "#dddddd60"},
            }
            )
        self.apps[choose]()


        

        # st.sidebar.title("Portfolio")
        # st.sidebar.subheader("by Natapol Lim")

        # app = st.sidebar.selectbox(
        #     'Topics',
        #     self.apps,
        #     format_func=lambda app: app['title'],
        #     )
        # app['function']()

def footer():
    st.markdown("""<hr class="style1">""", unsafe_allow_html=True)
    st.markdown('''#### Contact''')
    _, c2 ,c3, _ = st.columns((3,1,1,3))

    linkedin_img_html = html_display_img_with_href(
        'src/profile/640px-LinkedIn_logo_initials.png',
        'https://www.linkedin.com/in/natapol-limpananuwat-686595202'
        )
    c2.markdown(linkedin_img_html, unsafe_allow_html=True)

    github_img_html = html_display_img_with_href(
        'src/profile/1164606_telegram-icon-github-icon-png-white-png-download.png-removebg-preview.png',
        'https://github.com/NatapolLim'
        )
    c3.markdown(github_img_html, unsafe_allow_html=True)

    _, c2 ,_ = st.columns((1,3,1))

    c2.markdown("""<p id='footer'>
    Address: Bangkoknoi Bangkok 10700</br>
    Email: Natapolllim@gmail.com</br>
    Tel: 084-926-7299
    </p>
    """, unsafe_allow_html=True)
