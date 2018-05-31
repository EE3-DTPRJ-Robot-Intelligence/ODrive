
import numpy as np
import matplotlib.pyplot as plt

adchist = [(0, 137477),
(1, 98524),
(2, 71744),
(3, 60967),
(4, 44372),
(5, 46348),
(6, 19944),
(7, 10092),
(8, 13713),
(9, 11182),
(10, 6903),
(11, 4072),
(12, 2642),
(13, 968),
(14, 296),
(15, 166),
(16, 17),
(17, 2),
(-1, 39662),
(-2, 43502),
(-3, 57596),
(-4, 33915),
(-5, 25611),
(-6, 10880),
(-7, 8237),
(-8, 3518),
(-9, 4789),
(-10, 4689),
(-11, 6345),
(-12, 3901),
(-13, 5781),
(-14, 4803),
(-15, 6428),
(-16, 3563),
(-17, 4478),
(-18, 976),
(-19, 491)]

adchist.sort()

adchist = np.array(adchist)

plt.figure()
plt.bar(adchist[:,0], adchist[:,1])
plt.show()