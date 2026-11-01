# Technical notes

This is the technical companion to the [README](README.md). It covers the data, the method, the full set of tests
and how to reproduce everything. Every table is in [results/FINDINGS.md](results/FINDINGS.md), and a review of the
original paper's methods is in [METHODS_REVIEW.md](METHODS_REVIEW.md).

## The original study

Philippe Aghion and Peter Howitt, "A Model of Growth Through Creative Destruction," *Econometrica* 60(2), March
1992, pp. 323–351; first circulated as NBER Working Paper 3223, January 1990. The paper is theoretical and has no
data. Innovations arrive as a Poisson process with rate $`\lambda n`$, where $`n`$ is research labor; each one is a
patent that earns monopoly profit $`\pi`$ until the next arrives. Its headline results, checked against the working
paper's equations 2.17 and 4.8 and the published abstract, are the value of an innovation and the average growth
rate on the balanced growth path.

```math
V = \frac{\pi}{r + \lambda n}, \qquad \text{AGR} = \lambda \hat{n} \ln \gamma
```

The working paper writes $`\gamma < 1`$ as the factor by which each innovation cuts unit cost and so has
$`\text{AGR} = -\lambda \hat{n} \ln \gamma`$; I write $`\gamma > 1`$ for the productivity step, which is the same
thing. Research, and so growth, rises with $`\lambda`$, with the step size and with the labor force, and falls with
$`r`$ (Proposition 3). The paper gives no empirical headline number.

## Headline results

| Test | Estimate | 95% CI | p | N |
|---|---|---|---|---|
| Leader-replacement hazard on R&D intensity (pp per pp), 3-digit SIC | 0.233 (0.230) | −0.217 to 0.683 | 0.31 | 141 |
| Intercept (hazard with no R&D, % a year) | 9.20 (1.05) | | | 141 |
| Same, 4-digit SIC | 0.036 (0.226) | −0.407 to 0.478 | 0.87 | 179 |
| Lasting changes only, 3-digit SIC | 0.233 (0.141) | −0.043 to 0.509 | 0.098 | 141 |
| 2024 leader differs from 2011 leader (pp per pp), 3-digit SIC | 4.25 (0.89) | 2.51 to 6.00 | < 0.001 | 141 |
| Same, without the 4 industries above 8% R&D | 5.13 (2.45) | 0.32 to 9.94 | 0.037 | 137 |
| Same, 4-digit SIC | 0.44 (0.91) | −1.34 to 2.22 | 0.63 | 179 |
| TFP growth on log research effort, 1950–2025 | −0.525 (0.232) | −0.981 to −0.070 | 0.024 | 76 |
| TFP growth on private R&D share of GDP | −0.531 (0.302) | −1.124 to 0.061 | 0.079 | 76 |

The pooled leader-replacement hazard is 9.49% a year (174 changes in 1,833 industry-years), an expected tenure of
10.5 years. By R&D group it is 9.7%, 7.7%, 11.7% and 11.5% from no R&D to 8% or more of revenue. Research effort
in the 2020s is 11.0 times its 1950s level, while TFP growth fell from 1.87% to 1.03% a year.

## Data

- **Firm financials:** SEC Financial Statement Data Sets, all 58 quarterly files from 2012q1 to 2026q2
  (`fsds_YYYYqN.zip`, about 5 GB, read into `data/raw/sec/` and ignored by git). Only `sub.txt` (filer, SIC code,
  form, period) and `num.txt` (tagged values) are used. `src/build_sec_panel.py` reduces them to the committed
  files `data/raw/sec_firm_years.csv.gz` (72,184 firm-years, 10,397 filers, fiscal 2011–2024) and
  `data/raw/sec_sic.csv`. During the build the SEC was refusing requests from this machine's shared address, so
  the zips came from the Internet Archive's captures of the same sec.gov URLs; the script tries sec.gov first.
- **Industry titles:** `data/raw/sic_codes.csv`, the SEC's SIC code list (sec.gov page "Standard Industrial
  Classification (SIC) Code List," Internet Archive capture of October 1, 2026).
- **National accounts (FRED, committed in `data/raw/fred/`):** MFPNFBS (BLS total factor productivity, private
  nonfarm business, 1948–2025), Y006RC1A027NBEA (BEA private R&D investment), Y694RC1A027NBEA (BEA total R&D),
  GDPA (BEA GDP), COMPNFB (BLS hourly compensation, nonfarm business, quarterly), DFII10 (10-year TIPS yield).
  Downloaded November 1, 2026.

## Method

Rules fixed before looking at results, with two coverage repairs noted under Panel and Leader:

- **Panel.** 10-K filings only; consolidated, four-quarter, US-dollar values of standard us-gaap tags. Revenue is the
  largest of 17 total-revenue tags (listed in `src/build_sec_panel.py`) plus Exxon Mobil's own tag for its 2011–2016
  filings; R&D is the largest of three R&D tags; untagged R&D counts as zero. A first pass used only the five most
  common revenue tags, which dropped HCA, ManpowerGroup, Carnival, Newmont, Avis Budget and Exxon Mobil for most of
  2011–2017 and created a false leader change whenever one reappeared. The list was widened to fix that coverage
  before the tests below were run; companies that used only their own tags (D.R. Horton before 2016) are still
  missing for those years. A fiscal year ending
  July–December belongs to that calendar year, January–June to the year before (the SEC frames convention). The
  value from the filing in which the year is current wins over a later comparison column.
- **Industries.** Three-digit SIC from each filer's latest 10-K. Excluded: SIC 6000–6799 (finance, insurance, real
  estate), 4900–4949 (regulated utilities), 9100–9999 and 0. Firm-years under $1 million of revenue dropped. An
  industry needs four or more filers with revenue in every year 2011–2024. One-year interior gaps in a filer's
  revenue are filled by linear interpolation.
