# Aghion and Howitt (1992) on modern data: findings

## In plain English

Aghion and Howitt's model says every innovation creates a monopoly that lasts until the next innovation, so the
more research an industry does, the sooner its leading company should be replaced. I counted how often the revenue
leader changed in 141 industries of SEC-filing companies from fiscal 2011 to 2024.

- **Leaders fall about once a decade everywhere.** The chance that an industry's revenue leader is replaced in a
  given year is between 7.7% and 11.7% in every research group, whether the industry spends nothing on research
  (railroads: Union Pacific and BNSF) or a fifth of its revenue (drugs: Pfizer and Johnson & Johnson). The slope on
  research intensity has the model's sign but is not distinguishable from zero.
- **The research-driven displacements are real but not much more frequent.** Nvidia passed Intel in chips, Alphabet
  passed Microsoft in software and internet services, and Apple passed HP in computers. In engines (Cummins),
  construction machinery (Caterpillar) and farm equipment (Deere) the same company led every year. All four of the
  most research-intensive three-digit industries ended the period with a new leader, but that pattern disappears
  at the four-digit level.
- **Many leadership changes have nothing to do with research.** Near-ties (Crown and Ball in metal cans were
  $6 million apart in 2024), commodity prices (Occidental, Devon and Chesapeake in oil and gas), a grounded airplane
  (Boeing and RTX) and mergers move the rankings.
- **Research effort has grown elevenfold since the 1950s while productivity growth has fallen from 1.87% to 1.03% a
  year**, the opposite of the model's prediction that growth rises with research effort, as Charles Jones argued in
  1995.

A friendlier tour is in the [README](../README.md). The rest of this page is the technical detail.

**Key to the labels below.** *Hazard* = leader changes divided by year-to-year transitions (13 per industry for
fiscal 2011 to 2024). *Lasting change* = a change in which the new leader is still on top the next year (12
possible per industry, 2012 to 2023). *New leader by 2024* = the 2024 leader is a different company from the 2011
leader. *Top-4 turnover* = share of the 2011 top four companies (by revenue) not in the 2024 top four. *R&D group* =
industry R&D expense as a share of industry revenue, all companies, 2011 to 2024. *3-digit / 4-digit SIC* =
industry level of the Standard Industrial Classification. *Effort* = private R&D investment divided by average
hourly compensation. Standard errors are HC1 for cross-sections and Newey-West (4 lags) for annual time series.

## Leader replacement by research intensity

3-digit SIC, 141 industries (`results/leader_hazard_by_rd.csv`). The 95% interval is the exact Poisson interval
for the pooled count of changes.

| R&D group | Industries | Leader changes | Industry-years | Hazard | 95% CI | Tenure (years) | Lasting-change hazard | New leader by 2024 | Top-4 turnover | Never changed |
|---|---|---|---|---|---|---|---|---|---|---|
| No R&D (under 0.05% of revenue) | 76 | 96 | 988 | 9.7% | 7.9% to 11.9% | 10.3 | 6.9% | 39% | 33% | 35 |
| Some R&D (0.05% to 2%) | 40 | 40 | 520 | 7.7% | 5.5% to 10.5% | 13.0 | 6.9% | 42% | 46% | 18 |
| R&D-intensive (2% to 8%) | 21 | 32 | 273 | 11.7% | 8.0% to 16.5% | 8.5 | 8.3% | 62% | 36% | 5 |
| Research-driven (8% or more) | 4 | 6 | 52 | 11.5% | 4.2% to 25.1% | 8.7 | 10.4% | 100% | 31% | 0 |

4-digit SIC, 179 industries (`results/leader_hazard_by_rd_sic4.csv`).

| R&D group | Industries | Leader changes | Industry-years | Hazard | 95% CI | Tenure (years) | Lasting-change hazard | New leader by 2024 | Top-4 turnover | Never changed |
|---|---|---|---|---|---|---|---|---|---|---|
| No R&D (under 0.05% of revenue) | 83 | 98 | 1079 | 9.1% | 7.4% to 11.1% | 11.0 | 6.8% | 40% | 35% | 39 |
| Some R&D (0.05% to 2%) | 48 | 66 | 624 | 10.6% | 8.2% to 13.5% | 9.5 | 7.8% | 48% | 41% | 18 |
| R&D-intensive (2% to 8%) | 33 | 36 | 429 | 8.4% | 5.9% to 11.6% | 11.9 | 6.6% | 39% | 44% | 16 |
| Research-driven (8% or more) | 15 | 17 | 195 | 8.7% | 5.1% to 14.0% | 11.5 | 7.8% | 53% | 43% | 6 |

## Regressions on research intensity

Slope = change in the outcome (percentage points a year for hazards, percentage points for the other outcomes) for
one percentage point of R&D intensity. The Poisson row reports the coefficient on R&D intensity in a log-rate model
with an exposure offset and the same controls. Controls are the log of the average number of filers and the
industry's annual revenue growth. (`results/leader_regressions.csv`)

