import plotly.graph_objects as go
import plotly.express as px
import plotly
import pandas as pd
import pickle
import json

# Load your data
day_texts = pickle.load(open("data/day_texts.p", "rb"))
eddy_day_counts = [len(day['ogola']) for day in day_texts.values()]
puru_day_counts = [len(day['Prudence']) for day in day_texts.values()]

# Create your figures (copied from your original app)
# Time series plot
x = list(day_texts.keys())
df = pd.DataFrame({
    'day': x,
    'Ogola': eddy_day_counts,
    'Prudence': puru_day_counts,
})
df_melted = df.melt(id_vars=["day"], value_vars=["Ogola", "Prudence"], var_name="name", value_name="count")

fig = px.line(df_melted, x="day", y="count", color="name", title="Messages Over Time")
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(
    hovermode="x",
    title_x=0.5,
    height=400,
    margin=dict(t=50, b=50),
    font_family="Courier New"
)

# Pie chart
total_texts = pd.DataFrame({
    'Ogola': [3075],
    'Prudence': [2307],
}, index=['Index1'])
fig1 = px.pie(total_texts, names=total_texts.columns, values=total_texts.loc['Index1'])
fig1.update_traces(hovertemplate="%{label} sent %{value} messages")
fig1.update_layout(
    title="Total Messages Share",
    title_x=0.5,
    showlegend=False,
    margin=dict(t=50, b=0, l=0, r=0),
    font_family="Courier New"
)

# Bar chart
fig2 = go.Figure(go.Bar(
    x=[19, 18],
    y=["Ogola", "Prudence"],
    orientation="h",
    marker=dict(color=['#636EFA', '#EF553B']),
))
fig2.update_traces(hovertemplate="%{y} initiated %{x}/37 days")
fig2.update_layout(
    title="Conversation Initiation",
    title_x=0.5,
    margin=dict(t=50, b=0, l=0, r=0),
    font_family="Courier New"
)

# Convert figures to JSON
graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Create the static HTML
static_html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>SNH Sentiment Analysis</title>
    <base href="/snh/">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            margin: 0;
            font-family: 'Courier New', monospace;
            color: #4A4A4A;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .number {{
            font-size: 2.5rem;
            font-weight: 300;
            letter-spacing: 0.1em;
            margin-right: 0.5rem;
        }}
        .text {{
            font-size: 1.1rem;
        }}
        .bold-date {{
            font-size: 1.1rem;
            font-weight: bold;
        }}
        .hr-style {{
            border: none;
            border-top: 1px solid #A9A9A9;
            margin: 1rem 0;
        }}
        .todo-section {{
            padding: 2rem;
            background-color: #f5f5f5;
            border-radius: 8px;
        }}
        .todo-header {{
            font-size: 1.8rem;
            font-weight: 300;
            margin-bottom: 1rem;
        }}
        .todo-item {{
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }}
        .intro-text {{
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 style="text-align: center; margin-bottom: 2rem; font-weight: bold; font-size: 2.5rem;">
            SNH Sentiment Analysis
        </h1>
        
        <div style="display: flex; margin-bottom: 2rem;">
            <!-- Left side text -->
            <div style="width: 30%; padding: 2rem; display: flex; flex-direction: column; justify-content: center;">
                <div class="intro-text">
                    So I, psychotically, kept message logs from my first relationship(I was that butt-hurt).
                    I recently came across the text dump and did some basic analysis to inspect the progression of the relationship.
                </div>
                <hr class="hr-style">
                <div style="margin-bottom: 1rem">
                    <span class="number">36.6</span>
                    <span class="text">days / </span>
                    <span class="number">5.2</span>
                    <span class="text">weeks of messages</span>
                </div>
                <div style="margin-bottom: 1rem">
                    <span class="text">from </span>
                    <span class="bold-date">04/13/2020</span><br>
                    <span class="text">to </span>
                    <span class="bold-date">05/19/2020</span>
                </div>
                <div>
                    <span class="number">5,382</span><br>
                    <span class="text">total messages exchanged</span><br>
                    <span class="text">during this first</span><br>
                    <span class="text">relationship</span>
                </div>
            </div>
            
            <!-- Right side charts -->
            <div style="width: 70%; padding: 1rem;">
                <div id="chart1"></div>
                <div id="chart2"></div>
            </div>
        </div>
        
        <!-- Bottom - Time series graph -->
        <div id="chart3"></div>
        
        <hr class="hr-style">
        
        <div class="todo-section">
            <h2 class="todo-header">TODO</h2>
            <div class="todo-item">[ ] Add sentiment analysis over time</div>
            <div class="todo-item">[ ] Track conversation patterns (time of day)</div>
            <div class="todo-item">[ ] Identify common topics/keywords</div>
            <div class="todo-item">[ ] Add emoji usage analysis</div>
        </div>
    </div>

    <script>
        // Create the charts using the JSON data
        var graphs1 = {graphJSON1};
        Plotly.newPlot('chart1', graphs1.data, graphs1.layout);
        
        var graphs2 = {graphJSON2};
        Plotly.newPlot('chart2', graphs2.data, graphs2.layout);
        
        var graphs3 = {graphJSON3};
        Plotly.newPlot('chart3', graphs3.data, graphs3.layout);
    </script>
</body>
</html>
'''

# Write to file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(static_html)