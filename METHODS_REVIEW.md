# Methods review: Aghion and Howitt (1992)

- **Paper:** Philippe Aghion and Peter Howitt, "A Model of Growth Through Creative Destruction,"
  *Econometrica* 60(2), March 1992, pp. 323–351. Circulated earlier as NBER Working Paper 3223, January 1990.
- **Statistical focus:** the balanced-growth formula for the average growth rate, AGR = λn̂·ln(1/γ) (working
  paper equation 4.8), together with the value of an innovation V = π/(r + λn) (equation 2.17) on which it rests;
  and the signed comparative statics of Proposition 3 that turn the formula into predictions.
- **Review standard:** internal consistency of the formal results, explicitness of assumptions, and the
  testability of the predictions; for the few numerical statements, whether their source and units are stated.
- **What was read:** the full text of NBER Working Paper 3223 (January 1990, 50 pages, free from nber.org),
  and the published abstract of the 1992 *Econometrica* article on the Econometric Society's website. The
  published article itself was not read. Where the two versions may differ (notation, the endogenous size of
  innovations, the treatment of skilled labor), this review describes the working paper and says so. Equation
  and page numbers below refer to the working paper.

## Methods summary

The paper is a theoretical model with no data. It builds a continuous-time general-equilibrium economy with a
fixed labor force N, a consumption good made from land and a continuum of intermediate goods, and a research
sector. Labor in research, n, produces innovations as a Poisson process with arrival rate λn (section 2a). Each
innovation lowers the unit-cost parameter of every intermediate sector by the factor γ < 1 (equation 2.3) and is
patented; the patent holder in each sector is a monopolist until the next innovation arrives (section 2a). Free
entry into research equates the wage to the expected value of the next patent, w = λV (equations 2.16 and 2.18),
and the value of a patent is the flow of monopoly profit discounted at the interest rate plus the rate of creative
destruction, V = π/(r + λn) (equation 2.17). Combining these with labor-market clearing x + n = N gives a
forward-looking difference equation in manufacturing employment, x_t = ψ(x_{t+1}) (equation 3.2).

The formal results are: a unique stationary equilibrium plus possible two-cycles and a "no-growth trap"
(Proposition 1); conditions for a real two-cycle (Proposition 2); comparative statics of research employment in
the stationary equilibrium (Proposition 3: research falls with r, rises with λ, with the size of innovations and
with N; Proposition 4: rises with monopoly power); the growth formula and its variance (equation 4.8); a welfare
comparison identifying three distortions, the intertemporal spillover, the business-stealing effect and the
monopoly distortion (equations 4.12 to 4.14); extensions to learning by doing (section 4c), consumption smoothing
(section 5), endogenous size of innovations (section 6, Proposition 5: innovations are too small under laissez
faire) and a random arrival parameter (section 7).

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Value of an innovation | V_t = π_{t+1}/(r + λn_{t+1}), consumption-good units | Eq. 2.17, p. 9 | Expected discounted monopoly profit over a tenure that ends at rate λn | That real patents or market positions end at a constant hazard, or that λ is the same across industries |
| Expected tenure of a monopolist | 1/(λn) units of time (implied by the exponential interval length) | Section 2a, p. 4–5; discussion after eq. 2.17, p. 10 | Mean time until the next innovation displaces the incumbent | Any empirical tenure; the paper reports none |
| Average growth rate | AGR = −λn̂ ln γ, log points per unit time | Eq. 4.8, p. 22 | Drift of log output under balanced growth | That growth rises with research effort in data; no estimate is given |
| Variance of growth | VGR = λn̂ (ln γ)², per unit time | Eq. 4.8, p. 22 | Variance of the annual increment of log output | That observed output volatility comes from innovations; the paper says output never falls in the model (p. 23) |
| Comparative statics of research | ∂n̂/∂r < 0, ∂n̂/∂λ > 0, ∂n̂/∂(1/γ) > 0, ∂n̂/∂N > 0 | Proposition 3, p. 20 | Signs of the response of steady-state research | Magnitudes; the signs are qualitative |
| Scale effect | In the Cobb–Douglas case a doubling of population "should more than double" the growth rate | p. 23, citing footnote 20 | Strength of the scale effect implied by the model | The authors themselves accept that the model "has little to say" about population and growth (p. 23) |
| Positive-growth condition (Cobb–Douglas) | α < α* < 1, where 1 − α is the Lerner index (exact expression for α* illegible in the scan) | Eq. 3.5, p. 15 | Minimum monopoly power needed for any research | A calibrated value of α for any economy |
| Research share of labor | "no more than 2 or 3 percent" of the labor force | p. 18–19 | Authors' stated magnitude, used to argue cycles would be small in output | Unsourced in the text; no citation or year given |
| Random-arrival example | Asymptotic innovation frequency f = 1/3 at the baseline; f → 0 as λ in one state becomes infinite | Section 7, eqs. 7.2–7.5, p. 37–38 | That more productive research in one state can stop research in the other | Any frequency in real data; parameters r = N = 1 are normalizations |
| Social return to process R&D (cited) | 71% to 104%, US industry, 1973–1978 | Footnote 6, citing Scherer (1984) | Motivation for treating innovations as inputs to production | Anything estimated by the authors |

