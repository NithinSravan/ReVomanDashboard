#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import json
#######################
# Page configuration
st.set_page_config(
    page_title="ReVoman Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data
file_path='data/data.json'
with open(file_path, "r") as file:
    json_data = json.load(file)

#######################
# Sidebar
with st.sidebar:
    st.title('🏂 ReVoman Dashboard')
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="StepIndex", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="Time Data", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'{input_color}:Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=500,height=300
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        ) 
    # height=300
    return heatmap

#Line Plot
def make_lineplot(df,input_y,input_x):
    
    # Plot using Altair
    lineplot = alt.Chart(df).mark_line().encode(
        y=alt.Y(f'{input_y}:Q', axis=alt.Axis(title="Time (in Seconds)", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="StepIndex", titleFontSize=18, titlePadding=15, titleFontWeight=900,labelAngle=0)),
    ).properties(
        title='Total Time vs Step Index'
    )

    return lineplot

# Donut chart
def make_pie(df):

  pie_chart = alt.Chart(df).mark_arc().encode(
        color=alt.Color('isSuccessful:N', scale=alt.Scale(domain=['true', 'false'], range=['#1f77b4', '#ff7f0e']),legend=alt.Legend(title="Legend")),
        theta=alt.Theta( 'count:Q')
    ).properties(
        width=300,
        height=300,
        title='Test Success Rate')
    
  return pie_chart

#######################
# Dashboard Main Panel
col = st.columns((4.5, 4.5), gap='medium')

with col[0]:
    st.markdown('#### Time Consumed by Tasks in a Step Report')
    # Extract time data from nested structure and create a DataFrame
    df_hm = pd.DataFrame(json_data['stepReports'])

    # Exclude 'stepIndex' and 'isSuccessful' columns
    df_hm = df_hm.drop(columns=['stepIndex', 'isSuccessful'])
    df_hm = df_hm.stack().reset_index()

    df_hm.columns = ['Step', 'Metric', 'Value']
    heatmap = make_heatmap(df_hm, 'Step', 'Metric', 'Value', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)

    # Convert JSON to DataFrame
    df_p = pd.DataFrame(json_data['stepReports'])

    # Count occurrences of each value in "isSuccessful"
    is_successful_counts = df_p['isSuccessful'].value_counts()

    print(is_successful_counts)

    # Create DataFrame from counts
    df_counts = pd.DataFrame({'isSuccessful': is_successful_counts.index, 'count': is_successful_counts.values})

    pie=make_pie(df_counts)
    st.altair_chart(pie, use_container_width=True)
    

with col[1]:
    st.markdown('#### Time Consumed per Step Report')
    # Convert JSON to DataFrame
    df_lp = pd.DataFrame(json_data['stepReports'])

    # Sum the times in each object
    df_lp['TotalTime'] = df_lp.drop(columns=['stepIndex', 'isSuccessful']).sum(axis=1)

    lineplot=make_lineplot(df_lp,'TotalTime','stepIndex')

    st.altair_chart(lineplot, use_container_width=True)