import matplotlib.pyplot as plt
import numpy as np


# koef_nomb_max =5
# koef_nomb = 5
# na = 0
# Aa = 1300
# Bb = 730
# Bbd = 530
# MU3 = np.zeros(2000, 200)
# MdU = np.zeros(2000)
# MU = np.zeros(2000)
# MU2 = np.zeros(2000)
# MI = np.zeros(2000)
# MI2 = np.zeros(2000)
# x1 = np.zeros(koef_nomb_max+4)
# x2 = np.zeros(koef_nomb_max+4)
# x3 = np.zeros(320, (koef_nomb_max+4))
# fileNamee = r"C:\Users\vika-\Magnetic-Plethysmography\super-puper.txt"
# U = []
#
# # read file
# with open(fileNamee, "r") as file:
#     for line in file:
#         line = line[7:]
#         U.append(float(line[:-1]))
#
#
# for ind in range(0,99):
#     n = str(ind)
#     if ind<10:
#         n = '000'+n
#     if (ind >= 10) and (ind < 100):
#         n = '00'+n
#
#
#     for i in range(0, Aa-1):
#         if (U[i] > 10 ** 7) and (U[i] < -10 ** 7):
#             U[i] = 0


# for i in range(0, Aa-1):
#     MU2 += (U[i])
#     MU += (0)

#hebyshev Fpass=20, Fstop=35
def processing(U):

    U11 = U[2]
    U12 = U[2]
    U10 = U[2]
    U21 = U[2]
    U22 = U[2]
    U20 = U[2]
    U31 = U[2]
    U32 = U[2]
    U30 = U[2]
    U41 = U[2]
    U42 = U[2]
    U40 = U[2]
    leng = len(U)
    for i in range(3, leng):
        U12 = U11
        U11 = U10
        U10 = ((U[i] * 0.4368896484375) - (U[i - 1] * 0.4368896484375 * 1.7928466796875) + (U[i - 2] * 0.441925048828125) + (U11 * 1.82476806640625) - (U12 * 0.915283203125))
        U22 = U21
        U21 = U20
        U20 = ((U10 * 0.333099365234375) - (U11 * 0.333099365234375 * 1.71746826171875) + (U12 * 0.333099365234375) + (U21 * 1.65509033203125) - (U22 * 0.74920654296875))
        U32 = U31
        U31 = U30
        U30 = ((U20 * 0.181549072265625) - (U21 * 0.181549072265625 * 1.41815185546875) + (U22 * 0.1869049072265625) + (U31 * 1.4730224609375) - (U32 * 0.57867431640625))
        U42 = U41
        U41 = U40
        U40 = ((U30 * 0.0504913330078125) - (U31 * 0.0504913330078125 * 0.319580078125) + (U32 * 0.0504913330078125) + (U41 * 1.331787109375) - (U42 * 0.44891357421875))
        U[i] = U40
    return U

#hebyshev Fpass=30, Fstop=49
#def processing(U):
#    U11 = U[2]
#    U12 = U[2]
#    U10 = U[2]
#    U21 = U[2]
#    U22 = U[2]
#    U20 = U[2]
#    U31 = U[2]
#    U32 = U[2]
#    U30 = U[2]
#    U41 = U[2]
#    U42 = U[2]
#    U40 = U[2]
#    leng = len(U)
#    for i in range(3, leng):
#        U12 = U11
#        U11 = U10
#        U10 = ((U[i] * 0.441925048828125) - (U[i - 1] * 0.441925048828125 * 1.60125732421875) + (
#                U[i - 2] * 0.441925048828125) + (U11 * 1.70794677734375) - (U12 * 0.8841552734375))
#        U22 = U21
#        U21 = U20
#        U20 = ((U10 * 0.331634521484375) - (U11 * 0.331634521484375 * 1.466064453125) + (
#                U12 * 0.331634521484375) + (U21 * 1.491455078125) - (U22 * 0.66851806640625))
#        U32 = U31
#        U31 = U30
#        U30 = ((U20 * 0.1869049072265625) - (U21 * 0.1869049072265625 * 0.973876953125) + (
#                U22 * 0.1869049072265625) + (U31 * 1.2708740234375) - (U32 * 0.462646484375))
#        U42 = U41
#        U41 = U40
#        U40 = ((U30 * 0.07025146484375) - (U31 * 0.07025146484375 * 0.9468994140625) + (U32 * 0.07025146484375) + (
#                U41 * 1.1087646484375) - (U42 * 0.3157958984375))
#        U[i] = U40
#    return U







    #     for i in range(0, Aa - 1):
    #         MU[i] = (MU[i] * 1.2 * 4.6) / 2 ** 24  # (8388608 / 5)
    #
    #     tmu = MU[Bb - 1]
    #     for i in range(0, Aa - 1):
    #         MU[i] = MU[i] - tmu
    #     for i in range(0, 49):
    #         MU[i] = 0
    #     for i in range(Aa - 51, Aa - 1):
    #         MU[i] = 0
    #     for i in range(0, Aa - 1):
    #         MU3[i][ind + 1] = MU[i]
    #
    # plt.figure(3)
    # plt.plot(range(len(MU2)), MU2)

 #          MU[i] = MU3[i, ind]
  #      for i in range(1, Aa - 2):
  #          MdU[i].append(((MU[i + 1] - MU[i - 1])) / (2 / 1953))
  #      Q = []
  #      for cl in range(Bb-1, Bbd+Bb-1):
  #          for kon in range(0, koef_nomb-1):
  #              Q[cl][kon] = MU[cl] ** (kon)
  #          Q[cl][koef_nomb + 1] = MdU[cl]
  #      A = []
  #      B = []
  #      for kon1 in range(0, koef_nomb):
  #          for kon2 in range(0, koef_nomb):
  #              for c1 in range(Bd-1, Bbd+Bb - 1):
  #                  A[kon1][kon2] = A[kon1][kon2] + (Q[cl][kon1] .* Q[cl][kon2])
  #          for c1 in range(Bd - 1, Bbd + Bb - 1):
  #              B[1][kon1] = B[1][kon1] + (MI[cl].* Q[cl][kon1])
   #     x(1: (koef_nomb + 1)) = B / A
#
 #       for kon in range(0,koef_nomb):
  #          x2[kon] = x[kon]
   #     x2[koef_nomb + 3] = x2[0] - 3.37 * 10 ** -8
   #     x2[koef_nomb + 1] = 1 / x2[koef_nomb + 3]
    #    for kon in range(0,koef_nomb + 3):
     #       x3[ind][kon] = x2[kon]
   # plt.figure(5)
    #plt.plot(range(len(x3)), x3)
    # plt.show()


















