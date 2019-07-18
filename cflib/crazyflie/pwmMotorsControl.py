#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2011-2013 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
Used for sending PWM values to the Crazyflie motors
"""
import struct

from cflib.crtp.crtpstack import CRTPPacket
from cflib.crtp.crtpstack import CRTPPort

__author__ = 'BillTsou'
__all__ = ['PwmMotors']

TYPE_STOP = 0
TYPE_STOP_MOTORS = 0
TYPE_SET_EACH_MOTOR = 1
TYPE_SET_ALL_MOTORS = 2
TYPE_SET_SWEEP = 3

class PwmMotors():
    """
    Used for sending control setpoints to the Crazyflie
    """

    def __init__(self, crazyflie=None):
        """
        Initialize the commander object. By default the commander is in
        +-mode (not x-mode).
        """
        self._cf = crazyflie
        #self._x_mode = False

    def send_PWMsetpoint(self, pwmPercM1, pwmPercM2, pwmPercM3, pwmPercM4):
        """
        Send a new control setpoint for XXX

        The arguments XXX is the new setpoints that should
        be sent to the copter
        """
        if pwmPercM1 > 0xFFFF or pwmPercM1 < 0:
            raise ValueError('Thrust must be between 0 and 0xFFFF')

        if pwmPercM2 > 0xFFFF or pwmPercM2 < 0:
            raise ValueError('Thrust must be between 0 and 0xFFFF')

        if pwmPercM3 > 0xFFFF or pwmPercM3 < 0:
            raise ValueError('Thrust must be between 0 and 0xFFFF')

        if pwmPercM4 > 0xFFFF or pwmPercM4 < 0:
            raise ValueError('Thrust must be between 0 and 0xFFFF')

        pk = CRTPPacket()
        #pk.port = CRTPPort.PWM_SET
        pk.set_header(CRTPPort.PWM_SET, TYPE_SET_EACH_MOTOR)
        pk.data = struct.pack('<HHHH', pwmPercM1, pwmPercM2, pwmPercM3, pwmPercM4)
        self._cf.send_packet(pk)

    def send_PWMsetpointAll(self, pwmPercM, durationSec):
        """
        Send a new control setpoint for XXX

        The arguments roll/pitch/yaw/trust is the new setpoints that should
        be sent to the copter
        """
        if pwmPercM > 0xFFFF or pwmPercM < 0:
            raise ValueError('Thrust must be between 0 and 0xFFFF')

        pk = CRTPPacket()
        #pk.port = CRTPPort.PWM_SET
        pk.set_header(CRTPPort.PWM_SET, TYPE_SET_ALL_MOTORS)
        pk.data = struct.pack('<HL', pwmPercM, durationSec)
        self._cf.send_packet(pk)

    def send_PWMsweep(self, startPercM, endPercM, pwmPercMInc, durationSec):
        """
        Send a new control setpoint for XXX

        The arguments roll/pitch/yaw/trust is the new setpoints that should
        be sent to the copter
        """

        pk = CRTPPacket()
        #pk.port = CRTPPort.PWM_SET
        pk.set_header(CRTPPort.PWM_SET, TYPE_SET_SWEEP)
        pk.data = struct.pack('<HHHL', startPercM, endPercM, pwmPercMInc, durationSec)
        self._cf.send_packet(pk)

    def send_stop_setpointGeneric(self):
        """
        Send STOP setpoing, stopping the motors and (potentially) falling.
        """
        pk = CRTPPacket()
        pk.port = CRTPPort.COMMANDER_GENERIC
        pk.data = struct.pack('<B', TYPE_STOP)
        self._cf.send_packet(pk)

    def send_PWMstop_setpoint(self):
        """
        Send STOP setpoing, stopping the motors and (potentially) falling.
        """
        pk = CRTPPacket()
        #pk.port = CRTPPort.PWM_SET
        pk.set_header(CRTPPort.PWM_SET, TYPE_STOP_MOTORS)
        pk.data = struct.pack('<HHHH', 0, 0, 0, 0)
        self._cf.send_packet(pk)
