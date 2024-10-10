import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from mask_to_polygon import get_polygons_from_mask

def create_krpano_hotspot(polygon, name, fill_color="0xAA0000", fill_alpha="0.5", border_color="0xAA0000", border_width="3.0"):
    hotspot = ET.Element("hotspot")
    hotspot.set("name", name)
    hotspot.set("keep", "false")
    hotspot.set("zorder", "0")
    hotspot.set("fillcolor", fill_color)
    hotspot.set("fillalpha", fill_alpha)
    hotspot.set("bordercolor", border_color)
    hotspot.set("borderwidth", border_width)
    hotspot.set("visible", "true")
    hotspot.set("enabled", "true")
    
    for x, y in polygon:
        point = ET.SubElement(hotspot, "point")
        # Convert normalized coordinates to spherical coordinates
        ath = str(x * 360 - 180)  # Convert x from [0, 1] to [-180, 180]
        atv = str(-90 + y * 180)  # Convert y from [0, 1] to [-90, 90], flipping the vertical axis
        point.set("ath", ath)
        point.set("atv", atv)
    
    return hotspot

def polygons_to_krpano_xml(polygons):
    root = ET.Element("krpano")
    
    for i, polygon in enumerate(polygons):
        hotspot = create_krpano_hotspot(polygon, f"hotspot_{i+1}")
        root.append(hotspot)
    
    # Convert to string and pretty-print
    xml_str = ET.tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    
    return pretty_xml

# Example usage
image_path = 'test/merged_sphere_level_1_annotation.jpg'
polygons = get_polygons_from_mask(image_path)
krpano_xml = polygons_to_krpano_xml(polygons)

# print(krpano_xml)

# Optionally, save to file
with open("test/hotspots.xml", "w") as f:
    f.write(krpano_xml)