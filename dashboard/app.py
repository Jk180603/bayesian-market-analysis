import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Bayesian Marketing Analytics", layout="wide")

st.title("📊 Bayesian Marketing Analytics Dashboard")

channel_df = pd.read_csv("reports/channel_effectiveness.csv")

st.subheader("Channel Effectiveness")

st.dataframe(channel_df)

fig, ax = plt.subplots(figsize=(10, 5))

ax.bar(
    channel_df["channel"],
    channel_df["mean_effect"],
)

ax.set_title("Estimated Channel Effectiveness")
ax.set_ylabel("Mean Bayesian Effect")

st.pyplot(fig)

st.subheader("Uncertainty Intervals")

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.errorbar(
    channel_df["channel"],
    channel_df["mean_effect"],
    yerr=[
        channel_df["mean_effect"] - channel_df["lower_94_hdi"],
        channel_df["upper_94_hdi"] - channel_df["mean_effect"],
    ],
    fmt="o",
    capsize=5,
)

ax2.set_title("94% HDI Uncertainty Intervals")
ax2.set_ylabel("Effect Estimate")

st.pyplot(fig2)

best_channel = channel_df.sort_values(
    by="mean_effect",
    ascending=False
).iloc[0]

st.success(
    f"Best performing channel: {best_channel['channel']}"
)