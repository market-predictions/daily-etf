# ETF Review OS — Bilingual output rules

This file defines the production-safe bilingual pattern for the ETF report family.

## Canonical truth rule
The English pro report remains the canonical production report for a run.
The Dutch report is a companion render derived from that completed English report.

The Dutch companion must not:
- re-run the research
- change rankings
- change actions
- change numbers
- change holdings
- change continuity facts
- change material caveats

## Paired output rule
For bilingual runs, write:
- English canonical report:
  - `output/weekly_analysis_pro_YYMMDD.md`
  - or versioned: `output/weekly_analysis_pro_YYMMDD_NN.md`
- Dutch companion report:
  - `output/weekly_analysis_pro_nl_YYMMDD.md`
  - or versioned: `output/weekly_analysis_pro_nl_YYMMDD_NN.md`

The English and Dutch reports must:
- share the same date
- share the same same-day version number
- be written together as a matched pair

## Delivery rule
A bilingual production run should produce:
- one canonical English markdown report
- one Dutch companion markdown report
- one English PDF
- one Dutch PDF
- one English email
- one Dutch email

## Lane artifact rule
The lane assessment artifact remains analytical rather than linguistic.
A bilingual run still writes only one lane artifact, matched to the English canonical report date and version.
