class MPPTController:
    def __init__(self, data):
        self.battery_voltage = data["Battery"]["rVoltage_V"]
        self.battery_current = data["Battery"]["rCurrent_A"]
        self.solar_voltage = data["Solar"]["rVoltage_V"]
        self.solar_current = data["Solar"]["rCurrent_A"]
        self.duty_cycle = data["Charger"]["rPWMfrequency"]
        self.load_current = data["Load"]["rCurrent_A"]
        self.load_state = data["Load"]["rState"]

    def __str__(self):
        return str(self.battery_voltage)