# Lightcurve

A simple Python tool for generating exoplanet-style light curves from video observations.

The program allows users to:

- Load a video file
- Select a region of interest (ROI) around a star
- Measure brightness over time
- Generate an interactive light curve
- Export brightness data to CSV

Built using:
- Tkinter
- OpenCV
- NumPy
- Matplotlib
- Plotly
- Pandas

---

# Features

- Interactive ROI selection
- Automatic brightness extraction
- Relative flux normalisation
- Interactive Plotly graph
- CSV export for further analysis

---

# Installation

## macOS
```bash
git clone https://github.com/Seanasaurus/lightcurve.git
cd lightcurve
chmod +x setup.sh
./setup.sh
make run
```

---

# Manual Installation

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python lightcurve_app.py
```

---

# Usage

1. Click **Load Video**
2. Select a video file
3. Drag a rectangle around the target star
4. Click **Generate Light Curve**
5. Explore the interactive graph
6. Save data using **Save CSV**

---

# Output

The exported CSV contains:

| Column | Description |
|---|---|
| Frame | Video frame number |
| Relative_Brightness | Normalised brightness value |

---

# Supported Video Formats

- `.mp4`
- `.mov`
- `.avi`

---

# Dependencies

- Python 3.10+
- NumPy
- Matplotlib
- OpenCV
- Plotly
- Pandas

---

# Future Improvements

Potential future additions:

- Background subtraction
- Aperture photometry
- Multiple star comparison
- Real timestamp support
- FITS file support
- Transit fitting tools

---

# License

MIT License
