from model import Seconds, Lightcolor


class Light:
    def __init__(
        self,
        cycle_period: Seconds = 20,
        proportion_x: float = 0.5,
        phase_offset: float = 0,
        yellow_phase: Seconds = 5,  # time needed to come to rest,   max speed / breaking acceleration
    ):
        # Indicates if the light is green for direction X
        self.is_on = True

        self.x_light = Lightcolor.Green
        self.y_light = Lightcolor.Red
        self.yellow_phase = yellow_phase

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
        progress_yellow = (
            (time_stamp + self.phase + self.yellow_phase) % self.cycle_period
        ) / self.cycle_period

        self.is_on = progress < self.proportion_x
        self.is_yellow = progress_yellow < self.proportion_x
        self.is_yellow = self.is_yellow ^ self.is_on

        if self.is_on:
            self.x_light = Lightcolor.Green
            self.y_light = Lightcolor.Red
        else:
            self.x_light = Lightcolor.Red
            self.y_light = Lightcolor.Green

        if self.is_on and self.is_yellow:
            self.x_light = Lightcolor.Yellow
        if not self.is_on and self.is_yellow:
            self.y_light = Lightcolor.Yellow
        # print("x", self.x_light,  "y", self.y_light, "yellow",self.is_yellow, "/n")
