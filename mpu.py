import smbus
from time import sleep

# some MPU6050 Registers and their Address
CONFIG = 0x1A
DEVICE_ADD = 0x68
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
INT_ENABLE = 0x38
GYRO_CONFIG = 0x1B

ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F

GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47


def mpu_init():
    # write to sample rate register
    bus.write_byte_data(DEVICE_ADD, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(DEVICE_ADD, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(DEVICE_ADD, CONFIG, 0)

    # Write to Gyro configuration register
    bus.write_byte_data(DEVICE_ADD, GYRO_CONFIG, 24)

    # Write to interrupt enable register
    bus.write_byte_data(DEVICE_ADD, INT_ENABLE, 1)


def read_raw_data(addr):
    # Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(DEVICE_ADD, addr)
    low = bus.read_byte_data(DEVICE_ADD, addr + 1)

    # concatenate higher and lower value
    value = ((high << 8) | low)

    # to get signed value from mpu6050
    if value > 32768:
        value = value - 65536
    return value


if __name__ == '__main__':
    bus = smbus.SMBus(0)  # or bus = smbus.SMBus(0) for older version boards
    mpu_init()

    while True:
        # Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)

        # Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)

        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x / 16384.0
        Ay = acc_y / 16384.0
        Az = acc_z / 16384.0

        Gx = gyro_x / 131.0
        Gy = gyro_y / 131.0
        Gz = gyro_z / 131.0

        print("\rGx=%.2f" % Gx, "\tGy=%.2f" % Gy, "\tGz=%.2f" % Gz, "\tAx=%.2f" % Ax, "\tAy=%.2f" % Ay, "\tAz=%.2f" % Az, end='')
        sleep(1)
