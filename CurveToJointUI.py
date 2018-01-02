#
#   Christopher Boyle (D00198519)
#
#   20171231    - First Release of CurveToJointUI
#
#   Helpful Notes:
#
#   A lot of the logic here was taken from lessons learned in
#   the "Python for Maya" which I found to be a great material for building
#   upon the UI lessons in class. As such, I opted to go with using the Qt,
#   library suggested in the course as I found it better for making more
#   maintainable UIs.
#
#   In terms of the UI and logic provided below, there are some minor issues
#   but I also feel a lot of that comes down to tool training e.g. the logic
#   breaks if you supply a low number of joints in comparison to the number of
#   spans the selected curve has. In furture versions of this tool,
#   this could be corrected by provided a more dynamic selection but I choose
#   to leave it out of this version.
#
#   Credit to mottosso for Qt.py - https://github.com/mottosso/Qt.py
#   Credit to dgovil for Python for Maya
#   - https://github.com/dgovil/PythonForMayaSamples
#

# Imports / Dependencies

from maya import cmds
from Qt import QtWidgets, QtCore, QtGui

# Classes

#
class CurveToJointUI(QtWidgets.QDialog):
    """
    CurveToJointUI Class is used to encapculate the UI and its
    functionality for creating a set of joints out of a curve selected by
    the user.

    It inherits from QrWidgets.QDialog, and as such requires Qt.py to functon.
    """

    def __init__(self):
        """
        Overriden version of the standard intializing function for the class.
        Calls the standard initalization through the super() and extends it
        further to set a window title and call buildUI().
        """
        super(CurveToJointUI, self).__init__()
        self.setWindowTitle('Curve to Joint UI')
        self.buildUI()

    def buildUI(self):
        """
        Builds the UI using elements from the Qt.py dependency.
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
        Creates the joints, and is triggered through the pushing of the UI's
        button.

        Retrieves the curve selected by the user, providing error handling to
        prevent major issues.

        Calculates the position of each joint based on the amount provided by
        the user and creates each joint.
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
    Creates an instance of the CurveToJointUI Class, calls the show() function
    which it inherited from QtWidgets.QDialog, and returns the instance of the
    UI.

    Please note, in order for the UI to remain active, the return value must be
    assigned to a variable.
    """

    # Creates an instance of the CurveToJointUI class, calling the show menu
    # and passing back the ui object for later usage.
    ui = CurveToJointUI()
    ui.show()
    return ui
