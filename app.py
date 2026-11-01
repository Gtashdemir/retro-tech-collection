# You will be building an application for a retro technology collector. This collector likes to
# collect old technology, like computers, cameras, phones etc. You will be building a small
# database program so the collector can record all the items in the collection.
# The collector must be able to:
# 1. Add items to the collection.
# 2. Show the items in the collection (by type).
# 3. Delete items from the collection.
# When the program runs, it should display a menu with the options above, as well as an
# exit option. The user will then choose an option, and the program will either ask for
# input, or display output, depending on the user’s choice.
# I will leave the GUI to the FE people :(

#                          ┌───────────────────┐
#                          │      app.py       │
#                          │                   │
#                          │ menus             │
#                          │ validation        │
#                          │ input/output      │
#                          └─────────┬─────────┘
#                                    │
#                             function calls
#                                    │
#                                    ▼
#                          ┌───────────────────┐
#                          │    database.py    │
#                          │                   │
#                          │ create_table()    │
#                          │ add_item()        │
#                          │ count_items()     │
#                          └─────────┬─────────┘
#                                    │
#                                   SQL
#                                    │
#                                    ▼
#                          ┌───────────────────┐
#                          │   collection.db   │
#                          └───────────────────┘

from datetime import datetime
import database
import csv
import os


database.create_table()


def get_valid_date(message):
    while True:
        date_text = input(message).strip()

        try:
            date = datetime.strptime(date_text, "%d/%m/%Y")
            return date.strftime("%d/%m/%Y")
        except ValueError:
            print("Invalid date. Please use DD/MM/YYYY.")


def get_item_type():
    print("\nTypes:")
    print("1. Computer")
    print("2. Camera")
    print("3. Phone")
    print("4. Video Player")

    while True:
        type_choice = input("Choose type: ").strip()

        if type_choice == "1":
            return "Computer"
        elif type_choice == "2":
            return "Camera"
        elif type_choice == "3":
            return "Phone"
        elif type_choice == "4":
            return "Video Player"
        else:
            print("Invalid type. Please enter a number from 1 to 4.")


