"""Compatibility import for the ETF delivery base layer.

The historical implementation currently lives in `send_report_OLD.py`.
This wrapper gives the active base layer a clearer name without removing the
legacy filename in the same change.

Cleanup sequence:
1. import this module from `send_report.py`
2. keep `send_report_OLD.py` for one validated production cycle
3. later move the implementation fully into this file or remove the legacy file
   only after validation proves it is no longer imported
"""

from send_report_OLD import *  # noqa: F401,F403
