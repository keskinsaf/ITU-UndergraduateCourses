import numpy as np
from Utils import convolve2Signals

c1 = np.random.rand(400000) * 100
c2 = np.random.rand(40000) * 10

print(c1.shape, c2.shape)

result = convolve2Signals(c1,c2)
np_result = np.convolve(c1,c2)

# for i in range(result.shape[0]):
#     print("For value " + str(i) + ":", end=" ")
#     print(result[i], end=" ")
#     print(np_result[i], end=" ")
#     print( np.allclose(result[i], np_result[i]), end="\n\n\n\n\n")
for i in range(220000, 220010):
    print(result[i], np_result[i])

print(np.allclose(result, np_result ))