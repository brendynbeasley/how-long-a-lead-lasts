"""Jones's (1995) counter-test of Aghion and Howitt (1992): does more research mean faster growth?

In Aghion and Howitt's balanced growth path the average growth rate is

    AGR = lambda * n * ln(gamma)

where n is the amount of labor in research, lambda the productivity of research and gamma
the size of each innovation. Holding lambda and gamma fixed, growth should rise in proportion
to research effort. Jones (1995) pointed out that US research effort had multiplied while
productivity growth had not. This script reruns that comparison on 1950-2025 US data.

Inputs (FRED, no key; downloaded once into data/raw/fred/ and committed):
    MFPNFBS            BLS total factor productivity, private nonfarm business, index
    Y006RC1A027NBEA    BEA private R&D investment, billions of current dollars
    Y694RC1A027NBEA    BEA total R&D (private plus government), billions of current dollars
    GDPA               BEA nominal GDP, billions of current dollars
    COMPNFB            BLS hourly compensation, nonfarm business, index (quarterly)

Outputs (results/):
    scale_decades.csv      decade averages of TFP growth, research effort and intensity
    scale_regressions.csv  time-series regressions with Newey-West standard errors
    scale_annual.csv       the annual series used
    scale_effects.png      research effort against TFP growth

Usage:
    python src/scale_effects.py
"""

from io import StringIO
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
FRED_DIR = ROOT / "data" / "raw" / "fred"
OUT = ROOT / "results"

SERIES = ["MFPNFBS", "Y006RC1A027NBEA", "Y694RC1A027NBEA", "GDPA", "COMPNFB"]
FIRST_YEAR = 1950       # first full decade with a TFP growth rate (the BLS index starts in 1948)
LAST_YEAR = 2025        # last complete year in every series
HAC_LAGS = 4            # Newey-West lags for annual data (rule of thumb 0.75 * T^(1/3), T = 77)
BASE_DECADE = "1950s"   # research effort is expressed relative to this decade


def fred(series_id):
    """Return one FRED series as an annual pandas Series, downloading it once."""
    path = FRED_DIR / f"{series_id}.csv"
    if not path.exists():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        FRED_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(r.text)
    df = pd.read_csv(path)
    df.columns = ["date", "value"]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna()
    df["year"] = pd.to_datetime(df["date"]).dt.year
    annual = df.groupby("year")["value"].mean()   # quarterly COMPNFB becomes an annual average
    print(f"  {series_id}: {len(df)} observations, {annual.index.min()}-{annual.index.max()}")
    return annual


def newey_west(y, X, label, rows):
    """OLS with Newey-West (HAC) standard errors; append the slope to rows."""
    X = sm.add_constant(X)
    fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": HAC_LAGS})
    name = X.columns[1]
    ci = fit.conf_int().loc[name]
    rows.append(dict(model=label, regressor=name, slope=fit.params[name], se=fit.bse[name],
                     ci_low=ci[0], ci_high=ci[1], p=fit.pvalues[name], n=int(fit.nobs),
                     r2=fit.rsquared))
    return fit


