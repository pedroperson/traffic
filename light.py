from model import Seconds


class Light:
    def __init__(
        self,
        cycle_period: Seconds = 20,
        proportion_x: float = 0.5,
        phase_offset: float = 0,
    ):
        # Indicates if the light is green for direction X
        self.is_on = True
        self.phase: Seconds = phase_offset * cycle_period
        # Total cycle period of the traffic light in seconds
        self.cycle_period = cycle_period
        # Proportion of the cycle period when the light is green for direction X
        self.proportion_x = proportion_x

    def update_state(self, time_stamp: Seconds):
        """
        Updates the state of the traffic light based on the given time stamp.
        """
        progress = ((time_stamp + self.phase) % self.cycle_period) / self.cycle_period
        self.is_on = progress < self.proportion_x
