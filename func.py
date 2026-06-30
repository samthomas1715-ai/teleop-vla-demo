import controller as cn
from dynamixel_sdk import *


class Dynamixelax:
    BAUDRATE = 57600
    port = PortHandler("COM6")
    ph = PacketHandler(1.0)
    port.openPort(1.0)
    port.setBaudRate(BAUDRATE)

   

    
   
    def __init__(self, dx_id):
        self.id = dx_id
        
    

    def close(self):
        self.port.closePort()
    
    def ping(self):
        model, res, error = self.ph.ping(self.port, self.id)
        if res != COMM_SUCCESS:
           print(self.ph.getTxRxResult(res))
           return None
        if error != 0:
           print(self.ph.getRxPacketError(error))
           return None
        return model
    def tq_enb(self):
        self.ph.write1byteTxRx(self.port, self.id, cn.TORQUE_ENABLE, cn.TORQUE_ON)
    def tq_dis(self):
        self.ph.write1byteTxRx(self.port, self.id, cn.TORQUE_ENABLE, cn.TORQUE_OFF)
    def get_pos(self):
        pos, _, __ =self.ph.read2byteTxRx(self.port, self.id, cn.PRESENT_POSITION)
    def moveto_pos(self, pos):
        pos = max(0, min(1023, pos))
        self.ph.write2byteTxRx(self.port, self.id, cn.GOAL_POSITION, pos)
    def set_speed(self, speed):
        speed = max(0, min(1023, int(speed)))
        self.packetHandler.write2ByteTxRx(self.portHandler,self.id, cn.MOVING_SPEED, speed)
    def set_trq_limit(self, value):
        value = max(0, min(1023, int(value)))
        self.packetHandler.write2ByteTxRx(self.portHandler, self.id,cn.TORQUE_LIMIT,value)
    def get_temp(self):
        temp, _, _ = self.packetHandler.read1ByteTxRx(self.portHandler,self.id,cn.PRESENT_TEMP)
        return temp
    def degrees_to_position(self, deg):
        deg = max(0, min(300, deg))
        return int(deg*1023/300)

    def position_to_degrees(self, pos):
        return pos*300 / 1023
        



            



