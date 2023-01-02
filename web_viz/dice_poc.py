import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


def create_remote_roles_donut_chart(roles_df: DataFrame) -> None:
    data = roles_df.remote.value_counts().values
    labels = ['Non Remote', 'Remote']
    fig, ax = plt.subplots()
    pie_chart = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    circle = plt.Circle((0, 0), 0.7, color='white')
    ax.add_artist(circle)
    st.pyplot(fig)


if __name__ == "__main__":
    dice_roles_df = pd.read_csv(
        '/Users/nicollegarber/Documents/GitHub/LinkedIn-Skills-Predictor/dice_data_scientist_roles.csv'
    ).drop('Unnamed: 0', axis=1)
    dice_roles_df = dice_roles_df[dice_roles_df.positions.str.lower().apply(lambda row: 'data scientist' in row)]
    dice_roles_df = dice_roles_df.fillna('')
    dice_roles_df['remote'] = dice_roles_df.locations.str.lower().apply(lambda row: 'remote' in row).astype(int)
    create_remote_roles_donut_chart(dice_roles_df)
