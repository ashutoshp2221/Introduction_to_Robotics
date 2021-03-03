import numpy as np

coord = np.array(list(map(float, input('Enter coordinates of the point: ').split()))).reshape((3, 1))

# np.deg2rad converts angle in degree to radians

angX = np.deg2rad(float(input("Rotation about X axis in degree: ")))
angY = np.deg2rad(float(input("Rotation about Y axis in degree: ")))
angZ = np.deg2rad(float(input("Rotation about Z axis in degree: ")))

rotX = np.array([[1, 0, 0],
                [0, np.cos(angX), -np.sin(angX)],
                [0, np.sin(angX), np.cos(angX)]])

rotY = np.array([[np.cos(angY), 0, np.sin(angY)],
                [0, 1, 0],
                [-np.sin(angY), 0, np.cos(angY)]])

rotZ = np.array([[np.cos(angZ),  -np.sin(angZ), 0],
                [np.sin(angZ), np.cos(angZ), 0],
                [0, 0, 1]])

rotation = ((rotX @ rotY) @ rotZ)
print("New coordinates: ", rotation@coord)
