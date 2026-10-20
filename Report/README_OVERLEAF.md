# Overleaf / LaTeX report

The report is deliberately **code-free**. MATLAB and Python implementations are stored outside `Report/` and are not embedded in the report.

## Upload to Overleaf

1. Create a ZIP archive containing only `main.tex` and the `Figures/` directory **from this folder**. The root of that ZIP must contain `main.tex` (not a nested project directory).
2. On [Overleaf](https://www.overleaf.com/), select **New Project → Upload Project** and upload the ZIP.
3. In **Menu**, select **Main document: `main.tex`** and **Compiler: pdfLaTeX**.
4. Click **Recompile** and download the PDF if needed.

### Required layout

```text
main.tex
Figures/
  F01_contrast_histograms.png
  ... (11 PNGs total)
  F10_pipeline.png
```

`main.tex` has no external code-file dependencies. Source files are *not* needed in Overleaf, and the MATLAB/Python source should not be imported into the report project.

The repository additionally provides an already formatted DOCX and PDF in this folder. Numeric results correspond to the executed Python reference run; the MATLAB implementation has not been independently run and may produce small differences, especially in CLAHE.

The report has a **References** section and a planned GitHub repository link. The repository URL will become active after publishing at `https://github.com/burakcakirer/ee3005-image-processing-assignment-2`. If you publish under a different name, update `REPOSITORY_URL` in `tools/build_report.py` and regenerate `main.tex` before submission.
