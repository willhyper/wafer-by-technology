import numpy as np

# https://investor.tsmc.com/english/quarterly-results/2021/q1

technology = ['5nm', '7nm', '10nm', '16nm', '20nm', '28nm',
              '40/45nm', '65nm', '90nm', '0.11/0.13um', '0.15/0.18um', '0.25um+']

measurements = {  # revenue, shipment, technology revenue share by quarter
    # quarter : Million NTD, K piece of wafer, %
    '2021Q1': (362410,	3359, np.array([14, 35, 0, 14, 0, 11, 7, 5, 3, 3, 6, 2])/100),
    '2020Q4': (361530,	3246, np.array([20, 29, 0, 13, 1, 11, 8, 5, 2, 3, 7, 1])/100),
    '2020Q3': (356430,	3240, np.array([8, 35, 0, 18, 1, 12, 8, 5, 2, 2, 7, 2])/100),
    '2020Q2': (310700,	2985, np.array([0, 36, 0, 18, 1, 14, 9, 6, 3, 3, 8, 2])/100),
    '2020Q1': (310600,	2925, np.array([0, 35, 0.5, 19, 1, 14, 10, 6, 3, 2, 8, 2])/100),
    '2019Q4': (317240,	2823, np.array([0, 35, 1, 20, 1, 13, 8, 7, 3, 3, 8, 1])/100),
    '2019Q3': (293050,	2733, np.array([0, 27, 2, 22, 1, 16, 10, 7, 2, 2, 9, 2])/100),
    '2019Q2': (241000,	2308, np.array([0, 21, 3, 23, 1, 18, 11, 8, 3, 2, 8, 2])/100),
    '2019Q1': (218700,	2205, np.array([0, 22, 4, 16, 1, 20, 12, 8, 3, 3, 8, 3])/100),
    '2018Q4': (289770,	2686, np.array([0, 23, 6, 20, 1, 17, 10, 8, 3, 2, 8, 2])/100),
    '2018Q3': (260350,	2712, np.array([0, 11, 6, 23, 2, 19, 12, 8, 4, 3, 9, 3])/100),
    '2018Q2': (233280,	2674, np.array([0, 0, 13, 21, 4, 23, 11, 9, 5, 2, 9, 3])/100),
    '2018Q1': (248080,	2680, np.array([0, 0, 19, 18, 4, 20, 11, 9, 5, 2, 9, 3])/100),
}

# %% invariants

for quarter, (revenue, kpcs, shares) in measurements.items():
    # sum of shares must be about 100%. tolerating 1%
    _sum = sum(shares)
    assert abs(_sum - 1.0) < 0.01, f'{quarter} sum(shares) = {_sum}'

    # data structure must agree
    assert len(technology) == len(shares)


def revenue_share(tech: str) -> dict:
    index = technology.index(tech)
    return {quarter: shares[index] for quarter, (revenue, kpcs, shares) in measurements.items()}


def revenue_of_technology(tech: str) -> dict:
    index = technology.index(tech)
    return {quarter: shares[index] * revenue for quarter, (revenue, kpcs, shares) in measurements.items()}


def revenue_of_quarter(quarter: str) -> int:
    return measurements[quarter][0]  # Million NTD


def shipment(quarter: str) -> int:
    return measurements[quarter][1]  # K pcs of wafer


def technology_share(quarter: str):
    return measurements[quarter][2]  # %


def quarters():
    return measurements.keys()


def revenues():
    return {quarter: revenue for quarter, (revenue, kpcs, shares) in measurements.items()}


def shipments():
    return {quarter: kpcs for quarter, (revenue, kpcs, shares) in measurements.items()}
