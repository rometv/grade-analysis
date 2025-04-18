## Grade Analysis Dashboard

#### A web-based interactive dashboard for analysing student submission data. Flask is used for the backend, Altair/Vega for chart rendering and Bootstrap for frontend.

### Features
- Upload and parse zipped homework submission data
- Interactive date filtering
- Dynamic Altair charts rendered with VegaEmbed script
- Heatmaps, timelines and grading distribution visualisations
- Centralized data-store for clean architecture
- Unicode-safe parsing of execution file
- Class-based chart API with filtering

### Project structure
```
grade-analysis/
├── app.py              # Flask app entry point, routes, upload logic
├── chart_api.py        # MethodView classes for each chart endpoint 
├── analysis.py         # Altair chart-generating functions
├── data_frames.py      # Converts object-oriented data to pandas DataFrames 
├── data_classes.py     # Data model for Students, Submissions, and PointGroups 
├── parser.py           # Parses the contents of the uploaded zip file 
├── unpacker.py         # Unzips and reads in file data, invokes parser 
├── data_store.py       # Central in-memory store for DataFrames and metadata 
├── utils.py            # Pure utility functions (e.g. hashing, formatting)
├── helpers.py          # Flask-related helpers (e.g. get_date_filters) 
├── templates/
│ └── index.html        # Main HTML template with VegaEmbed and Datepicker
├── static/ 
│ └── scripts.js        # JS logic for chart loading, filtering, and UI 
├── requirements.txt    # Project dependencies 
└── README.md           # You're looking at it.
```

### How to run
1. Create and activate virtualenv
2. Install dependencies:
   - pip install -r requirements.txt
3. Flask run (in venv)

### Uploading data
The website displays an upload form. Upload a ```.zip``` file containing submission data.
Once uploaded:
1. File is unpacked and parsed
2. Parsed Student objects are then looped over and converted to 4 pandas DataFrames.
3. Stored in memory (in data_store.py)
4. User is redirected to the dashboard

### Currently available charts
- Submission timeline   # Daily submission counts
- Submission heatmap    # Time of day vs date grid
- Grading distribution  # Point group data
- Starting time effect  # How starting time correlates with grade quality