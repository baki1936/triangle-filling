def vector_interp1(p1, p2, V1, V2, coord, dim):
    x1, y1 = p1
    x2, y2 = p2
    if dim == 1:
        if x2 == x1: # in case the denominator is 0
            return V1
        interp = (coord - x1)/(x2 - x1)
    elif dim == 2:
        if y2 == y1:
            return V1
        interp = (coord - y1)/(y2 - y1)
    else:
        return None
    V = [V1[i] + interp*(V2[i] - V1[i]) for i in range(len(V1))]
    return V