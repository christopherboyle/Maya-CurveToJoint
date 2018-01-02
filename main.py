#
#   Christopher Boyle (D00198519)
#
#   20171231    - First Release of CurveToJointUI
#
#   Helpful Notes:
#
#   This is just a simple example code for using the UI created in the
#   CurveToJointUI.py file. As that file depends on Qt.py, both files should
#   be placed in the Maya script directory prior to execution.

# Imports / Dependencies

import CurveToJointUI
reload(CurveToJointUI)

# Execution

ui = CurveToJointUI.loadUI()
