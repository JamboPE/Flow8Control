# Low function setting is not linear so the values per midi value have been hard coded
import flow8Control as f8c
freqs = [
    20, 20, 21, 21, 22, 22, 23, 24, 24, 25, 26, 26, 27, 28, 29, 29, 30, 31, 32, 33,
    34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 48, 49, 51, 52, 53,
    55, 56, 58, 59, 61, 63, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 87,
    89, 92, 94, 97, 99, 102, 105, 108, 111, 114, 117, 120, 123, 126, 130, 133, 137, 141,
    145, 149, 153, 157, 161, 165, 170, 175, 179, 184, 189, 194, 200, 205, 211, 216, 222, 228,
    234, 241, 247, 254, 261, 268, 275, 283, 291, 299, 307, 315, 324, 332, 341, 351,
    360, 370, 380, 390, 401, 412, 423, 435, 446, 459, 471, 484, 497, 510,
    524, 539, 553, 568, 584, 600
]

def getMidiValue(freq):
    if freq in freqs:
        return freqs.index(freq)
    if freq >= 592:
        return 127
    for i in range(len(freqs)):
        if freqs[i] > freq:
            if freqs[i] - freq < freq - freqs[i-1]:
                return i
            else:
                return i-1
    exit(1)