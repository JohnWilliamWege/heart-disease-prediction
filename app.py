import streamlit as st
from multiapp import MultiApp
import predict
import overview
import report

app = MultiApp()


app.add_app("Predict", predict.app)
app.add_app("Overview", overview.app)
app.add_app("Report", report.app)

# The main app
app.run()