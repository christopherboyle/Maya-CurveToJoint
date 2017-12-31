from maya import cmds
from Qt import QtWidgets, QtCore, QtGui

class CurveToJointUI(QtWidgets.QDialog):

    def __init__(self):
        super(CurveToJointUI, self).__init__()
        self.setWindowTitle('Curve to Joint UI')
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        instructionsLbl = QtWidgets.QLabel('Select the chosen curve, set the number of joints and press the button below.')
        layout.addWidget(instructionsLbl)

        self.jointAmountSB = QtWidgets.QSpinBox()
        self.jointAmountSB.setMinimum(2)
        self.jointAmountSB.setMaximum(999)
        layout.addWidget(self.jointAmountSB)

        createJointsBtn = QtWidgets.QPushButton('Create Joints')
        createJointsBtn.clicked.connect(self.createJoints)
        layout.addWidget(createJointsBtn)

    def createJoints(self):
        NUM_OF_SPANS = cmds.getAttr('curveShape1.spans')

        NUM_OF_JOINTS = float(self.jointAmountSB.value())
        POS_DIFF = float(NUM_OF_SPANS) / (NUM_OF_JOINTS - 1.0)

        for i in range (0, int(NUM_OF_JOINTS)):
            print((i * POS_DIFF))
            point = cmds.pointOnCurve( 'curve1', pr = (i * POS_DIFF), p = True )
            print(point)
            cmds.joint( p = point )
