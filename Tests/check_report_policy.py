"""Validate the explicit project policy: the report must not contain code listings.

Only Python's standard library is required for this structural test.
"""
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "Report"

tex = (REPORT / "main.tex").read_text(encoding="utf-8")
assert r"\lstinputlisting" not in tex
assert r"\begin{lstlisting}" not in tex
assert r"\begin{verbatim}" not in tex
assert r"\usepackage{listings}" not in tex
assert "Appendix A - Complete MATLAB source code" not in tex
assert "Code/run_assignment2.m" not in tex
assert not (REPORT / "Code").exists()

with ZipFile(REPORT / "EE3005_Assignment2_Report.docx") as z:
    xml = z.read("word/document.xml").decode("utf-8")
    assert "Appendix A - Complete MATLAB source code" not in xml
    assert "Complete MATLAB source for Tasks" not in xml
    assert "%% Task 1:" not in xml
    assert "function out=contra_mean" not in xml

for p in ("EE3005_Assignment2_Report.pdf", "EE3005_Assignment2_Report.docx", "main.tex"):
    assert (REPORT / p).is_file() and (REPORT / p).stat().st_size > 100
print("Report policy verified: no embedded source-code appendix or listings.")
