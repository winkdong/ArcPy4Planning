# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# LST.py
# Created on: 2016-10-20 By dongxu
# Description: Calculate Land Surface Temperature with Landsat 8 Data
# Reference: https://www.youtube.com/watch?v=uDQo2a5e7dM , Usman Buhari
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
arcpy.env.overwriteOutput = True
from arcpy.sa import *
# Set workspace
arcpy.env.workspace = "E:/GIS/Longhua/Input/test.gdb"
print "Input Data Finish: (BAND10,BAND11,NDVI)"
print arcpy.Exists("BAND10"),arcpy.Exists("BAND11"),arcpy.Exists("NDVI_b5b41")
sr = arcpy.Describe("BAND10").spatialReference
print "Spatial Reference System:"
print sr.name

# Check out any necessary licenses
print "Spatial Analyst Extension Available:"
print arcpy.CheckOutExtension("spatial")


# Local variables:
# Input 
BAND10 = Raster("BAND10")
BAND11 = Raster("BAND11")
NDVI = Raster("NDVI_b5b41")

# BAND 11 Gradadiance
BAND11Gradiance = BAND11 * 0.0003342 + 0.1

# BAND 11 Satelite Temperature
BAND11SatTemp = 1201.14 / Ln(480.89 / BAND11Gradiance + 1)  - 272.15

# BAND 10 Gradadiance
BAND10Gradiance = BAND10 * 0.0003342

# BAND 10 Satelite Temperature
BAND10SatTemp = 1321.08 / Ln(774.89 / BAND10Gradiance + 1)  - 272.15

# Proportion of Vegetation from NDVI, according to Carlson & Ripley, 1997
# PropVEG = Square((NDVI - NDVI_s)/(NDVI_v-NDVI_s))
PropVEG = Square((NDVI + 1)/(1 -(-1))) # a missing bracket in this line, cause an error on the next line...

# Deriving LSE
LSE = 0.004 * PropVEG + 0.986

# BAND 10 Land Surface Temperature
BAND10LST = BAND10SatTemp / 1 + BAND10 * (BAND10SatTemp / 14380) * Ln(LSE)
BAND11LST = BAND11SatTemp / 1 + BAND11 * (BAND11SatTemp / 14380) * Ln(LSE)
# Save Final Land Surface Temperature Raster
LST = (BAND10LST+BAND11LST)/2
LST.save("LST")
print "All done, Please Check the 'BAND10LST' Raster in Current Workspace."
