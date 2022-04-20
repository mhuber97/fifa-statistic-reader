class Match():
    def __init__(self, home, away, time, cancelled=False):
        self.home = home
        self.away = away
        self.time = time
        self.cancelled = cancelled
        
    def __str__(self):
        if self.cancelled:    
            return self.home.name + " - " + self.away.name + " \t" \
                + " (Cancelled after " + str(self.time) + ")"
        else:
            return self.home.name + " - " + self.away.name + " \t" \
                + str(self.home.score) + ":" + str(self.away.score) + " (" + str(self.time) + ")"
        
    def get_data_frame(self, filename=None):
        return pd.DataFrame.from_dict({
                   "h_team": [self.home.name],\
                   "a_team": [self.away.name],\
                   "time": [self.time],\
                   "h_score": [self.home.score],\
                   "a_score": [self.away.score],\
                   "cancelled": [self.cancelled],\
                   "h_shots": [self.home.shots],\
                   "h_shots_on_target": [self.home.shots_on_target],\
                   "h_possession": [self.home.possession],\
                   "h_tackles": [self.home.tackles],\
                   "h_fouls": [self.home.fouls],\
                   "h_corners": [self.home.corners],\
                   "h_shot_acc": [self.home.shot_acc],\
                   "h_pass_acc": [self.home.pass_acc],\
                   "a_shots": [self.away.shots],\
                   "a_shots_on_target": [self.away.shots_on_target],\
                   "a_possession": [self.away.possession],\
                   "a_tackles": [self.away.tackles],\
                   "a_fouls": [self.away.fouls],\
                   "a_corners": [self.away.corners],\
                   "a_shot_acc": [self.away.shot_acc],\
                   "a_pass_acc": [self.away.pass_acc],\
                   "filename": [filename]
                  }
        )
