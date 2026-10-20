# EE3005 · Biomedical System Design Capsule-S1 — Image Processing Assignment 2

**Image enhancement · Spatial filtering · Denoising · Sharpening · Edge detection**

**Author:** Burak Bekir Çakırer  
**Student ID:** 2211011008  
**Course:** EE3005 — BIOMEDICAL SYSTEM DESIGN CAPSULE-S1  
**Deliverable:** Image Processing Assignment 2, Tasks 1–8  
**Planned GitHub URL:** https://github.com/burakcakirer/ee3005-image-processing-assignment-2 *(available after publication)*

This repository contains a reproducible set of **image-processing experiments on course-provided biomedical examples**. It includes a MATLAB implementation, an independently executed Python reference, fixed image/noise inputs, quantitative results, report figures, validation checks, and a report in **PDF, DOCX, and Overleaf-ready LaTeX**.

**Report policy:** The report contains the methodology, equations, intermediate calculations, results, figures, and interpretation—**no MATLAB or Python code listings**. Complete source code is available separately in `MATLAB/`, `Python_Reference/`, and `tools/`.

> **Execution transparency:** The numerical results and figures in the report were generated with the **executed Python reference** and checked for internal consistency. The MATLAB implementation is supplied for the assignment but **has not been executed in MATLAB in this environment**. Library-specific differences (especially CLAHE and boundary conventions) can affect exact MATLAB outputs. Do not describe these measurements as MATLAB-verified before running the `.m` file.

## Contents

| Task | Subject | Experiment / deliverable |
|:---:|---|---|
| 1 | Histogram equalization, AHE, CLAHE | Global vs. local contrast; two CLAHE configurations; histograms and local contrast metrics |
| 2 | Correlation, convolution, borders | Hand-calculated center-pixel outputs; zero, replicate, reflect, and circular padding |
| 3 | Separable Gaussian filtering | 2D vs. successive 1D filters; maximum numerical difference and operation count |
| 4 | Linear noise removal | Gaussian and salt-and-pepper noise; mean/Gaussian alternatives; PSNR comparison |
| 5 | Nonlinear filters | Median, geometric/harmonic means, contra-harmonic polarity and order; PSNR |
| 6 | Unsharp masking | Three gain levels; detail visibility and over-sharpening artifacts |
| 7 | Edge detection | Sobel, Laplacian, LoG, DoG; noise sensitivity and scale effects |
| 8 | Integrated pipeline | Median → CLAHE → unsharp masking; intermediates and critical evaluation |

### Example result

![Pipeline showing noisy radiograph, median filtered image, CLAHE, and sharpening](Report/Figures/F10_pipeline.png)

<sub>Task 8: The integrated workflow. All image examples are for coursework, not diagnostic use.</sub>

## Key measured findings

| Measurement | Reference result |
|---|---:|
| Task 2 — central correlation | **−80** |
| Task 2 — central convolution | **+80** |
| Task 3 — max. 2D / separable difference | **≈ 3.33 × 10⁻¹⁶** |
| Task 3 — multiplication count (3×3) | **9 → 6 per pixel** |
| Task 4 — best tested filter for Gaussian noise | **3×3 Gaussian, σ = 0.8; 30.74 dB PSNR** |
| Task 5 — salt-and-pepper: median 3×3 vs. mean 3×3 | **34.88 vs. 23.03 dB PSNR** |

Scores are calculated against each clean reference using the stored noise realizations. Higher PSNR does not automatically imply clinically better visibility; contrast operations may deliberately change the intensity distribution. Full tables and limitations are in the report.

## Repository layout

```text
ee3005-image-processing-assignment-2/
├── .gitignore
├── .gitattributes
├── README.md
├── docs/
│   └── GITHUB_DESKTOP_TR.md        # Windows / D:\GitHub upload walkthrough (Turkish)
├── MATLAB/
│   └── run_assignment2.m           # MATLAB implementation for Tasks 1–8
├── Python_Reference/
│   ├── reproduce_results.py        # Executed reference experiments and figure generator
│   └── requirements.txt
├── Source_Images/
│   ├── Original_Samples/           # Instructor-supplied examples (includes DICOM)
│   └── Prepared_Inputs/            # Converted grayscale and deterministic noisy PNGs
├── Outputs/
│   └── Results/                    # CSV, JSON, manual calculation log
├── Report/
│   ├── EE3005_Assignment2_Report.pdf
│   ├── EE3005_Assignment2_Report.docx
│   ├── main.tex                    # Text/results only; no embedded code
│   ├── Figures/                    # 11 result figures referenced by the report
│   └── README_OVERLEAF.md
├── Original_Assignment/
│   └── Assignment_2_Instructions.pdf
├── Tests/
│   ├── validate_outputs.py
│   └── check_report_policy.py       # Confirms code listings are absent from report
└── tools/
    └── build_report.py            # Regenerates code-free DOCX and main.tex
```

The project root is the working directory. Keep the relative directory structure intact: scripts find input and output directories relative to their own locations.

## Get started

### MATLAB (course-required implementation)

**Requirements:** MATLAB with **Image Processing Toolbox**. The script uses `exportgraphics` (MATLAB R2020a or newer recommended).

