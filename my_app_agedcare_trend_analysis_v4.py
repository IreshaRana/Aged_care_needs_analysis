import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Import data
file_path = 'C:/Iresha_Code/ML_my_projects/Aged_care/df_clean.csv'

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Clean column names if necessary (e.g., remove leading/trailing spaces)
df.columns = df.columns.str.strip()

# Streamlit App Layout
st.title("Aged Care Needs - Trend Analysis")

# Introductory Text with Note
st.write("""
This is an analysis of aged care recipients in Australia. Explore trends and insights into activities of daily living (ADL), behavior and cognition (BEH) and complex health care (CHC) indicators across different states, age groups, and sexes.  
Start your exploration using the options in the sidebar!
         
**Note:** Data for the year 2008 is only partially available.  
Data Source: [Care needs of people in aged care dataset](https://example-link-to-dataset.com)  
""")

# Sidebar Filters
state = st.sidebar.selectbox("Select State", ['All States'] + df['STATE'].unique().tolist())
age_group = st.sidebar.selectbox("Select Age Group", ['All'] + df['AGE_GROUP'].unique().tolist())
sex = st.sidebar.selectbox("Select Sex", ['All'] + df['SEX'].unique().tolist())

# Filter the data based on user selection
filtered_df = df.copy()

if state != 'All States':
    filtered_df = filtered_df[filtered_df['STATE'] == state]

if age_group != 'All':
    filtered_df = filtered_df[filtered_df['AGE_GROUP'] == age_group]

if sex != 'All':
    filtered_df = filtered_df[filtered_df['SEX'] == sex]


# Add Pie Charts for ADL, BEH, CHC (Year 2022)
st.write("### Indicator Distribution for 2022")

def plot_pie_chart(data, indicator, title):
    # Filter data for the year 2022
    data_2022 = data[data['YEAR'] == 2022]
    # Calculate percentage distribution
    distribution = data_2022[indicator].value_counts(normalize=True) * 100
    labels = distribution.index
    sizes = distribution.values

    # Plot pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.set_title(title)
    return fig

col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(plot_pie_chart(filtered_df, "ADL", "ADL Distribution (2022)"))

with col2:
    st.pyplot(plot_pie_chart(filtered_df, "BEH", "BEH Distribution (2022)"))

with col3:
    st.pyplot(plot_pie_chart(filtered_df, "CHC", "CHC Distribution (2022)"))

# Customizing font size (smaller font for the legend)
st.markdown(
    """
    <style>
    .legend-text {
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# Displaying the legend
st.markdown('<p class="legend-text">N: Nil, L: Low, M: Medium, H: High</p>', unsafe_allow_html=True)

# Trend Analysis - ADL, BEH, CHC over the years
def plot_trends(indicator):
    # Group by year and indicator, then calculate the count for each level
    trend_data = filtered_df.groupby(['YEAR', indicator]).size().unstack().fillna(0)
    
    # Plot the trend for each level of the indicator (N, L, M, H)
    trend_data.plot(kind='line', marker='o', figsize=(10, 6))
    
    # Adding labels and title
    plt.title(f"Trend of {indicator} in {state} (2008-2022)")
    plt.xlabel("Year")
    plt.ylabel("Number of recipients")
    plt.grid(True)
    st.pyplot(plt)

# Display trends for ADL, BEH, and CHC
st.write(f"### Trend Analysis for {state}, Age Group: {age_group}, Sex: {sex}")
st.write("These line charts show trends for Activities of Daily Living (ADL), Behavior and Cognition (BEH), and Complex Health Care (CHC) over the years.")

# Display number of records (normal text)
record_count = len(filtered_df)
st.write(f"Total number of records for the selected options in the sidebar: {record_count:,}")

# Plot trends for each indicator
plot_trends("ADL")
plot_trends("BEH")
plot_trends("CHC")