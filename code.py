from skimage import measure
from shapely.geometry import Polygon
import fiona
import geopandas as gpd

# Load the image and convert to binary
img = skimage.io.imread('image.png')
binary_img = img > threshold_value # replace threshold_value with your desired threshold

# Find contours in the binary image
contours = measure.find_contours(binary_img, 0.5)

# Convert each contour to a polygon and write to a shapefile
schema = {'geometry': 'Polygon', 'properties': {'id': 'int'}}
crs_epsg = 4326 # replace with your desired CRS
with fiona.open('output_shapefile.shp', 'w', 'ESRI Shapefile', schema=schema, crs=f'EPSG:{crs_epsg}') as output:
    for i, contour in enumerate(contours):
        # Convert the contour to a polygon
        poly = Polygon(contour)

        # Write the polygon to the shapefile
        output.write({
            'geometry': gpd.GeoSeries(poly).to_json(),
            'properties': {'id': i},
        })
