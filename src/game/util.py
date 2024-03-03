from .models import Position


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def get_direction(current_x, current_y, dest_x, dest_y, teleport1_x, teleport1_y, teleport2_x, teleport2_y):
    delta_x = clamp(dest_x - current_x, -1, 1)
    delta_y = clamp(dest_y - current_y, -1, 1)
    print("delta_x: ", delta_x)
    print("delta_y: ", delta_y)
    print("current_x: ", current_x)
    print("current_y: ", current_y)
    print("teleport1: ", teleport1_x, teleport1_y)
    print("teleport2: ", teleport2_x, teleport2_y)

    if delta_x != 0 and delta_y != 0:
        if (current_x + delta_x, current_y) not in [(teleport1_x, teleport1_y), (teleport2_x, teleport2_y)]:
            delta_y = 0
        else:
            print("teleport1\n\n")
            delta_x = 0
    elif delta_x != 0 and delta_y == 0:
        if (current_x + delta_x, current_y) in [(teleport1_x, teleport1_y), (teleport2_x, teleport2_y)]:
            print("teleport2\n\n")
            delta_x = 0
            if current_y == 14 or current_y == 0:
                delta_y = -1
            else:
                delta_y = 1
    elif delta_x == 0 and delta_y != 0:
        if (current_x, current_y + delta_y) in [(teleport1_x, teleport1_y), (teleport2_x, teleport2_y)]:
            print("teleport3\n\n")
            delta_y = 0
            if current_x == 14 or current_x == 0:
                delta_x = -1
            else:
                delta_x = 1
    if current_x + delta_x == dest_x and (current_x + delta_x, current_y + dest_y) in [(teleport1_x, teleport1_y), (teleport2_x, teleport2_y)]:
            print("teleport0\n\n")
            delta_x = 0
            delta_y = clamp(dest_y - current_y, -1, 1)
    elif current_y + delta_y == dest_y and (current_x + delta_x, current_y + dest_y) in [(teleport1_x, teleport1_y), (teleport2_x, teleport2_y)]:
        print("teleport0\n\n")
        delta_x = clamp(dest_x - current_x, -1, 1)
        delta_y = 0
    print("delta_x1: ", delta_x)
    print("delta_y2: ", delta_y)
    return delta_x, delta_y


def position_equals(a: Position, b: Position):
    return a.x == b.x and a.y == b.y
