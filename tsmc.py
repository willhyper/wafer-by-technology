import pandas as pd

# https://investor.tsmc.com/english/quarterly-results/2021/q1

m = {
    'quarter': ['2021Q2', '2021Q1', '2020Q4', '2020Q3', '2020Q2', '2020Q1', '2019Q4', '2019Q3', '2019Q2', '2019Q1', '2018Q4', '2018Q3', '2018Q2', '2018Q1'],
    'revenue(MNTD)': [372145, 362410, 361530, 356430, 310700, 310600, 317240, 293050, 241000, 218700, 289770, 260350, 233280, 248080],
    'shipment(Kpcs)': [3449, 3359, 3246, 3240, 2985, 2925, 2823, 2733, 2308, 2205, 2686, 2712, 2674, 2680],
    '5nm%': [0.18, 0.14, 0.2, 0.08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    '7nm%': [0.31, 0.35, 0.29, 0.35, 0.36, 0.35, 0.35, 0.27, 0.21, 0.22, 0.23, 0.11, 0.0, 0.0],
    '10nm%': [0, 0, 0, 0, 0, 0.005, 0.01, 0.02, 0.03, 0.04, 0.06, 0.06, 0.13, 0.19],
    '16nm%': [0.14, 0.14, 0.13, 0.18, 0.18, 0.19, 0.2, 0.22, 0.23, 0.16, 0.2, 0.23, 0.21, 0.18],
    '20nm%': [0, 0, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02, 0.04, 0.04],
    '28nm%': [0.11, 0.11, 0.11, 0.12, 0.14, 0.14, 0.13, 0.16, 0.18, 0.2, 0.17, 0.19, 0.23, 0.2],
    '40/45nm%': [0.07, 0.07, 0.08, 0.08, 0.09, 0.1, 0.08, 0.1, 0.11, 0.12, 0.1, 0.12, 0.11, 0.11],
    '65nm%': [0.05, 0.05, 0.05, 0.05, 0.06, 0.06, 0.07, 0.07, 0.08, 0.08, 0.08, 0.08, 0.09, 0.09],
    '90nm%': [0.03, 0.03, 0.02, 0.02, 0.03, 0.03, 0.03, 0.02, 0.03, 0.03, 0.03, 0.04, 0.05, 0.05],
    '110/130nm%': [0.03, 0.03, 0.03, 0.02, 0.03, 0.02, 0.03, 0.02, 0.02, 0.03, 0.02, 0.03, 0.02, 0.02],
    '150/180nm%': [0.06, 0.06, 0.07, 0.07, 0.08, 0.08, 0.08, 0.09, 0.08, 0.08, 0.08, 0.09, 0.09, 0.09],
    '250nm+%': [0.02, 0.02, 0.01, 0.02, 0.02, 0.02, 0.01, 0.02, 0.02, 0.03, 0.02, 0.03, 0.03, 0.03]
}

df = pd.DataFrame(m)

technology = df.columns.drop(['quarter', 'revenue(MNTD)', 'shipment(Kpcs)'])
# %% invariants
near_zeros = df[technology].apply(sum, axis=1).apply(lambda x: abs(x-1))
assert (near_zeros < 0.01).all(), f'sum of % shall be 1. deviation too much\n {near_zeros}'


def revenue_share(tech: str):
    return df[['quarter', tech+"%"]]


def revenue_of_technology(tech: str):
    r = df['revenue(MNTD)']*df[tech+'%']
    return pd.concat([df['quarter'], r.rename(f"revenue(MNTD) of {tech}")], axis=1)


def revenue_of_quarter(quarter: str):
    return df[df.quarter == quarter]['revenue(MNTD)']  # Million NTD


def shipment(quarter: str):
    return df[df.quarter == quarter]['shipment(Kpcs)']  # K pcs of wafer


def technology_share(quarter: str):
    cols = df.columns.drop(['revenue(MNTD)', 'shipment(Kpcs)'])
    dfqts = df[cols]
    dfts = dfqts[dfqts.quarter == quarter]
    return dfts[dfts.columns.drop('quarter')]
