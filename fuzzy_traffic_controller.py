import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

no_vehicle_current_lane = ctrl.Antecedent(np.arange(0, 41, 1), 'no_vehicle_current_lane')
no_vehicle_other_lane = ctrl.Antecedent(np.arange(0, 41, 1), 'no_vehicle_other_lane')

waiting_time_current_lane = ctrl.Antecedent(np.arange(0, 121, 1), 'waiting_time_current_lane')

emergency_vehicles_in_other_lane = ctrl.Antecedent(np.arange(0, 4, 1), 'emergency_vehicles_in_other_lane')
emergency_vehicles_in_current_lane = ctrl.Antecedent(np.arange(0, 4, 1), 'emergency_vehicles_in_current_lane')

emv_waiting_time_green_lane = ctrl.Antecedent(np.arange(0, 70, 1), 'emv_waiting_time_green_lane')
emv_waiting_time_red_lane = ctrl.Antecedent(np.arange(0, 70, 1), 'emv_waiting_time_red_lane')

traffic_light_signal = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'traffic_light_signal')

no_vehicle_current_lane['very-few'] = fuzz.trapmf(no_vehicle_current_lane.universe, [0, 0, 3, 8])
no_vehicle_current_lane['few'] = fuzz.trimf(no_vehicle_current_lane.universe, [5, 10, 20])
no_vehicle_current_lane['moderate'] = fuzz.trimf(no_vehicle_current_lane.universe, [15, 25, 35])
no_vehicle_current_lane['many'] = fuzz.trimf(no_vehicle_current_lane.universe, [25, 30, 35])  # diturunkan
no_vehicle_current_lane['extreme'] = fuzz.trapmf(no_vehicle_current_lane.universe, [32, 36, 40, 40])  # diturunkan
# no_vehicle_current_lane.view()

no_vehicle_other_lane['very-few'] = fuzz.trapmf(no_vehicle_other_lane.universe, [0, 0, 5, 10])
no_vehicle_other_lane['few'] = fuzz.trimf(no_vehicle_other_lane.universe, [5, 10, 18])
no_vehicle_other_lane['moderate'] = fuzz.trimf(no_vehicle_other_lane.universe, [15, 20, 28])
no_vehicle_other_lane['many'] = fuzz.trimf(no_vehicle_other_lane.universe, [20, 30, 35])  # lebih awal
no_vehicle_other_lane['extreme'] = fuzz.trapmf(no_vehicle_other_lane.universe, [28, 32, 40, 40])  # lebih awal
# no_vehicle_current_lane.view()

waiting_time_current_lane['short'] = fuzz.trapmf(waiting_time_current_lane.universe, [0, 0, 10, 20])
waiting_time_current_lane['medium'] = fuzz.trimf(waiting_time_current_lane.universe, [15, 30, 50])  # overlap naik
waiting_time_current_lane['long'] = fuzz.trapmf(waiting_time_current_lane.universe, [30, 50, 80, 120])  # mulai lebih awal
# waiting_time_current_lane.view()

emv_waiting_time_green_lane['short']   = fuzz.trapmf(emv_waiting_time_green_lane.universe, [0, 0, 15, 25])
emv_waiting_time_green_lane['medium']  = fuzz.trimf(emv_waiting_time_green_lane.universe, [20, 35, 50])
emv_waiting_time_green_lane['long']    = fuzz.trapmf(emv_waiting_time_green_lane.universe, [45, 55, 70, 70])
# emv_waiting_time_green_lane.view()

emv_waiting_time_red_lane['short']   = fuzz.trapmf(emv_waiting_time_red_lane.universe, [0, 0, 15, 25])
emv_waiting_time_red_lane['medium']  = fuzz.trimf(emv_waiting_time_red_lane.universe, [20, 35, 50])
emv_waiting_time_red_lane['long']    = fuzz.trapmf(emv_waiting_time_red_lane.universe, [45, 55, 70, 70])
# emv_waiting_time_red_lane.view()

emergency_vehicles_in_current_lane['none'] = fuzz.trimf(emergency_vehicles_in_current_lane.universe, [0, 0, 1])
emergency_vehicles_in_current_lane['some'] = fuzz.trimf(emergency_vehicles_in_current_lane.universe, [0, 1, 2])
emergency_vehicles_in_current_lane['many'] = fuzz.trapmf(emergency_vehicles_in_current_lane.universe, [1, 2, 3, 3])
# emergency_vehicles_in_current_lane.view()

emergency_vehicles_in_other_lane['none'] = fuzz.trimf(emergency_vehicles_in_other_lane.universe, [0, 0, 1])
emergency_vehicles_in_other_lane['some'] = fuzz.trimf(emergency_vehicles_in_other_lane.universe, [0, 1, 2])
emergency_vehicles_in_other_lane['many'] = fuzz.trapmf(emergency_vehicles_in_other_lane.universe, [1, 2, 3, 3])
# emergency_vehicles_in_other_lane.view()

traffic_light_signal['stay']  = fuzz.trimf(traffic_light_signal.universe, [0, 0, 0.5])
traffic_light_signal['switch'] = fuzz.trimf(traffic_light_signal.universe, [0.5, 1.0, 1.0])
# traffic_light_signal.view()

##### FUNCTIONS THAT PASSS IN THE INPUT ####
### no_vehicle_current_lane too-small small much  too-much

# Rule: Emergency vehicle prioritization
rule0a = ctrl.Rule(
    emergency_vehicles_in_current_lane['many'] & emergency_vehicles_in_other_lane['none'],
    traffic_light_signal['stay']
)

rule0b = ctrl.Rule(
    emergency_vehicles_in_current_lane['none'] & emergency_vehicles_in_other_lane['many'],
    traffic_light_signal['switch']
)

