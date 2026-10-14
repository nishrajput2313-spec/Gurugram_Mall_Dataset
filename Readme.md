# Malls and Shopping Centres in Gurugram: Mini Location Dataset

A small Python project that collects malls in Gurugram from a public web page,
cleans the data, finds each mall on a map and measures its distance from
Sohna Road.

## Source
Wikipedia: List of shopping malls in India (accessed 14 October 2026).

## What I did
1. **Extract** (`1_extract.py`): downloaded the page with requests and picked out
   the Gurgaon entries using BeautifulSoup and pandas. 23 rows collected.
2. **Clean** (`2_clean.py`): removed footnote marks and duplicates, and split the
   details into location, year opened and area. 23 rows before, 20 after.
3. **Geocode and distance** (`3_geocode_distance.py`): found coordinates using
   OpenStreetMap and calculated straight-line distance with the Haversine formula.
4. **Chart** (`4_chart.py`): grouped the malls by distance band.

## Problems found
- The page lists some malls twice across two tables. I removed the duplicates
  and kept the row with the fullest address.
- OpenStreetMap could not find every mall by name. 14 matched by name or
  name + address and 5 matched by address only, so those are approximate
  road-level locations (four share the same Sector-28 point). 1 mall
  (DLF South Point Mall) was not found. The `match_type` column records this.
- One lookup timed out. The script recorded it and used a fallback search.
- The reference point is approximate (Sohna Road, Gurugram).
- No result was more than 40 km away, so none were removed as wrong matches.

## Result
3 of the 19 located malls are within 5 km of Sohna Road. See `chart.png`.

## Files
- `raw_data.csv`: data as collected
- `clean_data.csv`: after cleaning
- `final_dataset.csv`: with coordinates, distance and match type
- `distance_summary.csv`: number of malls per distance band
- `chart.png`: the chart


## How to run it
Install the libraries:

    pip install requests beautifulsoup4 lxml pandas matplotlib

Then run the scripts in order:

    python 1_extract.py
    python 2_clean.py
    python 3_geocode_distance.py
    python 4_chart.py