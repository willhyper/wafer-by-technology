# https://investor.tsmc.com/english/quarterly-results/2021/q1

import pandas as pd

xlsx_link = 'https://docs.google.com/spreadsheets/d/1ge20fpSWJgiuI_6Cn5KyBKnkLe4gVhW9GutD-Qf5z38/export'
_df = pd.read_excel(xlsx_link)

df = _df.dropna() # in case excel cell is empty

technology = df.columns.drop(['Quarter', 'Revenue(MNTD)', 'shipment(Kpcs)'])
# %% invariants
near_zeros = df[technology].dropna().apply(sum, axis=1).apply(lambda x: abs(x-1))
assert (near_zeros < 0.01).all(), f'sum of % shall be 1. deviation too much\n {near_zeros}'


def revenue_share(tech: str):
    return df[['Quarter', tech]]


def revenue_of_technology(tech: str):
    r = df['Revenue(MNTD)']*df[tech]
    return pd.concat([df['Quarter'], r.rename(f"Revenue(MNTD) of {tech}")], axis=1)


def revenue_of_quarter(quarter: str):
    return df[df.quarter == quarter]['Revenue(MNTD)']  # Million NTD


def shipment(quarter: str):
    return df[df.quarter == quarter]['shipment(Kpcs)']  # K pcs of wafer


def technology_share(quarter: str):
    cols = df.columns.drop(['Revenue(MNTD)', 'shipment(Kpcs)'])
    dfqts = df[cols]
    dfts = dfqts[dfqts.quarter == quarter]
    return dfts[dfts.columns.drop('Quarter')]
