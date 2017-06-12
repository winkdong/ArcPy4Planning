# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# hydro.py
# Created on: 2016-12-06
# Usage: hydrology analysis
# Description: result include watershed, basin, stream(with order)
# ---------------------------------------------------------------------------
# Import arcpy module
import arcpy
arcpy.env.overwriteOutput = True
from arcpy import env
from arcpy.sa import *
# Set workspace
# arcpy.env.workspace = "D:\geodatabase\Yichuan\Yichuan.gdb"
# Input DEM ratser file
DEM = "DEM"
# Check SRS
# sr = arcpy.Describe(DEM).spatialReference
# print "Spatial Reference System:" + sr.name
# Check out any necessary licenses
# print "Spatial Analyst Extension Available:"
# print arcpy.CheckOutExtension("spatial")
# Process
fill = Fill(DEM)
flowdir = FlowDirection(fill, "NORMAL")
flowacc = FlowAccumulation(flowdir, "", "FLOAT")
streamrs = SetNull(flowacc, 1, "VALUE <= 90") # flowacc <=90 -> null, 90+ -> 1
streamlink = StreamLink(streamrs, flowdir)
watershedrs = Watershed(flowdir, streamlink, "VALUE")
arcpy.RasterToPolygon_conversion(watershedrs, "watershed", "NO_SIMPLIFY", "VALUE") # watershed polygon saved
streamorder = StreamOrder(streamrs, flowdir, "STRAHLER")
# Attention! this one goes wrong: stream = StreamToFeature(streamorder, flowdir, "SIMPLIFY")
StreamToFeature(streamorder, flowdir, "stream", "SIMPLIFY") # stream polyline saved
basinrs = Basin(flowdir)
arcpy.RasterToPolygon_conversion(basinrs, "basin", "NO_SIMPLIFY","VALUE") # basin polygon saved
print "All done, Check 'stream, basin, watershed' in Current Workspace."