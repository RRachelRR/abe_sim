# breadth-first search of processes
# for a process, loop through goals in descending order of importance
# for each goal, is it fulfilled?
#     yes: is it threatened by an existing process?
#         yes: mark threats for deletion
#     no: select a process for it; is it enacted already?
#         no: is any process attached to the goal?
#             yes: mark it for deletion
#             no: just add the proc to the tree and the tovisit list

class Goal:
    def __init__(self):
        self._establishmentProc = None
        self._debug = False
        self._debugState = False
        return
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return type(self).__name__ + "(" + self._strVarPart() + ")"
    def isFulfilled(self):
        if self._debug:
            return self._debugState
        return self._isFulfilled()
    def getEstablishmentProc(self):
        return self._establishmentProc
    def setEstablishmentProc(self, proc):
        self._establishmentProc = proc
    def _strVarPart(self):
        return ""
    def _isFulfilled(self):
        return True
    def getThreats(self, processes):
        return []
    def suggestProcess(self):
        return None

class Process:
    def __init__(self, coherence=[]):
        self._coherence = coherence
        self._markedForDeletion = False
        return
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return type(self).__name__ + "(" + self._strVarPart() + ")"
    def setCoherenceConditions(self, conditions):
        self._coherence = conditions
    def coherenceConditions(self):
        return self._coherence
    def isMarkedForDeletion(self):
        return self._markedForDeletion
    def isBodyProcess(self):
        return False
    def markForDeletion(self, replacement=None):
        self._markedForDeletion = True
        return self._markForDeletionInternal(replacement)
    def _strVarPart(self):
        retq = ""
        for c in self._coherence:
            retq = retq + str(c) + ","
        return retq[:-1]
    def _markForDeletionInternal(self,replacement=None):
        return None

class Stabilizer(Process):
    def markForDeletion(self,replacement=None):
        return None

class BodyProcess(Process):
    def isBodyProcess(self):
        return True
    def bodyAction(self):
        return None

class Garden:
    def __init__(self):
        self._commandProcess = None
        self._processes = {}
        self._processFlags = {}
        return
    def updateEstablisher(self, goal, proc):
        desc = str(proc)
        oproc = goal.getEstablishmentProc()
        odesc = str(oproc)
        if odesc == desc:
            return
        if None == proc:
            goal.setEstablishmentProc(None)
            return
        switching = []
        goal.setEstablishmentProc(proc)
        if (None != proc):
            desc = str(proc)
            if desc not in self._processes:
                self._processes[desc] = proc
    def updateGarden(self):
        if None == self._commandProcess:
            return []
        procsToVisit = [self._commandProcess]
        bodyProcesses = []
        visited = {}
        while procsToVisit:
            proc = procsToVisit.pop(0)
            #print("GV", proc, proc.coherenceConditions())
            s = str(proc)
            if s in visited:
                continue
            visited[s] = True
            if proc.isMarkedForDeletion():
                continue
            if proc.isBodyProcess():
                doProc = True
                for g in proc.coherenceConditions():
                    if not g.isFulfilled():
                        doProc = False
                if doProc:
                    bodyProcesses.append(proc)
                continue
            stopNow = False
            for g in proc.coherenceConditions():
                if g.isFulfilled():
                    threats = g.getThreats(self._processes)
                    stabilizerGoals = [threat.markForDeletion() for threat in threats]
                    stabilizerGoals = [g for g in stabilizerGoals if None != g]
                    if [] != stabilizerGoals:
                        #print("STABILITYYYYY", g, stabilizerGoals)
                        self.updateEstablisher(g, Stabilizer(coherence=stabilizerGoals))
                    else:
                        self.updateEstablisher(g, None)
                else: ### goal not fulfilled
                    self.updateEstablisher(g, g.suggestProcess())
                    stopNow = True
                pa = g.getEstablishmentProc()
                if None != pa:
                    #print("APPENDING", g, g.getThreats(self._processes), g.isFulfilled(), pa)
                    procsToVisit.append(pa)
                if stopNow:
                    break
            toDel = []
            for s, p in self._processes.items():
                if not p.isMarkedForDeletion():
                    continue
                found = False
                for g in p.coherenceConditions():
                    if not g.isFulfilled():
                        found = True
                        break
                if found:
                    #print("DELETE PROC", s)
                    toDel.append(s)
            [self._processes.pop(s) for s in toDel]
        #print("bps", bodyProcesses)
        return bodyProcesses

