import xml.etree.ElementTree as ET

# Load and inspect the XML file
try:
    tree = ET.parse("data.xml")
    root = tree.getroot()
    
    print("=" * 60)
    print("ROOT ELEMENT:", root.tag)
    print("=" * 60)
    
    # Print first few records
    records = root.findall(".//record")
    print(f"\nTotal records found: {len(records)}")
    print("\nFirst 3 records structure:")
    print("-" * 60)
    
    for i, record in enumerate(records[:3]):
        print(f"\nRecord {i+1}:")
        for child in record:
            print(f"  {child.tag}: {child.text}")
            # If it has sub-elements, show them
            if child.tag == "crops":
                for crop in child:
                    crop_name = crop.get("name")
                    prod_elem = crop.find("production")
                    prod_val = prod_elem.text if prod_elem is not None else "N/A"
                    print(f"    - {crop.tag}[@name='{crop_name}']: {prod_val}")
    
    print("\n" + "=" * 60)
    print("FULL XML PREVIEW (first 1000 chars):")
    print("=" * 60)
    with open("data.xml", "r") as f:
        content = f.read()
        print(content[:1000])
        if len(content) > 1000:
            print("...[truncated]...")

except FileNotFoundError:
    print("ERROR: data.xml file not found!")
except Exception as e:
    print(f"ERROR: {e}")