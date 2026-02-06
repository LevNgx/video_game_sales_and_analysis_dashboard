import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.write("🚀 App is starting...")
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    layout="wide"
)


st.title("🎮 Video Game Sales Analysis Dashboard")

st.markdown("""
This interactive dashboard allows you to explore global video game sales trends across  
**time, platforms, genres, and critic ratings**, based on historical sales data.

Use the filters on the left to explore different segments of the market!.
""")

@st.cache_data
def load_data():
    df = pd.read_csv("../data/Video_Game_Sales_as_of_Jan_2017.csv")
    return df

df = load_data()


# making sure that year column be int 

df = df.dropna(subset=["Year_of_Release"])
df["Year_of_Release"] = df["Year_of_Release"].astype(int)


st.sidebar.header("Filter Options")


# adding year range filter into the side bar 
min_year = int(df["Year_of_Release"].min())
max_year = int(df["Year_of_Release"].max())

year_range = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    (min_year, max_year)
)



# Adding the platform filter to choose from the available gaming platforms
platforms = sorted(df["Platform"].dropna().unique())

default_platforms = [p for p in ["PS2", "X360"] if p in platforms]

selected_platforms = st.sidebar.multiselect(
    "Select Platforms",
    platforms,
    default=default_platforms
)



# filter to apply on genre
genres = sorted(df["Genre"].dropna().unique())

default_genres = [g for g in ["Action", "Sports"] if g in genres]

selected_genres = st.sidebar.multiselect(
    "Select Genres",
    genres,
    default=default_genres
)

# applying the selected filters on the data frame
filtered_df = df[
    (df["Year_of_Release"].between(year_range[0], year_range[1])) &
    (df["Platform"].isin(selected_platforms)) &
    (df["Genre"].isin(selected_genres))
]



# Global sales over time
sales_over_time = (
    filtered_df
    .groupby("Year_of_Release")["Global_Sales"]
    .sum()
    .reset_index()
    .sort_values("Year_of_Release")
)


# plot

st.subheader("Global Video Game Sales Over Time")

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(
    sales_over_time["Year_of_Release"],
    sales_over_time["Global_Sales"],
    marker="o"
)

ax.set_xlabel("Year of Release")
ax.set_ylabel("Global Sales (Million Units)")
ax.set_title("Global Sales Trend")

st.pyplot(fig)



# top platforms by global sales 
platform_sales = (
    filtered_df
    .groupby("Platform")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# keeping the top 10 platforms for better visual clarity
# platform_sales_top = platform_sales.head(10)


st.subheader("Top Platforms by Global Sales")

fig, ax = plt.subplots(figsize=(10, 4))

ax.bar(
    platform_sales["Platform"],
    platform_sales["Global_Sales"]
)

ax.set_xlabel("Platform")
ax.set_ylabel("Global Sales (Million Units)")
ax.set_title("Top Platforms by Global Sales")
ax.tick_params(axis="x", rotation=45)

st.pyplot(fig)

# top genres by global sales
genre_sales = (
    filtered_df
    .groupby("Genre")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# # considering top 10 genres for readability
# genre_sales_top = genre_sales.head(10)


st.subheader("Top Genres by Global Sales")

fig, ax = plt.subplots(figsize=(10, 4))

ax.bar(
    genre_sales["Genre"],
    genre_sales["Global_Sales"]
)

ax.set_xlabel("Genre")
ax.set_ylabel("Global Sales (Million Units)")
ax.set_title("Top Genres by Global Sales")
ax.tick_params(axis="x", rotation=45)

st.pyplot(fig)

# Genre performance across regions
genre_region_sales = (
    filtered_df
    .groupby("Genre")[["NA_Sales", "EU_Sales", "JP_Sales"]]
    .sum()
    .reset_index()
)


genre_region_sales["Total_Sales"] = (
    genre_region_sales["NA_Sales"] +
    genre_region_sales["EU_Sales"] +
    genre_region_sales["JP_Sales"]
)

genre_region_sales = (
    genre_region_sales
    .sort_values("Total_Sales", ascending=False)
  
)


st.subheader("Genre Performance Across Regions")

fig, ax = plt.subplots(figsize=(10, 4))

ax.bar(
    genre_region_sales["Genre"],
    genre_region_sales["NA_Sales"],
    label="North America"
)

ax.bar(
    genre_region_sales["Genre"],
    genre_region_sales["EU_Sales"],
    bottom=genre_region_sales["NA_Sales"],
    label="Europe"
)

ax.bar(
    genre_region_sales["Genre"],
    genre_region_sales["JP_Sales"],
    bottom=genre_region_sales["NA_Sales"] + genre_region_sales["EU_Sales"],
    label="Japan"
)

ax.set_xlabel("Genre")
ax.set_ylabel("Sales (Million Units)")
ax.set_title("Genre-wise Sales Distribution Across Regions")
ax.legend()

st.pyplot(fig)


# Critics score vs Global sales

df_critic = filtered_df.dropna(subset=["Critic_Score"]).copy()

# making sure the critic score will be of float data type
df_critic["Critic_Score"] = df_critic["Critic_Score"].astype(float)


st.subheader("Critic Score vs Global Sales")

fig, ax = plt.subplots(figsize=(10, 4))

ax.scatter(
    df_critic["Critic_Score"],
    df_critic["Global_Sales"],
    alpha=0.6
)

ax.set_xlabel("Critic Score")
ax.set_ylabel("Global Sales (Million Units)")
ax.set_title("Relationship Between Critic Scores and Global Sales")

st.pyplot(fig)
