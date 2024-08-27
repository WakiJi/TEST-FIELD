from Crypto.Util.number import *

# 原始参数
p = 10297529403524403127640670200603184608844065065952536889
a = 2
G = (8879931045098533901543131944615620692971716807984752065, 4106024239449946134453673742202491320614591684229547464)
Q = (6784278627340957151283066249316785477882888190582875173, 6078603759966354224428976716568980670702790051879661797)

# 定义加法
def add_THcurve(P, Q):
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    x1, y1 = P
    x2, y2 = Q
    x3 = (x1 - y1 ** 2 * x2 * y2) * pow(a * x1 * y1 * x2 ** 2 - y2, -1, p) % p
    y3 = (y1 * y2 ** 2 - a * x1 ** 2 * x2) * pow(a * x1 * y1 * x2 ** 2 - y2, -1, p) % p
    return x3, y3

# 定义标量乘法
def mul_THcurve(n, P):
    R = (0, 0)
    while n > 0:
        if n % 2 == 1:
            R = add_THcurve(R, P)
        P = add_THcurve(P, P)
        n = n // 2
    return R

# 逆向过程
def reverse_mul_THcurve(Q, G, p):
    # 假设我们通过逐步“减去”G的贡献
    m = 0
    current = Q
    step = 1
    
    while current != (0, 0):
        for i in range(1, p):
            if add_THcurve(mul_THcurve(i, G), mul_THcurve(m, G)) == current:
                m += i * step
                current = (current[0] * pow(i, -1, p)) % p, (current[1] * pow(i, -1, p)) % p
                step *= 2
                break
        else:
            break
    return m

# 尝试逆向计算 m
m = reverse_mul_THcurve(Q, G, p)
print("Recovered m =", m)
print("FLAG =", long_to_bytes(m))