| Sample | Model | Slope | SE | 95% CI | p | Intercept | N |
|---|---|---|---|---|---|---|---|
| 3-digit SIC | Linear hazard on R&D intensity | 0.233 | 0.230 | −0.217 to 0.683 | 0.311 | 9.20 | 141 |
| 3-digit SIC | Linear hazard with controls | 0.476 | 0.326 | −0.163 to 1.115 | 0.144 | 12.86 | 141 |
| 3-digit SIC | Linear hazard on 2011-13 R&D intensity | 0.122 | 0.279 | −0.424 to 0.668 | 0.662 | 9.37 | 141 |
| 3-digit SIC | Lasting leader changes (linear hazard) | 0.233 | 0.141 | −0.043 to 0.509 | 0.098 | 6.92 | 141 |
| 3-digit SIC | Leader in last year differs from first (pct, LPM) | 4.252 | 0.891 | 2.506 to 5.998 | < 0.001 | 40.12 | 141 |
| 3-digit SIC | Top-4 turnover (pct) on R&D intensity | −0.051 | 0.434 | −0.902 to 0.799 | 0.906 | 36.77 | 141 |
| 3-digit SIC | Poisson leader changes on R&D intensity | 0.047 | 0.031 | −0.014 to 0.108 | 0.131 | −2.01 | 141 |
| 3-digit SIC | Spearman rank correlation of hazard and R&D | 0.058 |  |  | 0.494 |  | 141 |
| 4-digit SIC | Linear hazard on R&D intensity | 0.036 | 0.226 | −0.407 to 0.478 | 0.875 | 9.25 | 179 |
| 4-digit SIC | Linear hazard with controls | −0.058 | 0.244 | −0.536 to 0.420 | 0.811 | 5.61 | 179 |
| 4-digit SIC | Linear hazard on 2011-13 R&D intensity | −0.027 | 0.249 | −0.515 to 0.461 | 0.913 | 9.38 | 179 |
| 4-digit SIC | Lasting leader changes (linear hazard) | 0.142 | 0.212 | −0.273 to 0.558 | 0.502 | 6.81 | 179 |
| 4-digit SIC | Leader in last year differs from first (pct, LPM) | 0.439 | 0.910 | −1.345 to 2.224 | 0.629 | 42.06 | 179 |
| 4-digit SIC | Top-4 turnover (pct) on R&D intensity | 0.550 | 0.353 | −0.141 to 1.242 | 0.119 | 37.49 | 179 |
| 4-digit SIC | Poisson leader changes on R&D intensity | −0.006 | 0.025 | −0.055 to 0.043 | 0.805 | −2.78 | 179 |
| 4-digit SIC | Spearman rank correlation of hazard and R&D | −0.005 |  |  | 0.943 |  | 179 |
| 3-digit SIC, 10+ filers | Linear hazard on R&D intensity | 0.260 | 0.234 | −0.199 to 0.720 | 0.267 | 8.51 | 86 |
| 3-digit SIC, 10+ filers | Linear hazard with controls | 0.460 | 0.415 | −0.353 to 1.273 | 0.267 | 12.06 | 86 |
| 3-digit SIC, 10+ filers | Linear hazard on 2011-13 R&D intensity | 0.285 | 0.272 | −0.248 to 0.819 | 0.295 | 8.54 | 86 |
| 3-digit SIC, 10+ filers | Lasting leader changes (linear hazard) | 0.202 | 0.155 | −0.101 to 0.506 | 0.192 | 7.13 | 86 |
| 3-digit SIC, 10+ filers | Leader in last year differs from first (pct, LPM) | 4.711 | 0.930 | 2.889 to 6.534 | < 0.001 | 39.89 | 86 |
| 3-digit SIC, 10+ filers | Top-4 turnover (pct) on R&D intensity | −0.594 | 0.400 | −1.378 to 0.190 | 0.138 | 39.93 | 86 |
| 3-digit SIC, 10+ filers | Poisson leader changes on R&D intensity | 0.047 | 0.043 | −0.037 to 0.131 | 0.274 | −2.10 | 86 |
| 3-digit SIC, 10+ filers | Spearman rank correlation of hazard and R&D | 0.116 |  |  | 0.287 |  | 86 |
| 3-digit SIC, under 8% R&D | Linear hazard on R&D intensity | 0.225 | 0.438 | −0.633 to 1.083 | 0.608 | 9.24 | 137 |
| 3-digit SIC, under 8% R&D | Linear hazard with controls | 0.389 | 0.451 | −0.495 to 1.273 | 0.389 | 13.03 | 137 |
| 3-digit SIC, under 8% R&D | Linear hazard on 2011-13 R&D intensity | −0.144 | 0.423 | −0.973 to 0.685 | 0.733 | 9.53 | 137 |
| 3-digit SIC, under 8% R&D | Lasting leader changes (linear hazard) | 0.139 | 0.310 | −0.469 to 0.747 | 0.653 | 7.00 | 137 |
| 3-digit SIC, under 8% R&D | Leader in last year differs from first (pct, LPM) | 5.127 | 2.453 | 0.319 to 9.936 | 0.037 | 39.48 | 137 |
| 3-digit SIC, under 8% R&D | Top-4 turnover (pct) on R&D intensity | 0.840 | 0.972 | −1.065 to 2.745 | 0.387 | 36.15 | 137 |
| 3-digit SIC, under 8% R&D | Poisson leader changes on R&D intensity | 0.038 | 0.042 | −0.045 to 0.121 | 0.373 | −1.98 | 137 |
| 3-digit SIC, under 8% R&D | Spearman rank correlation of hazard and R&D | 0.038 |  |  | 0.660 |  | 137 |

