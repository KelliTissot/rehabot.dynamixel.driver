from reachy.parts.arm import RightArm
from reachy.parts.part import ReachyPart
from reachy.parts.hand import RightEmptyHand
from reachy.io import IO
from collections import OrderedDict

class RehabotHand(RightEmptyHand):
    dxl_motors = OrderedDict([
        ('forearm_yaw', {
            'id': 14, 'offset': -281, 'orientation': 'indirect',
            'angle-limits': [-100, 100],
            'link-translation': [0, 0, 0], 'link-rotation': [0, 0, 1],
        }),
        ('wrist_pitch', {
            'id': 15, 'offset': 183, 'orientation': 'indirect',
            'angle-limits': [-45, 45],
            'link-translation': [0, 0, -0.25], 'link-rotation': [0, 1, 0],
        }),
        ('wrist_roll', {
            'id': 16, 'offset': 349, 'orientation': 'indirect',
            'angle-limits': [-45, 45],
            'link-translation': [0, 0, -0.0325], 'link-rotation': [1, 0, 0],
        }),
    ])


class RehabotArm(RightArm):
    dxl_motors = OrderedDict([
        ('shoulder_pitch', {
            'id': 10, 'offset': -95, 'orientation': 'indirect',
            'angle-limits': [-180, 60],
            'link-translation': [0, -0.19, 0], 'link-rotation': [0, 1, 0],
        }),
        ('shoulder_roll', {
            'id': 11, 'offset': -268, 'orientation': 'indirect',
            'angle-limits': [-100, 90],
            'link-translation': [0, 0, 0], 'link-rotation': [1, 0, 0],
        }),
        ('arm_yaw', {
            'id': 12, 'offset': -322, 'orientation': 'indirect',
            'angle-limits': [-90, 90],
            'link-translation': [0, 0, 0], 'link-rotation': [0, 0, 1],
        }),
        ('elbow_pitch', {
            'id': 13, 'offset': 150, 'orientation': 'direct',
            'angle-limits': [0, 125],
            'link-translation': [0, 0, -0.28], 'link-rotation': [0, 1, 0],
        }),
    ])

    def __init__(self, io):
        ReachyPart.__init__(self, name='right_arm', io=io)
        self.side = 'right'

        dxl_motors = OrderedDict(RehabotArm.dxl_motors)

        self.attach_dxl_motors(dxl_motors)

        hand_part = RehabotHand(root=self, io=io)
        self.motors += hand_part.motors
        self.hand = hand_part

        for m, conf in RehabotHand.dxl_motors.items():
            dxl_motors[m] = conf

        self.attach_kinematic_chain(dxl_motors)

                    