def validate(start_point, end_point, eps, num_of_segments, h_min):
    if start_point > end_point or eps <= 0 or num_of_segments == 0 or h_min < 0:
        return False
    return True


def approximate(f, start_point, end_point):
    return (f(start_point) + f(end_point)) * (end_point - start_point) / 2

def I(f, start_point, end_point, h):
    val = 0
    x = start_point
    while x + h <= end_point:
        val += approximate(f, x, x + h)
        x += h

    return val

def getRungeeErr(I_h, I_h2):
    return abs((I_h - I_h2) / (pow(0.5, 2) - 1))

def integral(f, start_point, end_point, eps=1e-2, num_of_segments=100, h_min=1e-8):
    if not validate(start_point, end_point, eps, num_of_segments, h_min):
        raise Exception("Не валидные данные при нахождении интеграла")

    h = (end_point - start_point) / num_of_segments
    I_h = I(f, start_point, end_point, h)
    I_h2 = I(f, start_point, end_point, h / 2)
    err = getRungeeErr(I_h, I_h2)

    print(h)
    while err > eps:
        h /= 2

        if h < h_min:
            raise Exception("Решение не получено, шаг интегрирования стал недопустимо малым")

        I_h = I_h2
        I_h2 = I(f, start_point, end_point, h / 2)

        new_err = getRungeeErr(I_h, I_h2)
        if abs(err - new_err) <= eps / 100:
            raise Exception("Решение не получено, погрешность перестала уменьшаться")

        err = new_err

    print(h)
    print("=====")
    return I_h


def integral_sum(f, start_point, end_point, eps=1e-2, num_of_segments=1000, h_min=1e-8):
    if not validate(start_point, end_point, eps, num_of_segments, h_min):
        raise Exception("Не валидные данные при нахождении интеграла")

    val = 0
    i = start_point
    h = 1

    while i + h <= end_point:
        val += f(i)
        i += h

    return val