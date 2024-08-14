

def grouped(list, size=4):
    grouped = []
    for i in range(0, len(list), size):
        grouped.append(list[i:i + size])
    return grouped