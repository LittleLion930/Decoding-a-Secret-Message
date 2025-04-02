import requests
import re

def fetch_google_doc_data(url):
    """
    Fetches and parses the data from the Google Doc URL.
    """
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve document.")
        return

    # Extract content within <p> tags
    text = response.text
    content = re.findall(r'<p[^>]*>(.*?)</p>', text)

    # Initialize variables
    char_map = {}

    # Process extracted data
    i = 0
    while i < len(content) - 2:
        try:
            x = int(re.search(r'>(\d+)<', content[i]).group(1))
            char = re.search(r'>([^<]+)<', content[i + 1]).group(1)
            y = int(re.search(r'>(\d+)<', content[i + 2]).group(1))

            char_map[(x, y)] = char
            i += 3
        except (ValueError, AttributeError):
            i += 1

    # Determine grid dimensions
    if not char_map:
        print("No valid data found.")
        return

    max_x = max(coord[0] for coord in char_map.keys())
    max_y = max(coord[1] for coord in char_map.keys())

    # Create and populate the grid
    grid = [[" " for _ in range(max_y + 1)] for _ in range(max_x + 1)]
    for (x, y), char in char_map.items():
        grid[x][y] = char

    # Print the grid
    for row in grid:
        print("".join(row))

# Example usage with the provided URL
fetch_google_doc_data("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")