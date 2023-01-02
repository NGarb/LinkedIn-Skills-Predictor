import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame
import spacy
import torch.nn.functional as F
import torch
from transformers import BertTokenizer, BertModel
import seaborn as sns


def _get_years_of_experience(descriptions):
    nlp = spacy.load('en_core_web_sm')
    years_of_experience = []
    for description in descriptions:
        role_years_of_experience = np.nan
        doc = nlp(description)
        for i, token in enumerate(doc):
            if token.like_num:
                phrase_containing_number = doc[i : i + 6].text
                if 'month' not in phrase_containing_number.lower() and 'week' not in phrase_containing_number.lower():
                    sim = _get_similarity_of_query_to_phrase("years experience", phrase_containing_number)
                    if sim[0] >= 0.65:
                        role_years_of_experience = token.text
        years_of_experience.append(role_years_of_experience)
    return years_of_experience


def _get_similarity_of_query_to_phrase(query, document):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = BertModel.from_pretrained('bert-base-uncased').to(device)
    query_tokens = torch.tensor([tokenizer.encode(query, add_special_tokens=True)]).to(device)
    document_tokens = torch.tensor([tokenizer.encode(document, add_special_tokens=True)]).to(device)
    with torch.no_grad():
        query_embeddings = model(query_tokens)[0]
        document_embeddings = model(document_tokens)[0]
    return F.cosine_similarity(query_embeddings.mean(dim=1), document_embeddings.mean(dim=1))


def _create_remote_roles_donut_chart(roles_df: DataFrame) -> None:
    data = roles_df.remote.value_counts().values
    labels = ['Non Remote', 'Remote']
    fig, ax = plt.subplots(figsize=(6, 6))
    pie_chart = ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#00b894', '#fdcb6e'])
    circle = plt.Circle((0, 0), 0.6, color='white')
    ax.add_artist(circle)
    ax.set_title('Remote Work in Data Science Roles', fontsize=18, fontweight='bold')
    ax.legend(title='Remote Work', labels=labels, bbox_to_anchor=(1, 0.5), loc='center left', fontsize=14)
    st.pyplot(fig)


def _create_years_of_experience_distribution(roles_df: DataFrame) -> None:
    plot = sns.displot(roles_df, x="years_of_experience", kind="kde", color='#00b894')
    plot.set_xlabels('Years of Experience', fontsize=14)
    plot.set_ylabels('Density', fontsize=14)
    plot.fig.suptitle('Distribution of Years of Experience in Data Science Roles', fontsize=18, fontweight='bold')
    fig = plot.fig
    st.pyplot(fig)


if __name__ == "__main__":
    dice_roles_df = pd.read_csv(
        '/Users/nicollegarber/Documents/GitHub/LinkedIn-Skills-Predictor/dice_data_scientist_roles.csv'
    ).drop('Unnamed: 0', axis=1)
    dice_roles_df = dice_roles_df[dice_roles_df.positions.str.lower().apply(lambda row: 'data scientist' in row)]
    dice_roles_df = dice_roles_df.fillna('')
    dice_roles_df['remote'] = dice_roles_df.locations.str.lower().apply(lambda row: 'remote' in row).astype(int)
    # dice_roles_df['years_of_experience'] = _get_years_of_experience(dice_roles_df.descriptions)
    # dice_roles_df['years_of_experience'] = dice_roles_df['years_of_experience'].mask(dice_roles_df['years_of_experience'] > 30, np.nan)

    _create_remote_roles_donut_chart(dice_roles_df)
