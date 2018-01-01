#
#   Christopher Boyle (D00198519)
#
#   20171231    -
#
#   Helpful Notes:
#
#

# Imports / Dependencies

from maya import cmds
from Qt import QtWidgets, QtCore, QtGui

# Classes

class CurveToJointUI(QtWidgets.QDialog):
    """

    """

    def __init__(self):
        """

        """
        super(CurveToJointUI, self).__init__()
        self.setWindowTitle('Curve to Joint UI')
        self.buildUI()

    def buildUI(self):
        """

        """

        # Creates Empty Layout
        layout = QtWidgets.QVBoxLayout(self)

        # Creates instructions and adds it to the layout.
        instructionsLbl = QtWidgets.QLabel('Select the chosen curve, set the number of joints and press the button below.')
        layout.addWidget(instructionsLbl)

        # Creates a Spinbox with a minimum value of 2, and a maximum of 99999,
        # as well as adding it to the layout. Unlike other componants, this
        # is given an expanded scope as it needs to be referenced later in
        # other functions.
        self.jointAmountSB = QtWidgets.QSpinBox()
        self.jointAmountSB.setMinimum(2)
        self.jointAmountSB.setMaximum(99999)
        layout.addWidget(self.jointAmountSB)

        # Creaes a Button, with the text "Create Joints" that once pushed will
        # execute the createJoints() function. Lastly added it to the layout.
        createJointsBtn = QtWidgets.QPushButton('Create Joints')
        createJointsBtn.clicked.connect(self.createJoints)
        layout.addWidget(createJointsBtn)

    def createJoints(self):
        """

        """

        # Retrieves selected elements in environment.
        selection = cmds.ls(selection = True, long = True)

        # Checks if 0 or more than 1 item was retrieved in the selection, if
        # either condition is true an error is displayed and execution is
        # stopped. Otherwise it continues execution.
        if (len(selection) == 0):
            print('error - please select a curve!')
            return
        elif (len(selection) > 1):
            print('error - please select a single curve!')
            return
        else:

            # tries to get the number of spans for the curve.
            # If it cannot, catches the error, displaying an appropriate message
            # and stopping execution.
            try:
                NUM_OF_CURVE_SPANS = cmds.getAttr(selection[0] + '.spans')
            except:
                print("error - please ensure selection is a curve!")
                return

            # Retrieves the current value from the Spinbox created in the
            # buildUI().
            NUM_OF_JOINTS = self.jointAmountSB.value()

            # Calculates the necessary amount of space between each joint to
            # span the entire curve for the amount of joints desired.
            DIFF_BETWEEN_JOINTS = NUM_OF_CURVE_SPANS / (NUM_OF_JOINTS - 1.0)

            # For the number of joints requested, iterates and for each joint
            # retrieving the point along the curve through the pointOnCurve()
            # function, followed by creating a joint with that point.
            # Please note, pointOnCurve() will return the origin is the number
            # supplied for the pr parameter is less than 0 or exceeds the span,
            # hence it's importance in calculations.
            for i in range (0, int(NUM_OF_JOINTS)):
                newPoint = cmds.pointOnCurve(selection[0], pr = (i * DIFF_BETWEEN_JOINTS), p = True)
                cmds.joint(p = newPoint)

# Functions

def loadUI():
    """

    """

    # Creates an instance of the CurveToJointUI class, calling the show menu
    # and passing back the ui object for later usage.
    ui = CurveToJointUI()
    ui.show()
    return ui