1. Open `MATLAB/run_assignment2.m` in MATLAB.
2. Choose **Run**; there is no need to modify absolute Windows paths.
3. Output images are written to `Outputs/MATLAB_Figures/`, and CSV/measurement data to `Outputs/MATLAB_Results/`.
4. Review MATLAB-generated results separately before claiming numerical equivalence to the Python reference.

This implementation loads the fixed, bundled `Source_Images/Prepared_Inputs` PNGs to keep the noise realization consistent across environments.

### Python reference (Windows PowerShell)

**Requirements:** Python 3.10 or later recommended. Run these commands from the repository root (for example `D:\GitHub\ee3005-image-processing-assignment-2`).

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r Python_Reference/requirements.txt
python Python_Reference/reproduce_results.py
python Tests/validate_outputs.py
```

If PowerShell blocks activation, you can run the executable directly: `\.venv\Scripts\python.exe Python_Reference\reproduce_results.py`. You may alternatively use an existing Python installation.

The reference uses RNG seed `3005`, rebuilds prepared image/noise PNGs, writes `Outputs/Results` data, and regenerates the 11 images in `Report/Figures/`. Its principal dependencies are NumPy, SciPy, scikit-image, OpenCV, Pillow, and Matplotlib.

### Validate packaged outputs

```powershell
python Tests/validate_outputs.py
python Tests/check_report_policy.py
```

Checks include Task 2's hand-computed outputs, separable Gaussian agreement, noise/filter comparisons, expected figures, and grayscale input formats. They check **reference-data consistency and the code-free report policy**, not full MATLAB-runtime correctness.

## Report files, academic references, and editing

| File | Purpose |
|---|---|
| [`Report/EE3005_Assignment2_Report.pdf`](Report/EE3005_Assignment2_Report.pdf) | Ready-to-read PDF report |
| [`Report/EE3005_Assignment2_Report.docx`](Report/EE3005_Assignment2_Report.docx) | Editable Word report |
| [`Report/main.tex`](Report/main.tex) | Standalone Overleaf document (`pdfLaTeX`) |
| [`Report/Figures/`](Report/Figures/) | Figures required by LaTeX and report |

The report is intentionally source-code-free. Its formulas, numerical computations, tables, and visual results **remain included**, alongside an academic **References** section and a clickable link to the proposed GitHub repository. The full implementation is linked from the repository rather than printed as an appendix.

To rebuild the **DOCX and `main.tex`** after editing measurements or narration, install `python-docx` and run:

```powershell
python -m pip install python-docx
python tools/build_report.py
```

Then export the updated DOCX as PDF, for example in Microsoft Word (*File → Export → Create PDF/XPS*) or a compatible office application. **Running the report builder does not automatically re-export the PDF**. For Overleaf upload instructions see [`Report/README_OVERLEAF.md`](Report/README_OVERLEAF.md).

> **Submission-format note:** The supplied assignment guidelines mention a **single Word report** and also request MATLAB source. This repository separates code from report by design. Follow your instructor's actual submission requirements when uploading to the LMS; the PDF is available because it was explicitly requested for this project.

## Experimental setup and limitations

- **Input examples:** `image3.jpg` (chest radiograph) and `image2.jpg` (brain MRI), extracted from the supplied assignment archive. Remaining original files are preserved; two DICOM files are included but not directly analyzed.
- **Image representation:** 8-bit grayscale files, intensity values normalized to `[0, 1]` during processing.
- **Noise:** Gaussian standard deviation `0.06`; salt-and-pepper density `0.08`, plus individual salt and pepper inputs. The pipeline uses Gaussian `0.03` + impulse density `0.025`.
- **Comparisons:** PSNR calculated against clean images, consistent input shapes, explicit kernel sizes and strengths.
- **Boundary conventions:** Python SciPy modes and MATLAB `imfilter` modes are documented separately. CLAHE implementation details and pixel rounding can vary.
- **Interpretation:** No clinical labels, diagnostic validation, patient metadata, or external medical ground truth are provided. Results are educational image-processing demonstrations only.

## Publishing with GitHub Desktop

For instructions specifically using **`D:\GitHub`**, GitHub Desktop's **Add Local Repository** workflow, committing, and **Publish repository**, see the [Turkish GitHub Desktop guide](docs/GITHUB_DESKTOP_TR.md).

**GitHub link notice:** The report links to `https://github.com/burakcakirer/ee3005-image-processing-assignment-2`. Publish using exactly this account and name for the report link to become valid. If you choose another name, update `REPOSITORY_URL` in `tools/build_report.py`, regenerate the reports, and replace the PDF before submitting.

**Do not place the project folder inside a second identically named folder.** After extracting the ZIP, this file should be at `D:\GitHub\ee3005-image-processing-assignment-2\README.md`.

**Dataset rights and privacy:** Source images and the assignment PDF came from course materials; their public redistribution rights are not established. Before creating a **public** repository, obtain permission or omit any restricted assets. A **private repository** is preferable if permission is uncertain. No software-wide open-source license is asserted here.

---

**Project owner:** Burak Bekir Çakırer · EE3005 — Biomedical System Design Capsule-S1 · Assignment 2 · 2211011008