rule0c = ctrl.Rule(
    emergency_vehicles_in_current_lane['some'] & emergency_vehicles_in_other_lane['none'],
    traffic_light_signal['stay']
)

rule0d = ctrl.Rule(
    emergency_vehicles_in_current_lane['none'] & emergency_vehicles_in_other_lane['some'],
    traffic_light_signal['switch']
)

# Rule: Vehicle count prioritization
rule1a = ctrl.Rule(
    no_vehicle_current_lane['many'] & no_vehicle_other_lane['few'],
    traffic_light_signal['stay']
)

rule1b = ctrl.Rule(
    no_vehicle_current_lane['extreme'] & no_vehicle_other_lane['moderate'],
    traffic_light_signal['stay']
)

rule1c = ctrl.Rule(
    no_vehicle_current_lane['few'] & no_vehicle_other_lane['moderate'],
    traffic_light_signal['switch']
)

rule1d = ctrl.Rule(
    no_vehicle_current_lane['very-few'] & no_vehicle_other_lane['extreme'],
    traffic_light_signal['switch']
)

# Rule: Waiting time
rule2a = ctrl.Rule(
    waiting_time_current_lane['short'],
    traffic_light_signal['stay']
)

rule2b = ctrl.Rule(
    waiting_time_current_lane['medium'],
    traffic_light_signal['stay']
)

rule2c = ctrl.Rule(
    waiting_time_current_lane['long'],
    traffic_light_signal['switch']
)

# Rule: Emergency waiting time analysis
rule3a = ctrl.Rule(
    emv_waiting_time_green_lane['long'] & emv_waiting_time_red_lane['short'],
    traffic_light_signal['stay']
)

rule3b = ctrl.Rule(
    emv_waiting_time_green_lane['short'] & emv_waiting_time_red_lane['long'],
    traffic_light_signal['switch']
)

rule3c = ctrl.Rule(
    emv_waiting_time_green_lane['medium'] & emv_waiting_time_red_lane['medium'],
    traffic_light_signal['switch']
)

rule3d = ctrl.Rule(
    emv_waiting_time_green_lane['short'] & emv_waiting_time_red_lane['medium'],
    traffic_light_signal['switch']
)

# Rule: Extreme congestion
rule4 = ctrl.Rule(
    no_vehicle_current_lane['extreme'] | waiting_time_current_lane['long'],
    traffic_light_signal['switch']
)

# Rule: If both lanes are equally heavy, alternate (to prevent starvation)
rule5 = ctrl.Rule(
    no_vehicle_current_lane['moderate'] & no_vehicle_other_lane['moderate'],
    traffic_light_signal['switch']
)

traffic_light_ctrl = ctrl.ControlSystem([
    rule0a, rule0b, rule0c, rule0d,
    rule1a, rule1b, rule1c, rule1d,
    rule2a, rule2b, rule2c,
    rule3a, rule3b, rule3c, rule3d,
    rule4, rule5
])
traffic_status = ctrl.ControlSystemSimulation(traffic_light_ctrl)

def fuzzy_controller_function(no_vehicles_in_red_lanes,
                              no_vehicles_in_green_lanes,
                              max_waiting_time_in_red_lanes,
                              emv_waiting_time_red_lanes, emv_waiting_time_green_lanes,
                              emv_current_lane, emv_other_lane):

    # tambahan
    sim = ctrl.ControlSystemSimulation(traffic_light_ctrl)
    sim.input['no_vehicle_current_lane'] = int(no_vehicles_in_green_lanes)
    sim.input['no_vehicle_other_lane']   = int(no_vehicles_in_red_lanes)
    sim.input['waiting_time_current_lane'] = int(max_waiting_time_in_red_lanes)
    sim.input['emergency_vehicles_in_current_lane'] = int(emv_current_lane)
    sim.input['emergency_vehicles_in_other_lane'] = int(emv_other_lane)
    sim.input['emv_waiting_time_red_lane'] = int(emv_waiting_time_red_lanes)
    sim.input['emv_waiting_time_green_lane'] = int(emv_waiting_time_green_lanes)

    # traffic_status.input['no_vehicle_current_lane'] = int(no_vehicles_in_red_lanes)
    # traffic_status.input['no_vehicle_other_lane'] = int(no_vehicles_in_green_lanes)
    # traffic_status.input['emergency_vehicles_in_current_lane'] = int(emv_current_lane)
    # traffic_status.input['emergency_vehicles_in_other_lane'] = int(emv_other_lane)
    # traffic_status.input['emv_waiting_time_red_lane'] = int(emv_waiting_time_red_lanes)
    # traffic_status.input['emv_waiting_time_green_lane'] = int(emv_waiting_time_green_lanes)
    # traffic_status.input['waiting_time_current_lane'] = int(max_waiting_time_in_red_lanes)

    sim.compute()
    
    print('no_vehicles_in_red_lane ' + str(no_vehicles_in_red_lanes))
    print('no_vehicles_in_green_lane ' + str(no_vehicles_in_green_lanes))
    print('max_waiting_time_in_red_lane ' + str(max_waiting_time_in_red_lanes))
    print('emv_current_lane ' + str(emv_current_lane))
    print('emv_waiting_time_red_lane ' + str(emv_waiting_time_red_lanes))
    print('emv_waiting_time_green_lane ' + str(emv_waiting_time_green_lanes))
    print('emv_other_lane ' + str(emv_other_lane))


    # traffic_status.compute()
    # output = traffic_status.output['traffic_light_signal']
    output = sim.output['traffic_light_signal']
    print('output ' + str(output))
    return output
    # return sim.output['traffic_light_signal']