## Interpretation notes

- The paper's "statistics" are formal results. Every quantitative statement is conditional on the model's
  assumptions: one-for-one research productivity (arrival rate linear in n), a constant innovation size γ, no
  memory in research, drastic innovations, lump-sum patent sales with no royalties, inelastic labor supply, and
  constant marginal utility outside section 5. Footnote 8 lists empirical work that casts doubt on three of these
  (Griliches 1989, Pakes 1986, Hausman, Hall and Griliches 1984), which is an unusually candid disclosure.
- The welfare result is a sign ambiguity, not a finding that growth is too fast. Laissez-faire growth exceeds the
  optimum only when monopoly power is large and innovations are not too large (p. 26). The paper gives no
  parameter values that would locate any real economy on either side.
- The growth formula links three unobservables (λ, n̂ and γ). Data can identify their product only when one of
  them is pinned down independently, which is why later empirical work turned to the model's ancillary
  predictions (turnover of incumbents, the response of growth to research effort).
- The scale effect is acknowledged in the text as an "unfortunate implication" (p. 23). It is therefore a known
  feature of this version of the model rather than an oversight discovered later.
- Section 3's cycles and the no-growth trap are presented as logical possibilities; the authors state that their
  empirical relevance is an open question (p. 18–19).

## Unanswered questions

- What empirical counterpart does the model intend for n, the flow of research labor: scientists and engineers,
  R&D spending deflated by wages, or the share of labor in research? The answer changes whether the scale effect
  is testable with levels or with shares.
- How should "an innovation" be counted in data? The model has one economy-wide innovation that replaces every
  sector's monopolist at once; real displacements occur product by product.
- Does the result that V depends on future research survive when incumbents can innovate on their own products?
  The working paper notes that non-drastic innovations would be implemented by incumbents (p. 8) but does not
  model it.
- How large is the business-stealing effect relative to the intertemporal spillover for plausible parameters? No
  calibration is offered.

## Items requiring expert verification

- The exact form of the positive-growth condition (3.5) and of the Cobb–Douglas expressions (2.10)–(2.12) and
  (3.4), which are partly illegible in the scanned working paper; they should be checked against the published
  article.
- Whether the published 1992 version keeps the working paper's notation (cost factor γ < 1, arrival rate λn) or
  changes it, and whether Proposition numbering matches.
- Whether the published version's welfare comparison and endogenous innovation size (summarized in its
  abstract) differ in substance from sections 4b and 6 of the working paper.
- The unsourced "2 or 3 percent" research share of the labor force should be checked against contemporary NSF
  figures before being quoted as fact.

## How the modern rerun relates

The repository does not reproduce anything in the paper, which contains no data. It takes two predictions that
follow from equations 2.17 and 4.8, that leaders are displaced faster where more research is done and that growth
rises with research effort, and confronts them with US public-company filings for fiscal 2011–2024 and US national
accounts for 1950–2025. A positive or negative result there speaks to the model's empirical reach, not to the
correctness of its derivations.
