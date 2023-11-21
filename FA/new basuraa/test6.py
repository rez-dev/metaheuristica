def merge_segments(firefly_i, firefly_j):
    def build_segment(node, firefly_i, firefly_j):
        segment = [node]
        index_i = firefly_i.index(node)
        while index_i < len(firefly_i) - 1 and firefly_i[index_i:index_i+2] in [firefly_j[i:i+2] for i in range(len(firefly_j) - 1)]:
            segment.extend(firefly_i[index_i:index_i+2])
            index_i += 2
        index_i = firefly_i.index(node)
        while index_i > 0 and firefly_i[index_i-1:index_i+1] in [firefly_j[i:i+2] for i in range(len(firefly_j) - 1)]:
            segment = firefly_i[index_i-1:index_i+1] + segment
            index_i -= 2
        return segment

    new_fireflies = []
    different_edges = [edge for edge in firefly_j if edge not in firefly_i]
    for selected_edge in different_edges:
        x, y = selected_edge[4], selected_edge[9]
        segment_x = build_segment(x, firefly_i, firefly_j)
        segment_y = build_segment(y, firefly_i, firefly_j)
        merged_1 = segment_x + segment_y
        merged_2 = segment_y + segment_x
        merged_3 = segment_x[::-1] + segment_y
        merged_4 = segment_y[::-1] + segment_x

        new_fireflies.extend([merged_1, merged_2, merged_3, merged_4])

    return new_fireflies

# Ejemplo de uso:
firefly_i = [6, 7, 8, 4, 2, 1, 5, 15, 12, 3, 16, 11, 9, 10, 13, 14]
firefly_j = [6, 7, 12, 13, 14, 1, 8, 4, 2, 3, 16, 11, 9, 10, 15, 5]

resulting_fireflies = merge_segments(firefly_i, firefly_j)
print(f"Firefly i: {firefly_i}")
print(f"Firefly j: {firefly_j}")
# print(f"Resulting fireflies: {resulting_fireflies}")
# print(f"Number of resulting fireflies: {len(resulting_fireflies)}")

for idx, firefly in enumerate(resulting_fireflies, start=1):
    print(f"Firefly i{idx}: {firefly}")