while True:
    print("\n" + "=" * 32)
    print("   RETRO TECH COLLECTION")
    print("=" * 32)
    print("  1. Add item")
    print("  2. Show items by type")
    print("  3. Update item")
    print("  4. Delete item")
    print("  5. Export collection")
    print("  6. Exit")
    print("-" * 32)

    choice_text = input("Choose an option: ").strip()

    # Validate menu choice
    if choice_text == "":
        print("Cannot be empty. Please enter a number from 1 to 6.")
        continue

    if choice_text not in ("1", "2", "3", "4", "5", "6"):
        print("Invalid choice. Please enter a number from 1 to 6.")
        continue

    choice = int(choice_text)

    # Add new item
    if choice == 1:
        print("\n" + "-" * 32)
        print("ADDING AN ITEM")
        print("-" * 32)

        name = input("Name: ").strip()

        while name == "":
            print("Name cannot be empty.")
            name = input("Name: ").strip()

        item_type = get_item_type()

        description = input("Description: ").strip()

        while description == "":
            print("Description cannot be empty.")
            description = input("Description: ").strip()

        date_added = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        date_made = get_valid_date(
            "Date of manufacture (DD/MM/YYYY): "
        )

        database.add_item(
            name,
            item_type,
            description,
            date_added,
            date_made
        )

        print("\nItem added successfully!")
        print("Date added:", date_added)

    # Show items by type
    elif choice == 2:
        item_count = database.count_items()

        if item_count == 0:
            print("\nThere are no items in the collection.")
            continue

        item_type = get_item_type()

        print("\n" + item_type, "Collection")
        print("-" * 32)
        print("[A] Show all")
        print("[S] Search by name")
        print("[B] Back")

        browse_choice = input("Choose an option: ").strip().lower()

        if browse_choice == "b":
            continue

        if browse_choice == "a":
            search_text = None
            total_items = database.count_items_by_type(item_type)

        elif browse_choice == "s":
            search_text = input("Search by name: ").strip()

            if search_text == "":
                print("\nSearch cannot be empty.")
                continue

            total_items = database.count_search_results(
                item_type,
                search_text
            )

        else:
            print("\nInvalid option.")
            continue

        if total_items == 0:
            print("\nNo items found.")
            continue

        page_size = 20
        page = 1

        total_pages = (total_items + page_size - 1) // page_size

        while True:
            offset = (page - 1) * page_size

            if search_text is None:
                items = database.get_items_by_type(
                    item_type,
                    limit=page_size,
                    offset=offset
                )
            else:
                items = database.search_items_by_name(
                    item_type,
                    search_text,
                    limit=page_size,
                    offset=offset
                )

            if search_text is None:
                print(
                    "\nShowing:",
                    item_type,
                    "- Page",
                    page,
                    "of",
                    total_pages
                )
            else:
                print(
                    '\nSearch results for "' + search_text + '"',
                    "- Page",
                    page,
                    "of",
                    total_pages
                )

            print("-" * 40)

            for item in items:
                print("ID:", item[0])
                print("Name:", item[1])
                print("Description:", item[3])
                print("Date added:", item[4])
                print("Date made:", item[5])
                print("-" * 40)

            print("[N] Next page")
            print("[P] Previous page")
            print("[B] Back")

            navigation = input("Choose an option: ").strip().lower()

            if navigation == "n":
                if page < total_pages:
                    page += 1
                else:
                    print("\nYou are already on the last page.")

            elif navigation == "p":
                if page > 1:
                    page -= 1
                else:
                    print("\nYou are already on the first page.")

            elif navigation == "b":
                break

            else:
                print("\nInvalid option. Please choose N, P or B.")

    # Update item
    elif choice == 3:
        print("\n" + "-" * 32)
        print("UPDATE AN ITEM")
        print("-" * 32)

        search_text = input("Search item by name: ").strip()

        if search_text == "":
            print("Search cannot be empty.")
            continue

        items = database.search_all_items_by_name(search_text)

        if not items:
            print("No items found.")
            continue

        print("\nSearch results:")
        print("-" * 40)

        for item in items:
            print("ID:", item[0])
            print("Name:", item[1])
            print("Type:", item[2])
            print("Description:", item[3])
            print("Date added:", item[4])
            print("Date made:", item[5])
            print("-" * 40)

        item_id_text = input("Enter the ID of the item to update: ").strip()

        if item_id_text == "":
            print("ID cannot be empty.")
            continue

        if not item_id_text.isdigit():
            print("Invalid ID. Please enter a number.")
            continue

        item_id = int(item_id_text)

        selected_item = None

        for item in items:
            if item[0] == item_id:
                selected_item = item
                break

        if selected_item is None:
            print("Please choose an ID from the search results.")
            continue

        print("\nSelected item:")
        print("-" * 40)
        print("ID:", selected_item[0])
        print("Name:", selected_item[1])
        print("Type:", selected_item[2])
        print("Description:", selected_item[3])
        print("Date added:", selected_item[4])
        print("Date made:", selected_item[5])
        print("-" * 40)

        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Type")
        print("3. Description")
        print("4. Date of manufacture")
        print("5. Cancel")

        update_choice = input("Choose an option: ").strip()

        if update_choice == "":
            print("Choice cannot be empty.")
            continue

        if update_choice not in ("1", "2", "3", "4", "5"):
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue


        if update_choice == "1":
            print("\nCurrent name:", selected_item[1])

            new_name = input("New name: ").strip()

            if new_name == "":
                print("Name cannot be empty.")
                continue

            database.update_item_name(
                item_id,
                new_name
            )

            print("Name updated successfully!")

        if update_choice == "2":
            print("\nCurrent type:", selected_item[2])

            print("\nChoose the new type:")
            new_type = get_item_type()

            database.update_item_type(
                item_id,
                new_type
            )

            print("Type updated successfully!")

        if update_choice == "3":
            print("\nCurrent description:", selected_item[3])

            new_description = input("New description: ").strip()

            if new_description == "":
                print("Description cannot be empty.")
                continue

            database.update_item_description(
                item_id,
                new_description
            )

            print("Description updated successfully!")

        if update_choice == "4":
            print("\nCurrent date:", selected_item[5])

            new_date_made = get_valid_date(
                "New date of manufacture (DD/MM/YYYY): "
            )

            database.update_item_date_made(
                item_id,
                new_date_made
            )

            print("Date of manufacture updated successfully!")

        if update_choice == "5":
            print("Update cancelled.")
            continue

    # Delete item
    elif choice == 4:
        print("\n" + "-" * 32)
        print("DELETE AN ITEM")
        print("-" * 32)

        search_text = input("Search item by name: ").strip()

        if search_text == "":
            print("Search cannot be empty.")
            continue

        items = database.search_all_items_by_name(search_text)

        if not items:
            print("No items found.")
            continue

        print("\nSearch results:")
        print("-" * 40)

        for item in items:
            print("ID:", item[0])
            print("Name:", item[1])
            print("Type:", item[2])
            print("Description:", item[3])
            print("Date added:", item[4])
            print("Date made:", item[5])
            print("-" * 40)

        item_id_text = input("Enter the ID of the item to delete: ").strip()

        if item_id_text == "":
            print("ID cannot be empty.")
            continue

        if not item_id_text.isdigit():
            print("Invalid ID. Please enter a number.")
            continue

        item_id = int(item_id_text)

        selected_item = None

        for item in items:
            if item[0] == item_id:
                selected_item = item
                break

        if selected_item is None:
            print("Please choose an ID from the search results.")
            continue

        print("\nSelected item:")
        print("-" * 40)
        print("ID:", selected_item[0])
        print("Name:", selected_item[1])
        print("Type:", selected_item[2])
        print("Description:", selected_item[3])
        print("Date added:", selected_item[4])
        print("Date made:", selected_item[5])
        print("-" * 40)

        confirmation = input(
            "Are you sure you want to delete this item? (Y/N): "
        ).strip().lower()

        if confirmation == "n":
            print("Delete cancelled.")
            continue

        if confirmation != "y":
            print("Invalid choice. Delete cancelled.")
            continue

        database.delete_item(item_id)

        print("Item deleted successfully!")


    elif choice == 5:

        while True:
            print("\n" + "-" * 32)
            print("EXPORT COLLECTION")
            print("-" * 32)

            print("1. Export all items")
            print("2. Export by type")
            print("3. Back")

            export_choice = input("Choose an option: ").strip()

            if export_choice == "":
                print("Choice cannot be empty. Please enter a number from 1 to 3.")
                continue

            if export_choice not in ("1", "2", "3"):
                print("Invalid choice. Please enter a number from 1 to 3.")
                continue

            if export_choice == "1":
                items = database.get_all_items()

                if not items:
                    print("There are no items to export.")
                    continue

                os.makedirs("exports", exist_ok=True)

                timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

                filename = f"retro_tech_collection_{timestamp}.csv"
                filepath = os.path.join("exports", filename)

                with open(filepath, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)

                    writer.writerow([
                        "ID",
                        "Name",
                        "Type",
                        "Description",
                        "Date Added",
                        "Date Made"
                    ])

                    writer.writerows(items)

                print("\nExported", len(items), "items successfully.")
                print("File:")
                print(filepath)


            elif export_choice == "2":
                item_type = get_item_type()
                items = database.get_all_items_by_type(item_type)

                if not items:
                    print("\nThere are no", item_type, "items to export.")
                    continue

                os.makedirs("exports", exist_ok=True)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
                type_filename = item_type.lower().replace(" ", "_")
                filename = f"{type_filename}_{timestamp}.csv"
                filepath = os.path.join("exports", filename)

                with open(filepath, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([

                        "ID",
                        "Name",
                        "Type",
                        "Description",
                        "Date Added",
                        "Date Made"
                    ])

                    writer.writerows(items)

                print("\nExported", len(items), item_type, "items successfully.")
                print("File:")
                print(filepath)

            elif export_choice == "3":
                break

    # Exit
    elif choice == 6:
        print("\nGoodbye!")
        break