"""Aghion and Howitt (1992) on modern data: does research shorten an industry leader's reign?

In the model each innovation hands its owner a monopoly that lasts until the next innovation.
Innovations arrive as a Poisson process at rate lambda * n, where n is research effort, so the
incumbent's expected tenure is 1 / (lambda * n) and the value of its position is
pi / (r + lambda * n). The sharpest prediction a stranger can check is that market leaders are
displaced more often where more research is done.

The test, on every US company that files 10-K financial statements with the SEC:
    1. Assign each filer to a 3-digit SIC industry (its SIC code on its latest 10-K).
    2. Rank filers in each industry by revenue in each fiscal year 2011-2024.
    3. Count the years in which the revenue leader changed (13 possible changes).
    4. Measure research intensity as industry R&D expense / industry revenue, 2011-2024.
    5. Regress the annual leader-replacement rate on research intensity.

Inputs (committed): data/raw/sec_firm_years.csv.gz and data/raw/sec_sic.csv, written by
src/build_sec_panel.py from the SEC Financial Statement Data Sets; data/raw/sic_codes.csv, the
SEC's list of SIC industry titles; and FRED series DFII10 (10-year TIPS yield, downloaded once
into data/raw/fred/) for the worked example of the value formula.

Usage:
    python src/creative_destruction.py
"""

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

YEARS = list(range(2011, 2025))   # fiscal years covered by src/build_sec_panel.py

MIN_FIRMS = 4        # an industry needs at least 4 filers with revenue in every year (a top 4)
MIN_REVENUE = 1e6    # firm-years with under $1 million of revenue are treated as missing
# Judgment exclusions, fixed before looking at results:
#   6000-6799 finance, insurance and real estate: "revenue" is not comparable across filers
#   4900-4949 regulated electric, gas and water utilities: territories are granted, not won
#   9100-9999 public administration and non-classifiable establishments
EXCLUDED = [(6000, 6799), (4900, 4949), (9100, 9999)]
# Words that cannot identify a company on their own, skipped when matching re-registrations
GENERIC = {"THE", "GENERAL", "AMERICAN", "UNITED", "NATIONAL", "FIRST", "INTERNATIONAL", "US", "U",
           "S", "NEW", "GLOBAL", "WESTERN", "SOUTHERN", "NORTHERN", "EASTERN", "PACIFIC"}
# Holding-company reorganizations that changed both the SEC number and the name of a leader,
# found by reading every industry's sequence of leaders (results/industries_sic*.csv)
ALIASES = {"ALPHABET": "GOOGLE", "IHEARTCOMMUNICATIONS": "IHEARTMEDIA"}
# A re-registration that also changed industry code: Walt Disney's SEC number before its 2019
# reorganization (1001039, coded 4841 on its last 10-K) is placed with its successor (7990)
SIC_OVERRIDES = {1001039: 7990}
RD_GROUPS = [(-0.001, 0.0005, "No R&D (under 0.05% of revenue)"),
             (0.0005, 0.02, "Some R&D (0.05% to 2%)"),
             (0.02, 0.08, "R&D-intensive (2% to 8%)"),
             (0.08, 10.0, "Research-driven (8% or more)")]


def load_panel():
    if not (RAW / "sec_firm_years.csv.gz").exists() or not (RAW / "sec_sic.csv").exists():
        raise SystemExit("Run python src/build_sec_panel.py first to build the SEC panel.")
    fy = pd.read_csv(RAW / "sec_firm_years.csv.gz")
    sic = pd.read_csv(RAW / "sec_sic.csv")
    print(f"Loaded {len(fy):,} filer-years ({fy['cik'].nunique():,} filers), "
          f"{len(sic):,} SIC codes")
    df = fy.merge(sic[["cik", "sic", "name"]], on="cik", how="left").rename(columns={"name": "entity"})
    n0 = len(df)
    df = df.dropna(subset=["sic"])
    print(f"  dropped {n0 - len(df):,} filer-years with no SIC code on file")
    df["sic"] = df["sic"].astype(int)
    df["sic"] = df["cik"].map(SIC_OVERRIDES).fillna(df["sic"]).astype(int)
    excl = np.zeros(len(df), dtype=bool)
    for lo, hi in EXCLUDED:
        excl |= df["sic"].between(lo, hi).to_numpy()
    excl |= (df["sic"] == 0).to_numpy()
    print(f"  dropped {excl.sum():,} filer-years in finance, utilities, government or unclassified")
    df = df[~excl]
    n1 = len(df)
    df = df[df["revenue"] >= MIN_REVENUE]
    print(f"  dropped {n1 - len(df):,} filer-years with revenue under $1 million")
    df["rd"] = df["rd"].fillna(0.0).clip(lower=0)   # untagged R&D is treated as zero
    df["sic3"] = df["sic"] // 10
    return df


