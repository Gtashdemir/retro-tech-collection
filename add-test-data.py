from datetime import datetime
import database


item_types = [
    "Computer",
    "Camera",
    "Phone",
    "Video Player"
]

for item_type in item_types:
    for number in range(1, 46):
        name = f"Test {item_type} {number}"
        description = f"Test item for {item_type} pagination"
        date_added = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        date_made = "01/01/2000"

        database.add_item(
            name,
            item_type,
            description,
            date_added,
            date_made
        )

print("Test data added successfully!")