## The value of leadership, V = pi / (r + lambda n)

Real rate = mean 10-year TIPS yield, 2011 to 2024 (FRED DFII10). V / pi is the value of holding the lead measured in
years of current profit. (`results/value_of_leadership.csv`)

| Group | Hazard | Real rate | V / pi (years of profit) | With no displacement |
|---|---|---|---|---|
| No R&D (under 0.05% of revenue) | 9.72% | 0.395% | 9.9 | 253 |
| Some R&D (0.05% to 2%) | 7.69% | 0.395% | 12.4 | 253 |
| R&D-intensive (2% to 8%) | 11.72% | 0.395% | 8.3 | 253 |
| Research-driven (8% or more) | 11.54% | 0.395% | 8.4 | 253 |
| All industries | 9.49% | 0.395% | 10.1 | 253 |

Implied innovation step (`results/implied_step.csv`). TFP growth over 2011 to 2024 (the log change from 2010 to
2024 divided by 14) of 0.735% a year, divided by the pooled hazard of 0.0949, gives ln(gamma) = 0.0774, a productivity
step of 8.0% per leadership change.

## Intel and Nvidia

Revenue and R&D expense in billions of dollars, by fiscal year as labeled in this study (Nvidia's year ending in
January is labeled with the previous calendar year). (`results/intel_nvidia.csv`)

| Year | Intel revenue | Intel R&D | Nvidia revenue | Nvidia R&D |
|---|---|---|---|---|
| 2011 | 54.0 | 8.3 | 4.0 | 1.0 |
| 2012 | 53.3 | 10.1 | 4.3 | 1.1 |
| 2013 | 52.7 | 10.6 | 4.1 | 1.3 |
| 2014 | 55.9 | 11.5 | 4.7 | 1.4 |
| 2015 | 55.4 | 12.1 | 5.0 | 1.3 |
| 2016 | 59.4 | 12.7 | 6.9 | 1.5 |
| 2017 | 62.8 | 13.1 | 9.7 | 1.8 |
| 2018 | 70.8 | 13.5 | 11.7 | 2.4 |
| 2019 | 72.0 | 13.4 | 10.9 | 2.8 |
| 2020 | 77.9 | 13.6 | 16.7 | 3.9 |
| 2021 | 79.0 | 15.2 | 26.9 | 5.3 |
| 2022 | 63.1 | 17.5 | 27.0 | 7.3 |
| 2023 | 54.2 | 16.0 | 60.9 | 8.7 |
| 2024 | 53.1 | 16.5 | 130.5 | 12.9 |

## Extension: research effort and productivity growth, 1950-2025

Decade averages (`results/scale_decades.csv`). Growth per effort = TFP growth divided by the effort index, relative
to the 1950s, which is the model's lambda times ln(gamma).

| Decade | Years | TFP growth (%) | Effort (1950s = 1) | Private R&D (% GDP) | Total R&D (% GDP) | Private R&D ($bn) | Growth per effort (1950s = 1) |
|---|---|---|---|---|---|---|---|
| 1950s | 1950-1959 | 1.87 | 1.00 | 0.65 | 1.56 | 2.8 | 1.000 |
| 1960s | 1960-1969 | 1.87 | 1.75 | 0.98 | 2.71 | 7.3 | 0.569 |
| 1970s | 1970-1979 | 1.05 | 2.22 | 1.05 | 2.38 | 18.0 | 0.252 |
| 1980s | 1980-1989 | 0.15 | 3.49 | 1.38 | 2.74 | 58.4 | 0.023 |
| 1990s | 1990-1999 | 0.82 | 5.00 | 1.64 | 2.66 | 125.5 | 0.087 |
| 2000s | 2000-2009 | 0.93 | 6.20 | 1.83 | 2.75 | 230.3 | 0.080 |
| 2010s | 2010-2019 | 0.74 | 7.96 | 2.12 | 2.95 | 385.4 | 0.050 |
| 2020s | 2020-2025 | 1.03 | 11.02 | 2.74 | 3.55 | 728.0 | 0.050 |

Time-series regressions of annual TFP growth in percent (`results/scale_regressions.csv`). Annual rows use
Newey-West standard errors with 4 lags; decade-mean rows use HC1.

| Model | Slope | SE | 95% CI | p | N | R2 |
|---|---|---|---|---|---|---|
| AH scale effect: growth on log research effort | −0.5251 | 0.2324 | −0.981 to −0.070 | 0.024 | 76 | 0.055 |
| Non-scale Schumpeterian: growth on R&D share of GDP | −0.5315 | 0.3025 | −1.124 to 0.061 | 0.079 | 76 | 0.035 |
| Jones: growth on a linear trend (per year) | −0.0158 | 0.0078 | −0.031 to −0.001 | 0.042 | 76 | 0.041 |
| Decade means: growth on log research effort | −0.4303 | 0.1697 | −0.763 to −0.098 | 0.011 | 8 | 0.380 |
| Decade means: growth on R&D share of GDP | −0.4052 | 0.2773 | −0.949 to 0.138 | 0.144 | 8 | 0.229 |

