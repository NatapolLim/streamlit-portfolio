"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

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
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        
        st.sidebar.title("Portfolio")
        st.sidebar.subheader("by Natapol Lim")
        
        # if not st.session_state:
        #     st.session_state.apps = [(i,app['title'], app['function']) for i, app in enumerate(self.apps)]
        #     st.session_state.page = 0

        # page = st.sidebar.selectbox(
        #     'Topics',
        #     st.session_state.apps,
        #     format_func=lambda app:app[1],
        #     key='test_pages',
        #     # index=st.session_state.page
        #     # on_change=reset_page,
        #     # args=(st.session_state.page,)
        #     )
            
        # st.session_state.page = page[0]
        # st.markdown(st.session_state.page)
        # st.session_state.apps[st.session_state.page][2]()

        app = st.sidebar.selectbox(
            'Topics',
            self.apps,
            format_func=lambda app: app['title'],
            )
        app['function']()

