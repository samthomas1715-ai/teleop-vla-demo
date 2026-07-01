from dynamixel_sdk import *
import config as con


class DynamixelController:

    def __init__(self, port, motor_ids):

        self.port = port
        self.motor_ids = motor_ids

        self.porthandler = PortHandler(self.port)
        self.packethandler = PacketHandler(con.PROTOCOL_VERSION)


    def connect(self):
        if self.porthandler.openPort():
            print(f"Connected to {self.port}")
        else:
            raise Exception(f"Failed to open {self.port}")

        if self.porthandler.setBaudRate(con.BAUDRATE):
            print(f"Baudrate set to {con.BAUDRATE}")
        else:
            raise Exception("Failed to set baudrate")


    def disconnect(self):
        self.porthandler.closePort()
        print(f"Disconnected from {self.port}")


#if no arguement passed for id then 
#torque for whole daisy chain will be enabled
    def tq_enb(self,dx_id=None):
        if dx_id == None:
            for id in self.motor_ids:
                self.packethandler.write1ByteTxRx(
                self.porthandler,
                id,
                con.ADDR_TORQUE,
                con.TORQUE_ENABLE)
        else:
            self.packethandler.write1ByteTxRx(
                self.porthandler,
                dx_id,
                con.ADDR_TORQUE,
                con.TORQUE_ENABLE)
            
    def tq_disb(self,dx_id=None):
        if dx_id == None:
            for id in self.motor_ids:
                self.packethandler.write1ByteTxRx(
                self.porthandler,
                id,
                con.ADDR_TORQUE,
                con.TORQUE_DISABLE)
        else:
            self.packethandler.write1ByteTxRx(
                self.porthandler,
                dx_id,
                con.ADDR_TORQUE,
                con.TORQUE_DISABLE)   
    
    
    def result_all(self):
        for id in self.motor_ids:
            pos,res,err = self.packethandler.read2ByteTxRx(self.port,id)
        if res != COMM_SUCCESS:
           print(self.ph.getTxRxResult(res))
           return None
        if err != 0:
           print(self.packethandler.getRxPacketError(err))
           return None
        return pos
    
    def get_pos(self, dx_id=None):
        if dx_id == None:
            positions = {}
            for id in self.motor_ids:
                pose, res, err = self.packethandler.read2ByteTxRx(
                    self.porthandler,
                    id,
                    con.ADDR_PRESENT_POSITION,
                )
                positions[id] = pose
            return positions
        else:
             position, res, err = self.packethandler.read2ByteTxRx(
            self.porthandler,
            dx_id,
            con.ADDR_PRESENT_POSITION
        )
        return position
    
    def move_to_pos(self, pos, dx_id):

        res, err = self.packethandler.write2ByteTxRx(
            self.porthandler,
            dx_id,
            con.ADDR_GOAL_POSITION,
            pos
        )
    
    def move_all_to_pos(self,positions):
        for id,pose in positions.items():
            res, err = self.packethandler.write2ByteTxRx(
            self.porthandler,
            id,
            con.ADDR_GOAL_POSITION,
            pose
        )

    def set_speed(self, speed, dx_id=None):

        if dx_id is None:
            for motor_id in self.motor_ids:
                self.packethandler.write2ByteTxRx(
                    self.porthandler,
                    motor_id,
                    con.ADDR_MOVING_SPEED,
                    speed
                )    
        else:
            self.packethandler.write2ByteTxRx(
                self.porthandler,
                dx_id,
                con.ADDR_MOVING_SPEED,
                speed
            )

         
            # if res != COMM_SUCCESS:
            #     print(self.packethandler.getTxRxResult(res))

            # if err != 0:
            #     print(self.packethandler.getRxPacketError(err))