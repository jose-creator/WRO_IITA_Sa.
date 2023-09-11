from imu import mpu6050
import time

mpu = mpu6050(0x68)

try:
    while True:
        giroscopio = mpu.get_gyro_data()
        
        print("X: {:.2f}°/s".format(giroscopio['x']))
        print("Y: {:.2f}°/s".format(giroscopio['y']))
        print("Z: {:.2f}°/s".format(giroscopio['z']))
        time.sleep(1)
except KeyboardInterrupt:
    pass