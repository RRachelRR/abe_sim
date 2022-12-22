import os
import abe_sim.pobject as pob

class Abe(pob.PObject):
    def _customInitPreLoad(self, *args, **kwargs):
        cDir = os.path.dirname(os.path.abspath(__file__))
        self._urdf = os.path.join(cDir, "./abe.urdf")
        self._useMaximalCoordinates = False
        self._customStateVariables = {"type": "agent", "hand_right_roll": {"canPull": True, "pushingclosed": False, "pullingopen": False, "uprighting": [], "pulling": [], "grasping": []}, "hand_left_roll": {"canPull": True, "pushingclosed": False, "pullingopen": False, "uprighting": [], "pulling": [], "grasping": []}}
    def _customInitDynamicModels(self):
        self._dynamics = {}

