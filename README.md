# grade analysis

### Attempting grade analysis based on a Moodle course automatic testing logs.

Use test.py for running the analysis without *Apache AirFlow*.

Breakdown:  
Running unpacker.py results in parsing of configured *Zip* files with respective Data object.  
Data object of type data_classes.Data can be conversed into pandas' DataFrame object using dataframes.py.  
In analysis.py Data object is conversed to a DataFrame and dataframes are respectively used to generate *Vega-Altair*
charts, which are saved to *plots/corresponding_plot*.