- **Leader.** The filer with the most revenue in the industry-year. Filers whose names share the first distinctive
  word (Eaton Corp and Eaton Corp plc; Hertz Corp and Hertz Global) count as one company, as do two holding-company
  renames found by reading every industry's list of leaders (Google Inc to Alphabet, iHeartCommunications to
  iHeartMedia). Walt Disney's pre-2019 SEC number, coded 4841 on its last 10-K, is moved to its successor's 7990.
- **Measures.** With $`C_j`$ leader changes over $`T_j = 13`$ transitions and research intensity $`n_j`$,

```math
\begin{aligned}
h_j &= \frac{C_j}{T_j} \\
n_j &= \frac{\sum_{i \in j}\sum_{t=2011}^{2024} RD_{it}}{\sum_{i \in j}\sum_{t=2011}^{2024} Rev_{it}}
\end{aligned}
```

- **Main test.** The model implies $`h_j = \lambda n_j`$, so the estimating equation and hypotheses are

```math
\begin{aligned}
100\,h_j &= \alpha + \beta \cdot 100\,n_j + \varepsilon_j \\
H_0&:\ \beta = 0, \qquad \text{model: } \alpha = 0,\ \beta > 0
\end{aligned}
```

  estimated by OLS with HC1 standard errors. Robustness: controls for log mean filers and annual industry revenue
  growth; R&D measured in 2011–2013 only; lasting changes; whether the 2024 leader differs from the 2011 leader
  (linear probability); top-4 turnover; a Poisson model of $`C_j`$ with offset
  $`\ln T_j`$ and the same controls; Spearman correlation; 4-digit SIC; industries with ten or more filers;
  industries under 8% R&D. Group hazards use exact Poisson intervals for the pooled count.
- **Extension (Jones 1995).** Effort $`R_t`$ is private R&D divided by hourly compensation; $`g_t`$ is 100 times the
  log change in TFP, 1950–2025.

```math
g_t = a + b \ln R_t + u_t, \qquad g_t = a' + b' s_t + u'_t, \qquad s_t = 100 \cdot \frac{RD_t}{GDP_t}
```

  OLS with Newey-West standard errors, four lags; decade-mean versions with HC1.
- **Worked examples.** $`V/\pi = 1/(r + h)`$ with $`r`$ the 2011–2024 mean TIPS yield (0.395%) and $`h`$ the pooled
  hazard (9.49%), giving 10.1; implied step $`\ln \gamma = g/h`$ with $`g`$ the 2011–2024 TFP growth rate (0.735% a
  year), giving 0.0774, a step of 8.0%.

## Full test statistics

Leader replacement, 3-digit SIC (N = 141): with controls 0.476 (0.326), p = 0.14; 2011–2013 R&D 0.122 (0.279),
p = 0.66; top-4 turnover −0.051 (0.434), p = 0.91; Poisson with controls 0.047 (0.031), p = 0.13; Spearman
ρ = 0.058, p = 0.49. 4-digit SIC (N = 179): with controls −0.058 (0.244); lasting changes 0.142 (0.212); top-4
turnover 0.550 (0.353), p = 0.12; Poisson −0.006 (0.025); Spearman ρ = −0.005. Industries with ten or more filers
(N = 86): hazard slope 0.260 (0.234), p = 0.27; end-of-period leader 4.71 (0.93), p < 0.001; top-4 turnover −0.594
(0.400), p = 0.14. Industries under 8% R&D (N = 137): hazard slope 0.225 (0.438), p = 0.61. The only specifications
with p below 0.10 are the end-of-period leader comparison at the 3-digit level, in every 3-digit sample, and the
lasting-change hazard at the 3-digit level (p = 0.098); neither holds at the 4-digit level. National accounts:
trend in TFP growth −0.0158 points a year (0.0078), p = 0.042; decade means on log effort −0.430 (0.170), p = 0.011,
N = 8.

## Reproducing the results

```bash
pip install -r requirements.txt
python src/build_sec_panel.py        # optional: rebuilds the committed SEC panel from the FSDS zips (about 5 GB)
python src/creative_destruction.py   # main test, tables, figure
python src/scale_effects.py          # extension
```

The last two run offline from the committed files and take under a minute.

## Repository layout

| Path | What it is |
|---|---|
| `src/build_sec_panel.py` | FSDS zips to the firm-year panel and SIC table |
| `src/creative_destruction.py` | Leader hazards, regressions, value and step examples, figure |
| `src/scale_effects.py` | Research effort and TFP growth, 1950–2025 |
| `data/raw/` | Compact SEC panel, SIC list, FRED series |
| `results/` | CSVs, figures and FINDINGS.md |

## References

- Aghion, P. & Howitt, P. (1992). A model of growth through creative destruction. *Econometrica* 60(2), 323–351.
- Bloom, N., Jones, C. I., Van Reenen, J. & Webb, M. (2020). Are ideas getting harder to find? *American Economic
  Review* 110(4), 1104 ff.
- Garcia-Macia, D., Hsieh, C.-T. & Klenow, P. J. (2016). How destructive is innovation? NBER Working Paper 22953.
- Jones, C. I. (1995). R&D-based models of economic growth. *Journal of Political Economy* 103, 759–784.
- Jones, C. I. (1995). Time series tests of endogenous growth models. *Quarterly Journal of Economics* 110,
  495–525.
- Schumpeter, J. A. (1942). *Capitalism, Socialism and Democracy*. Harper and Brothers.
