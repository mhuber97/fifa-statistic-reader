class Team():
    def __init__(self, shots, shots_on_target, possession, tackles, fouls, corners, shot_acc, pass_acc, name="", score=""):
        self.name = name
        self.score = score
        self.shots = shots
        self.shots_on_target = shots_on_target
        self.possession = possession
        self.tackles = tackles
        self.fouls = fouls
        self.corners = corners
        self.shot_acc = shot_acc
        self.pass_acc = pass_acc
        
    def __str__(self):
        return "Team:\t " + self.name + \
                    "\nScore:\t " + str(self.score) + \
                    "\nShots:\t " + str(self.shots) + \
                    "\nShots on target:\t " + str(self.shots_on_target) + \
                    "\nPossession:\t " + str(self.possession) + \
                    "\nTackles:\t " + str(self.tackles) + \
                    "\nFouls:\t " + str(self.fouls) + \
                    "\nCorners:\t " + str(self.corners) + \
                    "\nShot accuracy:\t " + str(self.shot_acc) + \
                    "\nPass accuracy:\t " + str(self.pass_acc)
