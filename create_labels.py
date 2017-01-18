import numpy as np

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out0.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out1.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out2.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out3.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out4.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out5.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out6.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out7.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out8.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_dataset/labels/out9.npy', a)

for i in range(10, 86):
	print i
	a = np.array([0,1,0,0,0])
	np.save('shirts_dataset/labels/out' +str(i)+ '.npy', a)

for i in range(86, 154):
	print i
	a = np.array([1,0,0,0,0])
	np.save('shirts_dataset/labels/out' +str(i)+ '.npy', a)



#test labels
a = np.array([1,0,0,0,0])
np.save('shirts_test/labels/out0.npy', a)

a = np.array([0,1,0,0,0])
np.save('shirts_test/labels/out1.npy', a)

a = np.array([0,1,0,0,0])
np.save('shirts_test/labels/out2.npy', a)

a = np.array([0,1,0,0,0])
np.save('shirts_test/labels/out3.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_test/labels/out4.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_test/labels/out5.npy', a)

a = np.array([0,1,0,0,0])
np.save('shirts_test/labels/out6.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_test/labels/out7.npy', a)

a = np.array([0,1,0,0,0])
np.save('shirts_test/labels/out8.npy', a)

a = np.array([1,0,0,0,0])
np.save('shirts_test/labels/out9.npy', a)