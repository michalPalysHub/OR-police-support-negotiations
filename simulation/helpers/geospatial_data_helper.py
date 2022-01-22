import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import random
import os


class GeospatialDataHelper:
    input_filename = 'dzielnice_Krakowa.shp'
    input_dir_name = 'dzielnice_Krakowa'

    # reading shp files of city district boundaries
    def read_data_from_shp(self):
        path = os.path.join(os.getcwd(), "simulation", "input_data", self.input_dir_name, self.input_filename)
        return gpd.read_file(path)

    # merge city districts geospatial and safety factor data
    def add_district_safety_factor_data_to_gdf(self, gdf, safety_data):
        gdf['safety_factor'] = safety_data['safety_factor']
        return gdf

    # coordinate system convertion to WGS84
    def convert_gdf_to_WGS84(self, gdf):
        return gdf.to_crs("EPSG:4326")

    # coordinate system convertion to CS92
    def convert_gdf_to_CS92(self, gdf):
        return gdf.to_crs("EPSG:2180")

    # generation of random points within passed polygon boundaries
    def generate_random_points_in_polygon(self, number, polygon):
        points = []
        min_x, min_y, max_x, max_y = polygon.bounds
        i= 0
        while i < number:
            point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
            if polygon.contains(point):
                points.append(point)
                i += 1
        return points  # returns list of shapely point

    # get all points in range of given radius for point
    def get_all_points_in_radius(self, points, point, radius):

        # delete point from points - to be improved
        points = points[points.lon != point.iloc[0].lon]
        points = points[points.lat != point.iloc[0].lat]

        points_gdf = gpd.GeoDataFrame(
            points,
            geometry=gpd.points_from_xy(
                points["lon"],
                points["lat"],
            ),
            crs={"init": "EPSG:4326"},
        )

        point_gdf = gpd.GeoDataFrame(
            point,
            geometry=gpd.points_from_xy(
                point["lon"],
                point["lat"],
            ),
            crs={"init": "EPSG:4326"},
        )

        points_gdf_proj = self.convert_gdf_to_CS92(points_gdf)
        point_gdf_proj = self.convert_gdf_to_CS92(point_gdf)

        x = point_gdf_proj.buffer(radius).unary_union
        neighbours = points_gdf_proj["geometry"].intersection(x)

        return points_gdf_proj[~neighbours.is_empty]
        

    # ===================
    # Example usage:
    #
    # points = random_points_in_polygon(65, gdf.iloc[3].geometry)
    # points += random_points_in_polygon(35, gdf.iloc[12].geometry)
    # points += random_points_in_polygon(35, gdf.iloc[9].geometry)
    # points_conv = []
    # for i, point in enumerate(points):
    #     points_conv.append([point.x, point.y])
    # st.map(pd.DataFrame(points_conv, columns=['lon', 'lat']))