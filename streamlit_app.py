# put streamlit code here as needed
# INSTRUCTIONS:
# 1. Open a "Terminal" by: View --> Terminal OR just the "Terminal" through the hamburger menu
# 2. run in terminal with: streamlit run streamlit_app.py
# 3. click the "Open in Browser" link that pops up OR click on "Ports" and copy the URL
# 4. Open a Simple Browswer with View --> Command Palette --> Simple Browser: Show
# 5. use the URL from prior steps as intput into this simple browser

import pandas as pd
import streamlit as st
import altair as alt


st.title('Streamlit App for IS445: ID14966')

st.text("The URL for this app is: https://johnmakowiecki-is445-hw6.streamlit.app/")
st.text("The URL for its GitHub repo is: https://github.com/jmakow/is445_hw6")

source = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"
df = pd.read_csv(source)
df = df[df["Year Acquired"] > 0]



alt.data_transformers.disable_max_rows()
df["Decade"] = (df["Year Acquired"] // 10) * 10
brush = alt.selection_interval(encodings=['x'])

bars = alt.Chart().mark_bar().encode(
    x='Decade:O',
    y='mean(Square Footage):Q',
    opacity = alt.when(brush).then(alt.value(1)).otherwise(alt.value(0.7)),
).add_params(brush)

line = alt.Chart().mark_rule(color='firebrick').encode(
    y='mean(Square Footage):Q',
    size=alt.SizeValue(3)
).transform_filter(
    brush
)

chart1 = alt.layer(bars, line, data=df).properties(
    title='Average Illinois Building Size by Decade Acquired'
)
st.altair_chart(chart1)

st.write("This chart shows the average size of state buildings by the decade they were acquired. "
         "Buildings from the 1830s to 1920s were bigger on average than newer ones. "
         "You can drag across decades and the red line shows the average for the decades selected. "
         "I removed buildings with unknown years and grouped years into decades. I used bars to compare decades in order. "
         "The bars are blue and the average line is red so it stands out. "
         "With more time, I would have removed the earilier decades. "
)

source = df[df["Year Acquired"] >= 1900].groupby("Year Acquired").size().reset_index()
source.columns = ["Year Acquired", "buildings"]
bar = alt.Chart(source).mark_bar().encode(
    x='Year Acquired:O',
    y='buildings:Q'
)

line = alt.Chart(source).mark_line(color='red').transform_window(
    # The field to average
    rolling_mean='mean(buildings)',
    # The number of values before and after the current value to include.
    frame=[-9, 0]
).encode(
    x='Year Acquired:O',
    y='rolling_mean:Q'
)

chart2 = (bar + line).properties(width=600)
st.altair_chart(chart2)

st.write(
    "This chart shows how many state buildings were acquired each year since 1900. "
    "The red line is a 10 year average that shows the overall trend. "
    "It goes with Chart 1, which shows how big "
    "buildings were, this one shows how many. "
    "I used bars for the yearly counts and a line for the average. "
    "With more time I would show fewer year labels. "
)