def fill_gaps(df):
    """Fill one-year interior holes in a filer's revenue series (a missing tag, not an exit)."""
    wide = df.pivot_table(index="cik", columns="year", values="revenue", aggfunc="max")
    wide = wide.reindex(columns=YEARS)
    filled = wide.interpolate(axis=1, limit=1, limit_area="inside")
    added = int(filled.notna().sum().sum() - wide.notna().sum().sum())
    print(f"  filled {added:,} one-year gaps inside filers' revenue series")
    long = filled.stack().dropna().rename("revenue").reset_index()
    return long


def company_key(name):
    """First distinctive word of a filer's name, so that a company that re-registers under a new
    SEC number (Eaton Corp to Eaton Corp plc, Hertz Corp to Hertz Global) is not counted as a
    new leader."""
    words = re.sub(r"[^A-Z0-9 ]", " ", str(name).upper()).split()
    words = [w for w in words if w not in GENERIC] or ["?"]
    return ALIASES.get(words[0], words[0])


def leader_stats(df, ind_col):
    """Industry-level leader changes, top-4 turnover and research intensity."""
    rev = fill_gaps(df)
    firm_ind = df.sort_values("year").groupby("cik")[[ind_col, "entity"]].last()
    rev = rev.join(firm_ind, on="cik")
    rev["key"] = rev["entity"].map(company_key)
    counts = rev.groupby([ind_col, "year"])["cik"].size().unstack(fill_value=0).reindex(columns=YEARS,
                                                                                        fill_value=0)
    keep = counts.index[(counts >= MIN_FIRMS).all(axis=1)]
    print(f"  {ind_col}: {len(counts)} industries, {len(keep)} have {MIN_FIRMS}+ filers in every "
          f"year {YEARS[0]}-{YEARS[-1]}")
    rev = rev[rev[ind_col].isin(keep)]
    rev = rev.sort_values([ind_col, "year", "revenue"], ascending=[True, True, False])
    rev["rank"] = rev.groupby([ind_col, "year"]).cumcount() + 1
    lead = rev[rev["rank"] == 1].set_index([ind_col, "year"])
    top4 = rev[rev["rank"] <= 4].groupby([ind_col, "year"])["key"].apply(set)
    tot = rev.groupby([ind_col, "year"])["revenue"].sum()

    sub = df[df[ind_col].isin(keep)]
    rd = sub.groupby(ind_col)[["rd", "revenue"]].sum()
    rd_early = sub[sub["year"] <= 2013].groupby(ind_col)[["rd", "revenue"]].sum()

    rows = []
    for j in keep:
        L = lead.loc[j]
        k = L["key"].to_numpy()
        switch = k[1:] != k[:-1]                      # leader in year t differs from year t-1
        changes = int(switch.sum())
        raw_changes = int((L["cik"].diff().fillna(0) != 0).sum())
        # a lasting change: the new leader is still on top the following year (t = 2012-2023)
        lasting = int((switch[:-1] & (k[2:] == k[1:-1])).sum())
        names = L["entity"]
        t4a, t4b = top4.loc[(j, YEARS[0])], top4.loc[(j, YEARS[-1])]
        share = L["revenue"] / tot.loc[j]
        rows.append({
            ind_col: j, "changes": changes, "years_at_risk": len(YEARS) - 1,
            "hazard": changes / (len(YEARS) - 1), "raw_cik_changes": raw_changes,
            "lasting_changes": lasting, "lasting_hazard": lasting / (len(YEARS) - 2),
            "distinct_leaders": len(pd.unique(k)), "new_leader_by_end": int(k[-1] != k[0]),
            "rd_intensity": rd.loc[j, "rd"] / rd.loc[j, "revenue"],
            "rd_intensity_2011_13": rd_early.loc[j, "rd"] / rd_early.loc[j, "revenue"],
            "top4_turnover": len(t4a - t4b) / 4,
            "leader_share_first": share.iloc[0], "leader_share_last": share.iloc[-1],
            "mean_firms": counts.loc[j].mean(),
            "revenue_growth": np.log(tot.loc[(j, YEARS[-1])] / tot.loc[(j, YEARS[0])]) / (len(YEARS) - 1),
            "industry_revenue_last_bn": tot.loc[(j, YEARS[-1])] / 1e9,
            "leader_first": names.iloc[0], "leader_last": names.iloc[-1],
            "leaders_in_order": " > ".join(pd.unique(names)),
        })
    return pd.DataFrame(rows), rev


