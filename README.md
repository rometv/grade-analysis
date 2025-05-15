## Grade Analysis Dashboard

#### This project provides a web-based interactive dashboard for the analysis of student submission data in programming courses. The backend is implemented using Flask, chart rendering is handled with Altair/Vega, and the frontend is styled with Bootstrap.

### Features
- Upload and parse zipped homework submission archives.
- Interactive date-based filtering of submission data.
- Dynamic Altair-generated charts rendered via the VegaEmbed library.
- Visualisations include heatmaps, timelines, and grading distributions.
- Centralised in-memory data store to support a clean and modular architecture.
- Unicode-safe parsing of execution logs.
- Class-based chart API supporting flexible filtering.

### Project structure
```
grade-analysis/
├── analysis.py            # Functions for generating Altair charts
├── app.py                 # Flask application entry point, routing, and file upload handling
├── chart_api.py           # MethodView classes for chart endpoints
├── data_store.py          # Central in-memory store for DataFrames and associated metadata
├── execution_grammar.py   # Lark parser object and grammar definition
├── helpers.py             # Helper functions for Flask operations (e.g., date filtering)
├── parse_homework.py      # Batch-based ZIP archive reader
├── parser_lark.py         # Main parsing logic
├── utils.py               # Utility functions (e.g., hashing, formatting)
├── templates/
│ └── dashboard.html       # Dashboard page template
│ └── upload.html          # Upload form template
├── static/
│ └── chart_endpoints.js   # JavaScript for dynamic chart loading
│ └── datepicker.js        # JavaScript for datepicker functionality
│ └── other.js             # Other supporting scripts
├── requirements.txt       # Project dependencies
└── README.md
```

### Running the Application
1. Create and activate a virtual environment.
2. Install dependencies:
   - pip install -r requirements.txt
3. ```flask run``` 

### Data Upload Procedure
Upon accessing the upload page, users are prompted to submit a .zip archive containing student submission data.
The upload process consists of the following steps:
1. The archive is unpacked and each execution.txt file is parsed.
2. The parsed data is transformed into four Pandas DataFrames.
3. The processed data is stored in memory using data_store.py.
4. The user is redirected to the dashboard for interactive data exploration.
