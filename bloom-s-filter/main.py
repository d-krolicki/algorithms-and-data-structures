import time

with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

S = ' '.join(text).lower()


def naiveSearch(S, W):
    indices = []
    i = len(W)
    m = 0
    count_comparisons = 0
    # print(type(S[m:m+i]))
    while True:
        if S[m:m+i] == W:
            indices.append(m)
        m += 1
        count_comparisons += 1
        if m >= len(S):
            break
    # print(indices)
    return len(indices),count_comparisons 

d = 256
q = 101

def hash(word):
    hw = 0
    for i in range(len(word)):  
        hw = (hw*d + ord(word[i])) % q
    return hw


def RabinKarp(S, W):
    indices = []
    i = len(W)
    m = 0
    count_comparisons = 0
    hashW = hash(W)
    while True:
        if hashW == hash(S[m:m+i]):
            count_comparisons += 1
            if S[m:m+i] == W:
                indices.append(m)
        m += 1
        count_comparisons += 1
        if m >= len(S):
            break
    return len(indices), count_comparisons


def RollingHash(S,W):
    hW = hash(W)
    lS = len(S)
    lW = len(W)
    indices = []
    count_comparisons = 0
    col = 0
    h = 1
    hashS = hash(S[0: lW])
    for y in range(lW - 1):
        h = (h * d) % q
    for m in range(1,lS-lW + 1):
        hashS = (d * (hashS - ord(S[m-1]) * h) + ord(S[m + lW-1])) % q
        if hashS == hW:
            count_comparisons += 1
            if S[m:m + lW] == W:
                indices.append(m)
            else:
                col += 1
    return len(indices), count_comparisons, col



def calcLPS(W):
    pos = 1
    cnd = 0
    LPS = [0 for _ in range(len(W)+1)]
    LPS[0] = -1
    while pos < len(W):
        if W[pos] == W[cnd]:
            LPS[pos] == LPS[cnd]
        else:
            LPS[pos] = cnd
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = LPS[cnd]
        pos += 1
        cnd += 1
    LPS[pos] = cnd
    return LPS


def KMP(S,W):
    m = 0
    k = 0
    count_comparisons = 0
    T = calcLPS(W)
    P = []

    while m < len(S):
        count_comparisons += 1
        if W[k] == S[m]:
            m += 1
            k += 1
            if k == len(W):
                P.append(m-k)
                k = T[k]
        else:
            k = T[k]
            if k<0:
                m += 1
                k += 1
    return len(P), count_comparisons 


def testNaive(W):
    t_start = time.perf_counter()
    print(naiveSearch(S, W))
    t_stop = time.perf_counter()
    print("Czas obliczeń dla naiveSearch:", "{:.7f}".format(t_stop - t_start))
    return None

def testRabinKarp(W):
    t_start = time.perf_counter()
    print(RabinKarp(S, W))
    t_stop = time.perf_counter()
    print("Czas obliczeń dla RabinKarp:", "{:.7f}".format(t_stop - t_start))
    return None

def testRollingHash(W):
    t_start = time.perf_counter()
    print(RollingHash(S, W))
    t_stop = time.perf_counter()
    print("Czas obliczeń dla RollingHash:", "{:.7f}".format(t_stop - t_start))
    return None

def testKMP(W):
    t_start = time.perf_counter()
    print(KMP(S, W))
    t_stop = time.perf_counter()
    print("Czas obliczeń dla KMP:", "{:.7f}".format(t_stop - t_start))
    return None

word = "book"

testNaive(word)
testRabinKarp(word)
testRollingHash(word)
testKMP(word)