def main():
    OUT.mkdir(exist_ok=True)
    print("Loading FRED series")
    s = {k: fred(k) for k in SERIES}
    df = pd.DataFrame({
        "tfp": s["MFPNFBS"],
        "rd_private": s["Y006RC1A027NBEA"],
        "rd_total": s["Y694RC1A027NBEA"],
        "gdp": s["GDPA"],
        "wage": s["COMPNFB"],
    })
    df["tfp_growth"] = 100 * np.log(df["tfp"]).diff()
    df = df.loc[FIRST_YEAR:LAST_YEAR].copy()
    before = len(df)
    df = df.dropna()
    print(f"Annual panel {FIRST_YEAR}-{LAST_YEAR}: kept {len(df)} years, dropped {before - len(df)} "
          "with a missing series")

    # Effective research effort: R&D spending divided by the hourly wage, as in Bloom, Jones,
    # Van Reenen and Webb (2020). It counts how many hours of work the R&D budget could buy.
    df["effort"] = df["rd_private"] / df["wage"]
    df["intensity"] = 100 * df["rd_private"] / df["gdp"]
    df["intensity_total"] = 100 * df["rd_total"] / df["gdp"]
    df["decade"] = (df.index // 10 * 10).astype(str) + "s"

    dec = df.groupby("decade").agg(
        first_year=("tfp", lambda x: x.index.min()), last_year=("tfp", lambda x: x.index.max()),
        tfp_growth=("tfp_growth", "mean"), effort=("effort", "mean"),
        intensity=("intensity", "mean"), intensity_total=("intensity_total", "mean"),
        rd_private_bn=("rd_private", "mean"))
    base = dec.loc[BASE_DECADE]
    dec["effort_index"] = dec["effort"] / base["effort"]
    # Aghion-Howitt research productivity, lambda * ln(gamma) = growth / effort, relative to base
    dec["growth_per_effort_index"] = (dec["tfp_growth"] / dec["effort_index"]) / base["tfp_growth"]
    dec["growth_per_intensity"] = dec["tfp_growth"] / dec["intensity"]
    dec = dec.drop(columns="effort").reset_index()
    dec.to_csv(OUT / "scale_decades.csv", index=False, float_format="%.4f")
    print("\nDecade averages")
    print(dec[["decade", "tfp_growth", "effort_index", "intensity", "growth_per_effort_index"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    rows = []
    df["log_effort"] = np.log(df["effort"])
    df["trend"] = df.index - FIRST_YEAR
    newey_west(df["tfp_growth"], df[["log_effort"]], "AH scale effect: growth on log research effort", rows)
    newey_west(df["tfp_growth"], df[["intensity"]], "Non-scale Schumpeterian: growth on R&D share of GDP", rows)
    newey_west(df["tfp_growth"], df[["trend"]], "Jones: growth on a linear trend (per year)", rows)
    # A decade-average version removes most of the year-to-year noise in measured TFP
    dd = df.groupby("decade")[["tfp_growth", "log_effort", "intensity"]].mean()
    for col, label in [("log_effort", "Decade means: growth on log research effort"),
                       ("intensity", "Decade means: growth on R&D share of GDP")]:
        X = sm.add_constant(dd[[col]])
        fit = sm.OLS(dd["tfp_growth"], X).fit(cov_type="HC1")
        ci = fit.conf_int().loc[col]
        rows.append(dict(model=label, regressor=col, slope=fit.params[col], se=fit.bse[col],
                         ci_low=ci[0], ci_high=ci[1], p=fit.pvalues[col], n=int(fit.nobs),
                         r2=fit.rsquared))
    reg = pd.DataFrame(rows)
    reg.to_csv(OUT / "scale_regressions.csv", index=False, float_format="%.5f")
    print("\nRegressions (Newey-West SE for annual, HC1 for decade means)")
    print(reg.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    keep = ["tfp", "tfp_growth", "rd_private", "rd_total", "gdp", "wage", "effort", "intensity",
            "intensity_total"]
    df[keep].to_csv(OUT / "scale_annual.csv", index_label="year", float_format="%.5f")

    # Figure: research effort (index) and ten-year average TFP growth
    effort_idx = df["effort"] / df.loc[1950:1959, "effort"].mean()
    roll = df["tfp_growth"].rolling(10).mean()
    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    ax1.plot(df.index, effort_idx, color="#1f5f99", lw=2)
    ax1.set_yscale("log")
    ax1.set_ylabel("Research effort, 1950s = 1 (log scale)", color="#1f5f99")
    ax2 = ax1.twinx()
    ax2.bar(df.index, df["tfp_growth"], color="#bbbbbb", width=0.8)
    ax2.plot(df.index, roll, color="#b5432a", lw=2)
    ax2.axhline(0, color="black", lw=0.5)
    ax2.set_ylabel("TFP growth, % a year (bars), 10-year average (line)", color="#b5432a")
    ax1.set_zorder(ax2.get_zorder() + 1)
    ax1.patch.set_visible(False)
    ax1.set_title(f"US private R&D effort and productivity growth, {FIRST_YEAR}-{LAST_YEAR}")
    fig.text(0.01, 0.01, "Sources: BEA private R&D investment over BLS hourly compensation; "
             "BLS private nonfarm business TFP (via FRED).", fontsize=7, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "scale_effects.png", dpi=150)
    print("\nWrote scale_decades.csv, scale_regressions.csv, scale_annual.csv, scale_effects.png")


if __name__ == "__main__":
    main()
