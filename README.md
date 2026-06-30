# DRAFT
## Porto Mobility

A simple data analysis of Porto city traffic using public data.

### Methodology 

The analysis consisted of four steps: 
- Data collection
- Modeling 
- Valuation
- Deployment

#### Data collection 

The data collection comprises the search, download and preparation of the public data used through the analysis.
A total of 7 data sources were used on this analysis:

1. Waze Live-Map: All alerts about traffic. Granularity: 15 minutes. Format: json. 
2. HERE traffic API: Porto traffic data using a private HERE API account. Granularity: 15 minutes. Format: json.
3. STCP bus location: The real-time bus location from Porto city using the Porto digital data portal. Granularity: 15 minutes. Format: json.
4. IPMA weather data: The metereology data from IPMA API. Granularity: 3 hours. Format: json. 
5. TomTom historical indicators of Porto city. One time collected. Format: csv.
6. Openstreetmap GIS information of the Porto city. One time collected. Format: GIS OSM file with csv database extracted using GIS tools.
7. Adittional data from Porto Digital Portal (e.g. parking lots, traffic conditioners, scooters spots, bus tracks, and subway stations). One time collected. Format: multiple file formats (e.g. json and csv).


The data ingestion was based on data conversion between the json and csv data to SQL database for reliable queries and secure storage of all information.

The data preparation comprised the query creation to merge the data tables between the differnret types of data. Inittially seven data tables were created with from different types of data (Waze, Here, STCP, IPMA, TomTom, Openstreetmap, and Porto Digital Data).
