
import shutil
from pathlib import Path

# Change this to the folder you want to organize
SOURCE_FOLDER = Path.home() / "Downloads"

# File extension categories
FILE_TYPES = {
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx",
        ".xls", ".xlsx", ".csv"
    ],
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
        ".webp", ".ico"
    ],
    "Videos": [
        ".mp4", ".mkv", ".mov", ".avi", ".webm"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ],
    "Code": [
        ".py", ".java", ".c", ".cpp", ".html", ".css",
        ".js", ".php", ".sql", ".json"
    ]
}


def get_category(file_path):
    """Return a folder name based on the file extension."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_path(destination):
    """Avoid overwriting a file with the same name."""
    if not destination.exists():
        return destination

    folder = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        new_path = folder / f"{stem}_{counter}{suffix}"

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(folder, preview=True):
    """Organize files and display a summary."""
    folder = Path(folder).expanduser()

    if not folder.exists():
        print(f"Error: Folder does not exist: {folder}")
        return

    if not folder.is_dir():
        print("Error: The selected path is not a directory.")
        return

    moved = 0
    skipped = 0
    errors = 0

    print("\nFILE ORGANIZER")
    print("=" * 50)
    print(f"Folder: {folder}")
    print("Mode:", "PREVIEW ONLY" if preview else "MOVE FILES")
    print("-" * 50)

    try:
        # Only inspect files directly inside this folder
        for item in folder.iterdir():
            if not item.is_file():
                continue

            category = get_category(item)
            target_folder = folder / category
            destination = get_unique_path(target_folder / item.name)

            if preview:
                print(f"[PREVIEW] {item.name} -> {category}/")
                moved += 1
                continue

            try:
                target_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(destination))
                print(f"[MOVED] {item.name} -> {category}/{destination.name}")
                moved += 1

            except PermissionError:
                print(f"[PERMISSION DENIED] {item.name}")
                errors += 1

            except (shutil.Error, OSError) as error:
                print(f"[ERROR] {item.name}: {error}")
                errors += 1

    except PermissionError:
        print("Permission denied while reading the folder.")
        return

    print("-" * 50)
    print("SUMMARY")
    print(f"Files {'previewed' if preview else 'moved'}: {moved}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")

    if preview:
        print("\nNo files were moved.")
        print("Review the preview before running in move mode.")


if __name__ == "__main__":
    print("1. Preview file organization")
    print("2. Organize and move files")

    choice = input("Choose (1 or 2): ").strip()

    if choice == "1":
        organize_files(SOURCE_FOLDER, preview=True)
    elif choice == "2":
        confirm = input(
            "This will move files in Downloads. Continue? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            organize_files(SOURCE_FOLDER, preview=False)
        else:
            print("Operation cancelled.")
    else:
        print("Invalid choice. Please enter 1 or 2.")
