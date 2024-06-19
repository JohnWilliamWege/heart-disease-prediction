import streamlit as st
from multiapp import MultiApp
import predict
import overview


app = MultiApp()


app.add_app("Predict", predict.app)
app.add_app("Overview", overview.app)

# The main app
app.run()