## Every industry in the main test

3-digit SIC industries, sorted by R&D intensity (`results/industries_sic3.csv`). The SEC title is that of the
group's "xx0" code where the SEC list has one, otherwise of another code in the group (so 371, motor vehicles,
shows the title of 3716, motor homes). Names are as on each company's latest 10-K, so Chesapeake Energy appears as
Expand Energy and United Technologies as RTX. Filers = average number of companies with revenue per year. The
4-digit version is in `results/industries_sic4.csv`, and the top two companies in every industry and year are in
`results/leaders_by_year_sic3.csv`.

| SIC | SEC title of the group | R&D % | Filers | Changes | Lasting | New leader by 2024 | Top-4 turnover % | Leaders in order |
|---|---|---|---|---|---|---|---|---|
| 283 | Biological Products, (No Diagnostic Substances) | 19.63 | 362 | 3 | 2 | 1 | 25 | Pfizer Inc > Johnson & Johnson |
| 737 | Services-Computer Programming, Data Processing, Etc. | 14.16 | 359 | 1 | 1 | 1 | 25 | Microsoft Corp > Alphabet Inc. |
| 366 | Radio & Tv Broadcasting & Communications Equipment | 13.21 | 60 | 1 | 1 | 1 | 25 | L 3 Communications Holdings Inc > Qualcomm Inc/De |
| 367 | Electronic Components & Accessories | 12.42 | 141 | 1 | 1 | 1 | 50 | Intel Corp > Nvidia Corp |
| 355 | Special Industry Machinery (No Metalworking Machinery) | 7.86 | 23 | 1 | 1 | 1 | 50 | Pentair Plc > Lam Research Corp |
| 386 | Photographic Equipment & Supplies | 7.33 | 5 | 2 | 1 | 0 | 50 | Eastman Kodak Co > Gopro, Inc. |
| 357 | Computer & Office Equipment | 6.57 | 56 | 1 | 1 | 1 | 25 | Hp Inc > Apple Inc |
| 384 | Electromedical & Electrotherapeutic Apparatus | 6.31 | 171 | 1 | 0 | 1 | 50 | 3M Co > Medtronic Plc |
| 382 | Measuring & Controlling Devices, Nec | 6.10 | 83 | 1 | 1 | 1 | 25 | Danaher Corp /De/ > Thermo Fisher Scientific Inc. |
| 873 | Services-Testing Laboratories | 5.48 | 17 | 0 | 0 | 0 | 50 | Iqvia Holdings Inc. |
| 365 | Phonograph Records & Prerecorded Audio Tapes & Disks | 5.33 | 8 | 3 | 2 | 1 | 75 | Harman International Industries Inc /De/ > Sonos Inc > Vizio Holding Corp. |
| 362 | Electrical Industrial Apparatus | 4.25 | 12 | 1 | 1 | 1 | 25 | Woodward, Inc. > Generac Holdings Inc. |
| 10 | Agricultural Production-Crops | 3.85 | 15 | 2 | 2 | 1 | 50 | Dole Food Co Inc > Fresh Del Monte Produce Inc > Corteva, Inc. |
| 352 | Lawn & Garden Tractors & Home Lawn & Gardens Equip | 3.59 | 6 | 0 | 0 | 0 | 0 | Deere & Co |
| 348 | Ordnance & Accessories, (No Vehicles/Guided Missiles) | 3.55 | 6 | 2 | 1 | 1 | 25 | National Presto Industries Inc > Vista Outdoor Inc. > Axon Enterprise, Inc. |
| 351 | Engines & Turbines | 3.48 | 10 | 0 | 0 | 0 | 25 | Cummins Inc |
| 807 | Services-Medical Laboratories | 3.38 | 22 | 1 | 1 | 1 | 50 | Quest Diagnostics Inc > Labcorp Holdings Inc. |
| 372 | Aircraft & Parts | 3.01 | 22 | 5 | 1 | 1 | 0 | Boeing Co > Rtx Corp |
| 359 | Misc Industrial & Commercial Machinery & Equipment | 3.00 | 5 | 0 | 0 | 0 | 25 | Eaton Corp > Eaton Corp Plc |
| 287 | Agricultural Chemicals | 2.94 | 12 | 1 | 1 | 1 | 25 | Monsanto Co /New/ > Mosaic Co |
| 394 | Sporting & Athletic Goods, Nec | 2.73 | 16 | 2 | 2 | 0 | 25 | Mattel Inc /De/ > Hasbro, Inc. |
| 282 | Plastic Material, Synth Resin/Rubber, Cellulos (No Glass) | 2.58 | 16 | 2 | 2 | 0 | 0 | Dow Chemical Co /De/ > Dupont De Nemours, Inc. > Dow Inc. |
| 801 | Services-Offices & Clinics Of Doctors Of Medicine | 2.54 | 7 | 4 | 3 | 1 | 100 | Amsurg Corp > Envision Healthcare Corp > Teladoc Health, Inc. > Cano Health, Inc. |
| 738 | Services-Miscellaneous Business Services | 2.35 | 119 | 0 | 0 | 0 | 50 | Accenture Sca > Accenture Plc |
| 369 | Miscellaneous Electrical Machinery, Equipment & Supplies | 2.09 | 24 | 3 | 1 | 1 | 25 | Spectrum Brands Holdings, Inc. > Enersys > Atkore Inc. |
| 353 | Construction, Mining & Materials Handling Machinery & Equip | 1.85 | 27 | 0 | 0 | 0 | 50 | Caterpillar Inc |
| 280 | Chemicals & Allied Products | 1.81 | 14 | 1 | 1 | 1 | 50 | Huntsman Corp > Olin Corp |
| 104 | Gold And Silver Ores | 1.76 | 10 | 0 | 0 | 0 | 50 | Newmont Corp /De/ |
| 399 | Miscellaneous Manufacturing Industries | 1.65 | 13 | 2 | 1 | 1 | 75 | International Game Technology > Hillenbrand, Inc. > Amcor Plc |
| 356 | General Industrial Machinery & Equipment | 1.52 | 31 | 0 | 0 | 0 | 50 | Illinois Tool Works Inc |
| 289 | Miscellaneous Chemical Products | 1.43 | 13 | 4 | 3 | 0 | 50 | Cabot Corp > Element Solutions Inc > Fuller H B Co |
| 381 | Search, Detection, Navagation, Guidance, Aeronautical Sys | 1.40 | 10 | 0 | 0 | 0 | 25 | Northrop Grumman Corp /De/ |
| 286 | Industrial Organic Chemicals | 1.23 | 32 | 0 | 0 | 0 | 25 | Lyondellbasell Industries N.V. |
| 489 | Communications Services, Nec | 1.04 | 23 | 2 | 2 | 1 | 50 | Directv > Dish Dbs Corp > Echostar Corp |
| 374 | Railroad Equipment | 0.99 | 4 | 1 | 1 | 1 | 25 | Trinity Industries Inc > Westinghouse Air Brake Technologies Corp |
| 820 | Services-Educational Services | 0.97 | 25 | 3 | 2 | 1 | 50 | Apollo Education Group Inc > Graham Holdings Co > Laureate Education, Inc. |
| 138 | Oil & Gas Field Services, Nec | 0.94 | 58 | 0 | 0 | 0 | 50 | Slb Limited/Nv |
| 371 | Motor Homes | 0.83 | 61 | 2 | 1 | 0 | 25 | General Motors Co > Ford Motor Co |
| 731 | Services-Advertising | 0.76 | 27 | 0 | 0 | 0 | 50 | Omnicom Group Inc. |
| 358 | Refrigeration & Service Industry Machinery | 0.72 | 11 | 0 | 0 | 0 | 25 | Johnson Controls International Plc |
| 281 | Industrial Inorganic Chemicals | 0.67 | 12 | 1 | 1 | 1 | 75 | Praxair Inc > Linde Plc |
| 140 | Mining & Quarrying Of Nonmetallic Minerals (No Fuels) | 0.66 | 15 | 1 | 1 | 1 | 25 | Mdu Resources Group Inc > Vulcan Materials Co |
| 335 | Rolling Drawing & Extruding Of Nonferrous Metals | 0.59 | 12 | 1 | 1 | 1 | 25 | Howmet Aerospace Inc. > Novelis Inc. |
| 308 | Miscellaneous Plastics Products | 0.56 | 18 | 1 | 1 | 1 | 50 | Newell Brands Inc. > Berry Global Group, Inc. |
| 363 | Household Appliances | 0.54 | 7 | 0 | 0 | 0 | 25 | Whirlpool Corp /De/ |
| 781 | Services-Allied To Motion Picture Production | 0.53 | 8 | 1 | 0 | 1 | 75 | Starz Entertainment Corp /Cn/ > Lionsgate Studios Corp. |
| 271 | Newspapers: Publishing Or Publishing & Printing | 0.50 | 9 | 0 | 0 | 0 | 25 | News Corp |
| 344 | Fabricated Structural Metal Products | 0.37 | 13 | 3 | 3 | 1 | 25 | Mcdermott International Inc > Valmont Industries Inc > Cornerstone Building Brands, Inc. |
| 720 | Services-Personal Services | 0.36 | 17 | 1 | 1 | 1 | 50 | H&R Block Inc > Service Corp International |
| 346 | Metal Forgings & Stampings | 0.31 | 5 | 3 | 3 | 0 | 0 | Materion Corp > Trimas Corp > Park Ohio Holdings Corp |
| 200 | Food And Kindred Products | 0.26 | 14 | 0 | 0 | 0 | 25 | Mondelez International, Inc. |
| 483 | Television Broadcasting Stations | 0.25 | 26 | 0 | 0 | 0 | 50 | Paramount Global |
| 507 | Wholesale-Hardware & Plumbing & Heating Equipment & Supplies | 0.24 | 5 | 2 | 2 | 1 | 75 | Watsco Inc > Resideo Technologies, Inc. > Ferguson Plc > Ferguson Enterprises Inc. /De/ |
| 590 | Retail-Miscellaneous Retail | 0.23 | 16 | 4 | 2 | 1 | 50 | Ferrellgas Partners L P > Party City Holdco Inc. > Firstcash Holdings, Inc. |
| 364 | Electric Lighting & Wiring Equipment | 0.23 | 10 | 1 | 1 | 1 | 50 | Cooper Industries Plc > Acuity Inc. (De) |
| 470 | Transportation Services | 0.22 | 12 | 2 | 2 | 0 | 50 | Booking Holdings Inc. > Xpo, Inc. |
| 251 | Household Furniture | 0.21 | 13 | 1 | 1 | 1 | 50 | Leggett & Platt Inc > Somnigroup International Inc. |
| 376 | Guided Missiles & Space Vehicles & Parts | 0.19 | 6 | 0 | 0 | 0 | 75 | Lockheed Martin Corp |
| 484 | Cable & Other Pay Television Services | 0.14 | 22 | 0 | 0 | 0 | 50 | Comcast Corp |
| 284 | Soap, Detergents, Cleang Preparations, Perfumes, Cosmetics | 0.13 | 22 | 0 | 0 | 0 | 50 | Procter & Gamble Co |
| 170 | Construction - Special Trade Contractors | 0.10 | 12 | 1 | 1 | 1 | 75 | Chicago Bridge & Iron Co N V > Topbuild Corp |
| 874 | Services-Facilities Support Management Services | 0.09 | 39 | 0 | 0 | 0 | 75 | Booz Allen Hamilton Holding Corp |
| 267 | Converted Paper & Paperboard Prods (No Contaners/Boxes) | 0.07 | 6 | 0 | 0 | 0 | 50 | Kimberly Clark Corp |
| 809 | Services-Misc Health & Allied Services, Nec | 0.07 | 15 | 0 | 0 | 0 | 75 | Davita Inc. |
| 701 | Hotels & Motels | 0.06 | 31 | 2 | 2 | 0 | 0 | Marriott International Inc /Md/ > Las Vegas Sands Corp |
| 503 | Wholesale-Lumber & Other Construction Materials | 0.05 | 8 | 5 | 2 | 1 | 0 | Boise Cascade Holdings, L.L.C. > Boise Cascade Co > Beacon Roofing Supply Inc |
| 262 | Paper Mills | 0.04 | 9 | 0 | 0 | 0 | 50 | International Paper Co /New/ |
| 354 | Metalworkg Machinery & Equipment | 0.04 | 8 | 1 | 1 | 1 | 25 | Spx Technologies, Inc. > Lincoln Electric Holdings Inc |
| 512 | Wholesale-Drugs, Proprietaries & Druggists' Sundries | 0.04 | 11 | 0 | 0 | 0 | 0 | Mckesson Corp |
| 70 | Agricultural Services | 0.03 | 7 | 1 | 1 | 1 | 50 | Vca Inc > Brightview Holdings, Inc. |
| 596 | Retail-Nonstore Retailers | 0.03 | 24 | 0 | 0 | 0 | 25 | Amazon Com Inc |
| 799 | Services-Miscellaneous Amusement & Recreation | 0.03 | 21 | 0 | 0 | 0 | 50 | Walt Disney Co/ > Walt Disney Co |
| 790 | Services-Amusement & Recreation Services | 0.03 | 13 | 2 | 1 | 0 | 75 | Live Nation Entertainment, Inc. > Warner Music Group Corp. |
| 342 | Cutlery, Handtools & General Hardware | 0.03 | 10 | 0 | 0 | 0 | 25 | Stanley Black & Decker, Inc. |
| 751 | Services-Auto Rental & Leasing (No Drivers) | 0.02 | 7 | 5 | 2 | 1 | 0 | Hertz Corp > Hertz Global Holdings, Inc > Avis Budget Group, Inc. > Ryder System Inc |
| 100 | Metal Mining | 0.02 | 8 | 2 | 1 | 0 | 25 | Freeport-Mcmoran Inc > Cleveland-Cliffs Inc. |
| 871 | Services-Engineering Services | 0.02 | 11 | 1 | 1 | 1 | 50 | Urs Corp /New/ > Aecom |
| 331 | Steel Works, Blast Furnaces & Rolling & Finishing Mills | 0.02 | 19 | 0 | 0 | 0 | 0 | Nucor Corp |
| 481 | Telephone Communications (No Radiotelephone) | 0.02 | 38 | 1 | 1 | 1 | 25 | At&T Inc. > Verizon Communications Inc |
| 245 | Prefabricated Wood Bldgs & Components | 0.01 | 5 | 1 | 1 | 1 | 25 | Cavco Industries, Inc. > Champion Homes, Inc. |
| 131 | Crude Petroleum & Natural Gas | 0.01 | 133 | 4 | 2 | 1 | 75 | Murphy Oil Corp > Occidental Petroleum Corp /De/ > Expand Energy Corp > Devon Energy Corp/De |
| 504 | Wholesale-Professional & Commercial Equipment & Supplies | 0.01 | 14 | 2 | 2 | 1 | 25 | Ingram Micro Inc > Tech Data Corp > Td Synnex Corp |
| 736 | Services-Help Supply Services | 0.01 | 26 | 0 | 0 | 0 | 25 | Manpowergroup Inc. |
| 805 | Services-Nursing & Personal Care Facilities | 0.01 | 10 | 3 | 2 | 1 | 75 | Kindred Healthcare, Inc > Genesis Healthcare, Inc. > Brookdale Senior Living Inc. > Ensign Group, Inc |
| 495 | Sanitary Services | 0.01 | 18 | 0 | 0 | 0 | 25 | Waste Management Inc |
| 162 | Water, Sewer, Pipeline, Comm & Power Line Construction | 0.01 | 8 | 0 | 0 | 0 | 25 | Mastec Inc |
| 599 | Retail-Retail Stores, Nec | 0.01 | 12 | 1 | 1 | 1 | 50 | Bath & Body Works, Inc. > Ulta Beauty, Inc. |
| 204 | Grain Mill Products | 0.00 | 7 | 0 | 0 | 0 | 25 | General Mills Inc |
| 211 | Cigarettes | 0.00 | 6 | 0 | 0 | 0 | 50 | Philip Morris International Inc. |
| 506 | Wholesale-Electrical Appliances, Tv & Radio Sets | 0.00 | 16 | 1 | 1 | 1 | 25 | Avnet Inc > Arrow Electronics, Inc. |
| 581 | Retail-Eating & Drinking Places | 0.00 | 64 | 1 | 1 | 1 | 25 | Mcdonalds Corp > Starbucks Corp |
| 509 | Wholesale-Misc Durable Goods | 0.00 | 6 | 1 | 1 | 1 | 25 | Spectrum Group International, Inc. > A-Mark Precious Metals, Inc. |
| 520 | Retail-Building Materials, Hardware, Garden Supply | 0.00 | 5 | 0 | 0 | 0 | 25 | Sherwin Williams Co |
| 207 | Fats & Oils | 0.00 | 5 | 0 | 0 | 0 | 25 | Archer-Daniels-Midland Co |
| 373 | Ship & Boat Building & Repairing | 0.00 | 5 | 0 | 0 | 0 | 25 | General Dynamics Corp |
| 349 | Miscellaneous Fabricated Metal Products | 0.00 | 8 | 0 | 0 | 0 | 25 | Parker-Hannifin Corp |
| 203 | Canned, Frozen & Preservd Fruit, Veg & Food Specialties | 0.00 | 8 | 2 | 1 | 1 | 50 | Heinz H J Co > J M Smucker Co > Kraft Heinz Co |
| 201 | Poultry Slaughtering And Processing | 0.00 | 7 | 0 | 0 | 0 | 0 | Tyson Foods, Inc. |
| 514 | Wholesale-Groceries & Related Products | 0.00 | 16 | 0 | 0 | 0 | 50 | Sysco Corp |
| 230 | Apparel & Other Finishd Prods Of Fabrics & Similar Matl | 0.00 | 12 | 4 | 3 | 1 | 25 | Levi Strauss & Co > Under Armour, Inc. > Lululemon Athletica Inc. |
| 160 | Heavy Construction Other Than Bldg Const - Contractors | 0.00 | 10 | 2 | 1 | 0 | 25 | Fluor Corp > Jacobs Solutions Inc. |
| 265 | Paperboard Containers & Boxes | 0.00 | 6 | 2 | 1 | 1 | 25 | Rock-Tenn Co > Westrock Co > Smurfit Westrock Plc |
| 591 | Retail-Drug Stores And Proprietary Stores | 0.00 | 10 | 0 | 0 | 0 | 75 | Cvs Health Corp |
| 515 | Wholesale-Farm Product Raw Materials | 0.00 | 5 | 0 | 0 | 0 | 25 | Chs Inc |
| 550 | Retail-Auto Dealers & Gasoline Stations | 0.00 | 20 | 4 | 4 | 1 | 50 | Murphy Usa Inc. > Autonation, Inc. > Penske Automotive Group, Inc. > Carmax Inc > Lithia Motors Inc |
| 451 | Air Transportation, Scheduled | 0.00 | 17 | 0 | 0 | 0 | 25 | Fedex Corp |
| 208 | Beverages | 0.00 | 29 | 0 | 0 | 0 | 0 | Pepsico Inc |
| 806 | Services-Hospitals | 0.00 | 16 | 0 | 0 | 0 | 0 | Hca Healthcare, Inc. |
| 594 | Retail-Miscellaneous Shopping Goods Stores | 0.00 | 15 | 2 | 2 | 1 | 75 | Staples Inc > Odp Corp > Dick's Sporting Goods, Inc. |
| 291 | Petroleum Refining | 0.00 | 21 | 0 | 0 | 0 | 25 | Exxon Mobil Corp |
| 232 | Men's & Boys' Furnishgs, Work Clothg, & Allied Garments | 0.00 | 7 | 1 | 0 | 1 | 0 | V F Corp > Cintas Corp |
| 122 | Bituminous Coal & Lignite Mining | 0.00 | 14 | 0 | 0 | 0 | 50 | Peabody Energy Corp |
| 209 | Miscellaneous Food Preparations & Kindred Products | 0.00 | 9 | 2 | 2 | 0 | 50 | Mccormick & Co Inc > Keurig Green Mountain, Inc. |
| 808 | Services-Home Health Care Services | 0.00 | 8 | 4 | 3 | 1 | 50 | Apria Healthcare Group Inc > Chemed Corp > Lhc Group, Inc > Option Care Health, Inc. > Brightspring Health Services, Inc. |
| 401 | Railroad Switching & Terminal Establishments | 0.00 | 8 | 6 | 2 | 0 | 25 | Union Pacific Corp > Burlington Northern Santa Fe, Llc |
| 341 | Metal Shipping Barrels, Drums, Kegs & Pails | 0.00 | 4 | 6 | 3 | 0 | 0 | Crown Holdings, Inc. > Ball Corp |
| 421 | Trucking & Courier Services (No Air) | 0.00 | 19 | 0 | 0 | 0 | 50 | United Parcel Service Inc |
| 153 | Operative Builders | 0.00 | 19 | 1 | 1 | 1 | 50 | Pultegroup Inc/Mi/ > Horton D R Inc /De/ |
| 440 | Water Transportation | 0.00 | 11 | 2 | 1 | 0 | 0 | Carnival Corp > Matson, Inc. |
| 441 | Deep Sea Foreign Transportation Of Freight | 0.00 | 7 | 4 | 0 | 1 | 50 | Seacor Holdings Inc /New/ > Pangaea Logistics Solutions Ltd. > Eagle Bulk Shipping Inc. > Dorian Lpg Ltd. |
| 783 | Services-Motion Picture Theaters | 0.00 | 7 | 1 | 1 | 1 | 25 | Regal Entertainment Group > Amc Entertainment Holdings, Inc. |
| 461 | Pipe Lines (No Natural Gas) | 0.00 | 16 | 2 | 2 | 0 | 50 | Plains All American Pipeline Lp > Energy Transfer Operating, L.P. |
| 521 | Retail-Lumber & Other Building Materials Dealers | 0.00 | 7 | 0 | 0 | 0 | 25 | Home Depot, Inc. |
| 735 | Services-Miscellaneous Equipment Rental & Leasing | 0.00 | 33 | 1 | 1 | 1 | 50 | Herc Holdings Inc > United Rentals, Inc. |
| 473 | Arrangement Of Transportation Of Freight & Cargo | 0.00 | 9 | 0 | 0 | 0 | 25 | C. H. Robinson Worldwide, Inc. |
| 517 | Wholesale-Petroleum Bulk Stations & Terminals | 0.00 | 8 | 0 | 0 | 0 | 50 | World Kinect Corp |
| 541 | Retail-Grocery Stores | 0.00 | 13 | 0 | 0 | 0 | 50 | Kroger Co |
| 553 | Retail-Auto & Home Supply Stores | 0.00 | 6 | 2 | 1 | 0 | 25 | Autozone Inc > Advance Auto Parts Inc |
| 560 | Retail-Apparel & Accessory Stores | 0.00 | 13 | 4 | 3 | 0 | 75 | Hanesbrands Inc. > Ascena Retail Group, Inc. |
| 565 | Retail-Family Clothing Stores | 0.00 | 12 | 0 | 0 | 0 | 0 | Tjx Companies Inc /De/ |
| 566 | Retail-Shoe Stores | 0.00 | 6 | 0 | 0 | 0 | 25 | Foot Locker, Inc. |
| 519 | Wholesale-Miscellaneous Nondurable Goods | 0.00 | 5 | 1 | 1 | 1 | 50 | Jarden Corp > Central Garden & Pet Co |
| 508 | Wholesale-Machinery, Equipment & Supplies | 0.00 | 12 | 3 | 2 | 1 | 50 | Mrc Global Inc. > Airgas Inc > Applied Industrial Technologies Inc |
| 533 | Retail-Variety Stores | 0.00 | 12 | 0 | 0 | 0 | 0 | Walmart Inc. |
| 505 | Wholesale-Metals & Minerals (No Petroleum) | 0.00 | 7 | 0 | 0 | 0 | 25 | Reliance, Inc. |
| 314 | Footwear, (No Rubber) | 0.00 | 6 | 2 | 2 | 1 | 25 | Caleres Inc > Wolverine World Wide Inc /De/ > Skechers Usa Inc |
| 206 | Sugar & Confectionery Products | 0.00 | 6 | 0 | 0 | 0 | 50 | Hershey Co |
| 310 | Leather & Leather Products | 0.00 | 4 | 4 | 3 | 0 | 25 | Tapestry, Inc. > Capri Holdings Ltd |
| 173 | Electrical Work | 0.00 | 4 | 1 | 1 | 1 | 25 | Emcor Group, Inc. > Quanta Services, Inc. |
| 732 | Services-Consumer Credit Reporting, Collection Agencies | 0.00 | 7 | 0 | 0 | 0 | 25 | S&P Global Inc. |
| 531 | Retail-Department Stores | 0.00 | 8 | 1 | 1 | 1 | 50 | Sears Holdings Corp > Macy's, Inc. |
