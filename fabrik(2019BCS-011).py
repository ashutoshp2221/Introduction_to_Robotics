import math
import numpy as np
import sys

class fabrik:
    def __init__(self, jtsP, tolerance: float):
        if tolerance <= 0:
            raise ValueError("Tolerance should be greater than 0")
        self.jts = jtsP
        self.tolerance: float = tolerance
        self.link_l = []
        a = jtsP[0]
        for b in jtsP[1:]:
            self.link_l.append(np.linalg.norm(a - b))
            a = b
        if any([l <= 0 for l in self.link_l]):
            raise ValueError("Lengths must be positive")
        self.lengths = self.link_l
        self.maxLen = sum(self.link_l)
        self._has_moved = True
        self._ang = []
        _ = self.ang

    def ang_degree(self):
        ang = self.ang()
        ang = [math.degrees(val) for val in ang]
        return ang

    def as_length(self, vector, length):
        return vector * length / np.linalg.norm(vector)

    def ang(self):
        if not self._has_moved:
            return self._ang
        ang = [math.atan2(self.jts[1][1], self.jts[1][0])]
        previousAngle: float = ang[0]
        for i in range(2, len(self.jts)):
            p = self.jts[i] - self.jts[i - 1]
            absoluteAngle: float = math.atan2(p[1], p[0])
            ang.append(absoluteAngle - previousAngle)
            previousAngle = absoluteAngle
        self.moved = False
        self._ang = ang
        return self._ang

    def mv_to(self, target, tryReaching=True):
        if not self.solvable(target):
            if not tryReaching:
                return 0
            target = self.as_length(target, self.maxLen)
        return self._iterate(target)

    def _iterate(self, target):
        it: int = 0
        initPos = self.jts[0]
        last: int = len(self.jts) - 1
        while np.linalg.norm(self.jts[-1] - target) > self.tolerance:
            it += 1
            self.jts[-1] = target
            for i in reversed(range(0, last)):
                next, cur = self.jts[i + 1], self.jts[i]
                len_share = self.lengths[i] / np.linalg.norm(next - cur)
                self.jts[i] = (1 - len_share) * next + len_share * cur
            self.jts[0] = initPos
            for i in range(0, last):
                next, cur = self.jts[i + 1], self.jts[i]
                len_share = self.lengths[i] / np.linalg.norm(next - cur)
                self.jts[i + 1] = (1 - len_share) * \
                    cur + len_share * next
        return it

    def solvable(self, target):
        return self.maxLen >= np.linalg.norm(target)

if __name__ == "__main__":
    c1 = list(
        map(
            int,
            input("Enter first coordinate: ").strip().split(),
        )
    )[:3]
    c2 = list(
        map(
            int,
            input("Enter second coordinate: ").strip().split(),
        )
    )[:3]
    c3 = list(
        map(
            int,
            input("Enter third coordinate: ").strip().split(),
        )
    )[:3]
    c4 = list(
        map(
            int,
            input("Enter fourth coordinate: ").strip().split(),
        )
    )[:3]
    
    tolerance = float(input("Tolerance: "))
    goal = list(map(int, input("Goal: ").strip().split()))[:3]
    
    initCoordinates = [
        np.array(c1),
        np.array(c2),
        np.array(c3),
        np.array(c4),
    ]
    initPos = initCoordinates
    fab = fabrik(initCoordinates, tolerance)
    iterations = fab.mv_to(np.array(goal))
    print(f"Result\nNumber of Iterations: {iterations}\nAngles: {fab.ang_degree()}\nLink position: {fab.jts}\nGoal Position: {goal}")