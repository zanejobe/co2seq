# Intro
what we aspire to: 
- https://atlas.cid.harvard.edu/explore
- https://globalfishingwatch.org/map
- https://data.permianmap.org/pages/operators
- https://viirs.skytruth.org/apps/heatmap/flarevolume.html
- https://eogmap.mines.edu/ol/worldview/?v=-104.44720720311545,31.03886515111136,-101.01727556249045,33.30644327611136&t=2021-05-24-T20%3A00%3A00Z&l=OrbitTracks_Suomi_NPP_Descending(hidden),VIIRS_NOAA20_Thermal_Anomalies_375m_All(hidden),Coastlines(hidden),Reference_Labels,Reference_Features,VIIRS_NPP_DNB_Annual,VIIRS_NPP_CLD_Daily(hidden),VIIRS_NPP_DNB_Daily,VIIRS_SNPP_DayNightBand_ENCC(hidden),VIIRS_NPP_CFCVG_Monthly(hidden),VIIRS_NPP_DNB_Monthly(hidden),VIIRS_SNPP_CorrectedReflectance_TrueColor(hidden),MODIS_Aqua_CorrectedReflectance_TrueColor(hidden),MODIS_Terra_CorrectedReflectance_TrueColor(hidden)
- 

Hmm, does this do what we want it to do? https://co2public.er.usgs.gov/viewer/

Also, Nice overviews of CCS
- https://www.netl.doe.gov/sites/default/files/netl-file/co2_eor_primer.pdf
- http://energy.mit.edu/publication/lessons-learned-from-ccs-demonstration-and-large-pilot-projects/  

# Interactive Map of Carbon Storage Potential and Emissions

This project is an interactive dashboard that uses public datasets relevant fo a co2 sink and source information from various
agencies for users to explore. The data is contained in the Data folder and described in config.json. Each dataset is imposed on 
a map of the US and Gulf of Mexico that the user is able to explore and view summary information for. Links to all data sources 
can be found below.   

The project is a built as a Dash app by Plotly, and uses the associated libraries to represent the data. All graphing is handeled in apps/seqGraph.py. And data is 
processed in utils.py and render.py.  

# To Install

-$ git clone $repo  
-$ poetry install (for poetry venv), for other venvs see pyproject.toml for necessary packages 

For local host:  

-in index.py set line 29 to:

-if __name__ == '__main__':  
    app.run_server(debug=False, use_reloader=False)    
    
in project folder:  

-$ python index.py  

# Team
The project is a headed by the Colorado School of Mines Geology Department  

Team lead: Professor Zane Jobe  
Contributers: Grant Falkner, Matt Plumb, Ryan Armstrong, Patrick Schassberger  
