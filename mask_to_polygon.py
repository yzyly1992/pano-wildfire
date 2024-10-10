import cv2
import numpy as np
from shapely.geometry import Polygon

def simplify_contour(contour, epsilon=0.01):
    peri = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, epsilon * peri, True)

def normalize_coordinates(points, image_shape):
    height, width = image_shape[:2]
    return [(x / width, y / height) for x, y in points]

def get_polygons_from_mask(image_path, simplify_epsilon=0.01):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Unable to read image at {image_path}")

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range for blue color in HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # Create a mask for blue color
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    polygons = []
    for contour in contours:
        # Simplify the contour
        simplified_contour = simplify_contour(contour, simplify_epsilon)
        
        # Convert to list of tuples and normalize coordinates
        points = [tuple(point[0]) for point in simplified_contour]
        normalized_points = normalize_coordinates(points, image.shape)
        
        # Create a Shapely polygon and simplify it further if needed
        polygon = Polygon(normalized_points)
        if not polygon.is_valid:
            polygon = polygon.buffer(0)
        
        polygons.append(list(polygon.exterior.coords))

    return polygons

# # Example usage
# image_path = 'path/to/your/mask_image.png'
# result = get_polygons_from_mask(image_path)

# print(f"Found {len(result)} polygons:")
# for i, polygon in enumerate(result):
#     print(f"Polygon {i + 1}: {polygon}")