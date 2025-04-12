import random

powers_dict = {
            'clear' : (255,215,0),
            'freeze': (147,249,255),
            'reverse' : (0,255,0),
            'invincible': (200,65,45), 
            'time' : (225,235,237)
}   

ran = random.choice(list(powers_dict.items()))
powers_up = ran[0]
powers_color = ran[-1]
# power_up = parts[0]
# power_color = parts[1]
print(f"{powers_up} is {powers_color}")