def regressions(ind, ind_col, rows, label):
    """Linear hazard (the model's lambda * n), Poisson count model and rank correlation."""
    d = ind.copy()
    d["rd_pct"] = 100 * d["rd_intensity"]
    d["rd_pct_early"] = 100 * d["rd_intensity_2011_13"]
    d["log_firms"] = np.log(d["mean_firms"])
    d["hazard_pct"] = 100 * d["hazard"]
    specs = [
        ("Linear hazard on R&D intensity", "hazard_pct ~ rd_pct", "ols"),
        ("Linear hazard with controls", "hazard_pct ~ rd_pct + log_firms + revenue_growth", "ols"),
        ("Linear hazard on 2011-13 R&D intensity", "hazard_pct ~ rd_pct_early", "ols"),
        ("Lasting leader changes (linear hazard)", "I(100 * lasting_hazard) ~ rd_pct", "ols"),
        ("Leader in last year differs from first (pct, LPM)", "I(100 * new_leader_by_end) ~ rd_pct", "ols"),
        ("Top-4 turnover (pct) on R&D intensity", "I(100 * top4_turnover) ~ rd_pct", "ols"),
        ("Poisson leader changes on R&D intensity", "changes ~ rd_pct + log_firms + revenue_growth", "poisson"),
    ]
    for name, f, kind in specs:
        if kind == "ols":
            fit = smf.ols(f, d).fit(cov_type="HC1")
        else:
            fit = smf.glm(f, d, family=sm.families.Poisson(),
                          offset=np.log(d["years_at_risk"])).fit(cov_type="HC1")
        x = "rd_pct_early" if "early" in f else "rd_pct"
        ci = fit.conf_int().loc[x]
        rows.append(dict(sample=label, model=name, slope=fit.params[x], se=fit.bse[x],
                         ci_low=ci[0], ci_high=ci[1], p=fit.pvalues[x],
                         intercept=fit.params["Intercept"], intercept_se=fit.bse["Intercept"],
                         n=int(fit.nobs)))
    rho, p = stats.spearmanr(d["rd_intensity"], d["hazard"])
    rows.append(dict(sample=label, model="Spearman rank correlation of hazard and R&D", slope=rho,
                     se=np.nan, ci_low=np.nan, ci_high=np.nan, p=p, intercept=np.nan,
                     intercept_se=np.nan, n=len(d)))


def group_table(ind):
    rows = []
    for lo, hi, name in RD_GROUPS:
        g = ind[(ind["rd_intensity"] > lo) & (ind["rd_intensity"] <= hi)]
        h = g["changes"].sum() / g["years_at_risk"].sum()
        # exact Poisson 95% interval for the pooled count of leader changes
        c, T = g["changes"].sum(), g["years_at_risk"].sum()
        lo_ci = stats.chi2.ppf(0.025, 2 * c) / 2 / T if c > 0 else 0.0
        hi_ci = stats.chi2.ppf(0.975, 2 * c + 2) / 2 / T
        rows.append(dict(group=name, industries=len(g), leader_changes=int(c), industry_years=int(T),
                         hazard=h, hazard_ci_low=lo_ci, hazard_ci_high=hi_ci,
                         expected_tenure_years=1 / h if h > 0 else np.nan,
                         median_rd_intensity=g["rd_intensity"].median(),
                         lasting_hazard=g["lasting_changes"].sum() / (g["years_at_risk"] - 1).sum(),
                         new_leader_by_end=g["new_leader_by_end"].mean(),
                         top4_turnover=g["top4_turnover"].mean(),
                         industries_with_no_change=int((g["changes"] == 0).sum())))
    return pd.DataFrame(rows)


