from solution import (
    read_coordinates,
    build_clusters,
    get_top_clusters_product
)

# Run on the full dataset with 1000 connections
num_connections = 1000

msg = "Running solution on full dataset (8.csv) with "
msg += f"{num_connections} connections..."
print(msg)
print()

coords = read_coordinates("8.csv")
print(f"Total points in dataset: {len(coords)}")
print()

print(f"Making {num_connections} connections...")
clusters = build_clusters(coords, num_connections)

print(f"Number of clusters formed: {len(clusters)}")
print()

# Get cluster sizes sorted
sizes = sorted([len(c) for c in clusters], reverse=True)
print(f"Top {min(10, len(sizes))} cluster sizes: {sizes[:10]}")
print()

# Calculate product of top 3
product = get_top_clusters_product(clusters, top_n=3)
print(f"Top 3 cluster sizes: {sizes[0]}, {sizes[1]}, {sizes[2]}")
print(f"Product of top 3 cluster sizes: {product}")
print()

# Show some statistics
print(f"Smallest cluster size: {sizes[-1]}")
print(f"Average cluster size: {sum(sizes) / len(sizes):.2f}")
print(f"Total points in all clusters: {sum(sizes)}")