def fred_annual(series_id):
    """Annual averages of one FRED series over the study years, downloading it once."""
    path = RAW / "fred" / f"{series_id}.csv"
    if not path.exists():
        r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}", timeout=120)
        r.raise_for_status()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(r.text)
    d = pd.read_csv(path)
    d.columns = ["date", "v"]
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    d["year"] = pd.to_datetime(d["date"]).dt.year
    return d.dropna().groupby("year")["v"].mean()


def main():
    OUT.mkdir(exist_ok=True)
    df = load_panel()
    print(f"Analysis panel: {len(df):,} filer-years, {df['cik'].nunique():,} filers, "
          f"{df['sic3'].nunique()} 3-digit SIC industries")

    reg_rows = []
    ind3, rev3 = leader_stats(df, "sic3")
    regressions(ind3, "sic3", reg_rows, "3-digit SIC")
    df4 = df.assign(sic4=df["sic"])
    ind4, _ = leader_stats(df4, "sic4")
    regressions(ind4, "sic4", reg_rows, "4-digit SIC")
    ind3_ex = ind3[ind3["mean_firms"] >= 10]
    regressions(ind3_ex, "sic3", reg_rows, "3-digit SIC, 10+ filers")
    regressions(ind3[ind3["rd_intensity"] < 0.08], "sic3", reg_rows, "3-digit SIC, under 8% R&D")
    reg = pd.DataFrame(reg_rows)
    reg.to_csv(OUT / "leader_regressions.csv", index=False, float_format="%.5f")

    groups = group_table(ind3)
    groups.to_csv(OUT / "leader_hazard_by_rd.csv", index=False, float_format="%.5f")
    groups4 = group_table(ind4)
    groups4.to_csv(OUT / "leader_hazard_by_rd_sic4.csv", index=False, float_format="%.5f")

    sic_names = pd.read_csv(RAW / "sic_codes.csv", dtype={"sic": int})
    # A 3-digit group takes the title of its "xx0" code where the SEC list has one
    sic_names = sic_names.assign(sic3=sic_names["sic"] // 10, is_group=sic_names["sic"] % 10 == 0)
    sic3_names = (sic_names.sort_values("is_group", ascending=False)
                  .groupby("sic3")["industry_title"].first())
    ind3["example_title"] = ind3["sic3"].map(sic3_names)
    ind3.sort_values("rd_intensity", ascending=False).to_csv(OUT / "industries_sic3.csv", index=False,
                                                              float_format="%.5f")
    ind4["industry_title"] = ind4["sic4"].map(sic_names.set_index("sic")["industry_title"])
    ind4.sort_values("rd_intensity", ascending=False).to_csv(OUT / "industries_sic4.csv", index=False,
                                                              float_format="%.5f")

    # Worked example of the value formula V = pi / (r + lambda n), using pooled hazards
    r = fred_annual("DFII10").loc[YEARS[0]:YEARS[-1]].mean() / 100
    ex = groups[["group", "hazard", "expected_tenure_years"]].copy()
    ex["real_rate"] = r
    ex["value_multiple_of_profit"] = 1 / (r + ex["hazard"])
    ex["value_multiple_no_destruction"] = 1 / r
    pooled = ind3["changes"].sum() / ind3["years_at_risk"].sum()
    ex.loc[len(ex)] = dict(group="All industries", hazard=pooled, expected_tenure_years=1 / pooled,
                           real_rate=r, value_multiple_of_profit=1 / (r + pooled),
                           value_multiple_no_destruction=1 / r)
    ex.to_csv(OUT / "value_of_leadership.csv", index=False, float_format="%.5f")

    # Growth formula AGR = lambda * n * ln(gamma): if every leader change were one innovation,
    # the step size implied by measured TFP growth over the same years
    tfp = np.log(fred_annual("MFPNFBS"))
    g = (tfp.loc[YEARS[-1]] - tfp.loc[YEARS[0] - 1]) / len(YEARS)
    step = pd.DataFrame([dict(tfp_growth_per_year=g, leader_hazard=pooled, implied_log_step=g / pooled,
                              implied_step_pct=100 * (np.exp(g / pooled) - 1))])
    step.to_csv(OUT / "implied_step.csv", index=False, float_format="%.5f")

    # Leader each year for the named industries in the README
    lead_years = rev3[rev3["rank"] <= 2][["sic3", "year", "rank", "entity", "revenue"]]
    lead_years = lead_years.assign(revenue_bn=lead_years["revenue"] / 1e9).drop(columns="revenue")
    lead_years.to_csv(OUT / "leaders_by_year_sic3.csv", index=False, float_format="%.3f")

    # Revenue and R&D of the two chip makers in the README's opening (SEC numbers 50863, 1045810)
    chips = df[df["cik"].isin([50863, 1045810])][["entity", "year", "revenue", "rd"]]
    chips = chips.assign(revenue_bn=chips["revenue"] / 1e9, rd_bn=chips["rd"] / 1e9)
    chips[["entity", "year", "revenue_bn", "rd_bn"]].sort_values(["entity", "year"]).to_csv(
        OUT / "intel_nvidia.csv", index=False, float_format="%.3f")

    print("\nLeader replacement by research intensity (3-digit SIC)")
    print(groups.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print("\nRegressions (HC1 standard errors)")
    print(reg[["sample", "model", "slope", "se", "p", "intercept", "n"]]
          .to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(f"\nPooled hazard {pooled:.4f}; mean 10-year TIPS yield {YEARS[0]}-{YEARS[-1]}: {r:.4f}")
    print(f"TFP growth {YEARS[0]}-{YEARS[-1]}: {100 * g:.3f}% a year; implied step per innovation "
          f"{step['implied_step_pct'].iloc[0]:.1f}%")

    # Figure: hazard against R&D intensity, one dot per industry, group means as steps
    fig, ax = plt.subplots(figsize=(8, 4.8))
    x = (100 * ind3["rd_intensity"]).clip(lower=0.01)
    jitter = np.random.default_rng(0).uniform(-0.6, 0.6, len(ind3))
    ax.scatter(x, 100 * ind3["hazard"] + jitter, s=12 + ind3["mean_firms"], alpha=0.55,
               color="#1f5f99", edgecolor="white", lw=0.5)
    for (lo, hi, name), (_, g) in zip(RD_GROUPS, groups.iterrows()):
        a, b = max(100 * lo, 0.01), min(100 * hi, 100 * ind3["rd_intensity"].max() * 1.2)
        ax.plot([a, b], [100 * g["hazard"]] * 2, color="#b5432a", lw=2.5)
    ax.set_xscale("log")
    ax.set_xlabel(f"Industry R&D spending as % of revenue, {YEARS[0]}-{YEARS[-1]} "
                  "(log scale; values under 0.01 shown at 0.01)")
    ax.set_ylabel("Revenue leader replaced, % of years")
    ax.set_title(f"Revenue leaders of {len(ind3)} industries (3-digit SIC), SEC filers, {YEARS[0]}-{YEARS[-1]}")
    fig.text(0.01, 0.01, "Dots: industries (size = number of filers, small vertical jitter). "
             "Red lines: pooled rate in each R&D group. Source: SEC Financial Statement Data Sets.",
             fontsize=7, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "leader_hazard.png", dpi=150)
    print("\nWrote leader_regressions.csv, leader_hazard_by_rd*.csv, industries_sic3.csv, "
          "industries_sic4.csv, value_of_leadership.csv, implied_step.csv, leaders_by_year_sic3.csv, "
          "intel_nvidia.csv, leader_hazard.png")


if __name__ == "__main__":
    main()
