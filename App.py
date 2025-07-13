import streamlit as st
import math

# =================================================================================
# --- DATA & LOGIC ---
# =================================================================================

# ---------------------------------------------------------------------------------
# 1. MASTER PARAMETER DEFINITIONS
# ---------------------------------------------------------------------------------
PARAMETERS = {
    # This dictionary is now cleaned of all duplicates and inconsistencies.
    
    # --- Core Forces & Ratios ---
    'Lift':                   {'display_name': 'Lift', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    'Drag':                   {'display_name': 'Drag', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    'Thrust Required (N)':    {'display_name': 'Thrust Required', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    'Thrust':                 {'display_name': 'Thrust', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    'Induced Drag (N)':       {'display_name': 'Induced Drag', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    'Parasite Drag (N)':      {'display_name': 'Parasite Drag', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    'L/D (Lift to Drag ratio)':{'display_name': 'L/D (Lift to Drag ratio)', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    'Thrust to Weight Ratio': {'display_name': 'Thrust to Weight Ratio', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    'Maximum Thrust to Weight Ratio': {'display_name': 'Maximum Thrust to Weight Ratio', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    'Minimum Thrust to Weight Ratio (Tr/W)min': {'display_name': 'Minimum Thrust to Weight Ratio (Tr/W)min', 'is_calculable': True, 'category': 'Core Forces & Ratios'},
    
    # --- Aerodynamic Coefficients & Numbers ---
    'CL (Lift Coefficient)':  {'display_name': 'CL (Lift Coefficient)', 'is_calculable': True, 'category': 'Aerodynamic Coefficients'},
    'CD (Drag Coefficient)':  {'display_name': 'CD (Drag Coefficient)', 'is_calculable': True, 'category': 'Aerodynamic Coefficients'},
    'CD0 (Zero-lift Drag Coefficient)': {'display_name': 'CD0 (Zero-lift Drag Coefficient)', 'is_calculable': True, 'category': 'Aerodynamic Coefficients'},
    'K (Induced drag factor)':{'display_name': 'K (Induced drag factor)', 'is_calculable': True, 'category': 'Aerodynamic Coefficients'},
    'CLmax':                  {'display_name': 'CLmax', 'is_calculable': True, 'category': 'Aerodynamic Coefficients'},
    'Reynolds Number (Re)':   {'display_name': 'Reynolds Number', 'is_calculable': True, 'category': 'Aerodynamic Coefficients'},
    'M (Mach Number)':        {'display_name': 'M (Mach Number)', 'is_calculable': False, 'category': 'Aerodynamic Coefficients'},
    'CL/CD Ratio':            {'display_name': 'CL/CD Ratio', 'is_calculable': True, 'category': 'Aerodynamic Coefficients'},
    'CL^0.5/CD Ratio':        {'display_name': 'CL^0.5/CD Ratio', 'is_calculable': True, 'category': 'Aerodynamic Coefficients'},
    'Power Ratio (CL^3/2/CD)':{'display_name': 'Power Ratio (CL^3/2/CD)', 'is_calculable': True, 'category': 'Aerodynamic Coefficients'},
    
    # --- Aircraft Properties ---
    'Aircraft Weight (N)':    {'display_name': 'Aircraft Weight', 'is_calculable': True, 'category': 'Aircraft Properties'},
    'Gross Weight (W0) (N)':  {'display_name': 'Gross Weight (W0)', 'is_calculable': True, 'category': 'Aircraft Properties'},
    'Empty Fuel Weight (W1) (N)': {'display_name': 'Empty Fuel Weight (W1)', 'is_calculable': True, 'category': 'Aircraft Properties'},
    'Fuel Weight (Wf) (N)':   {'display_name': 'Fuel Weight (Wf)', 'is_calculable': True, 'category': 'Aircraft Properties'},
    'Wing Area (m^2)':        {'display_name': 'Wing Area', 'is_calculable': True, 'category': 'Aircraft Properties'},
    'w/s (Wing Loading)':     {'display_name': 'w/s (Wing Loading)', 'is_calculable': True, 'category': 'Aircraft Properties'},
    'b (Wing Span)':          {'display_name': 'b (Wing Span)', 'is_calculable': True, 'category': 'Aircraft Properties'},
    'Aspect Ratio (AR)':      {'display_name': 'Aspect Ratio (AR)', 'is_calculable': True, 'category': 'Aircraft Properties'},
    'Characteristic Length (m)':{'display_name': 'Characteristic Length', 'is_calculable': False, 'category': 'Aircraft Properties'},
    'Oswald Efficiency (e)':  {'display_name': 'Oswald Efficiency (e)', 'is_calculable': False, 'category': 'Aircraft Properties'},

    # --- Atmospheric Properties ---
    'Altitude (m)':           {'display_name': 'Altitude', 'is_calculable': True, 'category': 'Atmospheric Properties'},
    'Air Density (kg/m^3)':   {'display_name': 'Air Density', 'is_calculable': True, 'category': 'Atmospheric Properties'},
    'Local Temperature (K)':  {'display_name': 'Local Temperature', 'is_calculable': True, 'category': 'Atmospheric Properties'},
    'Dynamic Pressure (Pa)':  {'display_name': 'Dynamic Pressure', 'is_calculable': True, 'category': 'Atmospheric Properties'},
    'a (Speed of Sound)':     {'display_name': 'Speed of Sound', 'is_calculable': True, 'category': 'Atmospheric Properties'},
    'Dynamic Viscosity (Pa*s)': {'display_name': 'Dynamic Viscosity', 'is_calculable': False, 'category': 'Atmospheric Properties'},

    # --- Propulsion ---
    'Power Available (W)':    {'display_name': 'Power Available', 'is_calculable': True, 'category': 'Propulsion'},
    'Thrust Available (N)':   {'display_name': 'Thrust Available', 'is_calculable': True, 'category': 'Propulsion'},
    'Engine Shaft Power (W)': {'display_name': 'Engine Shaft Power', 'is_calculable': True, 'category': 'Propulsion'},
    'Propeller Efficiency':   {'display_name': 'Propeller Efficiency', 'is_calculable': True, 'category': 'Propulsion'},
    'Sea Level Thrust Available (N)': {'display_name': 'Sea Level Thrust Available', 'is_calculable': True, 'category': 'Propulsion'},
    'Thrust Lapse Exponent (m)': {'display_name': 'Thrust Lapse Exponent', 'is_calculable': True, 'category': 'Propulsion'},
    'SFC - Jet (Ct) (1/s)':   {'display_name': 'SFC - Jet (Ct)', 'is_calculable': True, 'category': 'Propulsion'},
    'SFC - Prop (C) (N/W*s)': {'display_name': 'SFC - Prop (C)', 'is_calculable': True, 'category': 'Propulsion'},
    'Fuel Weight Flow Rate (N/s)': {'display_name': 'Fuel Weight Flow Rate', 'is_calculable': False, 'category': 'Propulsion'},

    # --- Flight Performance (General) ---
    'Velocity (m/s)':         {'display_name': 'Velocity', 'is_calculable': True, 'category': 'Flight Performance (General)'},
    'Range (m)':              {'display_name': 'Range', 'is_calculable': True, 'category': 'Flight Performance (General)'},
    'Endurance (s)':          {'display_name': 'Endurance', 'is_calculable': True, 'category': 'Flight Performance (General)'},
    'Rate of Climb (m/s)':    {'display_name': 'Rate of Climb', 'is_calculable': True, 'category': 'Flight Performance (General)'},
    'Climb Angle (radians)':  {'display_name': 'Climb Angle', 'is_calculable': True, 'category': 'Flight Performance (General)'},
    
    # --- Flight Performance (Max/Min) ---
    'Maximum L/D Ratio':      {'display_name': 'Maximum L/D Ratio', 'is_calculable': True, 'category': 'Flight Performance (Max/Min)'},
    'Maximum Rate of Climb (m/s)': {'display_name': 'Maximum Rate of Climb', 'is_calculable': True, 'category': 'Flight Performance (Max/Min)'},
    'Maximum Climb Angle (radians)': {'display_name': 'Maximum Climb Angle', 'is_calculable': True, 'category': 'Flight Performance (Max/Min)'},
    'Velocity at Max L/D (m/s)': {'display_name': 'Velocity at Max L/D', 'is_calculable': True, 'category': 'Flight Performance (Max/Min)'},
    'Velocity at Min Power Required (m/s)': {'display_name': 'Velocity at Min Power Required', 'is_calculable': True, 'category': 'Flight Performance (Max/Min)'},
    'Velocity at Max R/C (m/s)': {'display_name': 'Velocity at Max R/C', 'is_calculable': True, 'category': 'Flight Performance (Max/Min)'},
    
    # === Maneuvering Performance ===
    'Load Factor (n)':        {'display_name': 'Load Factor (n)', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Maximum Load Factor (n_max)': {'display_name': 'Maximum Load Factor (n_max)', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Bank Angle (rad)':       {'display_name': 'Bank Angle', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Maximum Bank Angle (rad)': {'display_name': 'Maximum Bank Angle', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Turn Rate (rad/s)':      {'display_name': 'Turn Rate', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Turn Radius (R) (m)':    {'display_name': 'Turn Radius', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Stall Velocity (m/s)':   {'display_name': 'Stall Velocity', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Corner Velocity (m/s)':  {'display_name': 'Corner Velocity', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Minimum Sustained Turn Radius (m)':   {'display_name': 'Minimum Sustained Turn Radius', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Maximum Sustained Turn Rate (rad/s)':  {'display_name': 'Maximum Sustained Turn Rate', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Minimum Instantaneous Turn Radius (m)':  {'display_name': 'Minimum Instantaneous Turn Radius', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Maximum Instantaneous Turn Rate (rad/s)': {'display_name': 'Maximum Instantaneous Turn Rate', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Pull-up Turn Radius (m)':{'display_name': 'Pull-up Turn Radius', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Pull-up Turn Rate (rad/s)': {'display_name': 'Pull-up Turn Rate', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Pull-down Turn Radius (m)':{'display_name': 'Pull-down Turn Radius', 'is_calculable': True, 'category': 'Maneuvering Performance'},
    'Pull-down Turn Rate (rad/s)': {'display_name': 'Pull-down Turn Rate', 'is_calculable': True, 'category': 'Maneuvering Performance'},

    # === Takeoff & Landing Performance ===
    'Ground Roll Distance (m)': {'display_name': 'Ground Roll Distance', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Total Takeoff Distance (m)': {'display_name': 'Total Takeoff Distance', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Liftoff Speed (m/s)':    {'display_name': 'Liftoff Speed (V_LO)', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Total Landing Distance (m)': {'display_name': 'Total Landing Distance', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Touchdown Velocity (V_TD)': {'display_name': 'Touchdown Velocity (V_TD)', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Ground Effect Factor (phi)': {'display_name': 'Ground Effect Factor (phi)', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Height of wing above ground (h)': {'display_name': 'Height of wing from ground', 'is_calculable': False, 'category': 'Takeoff & Landing'},
    'Rolling Resistance Coefficient': {'display_name': 'Rolling Resistance Coefficient', 'is_calculable': False, 'category': 'Takeoff & Landing'},
    'Thrust Reverser Force (T_rev)': {'display_name': 'Thrust Reverser Force', 'is_calculable': False, 'category': 'Takeoff & Landing'},
    'Obstacle Height (hob)':  {'display_name': 'Obstacle Height (hob)', 'is_calculable': False, 'category': 'Takeoff & Landing'},
    'Flare Height (hf)':      {'display_name': 'Flare Height', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Flare Distance (s_flare)': {'display_name': 'Flare Distance', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Flare Radius (R_flare)': {'display_name': 'Flare Radius', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Approach Distance (sa_landing)': {'display_name': 'Approach Distance (Landing)', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    'Approach Angle (θa)':    {'display_name': 'Approach Angle', 'is_calculable': True, 'category': 'Takeoff & Landing'},
    
    # === Stability & Control ===
    'Neutral Point (hn)': {'display_name': 'Neutral Point (hn)', 'is_calculable': True, 'category': 'Stability & Control'},
    'Static Margin': {'display_name': 'Static Margin', 'is_calculable': True, 'category': 'Stability & Control'},
    'CG Location (h)': {'display_name': 'CG Location (h)', 'is_calculable': False, 'category': 'Stability & Control'},
    'AC Location (h_ac,wb)': {'display_name': 'AC Location (h_ac,wb)', 'is_calculable': False, 'category': 'Stability & Control'},
    'Tail Volume Coefficient (VH)': {'display_name': 'Tail Volume Coefficient (VH)', 'is_calculable': False, 'category': 'Stability & Control'},
    'Tail Lift Curve Slope (at)': {'display_name': 'Tail Lift Curve Slope (at)', 'is_calculable': False, 'category': 'Stability & Control'},
    'Aircraft Lift Curve Slope (a)': {'display_name': 'Aircraft Lift Curve Slope (a)', 'is_calculable': False, 'category': 'Stability & Control'},
    'Downwash Derivative (de/da)': {'display_name': 'Downwash Derivative (de/da)', 'is_calculable': False, 'category': 'Stability & Control'},
}

# ---------------------------------------------------------------------------------
# 2. UNIT CONVERSION LOGIC
# ---------------------------------------------------------------------------------
CONVERSION_FACTORS = {
    'ft_to_m': 0.3048,
    'lbf_to_N': 4.44822,
    'slug_ft3_to_kg_m3': 515.379,
    'psf_to_Pa': 47.8803,  
    'psf_s_to_Pa_s': 47.8803,
    'ft_lbf_s_to_W': 1.35582,
    'hr_to_s': 3600,
    'lbf_per_lbf_hr_to_si': 1 / 3600, 
    'lb_per_hp_hr_to_si': 1.68966e-7, 
    'rad_to_deg': 57.2958,
    'deg_to_rad': 0.0174533,
}

PARAMETER_UNITS = {
    'Velocity (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Altitude (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Wing Area (m^2)': {
        'si_unit': 'm^2',
        'imperial_unit': 'ft^2',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m'] ** 2  
    },
    'Aircraft Weight (N)': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'b (Wing Span)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Air Density (kg/m^3)': {
        'si_unit': 'kg/m^3',
        'imperial_unit': 'slug/ft^3',
        'to_si_factor': CONVERSION_FACTORS['slug_ft3_to_kg_m3']
    },
    'w/s (Wing Loading)': {
        'si_unit': 'Pa',  
        'imperial_unit': 'psf', 
        'to_si_factor': CONVERSION_FACTORS['psf_to_Pa']
    },
    'Lift': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Drag': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
     'Thrust': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Thrust Required': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Rate of Climb (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Characteristic Length (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Dynamic Viscosity (Pa*s)': {
        'si_unit': 'Pa*s',
        'imperial_unit': 'lb-s/ft^2',
        'to_si_factor': CONVERSION_FACTORS['psf_s_to_Pa_s']
    },
    'Dynamic Pressure (Pa)': {
        'si_unit': 'Pa',
        'imperial_unit': 'psf',
        'to_si_factor': CONVERSION_FACTORS['psf_to_Pa']
    },
    'Power Required (W)': {
        'si_unit': 'W',
        'imperial_unit': 'ft-lbf/s',
        'to_si_factor': CONVERSION_FACTORS['ft_lbf_s_to_W']
    },
    'Thrust Required (N)': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Velocity at Min Power Required (m/s)': {
        'si_unit': 'm/s',
       'imperial_unit': 'ft/s',
       'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Velocity at Max L/D (m/s)' : {
        'si_unit' : 'm/s',
        'imperial_unit' : 'ft/s',
        'to_si_factor' : CONVERSION_FACTORS['ft_to_m']
    },
    'Power Available (W)': {
        'si_unit': 'W',
        'imperial_unit': 'ft-lbf/s',
        'to_si_factor': CONVERSION_FACTORS['ft_lbf_s_to_W']
    },
    'Engine Shaft Power (W)': {
        'si_unit': 'W',
        'imperial_unit': 'ft-lbf/s',
        'to_si_factor': CONVERSION_FACTORS['ft_lbf_s_to_W']
    },
    'Thrust Available (N)': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Sea Level Thrust Available (N)': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'SFC - Jet (Ct) (1/s)': {
        'si_unit': '1/s',
        'imperial_unit': '1/hr',
        'to_si_factor': 1 / 3600
   },
   'SFC - Prop (C) (N/W*s)': {
       'si_unit': 'N/W·s', 
        'imperial_unit': 'lb/(hp*hr)',
        'to_si_factor': 1.68966e-7
    },
    'Range (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Endurance (s)': {
        'si_unit': 's',
        'imperial_unit': 'hr',
        'to_si_factor': CONVERSION_FACTORS['hr_to_s']
    },
    'Gross Weight (W0) (N)': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Empty Fuel Weight (W1) (N)': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Fuel Weight (Wf) (N)': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Fuel Weight Flow Rate (N/s)': {
        'si_unit': 'N/s',
        'imperial_unit': 'lbf/hr',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N'] / CONVERSION_FACTORS['hr_to_s']
    },
    'Excess Power (W)': {
        'si_unit': 'W',
        'imperial_unit': 'ft-lbf/s',
        'to_si_factor': CONVERSION_FACTORS['ft_lbf_s_to_W']
    },
    'Velocity at Max Climb Angle (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Rate of Climb at Max Climb Angle (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Maximum Rate of Climb (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Velocity at Max R/C (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Turn Radius (R) (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Turn Rate (rad/s)': {
        'si_unit': 'rad/s',
        'imperial_unit': 'deg/s',
        'to_si_factor': 1 / CONVERSION_FACTORS['deg_to_rad']
    },
    'Bank Angle (rad)': {
        'si_unit': 'rad',
        'imperial_unit': 'deg',
        'to_si_factor': CONVERSION_FACTORS['deg_to_rad']
    },
    'Maximum Bank Angle (rad)': {
        'si_unit': 'rad',
        'imperial_unit': 'deg',
        'to_si_factor': CONVERSION_FACTORS['deg_to_rad']
    },
    'Stall Velocity (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Minimum Sustained Turn Radius (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Velocity at Min Turn Radius (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Maximum Sustained Turn Rate (rad/s)': {
        'si_unit': 'rad/s',
        'imperial_unit': 'deg/s',
        'to_si_factor': 1 / 57.2958 
    },
    'Velocity at Max Turn Rate (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Pull-up Turn Radius (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Pull-up Turn Rate (rad/s)': {
        'si_unit': 'rad/s',
        'imperial_unit': 'deg/s',
        'to_si_factor': CONVERSION_FACTORS['deg_to_rad']
    },
    'Pull-down Turn Radius (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Pull-down Turn Rate (rad/s)': {
        'si_unit': 'rad/s',
        'imperial_unit': 'deg/s',
        'to_si_factor': CONVERSION_FACTORS['deg_to_rad']
    },
    'Minimum Instantaneous Turn Radius (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Maximum Instantaneous Turn Rate (rad/s)': {
        'si_unit': 'rad/s',
        'imperial_unit': 'deg/s',
        'to_si_factor': CONVERSION_FACTORS['deg_to_rad']
    },
    'Corner Velocity (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Height of wing above ground (h)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Drag During Ground Roll (N)': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Ground Roll Distance (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Airborne Distance (sa)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Obstacle Height (hob)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Obstacle Angle (θob)': {
        'si_unit': 'rad',
        'imperial_unit': 'deg',
        'to_si_factor': CONVERSION_FACTORS['deg_to_rad']
    },
    'Total Takeoff Distance (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Approach Distance (sa_landing)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Approach Angle (θa)': {
        'si_unit': 'rad',
        'imperial_unit': 'deg',
        'to_si_factor': CONVERSION_FACTORS['deg_to_rad']
    },
    'Flare Height (hf)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Flare Distance (s_flare)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Flare Radius (R_flare)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Landing Ground Roll (s_g,l)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Total Landing Distance (m)': {
        'si_unit': 'm',
        'imperial_unit': 'ft',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Touchdown Velocity (V_TD)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
    'Thrust Reverser Force (T_rev)': {
        'si_unit': 'N',
        'imperial_unit': 'lbf',
        'to_si_factor': CONVERSION_FACTORS['lbf_to_N']
    },
    'Time to Climb (s)': {
        'si_unit': 's',
        'imperial_unit': 'min',
        'to_si_factor': 60
    },
    'Liftoff Speed (m/s)': {
        'si_unit': 'm/s',
        'imperial_unit': 'ft/s',
        'to_si_factor': CONVERSION_FACTORS['ft_to_m']
    },
}

# Converts a value from Imperial to SI if the parameter has a defined conversion.
def to_si(value: float, param_name_si: str) -> float:
    if param_name_si in PARAMETER_UNITS:
        factor = PARAMETER_UNITS[param_name_si]['to_si_factor']
        return value * factor
    return value  # Return original value if no conversion is defined for this parameter

#Converts a value from SI back to Imperial if the parameter has a defined conversion.
def from_si(value: float, param_name_si: str) -> float:
    if param_name_si in PARAMETER_UNITS:
        factor = PARAMETER_UNITS[param_name_si]['to_si_factor']
        # Avoid division by zero, although factors should never be zero.
        if factor != 0:
            return value / factor
    return value

#Converts betwwen display name and regular name
def get_unit_string(param_name_si, unit_system):
    param_info = PARAMETERS.get(param_name_si, {})
    base_name = param_info.get('display_name', param_name_si.split('(')[0].strip())

    if unit_system.lower() == 'imperial' and param_name_si in PARAMETER_UNITS:
        imperial_unit = PARAMETER_UNITS[param_name_si]['imperial_unit']
        return f"{base_name} ({imperial_unit})"
    return param_name_si


# ---------------------------------------------------------------------------------
# 3. FORMULA KNOWLEDGE BASE
# ---------------------------------------------------------------------------------
G = 9.80665; R = 287.0; GAMMA = 1.4; T0 = 288.15; RHO0 = 1.225; L = 0.0065; T11 = 216.65; RHO11 = 0.364
FORMULA_KB = [

   # ====================================
   # L/D and CL/CD RATIO FAMILY 
   # ====================================
    {
        'output': 'L/D (Lift to Drag ratio)',
        'inputs': ['CL/CD Ratio'],
        'name': 'L/D equals CL/CD',
        'alias': True
    },
    {
        'output': 'CL/CD Ratio',
        'inputs': ['L/D (Lift to Drag ratio)'],
        'name': 'CL/CD equals L/D',
        'alias': True
    },
    {
        'output': 'L/D (Lift to Drag ratio)',
        'inputs': ['Lift', 'Drag'],
        'calculate': lambda v: v['Lift'] / v['Drag'] if v['Drag'] != 0 else 0
    },
    {
        'output': 'Lift',
        'inputs': ['L/D (Lift to Drag ratio)', 'Drag'],
        'name' : 'From L/D ratio',
        'calculate': lambda v: v['L/D (Lift to Drag ratio)'] * v['Drag']
    },
    {
        'output': 'Drag',
        'inputs': ['L/D (Lift to Drag ratio)', 'Lift'],
        'name' : 'From L/D ratio',
        'calculate': lambda v: v['Lift'] / v['L/D (Lift to Drag ratio)'] if v['L/D (Lift to Drag ratio)'] != 0 else 0
    },
    {
        'output': 'CL/CD Ratio',
        'inputs': ['CL (Lift Coefficient)', 'CD (Drag Coefficient)'],
        'calculate': lambda v: v['CL (Lift Coefficient)'] / v['CD (Drag Coefficient)'] if v['CD (Drag Coefficient)'] != 0 else 0
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['CL/CD Ratio', 'CD (Drag Coefficient)'],
        'name' : 'From CL/CD ratio',
        'calculate': lambda v: v['CL/CD Ratio'] * v['CD (Drag Coefficient)']
    },
    {
        'output': 'CD (Drag Coefficient)',
        'inputs': ['CL/CD Ratio', 'CL (Lift Coefficient)'],
        'name' : 'From CL/CD ratio',
        'calculate': lambda v: v['CL (Lift Coefficient)'] / v['CL/CD Ratio'] if v['CL/CD Ratio'] != 0 else 0
    },
    {
        'output': 'Power Ratio (CL^3/2/CD)',
        'inputs': ['CL/CD Ratio', 'CL (Lift Coefficient)'],
        'name' : 'From CL/CD ratio and CL',
        'calculate': lambda v: v['CL/CD Ratio'] * v['CL (Lift Coefficient)']**0.5
    },
    {
        'output': 'CL/CD Ratio',
        'inputs': ['Power Ratio (CL^3/2/CD)', 'CL (Lift Coefficient)'],
        'name' : 'From CL^3/2/CD and CL',
        'calculate': lambda v: v['Power Ratio (CL^3/2/CD)'] / v['CL (Lift Coefficient)']**0.5 if v['CL (Lift Coefficient)'] > 0 else 0
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['Power Ratio (CL^3/2/CD)', 'CL/CD Ratio'],
        'name' : 'From CL^3/2/CD and CL/CD',
        'calculate': lambda v: (v['Power Ratio (CL^3/2/CD)'] / v['CL/CD Ratio'])**2 if v['CL/CD Ratio'] != 0 else 0
    },
    {
        'output': 'CL/CD Ratio',
        'inputs': ['CL^0.5/CD Ratio', 'CL (Lift Coefficient)'],
        'name' : 'From CL^0.5/CD and CL',
        'calculate': lambda v: v['CL^0.5/CD Ratio'] * v['CL (Lift Coefficient)']**0.5
    },
    {
        'output': 'CL^0.5/CD Ratio',
        'inputs': ['CL/CD Ratio', 'CL (Lift Coefficient)'],
        'name' : 'From CL/CD and CL',
        'calculate': lambda v: v['CL/CD Ratio'] / v['CL (Lift Coefficient)']**0.5 if v['CL (Lift Coefficient)'] > 0 else 0
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['CL/CD Ratio', 'CL^0.5/CD Ratio'],
        'name' : 'From CL^0.5/CD and CL/CD',
        'calculate': lambda v: (v['CL/CD Ratio'] / v['CL^0.5/CD Ratio'])**2 if v['CL^0.5/CD Ratio'] != 0 else 0
    },
    # ====================================================
    # COEFFICIENT RELATIONSHIPS FAMILY (DRAG POLAR) 
    # ====================================================
    {
        'output': 'CD (Drag Coefficient)',
        'inputs': ['CD0 (Zero-lift Drag Coefficient)', 'K (Induced drag factor)', 'CL (Lift Coefficient)'],
        'name' : 'From Drag polar equation',
        'calculate': lambda v: v['CD0 (Zero-lift Drag Coefficient)'] + v['K (Induced drag factor)'] * (v['CL (Lift Coefficient)']**2)
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['CD (Drag Coefficient)', 'CD0 (Zero-lift Drag Coefficient)', 'K (Induced drag factor)'],
        'name' : 'From Drag polar equation',
        'calculate': lambda v: math.sqrt(abs((v['CD (Drag Coefficient)'] - v['CD0 (Zero-lift Drag Coefficient)']) / v['K (Induced drag factor)'])) if v['K (Induced drag factor)'] != 0 else 0
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'inputs': ['CD (Drag Coefficient)', 'K (Induced drag factor)', 'CL (Lift Coefficient)'],
        'name' : 'From Drag polar equation',
        'calculate': lambda v: v['CD (Drag Coefficient)'] - v['K (Induced drag factor)'] * (v['CL (Lift Coefficient)']**2)
    },
    {
        'output': 'K (Induced drag factor)',
        'inputs': ['CD (Drag Coefficient)', 'CD0 (Zero-lift Drag Coefficient)', 'CL (Lift Coefficient)'],
        'name' : 'From Drag polar equation',
        'calculate': lambda v: (v['CD (Drag Coefficient)'] - v['CD0 (Zero-lift Drag Coefficient)']) / (v['CL (Lift Coefficient)']**2) if v['CL (Lift Coefficient)'] != 0 else 0
    },
    {
        'output': 'K (Induced drag factor)',
        'inputs': ['Oswald Efficiency (e)', 'Aspect Ratio (AR)'],
        'name' : 'From e and AR',
        'calculate': lambda v: 1 / (math.pi * v['Oswald Efficiency (e)'] * v['Aspect Ratio (AR)']) if v['Oswald Efficiency (e)'] != 0 and v['Aspect Ratio (AR)'] != 0 else 0
    },
    {
        'output': 'Oswald Efficiency (e)',
        'inputs': ['K (Induced drag factor)', 'Aspect Ratio (AR)'],
        'name' : 'From K and AR',
        'calculate': lambda v: 1 / (math.pi * v['K (Induced drag factor)'] * v['Aspect Ratio (AR)']) if v['K (Induced drag factor)'] != 0 and v['Aspect Ratio (AR)'] != 0 else 0
    },
    {
        'output': 'Aspect Ratio (AR)',
        'inputs': ['K (Induced drag factor)', 'Oswald Efficiency (e)'],
        'name' : 'From K and e',
        'calculate': lambda v: 1 / (math.pi * v['K (Induced drag factor)'] * v['Oswald Efficiency (e)']) if v['K (Induced drag factor)'] != 0 and v['Oswald Efficiency (e)'] != 0 else 0
    },
    {
        'output': 'CL^0.5/CD Ratio',
        'inputs': ['CL (Lift Coefficient)', 'CD (Drag Coefficient)'],
        'name' : 'From CL and CD',
        'calculate': lambda v: v['CL (Lift Coefficient)']**0.5 / v['CD (Drag Coefficient)'] if v['CD (Drag Coefficient)'] != 0 else 0
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['CL^0.5/CD Ratio', 'CD (Drag Coefficient)'],
        'name' : 'From CL^0.5/CD Ratio',
        'calculate': lambda v: (v['CL^0.5/CD Ratio'] * v['CD (Drag Coefficient)'])**2
    },
    {
        'output': 'CD (Drag Coefficient)',
        'inputs': ['CL^0.5/CD Ratio', 'CL (Lift Coefficient)'],
        'name' : 'From CL^0.5/CD Ratio',
        'calculate': lambda v: v['CL (Lift Coefficient)']**0.5 / v['CL^0.5/CD Ratio'] if v['CL^0.5/CD Ratio'] != 0 else 0
    }, 
    # ========================================
    # FUNDAMENTAL AERODYNAMIC PARAMETERS 
    # ========================================
    {
        'output': 'Reynolds Number (Re)',
        'inputs': ['Air Density (kg/m^3)', 'Velocity (m/s)', 'Characteristic Length (m)', 'Dynamic Viscosity (Pa*s)'],
        'calculate': lambda v: (v['Air Density (kg/m^3)'] * v['Velocity (m/s)'] * v['Characteristic Length (m)']) / v['Dynamic Viscosity (Pa*s)'] if v['Dynamic Viscosity (Pa*s)'] != 0 else 0
    },
    {
        'output': 'Dynamic Pressure (Pa)',
        'inputs': ['Air Density (kg/m^3)', 'Velocity (m/s)'],
        'calculate': lambda v: 0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2
    },

    # ================================== 
    # ATMOSPHERIC MODELS FAMILY 
    # ==================================
    {
        'output': 'Local Temperature (K)',
        'inputs': ['Altitude (m)'],
        'name' : 'From Altitude',
        'calculate': lambda v: T0 - L * v['Altitude (m)'] if v['Altitude (m)'] <= 11000 else T11
    },
    {
        'output': 'Altitude (m)',
        'inputs': ['Local Temperature (K)'],
        'conditions': ["Altitude (m) <= 11000"],
        'name' : 'From Local Temperature',
        'calculate': lambda v: (T0 - v['Local Temperature (K)']) / L if L != 0 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'inputs': ['Altitude (m)'],
        'name' : 'From Altitude',
        'calculate': lambda v: RHO0 * ((T0 - L * v['Altitude (m)']) / T0)**((G / (L * R)) - 1) if v['Altitude (m)'] <= 11000 else RHO11 * math.exp(-G * (v['Altitude (m)'] - 11000) / (R * T11))
    },
    {
        'output': 'a (Speed of Sound)',
        'inputs': ['Local Temperature (K)'],
        'calculate': lambda v: math.sqrt(abs(GAMMA * R * v['Local Temperature (K)']))
    },
    {
        'output': 'Local Temperature (K)',
        'inputs': ['a (Speed of Sound)'],
        'calculate': lambda v: v['a (Speed of Sound)']**2 / (GAMMA * R) if (GAMMA * R) != 0 else 0
    },
    {
        'output': 'a (Speed of Sound)',
        'inputs': ['Altitude (m)'],
        'name' : 'From Altitude',
        'calculate': lambda v: math.sqrt(abs(GAMMA * R * (T0 - L * v['Altitude (m)'])))
    },
    {
        'output': 'Velocity (m/s)',
        'inputs': ['M (Mach Number)', 'a (Speed of Sound)'],
        'name' : 'From Mach and speed of sound',
        'calculate': lambda v: v['M (Mach Number)'] * v['a (Speed of Sound)']
    },
    {
        'output': 'M (Mach Number)',
        'inputs': ['Velocity (m/s)', 'a (Speed of Sound)'],
        'name' : 'From Velocity and speed of sound',
        'calculate': lambda v: v['Velocity (m/s)'] / v['a (Speed of Sound)'] if v['a (Speed of Sound)'] != 0 else 0
    },
    # =====================================
    # AIRCRAFT GEOMETRY/WEIGHT FAMILY 
    # =====================================
    {
        'output': 'w/s (Wing Loading)',
        'inputs': ['Aircraft Weight (N)', 'Wing Area (m^2)'],
        'calculate': lambda v: v['Aircraft Weight (N)'] / v['Wing Area (m^2)'] if v['Wing Area (m^2)'] != 0 else 0
    },
    {
        'output': 'Wing Area (m^2)',
        'inputs': ['w/s (Wing Loading)', 'Aircraft Weight (N)'],
        'name' : 'From w/s',
        'calculate': lambda v: v['Aircraft Weight (N)'] / v['w/s (Wing Loading)'] if v['w/s (Wing Loading)'] != 0 else 0
    },
    {
        'output': 'Aircraft Weight (N)',
        'inputs': ['w/s (Wing Loading)', 'Wing Area (m^2)'],
        'name' : 'From w/s',
        'calculate': lambda v: v['w/s (Wing Loading)'] * v['Wing Area (m^2)']
    },
    {
        'output': 'Wing Area (m^2)',
        'inputs': ['b (Wing Span)', 'Aspect Ratio (AR)'],
        'name' : 'From b and AR',
        'calculate': lambda v: (v['b (Wing Span)']**2) / v['Aspect Ratio (AR)'] if v['Aspect Ratio (AR)'] != 0 else 0
    },
    {
        'output': 'b (Wing Span)',
        'inputs': ['Wing Area (m^2)', 'Aspect Ratio (AR)'],
        'name' : 'From Wing area and AR',
        'calculate': lambda v: math.sqrt(abs(v['Wing Area (m^2)'] * v['Aspect Ratio (AR)']))
    },
    {
        'output': 'Aspect Ratio (AR)',
        'inputs': ['b (Wing Span)', 'Wing Area (m^2)'],
        'name' : 'From b and Wing area',
        'calculate': lambda v: (v['b (Wing Span)']**2) / v['Wing Area (m^2)'] if v['Wing Area (m^2)'] != 0 else 0
    },
    # =========================
    # STEADY LEVEL FLIGHT 
    # =========================
    {
        'output': 'Load Factor (n)',
        'inputs': [], 
        'name' : 'Load factor is 1 in steady level flight',
        'conditions': ['Steady level flight'],
        'calculate': lambda v: 1.0
    },
    {
        'output': 'Thrust Required (N)',
        'inputs': ['Drag'],
        'name' : 'Drag = Thrust in steady level flight',
        'conditions': ['Steady level flight'],
        'alias': True
    },
    {
        'output': 'Drag',
        'inputs': ['Thrust Required (N)'],
        'name' : 'Drag = Thrust in steady level flight',
        'conditions': ['Steady level flight'],
        'alias': True
    },
    {
        'output': 'Thrust',
        'inputs': ['Thrust Required (N)'],
        'name' : 'Thrust required = Thrust in steady level flight',
        'conditions': ['Steady level flight'],
        'alias': True
    },
    {
        'output': 'Thrust Required (N)',
        'inputs': ['Thrust'],
        'name' : 'Thrust required = Thrust in steady level flight',
        'conditions': ['Steady level flight'],
        'alias': True
    },    
    {
        'output': 'Lift',
        'inputs': ['Aircraft Weight (N)'],
        'name' : 'Lift = Weight in steady level flight',
        'conditions': ['Steady level flight'],
        'alias': True
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['Aircraft Weight (N)', 'Dynamic Pressure (Pa)', 'Wing Area (m^2)'],
        'conditions': ['Steady level flight'],
        'name' : 'From Lift equation in steady level flight',
        'calculate': lambda v: v['Aircraft Weight (N)'] / (v['Dynamic Pressure (Pa)'] * v['Wing Area (m^2)']) if v['Dynamic Pressure (Pa)'] != 0 and v['Wing Area (m^2)'] != 0 else 0
    },
    {
        'output': 'Thrust Required (N)',
        'inputs': ['Aircraft Weight (N)', 'L/D (Lift to Drag ratio)'],
        'conditions': ['Steady level flight'],
        'calculate': lambda v: v['Aircraft Weight (N)'] / v['L/D (Lift to Drag ratio)'] if v['L/D (Lift to Drag ratio)'] != 0 else 0
    },
    {
        'output': 'Aircraft Weight (N)',
        'inputs': ['Thrust Required (N)', 'L/D (Lift to Drag ratio)'],
        'conditions': ['Steady level flight'],
        'calculate': lambda v: v['Thrust Required (N)'] * v['L/D (Lift to Drag ratio)']
    },
    {
        'output': 'L/D (Lift to Drag ratio)',
        'inputs': ['Aircraft Weight (N)', 'Thrust Required (N)'],
        'conditions': ['Steady level flight'],
        'calculate': lambda v: v['Aircraft Weight (N)'] / v['Thrust Required (N)'] if v['Thrust Required (N)'] != 0 else 0
    },

    # ======================================= 
    # STEADY CLIMBING FLIGHT CONDITION
    # =======================================
    {
        'output': 'Thrust',
        'inputs': ['Drag', 'Aircraft Weight (N)', 'Climb Angle (radians)'],
        'conditions': ['Steady climbing flight'],
        'name' : 'From climb angle in steady climbing flight',
        'calculate': lambda v: v['Drag'] + v['Aircraft Weight (N)'] * math.sin(v['Climb Angle (radians)'])
    },
    {
        'output': 'Drag',
        'inputs': ['Thrust', 'Aircraft Weight (N)', 'Climb Angle (radians)'],
        'conditions': ['Steady climbing flight'],
        'name' : 'From climb angle in steady climbing flight',
        'calculate': lambda v: v['Thrust'] - v['Aircraft Weight (N)'] * math.sin(v['Climb Angle (radians)'])
    },
    {
        'output': 'Aircraft Weight (N)',
        'inputs': ['Thrust', 'Drag', 'Climb Angle (radians)'],
        'conditions': ['Steady climbing flight'],
        'name' : 'From climb angle in steady climbing flight',
        'calculate': lambda v: (v['Thrust'] - v['Drag']) / math.sin(v['Climb Angle (radians)']) if math.sin(v['Climb Angle (radians)']) != 0 else 0
    },
    {
        'output': 'Lift',
        'inputs': ['Aircraft Weight (N)', 'Climb Angle (radians)'],
        'conditions': ['Steady climbing flight'],
        'name' : 'From climb angle in steady climbing flight',
        'calculate': lambda v: v['Aircraft Weight (N)'] * math.cos(v['Climb Angle (radians)'])
    },
    {
        'output': 'Aircraft Weight (N)',
        'inputs': ['Lift', 'Climb Angle (radians)'],
        'conditions': ['Steady climbing flight'],
        'name' : 'From climb angle in steady climbing flight',
        'calculate': lambda v: v['Lift'] / math.cos(v['Climb Angle (radians)']) if math.cos(v['Climb Angle (radians)']) != 0 else 0
    },
    {
        'output': 'Climb Angle (radians)',
        'inputs': ['Lift', 'Aircraft Weight (N)'],
        'conditions': ['Steady climbing flight'],
        'name' : 'From L and W in steady climbing flight',
        'calculate': lambda v: math.acos(v['Lift'] / v['Aircraft Weight (N)']) if v['Aircraft Weight (N)'] != 0 and -1 <= v['Lift'] / v['Aircraft Weight (N)'] <= 1 else 0
    },
    {
        'output': 'Rate of Climb (m/s)',
        'inputs': ['Velocity (m/s)', 'Climb Angle (radians)'],
        'conditions': ['Steady climbing flight'],
        'name' : 'From velocity and climb angle in steady climbing flight',
        'calculate': lambda v: v['Velocity (m/s)'] * math.sin(v['Climb Angle (radians)'])
    },
    {
        'output': 'Velocity (m/s)',
        'inputs': ['Rate of Climb (m/s)', 'Climb Angle (radians)'],
        'conditions': ['Steady climbing flight'],
        'name' : 'From climb angle and rate of climb in steady climbing flight',
        'calculate': lambda v: v['Rate of Climb (m/s)'] / math.sin(v['Climb Angle (radians)']) if math.sin(v['Climb Angle (radians)']) != 0 else 0
    },
    {
        'output': 'Climb Angle (radians)',
        'inputs': ['Rate of Climb (m/s)', 'Velocity (m/s)'],
        'conditions': ['Steady climbing flight'],
         'name' : 'From rate of clib and velocity in steady climbing flight',
        'calculate': lambda v: math.asin(v['Rate of Climb (m/s)'] / v['Velocity (m/s)']) if v['Velocity (m/s)'] != 0 and -1 <= v['Rate of Climb (m/s)'] / v['Velocity (m/s)'] <= 1 else 0
    },
    # ============================================
    # LIFT EQUATION FAMILY (L, rho, V, S, CL)
    # ============================================
    {
        'output': 'Lift',
        'inputs': ['Air Density (kg/m^3)', 'Velocity (m/s)', 'Wing Area (m^2)', 'CL (Lift Coefficient)'],
        'name' : 'From Lift equation',
        'calculate': lambda v: 0.5 * v['Air Density (kg/m^3)'] * (v['Velocity (m/s)']**2) * v['Wing Area (m^2)'] * v['CL (Lift Coefficient)']
    },
    {
        'output': 'Air Density (kg/m^3)',
        'inputs': ['Lift', 'Velocity (m/s)', 'Wing Area (m^2)', 'CL (Lift Coefficient)'],
        'name' : 'From Lift equation',
        'calculate': lambda v: v['Lift'] / (0.5 * v['Velocity (m/s)']**2 * v['Wing Area (m^2)'] * v['CL (Lift Coefficient)']) if v['Velocity (m/s)'] != 0 and v['Wing Area (m^2)'] != 0 and v['CL (Lift Coefficient)'] != 0 else 0
    },
    {
        'output': 'Velocity (m/s)',
        'inputs': ['Lift', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CL (Lift Coefficient)'],
        'name' : 'From Lift equation',
        'calculate': lambda v: math.sqrt(abs(v['Lift'] / (0.5 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CL (Lift Coefficient)']))) if v['Air Density (kg/m^3)'] != 0 and v['Wing Area (m^2)'] != 0 and v['CL (Lift Coefficient)'] != 0 else 0
    },
    {
        'output': 'Wing Area (m^2)',
        'inputs': ['Lift', 'Air Density (kg/m^3)', 'Velocity (m/s)', 'CL (Lift Coefficient)'],
        'name' : 'From Lift equation',
        'calculate': lambda v: v['Lift'] / (0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2 * v['CL (Lift Coefficient)']) if v['Air Density (kg/m^3)'] != 0 and v['Velocity (m/s)'] != 0 and v['CL (Lift Coefficient)'] != 0 else 0
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['Lift', 'Air Density (kg/m^3)', 'Velocity (m/s)', 'Wing Area (m^2)'],
        'name' : 'From Lift equation',
        'calculate': lambda v: v['Lift'] / (0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2 * v['Wing Area (m^2)']) if v['Air Density (kg/m^3)'] != 0 and v['Velocity (m/s)'] != 0 and v['Wing Area (m^2)'] != 0 else 0
    },
    # ==========================================
    # DRAG EQUATION FAMILY (D, rho, V, S, CD) 
    # ==========================================
    {
        'output': 'Drag',
        'inputs': ['Air Density (kg/m^3)', 'Velocity (m/s)', 'Wing Area (m^2)', 'CD (Drag Coefficient)'],
        'name' : 'From Drag equation',
        'calculate': lambda v: 0.5 * v['Air Density (kg/m^3)'] * (v['Velocity (m/s)']**2) * v['Wing Area (m^2)'] * v['CD (Drag Coefficient)']
    },
    {
        'output': 'Air Density (kg/m^3)',
        'inputs': ['Drag', 'Velocity (m/s)', 'Wing Area (m^2)', 'CD (Drag Coefficient)'],
        'name' : 'From Drag equation',
        'calculate': lambda v: v['Drag'] / (0.5 * v['Velocity (m/s)']**2 * v['Wing Area (m^2)'] * v['CD (Drag Coefficient)']) if v['Velocity (m/s)'] != 0 and v['Wing Area (m^2)'] != 0 and v['CD (Drag Coefficient)'] != 0 else 0
    },
    {
        'output': 'Velocity (m/s)',
        'inputs': ['Drag', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CD (Drag Coefficient)'],
        'name' : 'From Drag equation',
        'calculate': lambda v: math.sqrt(abs(v['Drag'] / (0.5 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CD (Drag Coefficient)']))) if v['Air Density (kg/m^3)'] != 0 and v['Wing Area (m^2)'] != 0 and v['CD (Drag Coefficient)'] != 0 else 0
    },
    {
        'output': 'Wing Area (m^2)',
        'inputs': ['Drag', 'Air Density (kg/m^3)', 'Velocity (m/s)', 'CD (Drag Coefficient)'],
        'name' : 'From Drag equation',
        'calculate': lambda v: v['Drag'] / (0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2 * v['CD (Drag Coefficient)']) if v['Air Density (kg/m^3)'] != 0 and v['Velocity (m/s)'] != 0 and v['CD (Drag Coefficient)'] != 0 else 0
    },
    {
        'output': 'CD (Drag Coefficient)',
        'inputs': ['Drag', 'Air Density (kg/m^3)', 'Velocity (m/s)', 'Wing Area (m^2)'],
        'name' : 'From Drag equation',
        'calculate': lambda v: v['Drag'] / (0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2 * v['Wing Area (m^2)']) if v['Air Density (kg/m^3)'] != 0 and v['Velocity (m/s)'] != 0 and v['Wing Area (m^2)'] != 0 else 0
    },

    # =========================
    # DRAG COMPONENT FAMILY 
    # =========================
    {
        'output': 'Induced Drag (N)',
        'name': 'from CL and K',
        'inputs': ['Dynamic Pressure (Pa)', 'Wing Area (m^2)', 'K (Induced drag factor)', 'CL (Lift Coefficient)'],
        'calculate': lambda v: v['Dynamic Pressure (Pa)'] * v['Wing Area (m^2)'] * v['K (Induced drag factor)'] * v['CL (Lift Coefficient)']**2
    },
    {
        'output': 'Drag',
        'inputs': ['Parasite Drag (N)', 'Induced Drag (N)'],
        'name' : 'Sum of parasite and induced drag',
        'calculate': lambda v: v['Parasite Drag (N)'] + v['Induced Drag (N)']
    },
    {
        'output': 'Parasite Drag (N)',
        'inputs': ['Drag', 'Induced Drag (N)'],
        'calculate': lambda v: v['Drag'] - v['Induced Drag (N)']
    },
    {
        'output': 'Induced Drag (N)',
        'inputs': ['Drag', 'Parasite Drag (N)'],
        'calculate': lambda v: v['Drag'] - v['Parasite Drag (N)']
    },
    {
        'output': 'Parasite Drag (N)',
        'inputs': ['Air Density (kg/m^3)', 'Velocity (m/s)', 'Wing Area (m^2)', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: 0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2 * v['Wing Area (m^2)'] * v['CD0 (Zero-lift Drag Coefficient)']
    },
    {
        'output': 'Induced Drag (N)',
        'inputs': ['Aircraft Weight (N)', 'K (Induced drag factor)', 'Wing Area (m^2)', 'Air Density (kg/m^3)', 'Velocity (m/s)'],
        'conditions': ['Steady level flight'], # Changed from Lift=Weight to be consistent
        'calculate': lambda v: (2 * v['K (Induced drag factor)'] * v['Aircraft Weight (N)']**2) / (v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2 * v['Wing Area (m^2)']) if v['Air Density (kg/m^3)'] != 0 and v['Velocity (m/s)'] != 0 and v['Wing Area (m^2)'] != 0 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'inputs': ['Parasite Drag (N)', 'Velocity (m/s)', 'Wing Area (m^2)', 'CD0 (Zero-lift Drag Coefficient)'],
        'name' : 'From Drag equation',
        'calculate': lambda v: v['Parasite Drag (N)'] / (0.5 * v['Velocity (m/s)']**2 * v['Wing Area (m^2)'] * v['CD0 (Zero-lift Drag Coefficient)']) if v['Velocity (m/s)'] > 0 and v['Wing Area (m^2)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
       'output': 'Velocity (m/s)',
       'inputs': ['Parasite Drag (N)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CD0 (Zero-lift Drag Coefficient)'],
       'name' : 'From Drag equation',
       'calculate': lambda v: math.sqrt(abs(v['Parasite Drag (N)'] / (0.5 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CD0 (Zero-lift Drag Coefficient)']))) if v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'inputs': ['Parasite Drag (N)', 'Air Density (kg/m^3)', 'Velocity (m/s)', 'Wing Area (m^2)'],
        'name' : 'From Drag equation',
        'calculate': lambda v: v['Parasite Drag (N)'] / (0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2 * v['Wing Area (m^2)']) if v['Air Density (kg/m^3)'] > 0 and v['Velocity (m/s)'] > 0 and v['Wing Area (m^2)'] > 0 else 0
    },
    # =================================
    # Thrust to Weight Ratio Family 
    # =================================
    {
        'output': 'Thrust to Weight Ratio',
        'inputs': ['Thrust', 'Aircraft Weight (N)'],
        'calculate': lambda v: v['Thrust'] / v['Aircraft Weight (N)'] if v['Aircraft Weight (N)'] != 0 else 0
    },
    {
        'output': 'Thrust',
        'inputs': ['Thrust to Weight Ratio', 'Aircraft Weight (N)'],
        'name' : 'From Thrust to Weight ratio',
        'calculate': lambda v: v['Thrust to Weight Ratio'] * v['Aircraft Weight (N)']
    },
    {
        'output': 'Aircraft Weight (N)',
        'inputs': ['Thrust to Weight Ratio', 'Thrust'],
        'name' : 'From Thrust to Weight ratio',
        'calculate': lambda v: v['Thrust'] / v['Thrust to Weight Ratio'] if v['Thrust to Weight Ratio'] != 0 else 0
    },


    # ======================================================================
    # SPECIAL CONDITION: L/D ratio is maximum (Thrust required min) 
    # ======================================================================
    {
        'output': 'Maximum L/D Ratio',
        'inputs': ['CD0 (Zero-lift Drag Coefficient)', 'K (Induced drag factor)'],
        'name': 'Value of Max L/D Ratio from CD0 and K',
        'calculate': lambda v: 1 / math.sqrt(4 * v['CD0 (Zero-lift Drag Coefficient)'] * v['K (Induced drag factor)']) if v['CD0 (Zero-lift Drag Coefficient)'] > 0 and v['K (Induced drag factor)'] > 0 else 0
    },
    {
        'output': 'L/D (Lift to Drag ratio)',
        'inputs': ['Maximum L/D Ratio'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'alias': True
    },
    {
        'output': 'Thrust Required (N)',
        'inputs': ['Aircraft Weight (N)', 'Maximum L/D Ratio'],
        'conditions': ['L/D ratio is maximum (Thrust required min)', 'Steady level flight'],
        'name': 'Min Tr from L/D max',
        'calculate': lambda v: v['Aircraft Weight (N)'] / v['Maximum L/D Ratio'] if v['Maximum L/D Ratio'] != 0 else 0
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'inputs': ['Maximum L/D Ratio', 'K (Induced drag factor)'], 
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'CD0 from L/D max',
        'calculate': lambda v: 1 / (4 * v['K (Induced drag factor)'] * v['Maximum L/D Ratio']**2) if v['K (Induced drag factor)'] > 0 and v['Maximum L/D Ratio'] > 0 else 0
    },
    {
        'output': 'K (Induced drag factor)',
        'inputs': ['Maximum L/D Ratio', 'CD0 (Zero-lift Drag Coefficient)'], 
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'CD0 from L/D max',
        'calculate': lambda v: 1 / (4 * v['CD0 (Zero-lift Drag Coefficient)'] * v['Maximum L/D Ratio']**2) if v['CD0 (Zero-lift Drag Coefficient)'] > 0 and v['Maximum L/D Ratio'] > 0 else 0
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['CD0 (Zero-lift Drag Coefficient)', 'K (Induced drag factor)'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'CL for Max L/D',
        'calculate': lambda v: math.sqrt(abs(v['CD0 (Zero-lift Drag Coefficient)'] / v['K (Induced drag factor)'])) if v['K (Induced drag factor)'] != 0 else 0
    },
    {
        'output': 'CD (Drag Coefficient)',
        'inputs': ['CD0 (Zero-lift Drag Coefficient)'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'CD for Max L/D',
        'calculate': lambda v: 2 * v['CD0 (Zero-lift Drag Coefficient)']
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'inputs': ['CD (Drag Coefficient)'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'CD0 from L/D Max CD',
        'calculate': lambda v: v['CD (Drag Coefficient)'] / 2
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'inputs': ['K (Induced drag factor)', 'CL (Lift Coefficient)'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'CD0 from L/D Max definition',
        'calculate': lambda v: v['K (Induced drag factor)'] * (v['CL (Lift Coefficient)']**2)
    },
    {
        'output': 'K (Induced drag factor)',
        'inputs': ['CD0 (Zero-lift Drag Coefficient)', 'CL (Lift Coefficient)'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'K from L/D Max CL and CD0',
        'calculate': lambda v: v['CD0 (Zero-lift Drag Coefficient)'] / (v['CL (Lift Coefficient)']**2) if v['CL (Lift Coefficient)'] != 0 else 0
    },
    {
        'output': 'Velocity at Max L/D (m/s)',
        'inputs': ['Air Density (kg/m^3)', 'w/s (Wing Loading)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: math.sqrt((2 / v['Air Density (kg/m^3)']) * math.sqrt(v['K (Induced drag factor)'] / v['CD0 (Zero-lift Drag Coefficient)']) * v['w/s (Wing Loading)']) if v['Air Density (kg/m^3)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'inputs': ['Velocity at Max L/D (m/s)', 'w/s (Wing Loading)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'name': 'From L/D max equation',
        'calculate': lambda v: (2 / v['Velocity at Max L/D (m/s)']**2) * math.sqrt(v['K (Induced drag factor)'] / v['CD0 (Zero-lift Drag Coefficient)']) * v['w/s (Wing Loading)'] if v['Velocity at Max L/D (m/s)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'w/s (Wing Loading)',
        'inputs': ['Velocity at Max L/D (m/s)', 'Air Density (kg/m^3)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'name': 'From L/D max equation',
        'calculate': lambda v: (v['Velocity at Max L/D (m/s)']**2 * v['Air Density (kg/m^3)']) / (2 * math.sqrt(v['K (Induced drag factor)'] / v['CD0 (Zero-lift Drag Coefficient)'])) if v['K (Induced drag factor)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'K (Induced drag factor)',
        'inputs': ['Velocity at Max L/D (m/s)', 'Air Density (kg/m^3)', 'w/s (Wing Loading)', 'CD0 (Zero-lift Drag Coefficient)'],
        'name': 'From L/D max equation',
        'calculate': lambda v: v['CD0 (Zero-lift Drag Coefficient)'] / ((2 * v['w/s (Wing Loading)']) / (v['Air Density (kg/m^3)'] * v['Velocity at Max L/D (m/s)']**2))**2 if v['Air Density (kg/m^3)'] > 0 and v['Velocity at Max L/D (m/s)'] > 0 else 0
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'inputs': ['Velocity at Max L/D (m/s)', 'Air Density (kg/m^3)', 'w/s (Wing Loading)', 'K (Induced drag factor)'],
        'name': 'From L/D max equation',
        'calculate': lambda v: v['K (Induced drag factor)'] * ((2 * v['w/s (Wing Loading)']) / (v['Air Density (kg/m^3)'] * v['Velocity at Max L/D (m/s)']**2))**2 if v['Air Density (kg/m^3)'] > 0 and v['Velocity at Max L/D (m/s)'] > 0 else 0
    },
    {
        'output': 'Minimum Thrust to Weight Ratio (Tr/W)min',
        'inputs': ['L/D (Lift to Drag ratio)'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'From L/D max',
        'calculate': lambda v: 1 / v['L/D (Lift to Drag ratio)'] if v['L/D (Lift to Drag ratio)'] != 0 else 0
    },
    {
        'output': 'L/D (Lift to Drag ratio)',
        'inputs': ['Minimum Thrust to Weight Ratio (Tr/W)min'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'From (Tr/W)min',
        'calculate': lambda v: 1 / v['Minimum Thrust to Weight Ratio (Tr/W)min'] if v['Minimum Thrust to Weight Ratio (Tr/W)min'] != 0 else 0
    },
    {
        'output': 'Minimum Thrust to Weight Ratio (Tr/W)min', 
        'inputs': ['CD0 (Zero-lift Drag Coefficient)', 'K (Induced drag factor)'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'From CD0 and K when L/D is max',
        'calculate': lambda v: math.sqrt(4 * v['CD0 (Zero-lift Drag Coefficient)'] * v['K (Induced drag factor)'])
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'inputs': ['Minimum Thrust to Weight Ratio (Tr/W)min', 'K (Induced drag factor)'], 
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'From (Tr/W)min and K when L/D is max',
        'calculate': lambda v: (v['Minimum Thrust to Weight Ratio (Tr/W)min']**2) / (4 * v['K (Induced drag factor)']) if v['K (Induced drag factor)'] != 0 else 0
    },
    {
        'output': 'K (Induced drag factor)',
        'inputs': ['Minimum Thrust to Weight Ratio (Tr/W)min', 'CD0 (Zero-lift Drag Coefficient)'],
        'conditions': ['L/D ratio is maximum (Thrust required min)'],
        'name': 'From CD0 and (Tr/W)min when L/D is max',
        'calculate': lambda v: (v['Minimum Thrust to Weight Ratio (Tr/W)min']**2) / (4 * v['CD0 (Zero-lift Drag Coefficient)']) if v['CD0 (Zero-lift Drag Coefficient)'] != 0 else 0
    
    },
    {
        'output': 'Power Required (W)',
        'inputs': ['Thrust Required (N)', 'Velocity (m/s)'],
        'name': '(from Thrust Required * Velocity)',
        'calculate': lambda v: v['Thrust Required (N)'] * v['Velocity (m/s)']
    },
    {
        'output': 'Thrust Required (N)',
        'inputs': ['Power Required (W)', 'Velocity (m/s)'],
        'name' : '(from Power required / Velocity)',
        'calculate': lambda v: v['Power Required (W)'] / v['Velocity (m/s)'] if v['Velocity (m/s)'] != 0 else 0
    },
    {
        'output': 'Velocity (m/s)',
        'inputs': ['Power Required (W)', 'Thrust Required (N)'],
        'name' : '(from Power Required / Thrust Required)',
        'calculate': lambda v: v['Power Required (W)'] / v['Thrust Required (N)'] if v['Thrust Required (N)'] != 0 else 0
    },
    # ====================================================================
    # POWER REQUIRED FAMILY (From Aircraft Parameters in Level Flight) 
    # ====================================================================
    {
        'output': 'Power Required (W)',
        'inputs': ['Aircraft Weight (N)', 'CD (Drag Coefficient)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CL (Lift Coefficient)'],
        'conditions': ['Steady level flight'],
        'name': 'Pr in steady level flight',
        'calculate': lambda v: math.sqrt( (2 * v['Aircraft Weight (N)']**3 * v['CD (Drag Coefficient)']**2) / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CL (Lift Coefficient)']**3) ) if v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['CL (Lift Coefficient)'] > 0 else 0
    },
    {
        'output': 'Aircraft Weight (N)',
        'inputs': ['Power Required (W)', 'CD (Drag Coefficient)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CL (Lift Coefficient)'],
        'conditions': ['Steady level flight'],
        'name': 'From Pr in steady level flight',
        'calculate': lambda v: ( (v['Power Required (W)']**2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CL (Lift Coefficient)']**3) / (2 * v['CD (Drag Coefficient)']**2) )**(1/3) if v['CD (Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'CD (Drag Coefficient)',
        'inputs': ['Power Required (W)', 'Aircraft Weight (N)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CL (Lift Coefficient)'],
        'conditions': ['Steady level flight'],
        'name': 'From Pr in steady level flight',
        'calculate': lambda v: math.sqrt( (v['Power Required (W)']**2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CL (Lift Coefficient)']**3) / (2 * v['Aircraft Weight (N)']**3) ) if v['Aircraft Weight (N)'] > 0 else 0
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['Power Required (W)', 'Aircraft Weight (N)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CD (Drag Coefficient)'],
        'conditions': ['Steady level flight'],
        'name': 'From Pr in steady level flight',
        'calculate': lambda v: ( (2 * v['Aircraft Weight (N)']**3 * v['CD (Drag Coefficient)']**2) / (v['Power Required (W)']**2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)']) )**(1/3) if v['Power Required (W)'] > 0 and v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 else 0
    },
    {
        'output': 'CD (Drag Coefficient)',
        'inputs': ['CD0 (Zero-lift Drag Coefficient)'],
        'conditions': ['Cl^3/2/Cd max (minimum power required)'],
        'name': 'CD for Min Power Required',
        'calculate': lambda v: 4 * v['CD0 (Zero-lift Drag Coefficient)']
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'inputs': ['CD (Drag Coefficient)'],
        'conditions': ['Cl^3/2/Cd max (minimum power required)'],
        'name': 'CD0 from Min Power Required CD',
        'calculate': lambda v: v['CD (Drag Coefficient)'] / 4
    },
    {
        'output': 'CL (Lift Coefficient)',
        'inputs': ['CD0 (Zero-lift Drag Coefficient)', 'K (Induced drag factor)'],
        'conditions': ['Cl^3/2/Cd max (minimum power required)'],
        'name': 'CL for Min Power Required',
        'calculate': lambda v: math.sqrt(abs(3 * v['CD0 (Zero-lift Drag Coefficient)'] / v['K (Induced drag factor)'])) if v['K (Induced drag factor)'] != 0 else 0
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'inputs': ['CL (Lift Coefficient)', 'K (Induced drag factor)'],
        'conditions': ['Cl^3/2/Cd max (minimum power required)'],
        'name': 'CD0 from Min Power Required CL',
        'calculate': lambda v: (v['K (Induced drag factor)'] * v['CL (Lift Coefficient)']**2) / 3
    },
    {
        'output': 'Power Required (W)',
        'inputs': ['Aircraft Weight (N)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CD (Drag Coefficient)', 'CL (Lift Coefficient)'],
        'conditions': ['Cl^3/2/Cd max (minimum power required)'],
        'name': 'Minimum power required',
        'calculate': lambda v: math.sqrt(abs((2 * v['Aircraft Weight (N)']**3 * v['CD (Drag Coefficient)']**2) / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CL (Lift Coefficient)']**3))) if v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['CL (Lift Coefficient)'] > 0 else 0
    },
    {
        'output': 'Power Required (W)',
        'inputs': ['Aircraft Weight (N)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'Power Ratio (CL^3/2/CD)'],
        'conditions': ['Cl^3/2/Cd max (minimum power required)'],
        'name': '(Minimum Power Required)',
        'calculate': lambda v: math.sqrt((2 * v['Aircraft Weight (N)']**3) / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'])) * (1 / v['Power Ratio (CL^3/2/CD)']) if v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['Power Ratio (CL^3/2/CD)'] > 0 else 0
    },
    {
        'output': 'Power Ratio (CL^3/2/CD)',
        'inputs': ['Aircraft Weight (N)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'Power Required (W)'],
        'conditions': ['Cl^3/2/Cd max (minimum power required)'],
        'name': 'From Pr equation when Cl^3/2/Cd is max',
        'calculate': lambda v: math.sqrt((2 * v['Aircraft Weight (N)']**3) / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'])) / v['Power Required (W)'] if v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['Power Required (W)'] > 0 else 0
    },
    {
        'output': 'Power Ratio (CL^3/2/CD)',
        'inputs': ['K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'name': 'Value of CL^3/2/CD at Min Power Required',
        'calculate': lambda v: (1/4) * (3 / (v['K (Induced drag factor)'] * v['CD0 (Zero-lift Drag Coefficient)']**(1/3)))**(3/4) if v['K (Induced drag factor)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    # ============================================
    # VELOCITY FOR MIN POWER REQUIRED FAMILY 
    # ============================================
    {
        'output': 'Velocity at Min Power Required (m/s)',
        'name': 'Velocity at Min Power required from properties',
        'inputs': ['Air Density (kg/m^3)', 'w/s (Wing Loading)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: math.sqrt((2 / v['Air Density (kg/m^3)']) * math.sqrt(abs(v['K (Induced drag factor)'] / (3 * v['CD0 (Zero-lift Drag Coefficient)']))) * v['w/s (Wing Loading)']) if v['Air Density (kg/m^3)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'w/s (Wing Loading)',
        'name': 'w/s from Velocity at Min Power required',
        'inputs': ['Velocity at Min Power Required (m/s)', 'Air Density (kg/m^3)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: (v['Velocity at Min Power Required (m/s)']**2 * v['Air Density (kg/m^3)']) / (2 * math.sqrt(abs(v['K (Induced drag factor)'] / (3 * v['CD0 (Zero-lift Drag Coefficient)']))) ) if v['K (Induced drag factor)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'name': 'rho from Velocity at Min Power required',
        'inputs': ['Velocity at Min Power Required (m/s)', 'w/s (Wing Loading)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: (2 / v['Velocity at Min Power Required (m/s)']**2) * math.sqrt(abs(v['K (Induced drag factor)'] / (3 * v['CD0 (Zero-lift Drag Coefficient)']))) * v['w/s (Wing Loading)'] if v['Velocity at Min Power Required (m/s)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'K (Induced drag factor)',
        'name': 'K from Velocity at Min Power required',
        'inputs': ['Velocity at Min Power Required (m/s)', 'Air Density (kg/m^3)', 'w/s (Wing Loading)', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: 3 * v['CD0 (Zero-lift Drag Coefficient)'] * ((v['Velocity at Min Power Required (m/s)']**2 * v['Air Density (kg/m^3)']) / (2 * v['w/s (Wing Loading)']))**2 if v['w/s (Wing Loading)'] > 0 else 0
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'name': 'CD0 from Velocity at Min Power required',
        'inputs': ['Velocity at Min Power Required (m/s)', 'Air Density (kg/m^3)', 'w/s (Wing Loading)', 'K (Induced drag factor)'],
        'calculate': lambda v: v['K (Induced drag factor)'] / (3 * ((v['Velocity at Min Power Required (m/s)']**2 * v['Air Density (kg/m^3)']) / (2 * v['w/s (Wing Loading)']))**2) if v['w/s (Wing Loading)'] > 0 else 0
    },
    # ===================================================
    # Power Available Family (for propeller driven) 
    # ===================================================
    {
        'output': 'Power Available (W)',
        'name' : 'Power available from propeller efficency and engine shaft power',
        'inputs': ['Propeller Efficiency', 'Engine Shaft Power (W)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: v['Propeller Efficiency'] * v['Engine Shaft Power (W)']
    },
    {
        'output': 'Propeller Efficiency',
        'name' : 'Propeller efficency from Power available and engine shaft power',
        'inputs': ['Power Available (W)', 'Engine Shaft Power (W)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: v['Power Available (W)'] / v['Engine Shaft Power (W)'] if v['Engine Shaft Power (W)'] != 0 else 0
   },
   {
        'output': 'Engine Shaft Power (W)',
        'name' : 'Engine shaft power from propeller efficency and power available',
        'inputs': ['Power Available (W)', 'Propeller Efficiency'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: v['Power Available (W)'] / v['Propeller Efficiency'] if v['Propeller Efficiency'] != 0 else 0
   },
   # =================================================================
   # Thrust available from power available (for propeller driven) 
   # =================================================================
   {
        'output': 'Thrust Available (N)',
        'name' : 'From power available and velocity',
        'inputs': ['Power Available (W)', 'Velocity (m/s)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: v['Power Available (W)'] / v['Velocity (m/s)'] if v['Velocity (m/s)'] != 0 else 0
    },
    {
        'output': 'Power Available (W)',
        'name' : 'From thrust available and velcoity',
        'inputs': ['Thrust Available (N)', 'Velocity (m/s)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: v['Thrust Available (N)'] * v['Velocity (m/s)']
    },
    {
        'output': 'Velocity (m/s)',
        'name' : 'From thrust available and power available',
        'inputs': ['Thrust Available (N)', 'Power Available (W)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: v['Power Available (W)'] / v['Thrust Available (N)'] if v['Thrust Available (N)'] != 0 else 0
    },
    # ===========================================================
    # Power available and thrust available (for jet driven) 
    # ===========================================================
    {
        'output': 'Power Available (W)',
        'name' : 'From thrust available and velocity',
        'inputs': ['Thrust Available (N)', 'Velocity (m/s)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: v['Thrust Available (N)'] * v['Velocity (m/s)']
    },
    {
        'output': 'Thrust Available (N)',
        'name' : 'From power available and velocity',
        'inputs': ['Power Available (W)', 'Velocity (m/s)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: v['Power Available (W)'] / v['Velocity (m/s)'] if v['Velocity (m/s)'] != 0 else 0
    },
    {
        'output': 'Velocity (m/s)',
        'name' : 'From power available and thrust available',
        'inputs': ['Power Available (W)', 'Thrust Available (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: v['Power Available (W)'] / v['Thrust Available (N)'] if v['Thrust Available (N)'] != 0 else 0
    },
    # =================================================
    # Thrust lapse with altitude (for jet driven) 
    # =================================================
    {
        'output': 'Thrust Available (N)',
        'inputs': ['Sea Level Thrust Available (N)', 'Air Density (kg/m^3)', 'Thrust Lapse Exponent (m)'],
        'conditions': ['Jet-propelled'],
        'name': 'From Thrust Lapse',
        'calculate': lambda v: v['Sea Level Thrust Available (N)'] * (v['Air Density (kg/m^3)'] / RHO0)**v['Thrust Lapse Exponent (m)']
    },
    {
        'output': 'Sea Level Thrust Available (N)',
        'inputs': ['Thrust Available (N)', 'Air Density (kg/m^3)', 'Thrust Lapse Exponent (m)'],
        'conditions': ['Jet-propelled'],
        'name': 'From Thrust Lapse',
        'calculate': lambda v: v['Thrust Available (N)'] / ((v['Air Density (kg/m^3)'] / RHO0)**v['Thrust Lapse Exponent (m)']) if (v['Air Density (kg/m^3)'] / RHO0) != 0 else 0
    },
    {
        'output': 'Thrust Lapse Exponent (m)',
        'inputs': ['Thrust Available (N)', 'Sea Level Thrust Available (N)', 'Air Density (kg/m^3)'],
        'conditions': ['Jet-propelled'],
        'name': 'From Thrust available',
        'calculate': lambda v: math.log(v['Thrust Available (N)'] / v['Sea Level Thrust Available (N)']) / math.log(v['Air Density (kg/m^3)'] / RHO0) if v['Thrust Available (N)'] > 0 and v['Sea Level Thrust Available (N)'] > 0 and v['Air Density (kg/m^3)'] > 0 and (v['Air Density (kg/m^3)'] / RHO0) != 1 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'inputs': ['Thrust Available (N)', 'Sea Level Thrust Available (N)', 'Thrust Lapse Exponent (m)'],
        'conditions': ['Jet-propelled'],
        'name': 'From Thrust Lapse',
        'calculate': lambda v: RHO0 * (v['Thrust Available (N)'] / v['Sea Level Thrust Available (N)'])**(1/v['Thrust Lapse Exponent (m)']) if v['Sea Level Thrust Available (N)'] > 0 and v['Thrust Lapse Exponent (m)'] != 0 else 0
    },
    # ============================================
    # Weight, Gross weight, Fuel Weight 
    # ============================================
    {
        'output': 'Gross Weight (W0) (N)',
        'inputs': ['Empty Fuel Weight (W1) (N)', 'Fuel Weight (Wf) (N)'],
        'calculate': lambda v: v['Empty Fuel Weight (W1) (N)'] + v['Fuel Weight (Wf) (N)']
   },
   {
        'output': 'Empty Fuel Weight (W1) (N)',
        'inputs': ['Gross Weight (W0) (N)', 'Fuel Weight (Wf) (N)'],
        'calculate': lambda v: v['Gross Weight (W0) (N)'] - v['Fuel Weight (Wf) (N)']
   },
   {
        'output': 'Fuel Weight (Wf) (N)',
        'inputs': ['Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'calculate': lambda v: v['Gross Weight (W0) (N)'] - v['Empty Fuel Weight (W1) (N)']
    },
    # ================
    # SFC family 
    # ================
    {
        'output': 'SFC - Prop (C) (N/W*s)',
        'inputs': ['Fuel Weight Flow Rate (N/s)', 'Power Available (W)'],
        'name' : 'From fuel weight flow rate and power available',
        'calculate': lambda v: v['Fuel Weight Flow Rate (N/s)'] / v['Power Available (W)'] if v['Power Available (W)'] != 0 else 0
    },
    {
        'output': 'Fuel Weight Flow Rate (N/s)',
        'inputs': ['SFC - Prop (C) (N/W*s)', 'Power Available (W)'],
        'name' : 'From power available and SFC',
        'calculate': lambda v: v['SFC - Prop (C) (N/W*s)'] * v['Power Available (W)']
    },
    {
        'output': 'SFC - Jet (Ct) (1/s)',
        'inputs': ['Fuel Weight Flow Rate (N/s)', 'Thrust Available (N)',],
        'name' : 'From fuel weight flow rate and thrust available',
        'calculate': lambda v: v['Fuel Weight Flow Rate (N/s)'] / v['Thrust Available (N)'] if v['Thrust Available (N)'] != 0 else 0
    },
    {
        'output': 'Fuel Weight Flow Rate (N/s)',
        'inputs': ['SFC - Jet (Ct) (1/s)', 'Thrust Available (N)'],
        'name' : 'From thrust available and SFC',
        'calculate': lambda v: v['SFC - Jet (Ct) (1/s)'] * v['Thrust Available (N)']
    },

    # ============================= 
    # SFC CONVERSION FAMILY 
    # =============================
    {
        'output': 'SFC - Jet (Ct) (1/s)',
        'inputs': ['SFC - Prop (C) (N/W*s)', 'Velocity (m/s)', 'Propeller Efficiency'],
        'name' : 'Converted from SFC for prop',
        'calculate': lambda v: (v['SFC - Prop (C) (N/W*s)'] * v['Velocity (m/s)']) / v['Propeller Efficiency'] if v['Propeller Efficiency'] != 0 else 0
    },
    {
        'output': 'SFC - Prop (C) (N/W*s)',
        'inputs': ['SFC - Jet (Ct) (1/s)', 'Velocity (m/s)', 'Propeller Efficiency'],
        'name' : 'Converted from SFC for jet',
        'calculate': lambda v: (v['SFC - Jet (Ct) (1/s)'] * v['Propeller Efficiency']) / v['Velocity (m/s)'] if v['Velocity (m/s)'] != 0 else 0
    },
    {
        'output': 'Velocity (m/s)',
        'inputs': ['SFC - Jet (Ct) (1/s)', 'SFC - Prop (C) (N/W*s)', 'Propeller Efficiency'],
        'name' : 'From Ct*propeller efficency /C',
        'calculate': lambda v: (v['SFC - Jet (Ct) (1/s)'] * v['Propeller Efficiency']) / v['SFC - Prop (C) (N/W*s)'] if v['SFC - Prop (C) (N/W*s)'] != 0 else 0
    },
    {
        'output': 'Propeller Efficiency',
        'inputs': ['SFC - Jet (Ct) (1/s)', 'SFC - Prop (C) (N/W*s)', 'Velocity (m/s)'],
        'name' : 'From C*velocity / propeller efficency',
        'calculate': lambda v: (v['SFC - Prop (C) (N/W*s)'] * v['Velocity (m/s)']) / v['SFC - Jet (Ct) (1/s)'] if v['SFC - Jet (Ct) (1/s)'] != 0 else 0
    },
    # =========================
    # Range equations (Jet) 
    # ==========================
    {
        'output': 'Range (m)',
        'name': 'Breguet Range equation (Assuming Constant V)',
        'inputs': ['Velocity (m/s)', 'SFC - Jet (Ct) (1/s)', 'L/D (Lift to Drag ratio)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['Velocity (m/s)'] / v['SFC - Jet (Ct) (1/s)']) * v['L/D (Lift to Drag ratio)'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)']) if v['SFC - Jet (Ct) (1/s)'] > 0 and v['Empty Fuel Weight (W1) (N)'] > 0 and v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'Velocity (m/s)',
        'name': 'From Breguet Range equation (Assuming Constant V)',
        'inputs': ['Range (m)', 'SFC - Jet (Ct) (1/s)', 'L/D (Lift to Drag ratio)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['Range (m)'] * v['SFC - Jet (Ct) (1/s)']) / (v['L/D (Lift to Drag ratio)'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)'])) if v['L/D (Lift to Drag ratio)'] != 0 and v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'SFC - Jet (Ct) (1/s)',
        'name': 'From Breguet Range equation (Assuming Constant V)',
        'inputs': ['Range (m)', 'Velocity (m/s)', 'L/D (Lift to Drag ratio)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['Velocity (m/s)'] * v['L/D (Lift to Drag ratio)'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)'])) / v['Range (m)'] if v['Range (m)'] != 0 else 0
    },
    {
        'output': 'L/D (Lift to Drag ratio)',
        'name': 'From Breguet Range equation (Assuming Constant V)',
        'inputs': ['Range (m)', 'Velocity (m/s)', 'SFC - Jet (Ct) (1/s)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['Range (m)'] * v['SFC - Jet (Ct) (1/s)']) / (v['Velocity (m/s)'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)'])) if v['Velocity (m/s)'] != 0 and v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'Gross Weight (W0) (N)',
        'name': 'From Breguet Range equation (Assuming Constant V)',
        'inputs': ['Range (m)', 'Velocity (m/s)', 'SFC - Jet (Ct) (1/s)', 'L/D (Lift to Drag ratio)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: v['Empty Fuel Weight (W1) (N)'] * math.exp((v['Range (m)'] * v['SFC - Jet (Ct) (1/s)']) / (v['Velocity (m/s)'] * v['L/D (Lift to Drag ratio)'])) if v['Velocity (m/s)'] != 0 and v['L/D (Lift to Drag ratio)'] != 0 else 0
    },
    {
        'output': 'Empty Fuel Weight (W1) (N)',
        'name': 'From Breguet Range equation (Assuming Constant V)',
        'inputs': ['Range (m)', 'Velocity (m/s)', 'SFC - Jet (Ct) (1/s)', 'L/D (Lift to Drag ratio)', 'Gross Weight (W0) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: v['Gross Weight (W0) (N)'] / math.exp((v['Range (m)'] * v['SFC - Jet (Ct) (1/s)']) / (v['Velocity (m/s)'] * v['L/D (Lift to Drag ratio)'])) if v['Velocity (m/s)'] != 0 and v['L/D (Lift to Drag ratio)'] != 0 else 0
    },

    # ======================================
    # Range equation version 2 (jet)
    # ======================================
    {
        'output': 'Range (m)',
        'name': 'Breguet Range Equation (Constant AoA)',
        'inputs': ['SFC - Jet (Ct) (1/s)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CL^0.5/CD Ratio', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (2 / v['SFC - Jet (Ct) (1/s)']) * math.sqrt(2 / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'])) * v['CL^0.5/CD Ratio'] * (v['Gross Weight (W0) (N)']**0.5 - v['Empty Fuel Weight (W1) (N)']**0.5) if v['SFC - Jet (Ct) (1/s)'] > 0 and v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 else 0
    },
    {
        'output': 'SFC - Jet (Ct) (1/s)',
        'name': 'From Breguet Range equation (Assuming Constant AoA)',
        'inputs': ['Range (m)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CL^0.5/CD Ratio', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (2 / v['Range (m)']) * math.sqrt(2 / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'])) * v['CL^0.5/CD Ratio'] * (v['Gross Weight (W0) (N)']**0.5 - v['Empty Fuel Weight (W1) (N)']**0.5) if v['Range (m)'] > 0 and v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'name': 'From Breguet Range equation (Assuming Constant AoA)',
        'inputs': ['Range (m)', 'SFC - Jet (Ct) (1/s)', 'Wing Area (m^2)', 'CL^0.5/CD Ratio', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: 2 * (( (2 / v['SFC - Jet (Ct) (1/s)']) * v['CL^0.5/CD Ratio'] * (v['Gross Weight (W0) (N)']**0.5 - v['Empty Fuel Weight (W1) (N)']**0.5) ) / v['Range (m)'])**2 / v['Wing Area (m^2)'] if v['Range (m)'] > 0 and v['Wing Area (m^2)'] > 0 else 0
    },
    {
        'output': 'Gross Weight (W0) (N)',
        'name': 'From Breguet Range equation (Assuming Constant AoA)',
        'inputs': ['Range (m)', 'SFC - Jet (Ct) (1/s)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CL^0.5/CD Ratio', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: ( (v['Range (m)'] / ((2 / v['SFC - Jet (Ct) (1/s)']) * math.sqrt(2 / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'])) * v['CL^0.5/CD Ratio'])) + v['Empty Fuel Weight (W1) (N)']**0.5 )**2 if v['SFC - Jet (Ct) (1/s)'] > 0 and v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['CL^0.5/CD Ratio'] > 0 else 0
    },
    {
        'output': 'Wing Area (m^2)',
        'name': 'From Breguet Range equation (Assuming Constant AoA)',
        'inputs': ['Range (m)', 'SFC - Jet (Ct) (1/s)', 'Air Density (kg/m^3)', 'CL^0.5/CD Ratio', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: 2 / v['Air Density (kg/m^3)'] * ( (v['Range (m)'] * v['SFC - Jet (Ct) (1/s)']) / (2 * v['CL^0.5/CD Ratio'] * (v['Gross Weight (W0) (N)']**0.5 - v['Empty Fuel Weight (W1) (N)']**0.5)) )**2 if v['Air Density (kg/m^3)'] > 0 and v['CL^0.5/CD Ratio'] != 0 and v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'CL^0.5/CD Ratio',
        'name': 'From Breguet Range equation (Assuming Constant AoA)',
        'inputs': ['Range (m)', 'SFC - Jet (Ct) (1/s)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['Range (m)'] * v['SFC - Jet (Ct) (1/s)']) / (2 * math.sqrt(2 / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'])) * (v['Gross Weight (W0) (N)']**0.5 - v['Empty Fuel Weight (W1) (N)']**0.5)) if v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'Empty Fuel Weight (W1) (N)',
        'name': 'From Breguet Range equation (Assuming Constant AoA)',
        'inputs': ['Range (m)', 'SFC - Jet (Ct) (1/s)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CL^0.5/CD Ratio', 'Gross Weight (W0) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['Gross Weight (W0) (N)']**0.5 - (v['Range (m)'] / ((2 / v['SFC - Jet (Ct) (1/s)']) * math.sqrt(2 / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'])) * v['CL^0.5/CD Ratio'])))**2 if v['SFC - Jet (Ct) (1/s)'] > 0 and v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['CL^0.5/CD Ratio'] > 0 else 0
    },
    # ============================
    # Range equation (prop) 
    # ============================
    {
        'output': 'Range (m)',
        'name': 'Breguet Range (Propeller)',
        'inputs': ['Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'L/D (Lift to Drag ratio)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (v['Propeller Efficiency'] / v['SFC - Prop (C) (N/W*s)']) * v['L/D (Lift to Drag ratio)'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)']) if v['SFC - Prop (C) (N/W*s)'] > 0 and v['Empty Fuel Weight (W1) (N)'] > 0 and v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'Propeller Efficiency',
        'name': 'From Breguet Range equation (Propeller)',
        'inputs': ['Range (m)', 'SFC - Prop (C) (N/W*s)', 'L/D (Lift to Drag ratio)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (v['Range (m)'] * v['SFC - Prop (C) (N/W*s)']) / (v['L/D (Lift to Drag ratio)'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)'])) if v['L/D (Lift to Drag ratio)'] != 0 and v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'SFC - Prop (C) (N/W*s)',
        'name': 'From Breguet Range equation (Propeller)',
        'inputs': ['Range (m)', 'Propeller Efficiency', 'L/D (Lift to Drag ratio)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (v['Propeller Efficiency'] * v['L/D (Lift to Drag ratio)'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)'])) / v['Range (m)'] if v['Range (m)'] != 0 else 0
    },
    {
        'output': 'L/D (Lift to Drag ratio)',
        'name': 'From Breguet Range equation (Propeller)',
        'inputs': ['Range (m)', 'Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (v['Range (m)'] * v['SFC - Prop (C) (N/W*s)']) / (v['Propeller Efficiency'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)'])) if v['Propeller Efficiency'] != 0 and v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'Gross Weight (W0) (N)',
        'name': 'From Breguet Range equation (Propeller)',
        'inputs': ['Range (m)', 'Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'L/D (Lift to Drag ratio)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: v['Empty Fuel Weight (W1) (N)'] * math.exp((v['Range (m)'] * v['SFC - Prop (C) (N/W*s)']) / (v['Propeller Efficiency'] * v['L/D (Lift to Drag ratio)'])) if v['Propeller Efficiency'] != 0 and v['L/D (Lift to Drag ratio)'] != 0 else 0
    },
    {
        'output': 'Empty Fuel Weight (W1) (N)',
        'name': 'From Breguet Range equation (Propeller)',
        'inputs': ['Range (m)', 'Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'L/D (Lift to Drag ratio)', 'Gross Weight (W0) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: v['Gross Weight (W0) (N)'] / math.exp((v['Range (m)'] * v['SFC - Prop (C) (N/W*s)']) / (v['Propeller Efficiency'] * v['L/D (Lift to Drag ratio)'])) if v['Propeller Efficiency'] != 0 and v['L/D (Lift to Drag ratio)'] != 0 else 0
    },

    # ======================
    # Endurance (Jet) 
    # ======================
    {
        'output': 'Endurance (s)',
        'name': 'Breguet Endurance (Jet)',
        'inputs': ['L/D (Lift to Drag ratio)', 'SFC - Jet (Ct) (1/s)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (1 / v['SFC - Jet (Ct) (1/s)']) * v['L/D (Lift to Drag ratio)'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)']) if v['SFC - Jet (Ct) (1/s)'] > 0 and v['Empty Fuel Weight (W1) (N)'] > 0 and v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'L/D (Lift to Drag ratio)',
        'name': 'From Breguet Endurance (Jet)',
        'inputs': ['Endurance (s)', 'SFC - Jet (Ct) (1/s)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['Endurance (s)'] * v['SFC - Jet (Ct) (1/s)']) / math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)']) if v['Gross Weight (W0) (N)'] > v['Empty Fuel Weight (W1) (N)'] else 0
    },
    {
        'output': 'SFC - Jet (Ct) (1/s)',
        'name': 'From Breguet Endurance (Jet)',
        'inputs': ['Endurance (s)', 'L/D (Lift to Drag ratio)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['L/D (Lift to Drag ratio)'] * math.log(v['Gross Weight (W0) (N)'] / v['Empty Fuel Weight (W1) (N)'])) / v['Endurance (s)'] if v['Endurance (s)'] > 0 else 0
    },
    {
        'output': 'Gross Weight (W0) (N)',
        'name': 'From Breguet Endurance (Jet)',
        'inputs': ['Endurance (s)', 'L/D (Lift to Drag ratio)', 'SFC - Jet (Ct) (1/s)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: v['Empty Fuel Weight (W1) (N)'] * math.exp((v['Endurance (s)'] * v['SFC - Jet (Ct) (1/s)']) / v['L/D (Lift to Drag ratio)']) if v['L/D (Lift to Drag ratio)'] != 0 else 0
    },
    {
        'output': 'Empty Fuel Weight (W1) (N)',
        'name': 'From Breguet Endurance (Jet)',
        'inputs': ['Endurance (s)', 'L/D (Lift to Drag ratio)', 'SFC - Jet (Ct) (1/s)', 'Gross Weight (W0) (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: v['Gross Weight (W0) (N)'] / math.exp((v['Endurance (s)'] * v['SFC - Jet (Ct) (1/s)']) / v['L/D (Lift to Drag ratio)']) if v['L/D (Lift to Drag ratio)'] != 0 else 0
    },
    # ======================================================
    # BREGUET ENDURANCE EQUATION (PROPELLER AIRCRAFT) 
    # ======================================================
    # This version assumes flight at a constant angle of attack and altitude.
    {
        'output': 'Endurance (s)',
        'name': 'Breguet Endurance (Propeller, Constant AoA)',
        'inputs': ['Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'Power Ratio (CL^3/2/CD)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (v['Propeller Efficiency'] / v['SFC - Prop (C) (N/W*s)']) * math.sqrt(2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)']) * v['Power Ratio (CL^3/2/CD)'] * (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5) if v['SFC - Prop (C) (N/W*s)'] > 0 else 0
    },
    {
        'output': 'Empty Fuel Weight (W1) (N)',
        'name': 'From Breguet Endurance (Propeller, Constant AoA)',
        'inputs': ['Endurance (s)', 'Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'Power Ratio (CL^3/2/CD)', 'Gross Weight (W0) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: ( v['Gross Weight (W0) (N)']**-0.5 + ( (v['Endurance (s)'] * v['SFC - Prop (C) (N/W*s)']) / (v['Propeller Efficiency'] * math.sqrt(2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)']) * v['Power Ratio (CL^3/2/CD)']) ) )**-2 if v['Propeller Efficiency'] > 0 and v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['Power Ratio (CL^3/2/CD)'] > 0 else 0
    },
    {
        'output': 'Gross Weight (W0) (N)',
        'name': 'From Breguet Endurance (Propeller, Constant AoA)',
        'inputs': ['Endurance (s)', 'Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'Power Ratio (CL^3/2/CD)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: ( v['Empty Fuel Weight (W1) (N)']**-0.5 - ( (v['Endurance (s)'] * v['SFC - Prop (C) (N/W*s)']) / (v['Propeller Efficiency'] * math.sqrt(2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)']) * v['Power Ratio (CL^3/2/CD)']) ) )**-2 if v['Propeller Efficiency'] > 0 and v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['Power Ratio (CL^3/2/CD)'] > 0 else 0
    },
    {
        'output': 'Propeller Efficiency',
        'name': 'From Breguet Endurance (Propeller, Constant AoA)',
        'inputs': ['Endurance (s)', 'SFC - Prop (C) (N/W*s)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'Power Ratio (CL^3/2/CD)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (v['Endurance (s)'] * v['SFC - Prop (C) (N/W*s)']) / (math.sqrt(2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)']) * v['Power Ratio (CL^3/2/CD)'] * (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5)) if v['Power Ratio (CL^3/2/CD)'] != 0 and (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5) != 0 else 0
    },
    {
        'output': 'SFC - Prop (C) (N/W*s)',
        'name': 'From Breguet Endurance (Propeller, Constant AoA)',
        'inputs': ['Endurance (s)', 'Propeller Efficiency', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'Power Ratio (CL^3/2/CD)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (v['Propeller Efficiency'] / v['Endurance (s)']) * math.sqrt(2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)']) * v['Power Ratio (CL^3/2/CD)'] * (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5) if v['Endurance (s)'] > 0 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'name': 'From Breguet Endurance (Propeller, Constant AoA)',
        'inputs': ['Endurance (s)', 'Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'Wing Area (m^2)', 'Power Ratio (CL^3/2/CD)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: 0.5 / v['Wing Area (m^2)'] * ( (v['Endurance (s)'] * v['SFC - Prop (C) (N/W*s)']) / (v['Propeller Efficiency'] * v['Power Ratio (CL^3/2/CD)'] * (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5)) )**2 if v['Wing Area (m^2)'] > 0 and v['Propeller Efficiency'] != 0 and v['Power Ratio (CL^3/2/CD)'] != 0 and (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5) != 0 else 0
    },
    {
        'output': 'Wing Area (m^2)',
        'name': 'From Breguet Endurance (Propeller, Constant AoA)',
        'inputs': ['Endurance (s)', 'Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'Air Density (kg/m^3)', 'Power Ratio (CL^3/2/CD)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: 0.5 / v['Air Density (kg/m^3)'] * ( (v['Endurance (s)'] * v['SFC - Prop (C) (N/W*s)']) / (v['Propeller Efficiency'] * v['Power Ratio (CL^3/2/CD)'] * (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5)) )**2 if v['Air Density (kg/m^3)'] > 0 and v['Propeller Efficiency'] != 0 and v['Power Ratio (CL^3/2/CD)'] != 0 and (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5) != 0 else 0
    },
    {
        'output': 'Power Ratio (CL^3/2/CD)',
        'name': 'From Breguet Endurance (Propeller, Constant AoA)',
        'inputs': ['Endurance (s)', 'Propeller Efficiency', 'SFC - Prop (C) (N/W*s)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'Gross Weight (W0) (N)', 'Empty Fuel Weight (W1) (N)'],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (v['Endurance (s)'] * v['SFC - Prop (C) (N/W*s)']) / (v['Propeller Efficiency'] * math.sqrt(2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)']) * (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5)) if v['Propeller Efficiency'] > 0 and v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and (v['Empty Fuel Weight (W1) (N)']**-0.5 - v['Gross Weight (W0) (N)']**-0.5) != 0 else 0
    },
    # ========================= 
    # Rate of climb family
    # =========================
    {
        'output': 'Rate of Climb (m/s)',
        'name': 'from Excess Power',
        'inputs': ['Excess Power (W)', 'Aircraft Weight (N)'],
        'calculate': lambda v: v['Excess Power (W)'] / v['Aircraft Weight (N)'] if v['Aircraft Weight (N)'] != 0 else 0
    },
    {
        'output': 'Excess Power (W)',
        'name': 'from Rate of Climb',
        'inputs': ['Rate of Climb (m/s)', 'Aircraft Weight (N)'],
        'calculate': lambda v: v['Rate of Climb (m/s)'] * v['Aircraft Weight (N)']
    },
    {
        'output': 'Aircraft Weight (N)',
        'name': 'from Rate of Climb',
        'inputs': ['Rate of Climb (m/s)', 'Excess Power (W)'],
        'calculate': lambda v: v['Excess Power (W)'] / v['Rate of Climb (m/s)'] if v['Rate of Climb (m/s)'] != 0 else 0
    },

    # ========================
    # EXCESS POWER FAMILY 
    # ========================
    {
        'output': 'Excess Power (W)',
        'name': 'From Power Available/Required',
        'inputs': ['Power Available (W)', 'Power Required (W)'],
        'calculate': lambda v: v['Power Available (W)'] - v['Power Required (W)']
    },
    {
        'output': 'Excess Power (W)',
        'name': 'From Thrust/Drag',
        'inputs': ['Thrust Available (N)', 'Drag', 'Velocity (m/s)'],
        'calculate': lambda v: (v['Thrust Available (N)'] - v['Drag']) * v['Velocity (m/s)']
    },
    # ===============================================
    # MAXIMUM CLIMB ANGLE FAMILY (JET AIRCRAFT) 
    # ================================================
    {
        'output': 'Maximum Climb Angle (radians)',
        'name': 'Max Climb Angle for a Jet',
        'inputs': ['Thrust Available (N)', 'Aircraft Weight (N)', 'Maximum L/D Ratio'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: math.asin((v['Thrust Available (N)'] / v['Aircraft Weight (N)']) - (1 / v['Maximum L/D Ratio'])) if v['Aircraft Weight (N)'] > 0 and v['Maximum L/D Ratio'] > 0 else 0
    },
    {
        'output': 'Thrust Available (N)',
        'name': 'From Max Climb Angle for a Jet',
        'inputs': ['Maximum Climb Angle (radians)', 'Aircraft Weight (N)', 'Maximum L/D Ratio'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: v['Aircraft Weight (N)'] * (math.sin(v['Maximum Climb Angle (radians)']) + (1 / v['Maximum L/D Ratio'])) if v['Maximum L/D Ratio'] != 0 else 0
    },
    {
        'output': 'Maximum L/D Ratio',
        'name': 'From Max Climb Angle for a Jet',
        'inputs': ['Maximum Climb Angle (radians)', 'Aircraft Weight (N)', 'Thrust Available (N)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: 1 / ((v['Thrust Available (N)'] / v['Aircraft Weight (N)']) - math.sin(v['Maximum Climb Angle (radians)'])) if (v['Thrust Available (N)'] / v['Aircraft Weight (N)']) - math.sin(v['Maximum Climb Angle (radians)']) != 0 else 0
    },
    # ====================================================
    # VELOCITY FOR MAX CLIMB ANGLE FAMILY (JET) 
    # ====================================================
    # This assumes thrust is approximately constant with velocity.
    {
        'output': 'Velocity at Max Climb Angle (m/s)',
        'inputs': ['Air Density (kg/m^3)', 'w/s (Wing Loading)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)', 'Maximum Climb Angle (radians)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: math.sqrt((2 / v['Air Density (kg/m^3)']) * (v['K (Induced drag factor)'] / v['CD0 (Zero-lift Drag Coefficient)'])**0.5 * v['w/s (Wing Loading)'] * math.cos(v['Maximum Climb Angle (radians)'])) if v['Air Density (kg/m^3)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'name': 'From velocity at max climb angle',
        'inputs': ['Velocity at Max Climb Angle (m/s)', 'w/s (Wing Loading)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)', 'Maximum Climb Angle (radians)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (2 / v['Velocity at Max Climb Angle (m/s)']**2) * (v['K (Induced drag factor)'] / v['CD0 (Zero-lift Drag Coefficient)'])**0.5 * v['w/s (Wing Loading)'] * math.cos(v['Maximum Climb Angle (radians)']) if v['Velocity at Max Climb Angle (m/s)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'w/s (Wing Loading)',
        'name': 'From velocity at max climb angle',
        'inputs': ['Velocity at Max Climb Angle (m/s)', 'Air Density (kg/m^3)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)', 'Maximum Climb Angle (radians)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['Velocity at Max Climb Angle (m/s)']**2 * v['Air Density (kg/m^3)']) / (2 * (v['K (Induced drag factor)'] / v['CD0 (Zero-lift Drag Coefficient)'])**0.5 * math.cos(v['Maximum Climb Angle (radians)'])) if v['K (Induced drag factor)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 and math.cos(v['Maximum Climb Angle (radians)']) != 0 else 0
    },
    # ================================
    # RATE OF CLIMB AT MAX ANGLE
    # ================================
    {
        'output': 'Rate of Climb at Max Climb Angle (m/s)',
        'name': 'From Velocity at max climb angle',
        'inputs': ['Velocity at Max Climb Angle (m/s)', 'Maximum Climb Angle (radians)'],
        'calculate': lambda v: v['Velocity at Max Climb Angle (m/s)'] * math.sin(v['Maximum Climb Angle (radians)'])
    },
    # ============================================
    # MAXIMUM RATE OF CLIMB (JET AIRCRAFT) 
    # ============================================
    {
        'output': 'Maximum Rate of Climb (m/s)',
        'name': 'Max Rate of Climb for a Jet',
        'inputs': [
            'w/s (Wing Loading)',
            'Air Density (kg/m^3)',
            'CD0 (Zero-lift Drag Coefficient)',
            'Thrust to Weight Ratio',
            'Maximum L/D Ratio'
        ],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (
            # This lambda function first calculates the helper variable Z, then uses it in the main expression.
            (lambda Z:
                ( (v['w/s (Wing Loading)'] * Z) / (3 * v['Air Density (kg/m^3)'] * v['CD0 (Zero-lift Drag Coefficient)']) )**0.5 *
                (v['Thrust to Weight Ratio'])**1.5 *
                (1 - (Z / 6) - (3 / (2 * v['Thrust to Weight Ratio']**2 * v['Maximum L/D Ratio']**2 * Z)))
            )(1 + math.sqrt(1 + 3 / (v['Maximum L/D Ratio']**2 * v['Thrust to Weight Ratio']**2)))
        ) if v['Air Density (kg/m^3)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 and v['Maximum L/D Ratio'] > 0 and v['Thrust to Weight Ratio'] > 0 else 0
    },
    # =========================================
    # VELOCITY FOR MAX RATE OF CLIMB (JET) 
    # =========================================
    {
        'output': 'Velocity at Max R/C (m/s)',
        'name': 'Velocity at max RC for a Jet',
        'inputs': [
            'Thrust to Weight Ratio',
            'w/s (Wing Loading)',
            'Air Density (kg/m^3)',
            'CD0 (Zero-lift Drag Coefficient)',
            'Maximum L/D Ratio'
        ],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (
            ( (v['Thrust to Weight Ratio'] * v['w/s (Wing Loading)']) / (3 * v['Air Density (kg/m^3)'] * v['CD0 (Zero-lift Drag Coefficient)']) ) *
            (1 + math.sqrt(1 + 3 / (v['Maximum L/D Ratio']**2 * v['Thrust to Weight Ratio']**2)))
        )**0.5 if v['Air Density (kg/m^3)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    # ====================================================
    # MAXIMUM RATE OF CLIMB & VELOCITY (PROPELLER) 
    # ====================================================
    {
        'output': 'Maximum Rate of Climb (m/s)',
        'name': 'Max R/C for a Propeller',
        'inputs': [
            'Propeller Efficiency',
            'Engine Shaft Power (W)',
            'Aircraft Weight (N)',
            'Air Density (kg/m^3)',
            'K (Induced drag factor)',
            'CD0 (Zero-lift Drag Coefficient)',
            'w/s (Wing Loading)',
            'Maximum L/D Ratio'
        ],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (
            (v['Propeller Efficiency'] * v['Engine Shaft Power (W)'] / v['Aircraft Weight (N)']) -
            (
                math.sqrt((2 / v['Air Density (kg/m^3)']) * math.sqrt(v['K (Induced drag factor)'] / (3 * v['CD0 (Zero-lift Drag Coefficient)'])) * v['w/s (Wing Loading)']) *
                (1.155 / v['Maximum L/D Ratio'])
            )
        ) if v['Aircraft Weight (N)'] > 0 and v['Maximum L/D Ratio'] > 0 else 0
    },
    {
        'output': 'Velocity at Max R/C (m/s)',
        'name': 'Velocity at max RC for a Propeller',
        'inputs': [
            'Air Density (kg/m^3)',
            'K (Induced drag factor)',
            'CD0 (Zero-lift Drag Coefficient)',
            'w/s (Wing Loading)'
        ],
        'conditions': ['Propeller-driven'],
        'calculate': lambda v: (
            (2 / v['Air Density (kg/m^3)']) * math.sqrt(v['K (Induced drag factor)'] / (3 * v['CD0 (Zero-lift Drag Coefficient)'])) * v['w/s (Wing Loading)']
        )**0.5 if v['Air Density (kg/m^3)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    # ==============================
    # LEVEL TURN PERFORMANCE 
    # ==============================
    {
        'output': 'Turn Radius (R) (m)',
        'name': 'Level Turn Radius',
        'inputs': ['Velocity (m/s)', 'Load Factor (n)'],
        'calculate': lambda v: (v['Velocity (m/s)']**2) / (G * math.sqrt(v['Load Factor (n)']**2 - 1)) if v['Load Factor (n)'] > 1 else 0
    },
    {
        'output': 'Velocity (m/s)',
        'name': 'From Level Turn Radius',
        'inputs': ['Turn Radius (R) (m)', 'Load Factor (n)'],
        'calculate': lambda v: math.sqrt(v['Turn Radius (R) (m)'] * G * math.sqrt(v['Load Factor (n)']**2 - 1)) if v['Load Factor (n)'] > 1 else 0
    },
    {
        'output': 'Load Factor (n)',
        'name': 'From Level Turn Radius',
        'inputs': ['Turn Radius (R) (m)', 'Velocity (m/s)'],
        'calculate': lambda v: math.sqrt( ((v['Velocity (m/s)']**2) / (v['Turn Radius (R) (m)'] * G))**2 + 1 ) if v['Turn Radius (R) (m)'] > 0 and G > 0 else 0
    },
    # =============================
    # LEVEL TURN PERFORMANCE 
    # =============================
    {
        'output': 'Turn Rate (rad/s)',
        'name': 'Level Turn Rate',
        'inputs': ['Load Factor (n)', 'Velocity (m/s)'],
        'calculate': lambda v: (G * math.sqrt(v['Load Factor (n)']**2 - 1)) / v['Velocity (m/s)'] if v['Velocity (m/s)'] > 0 else 0
    },
    {
        'output': 'Load Factor (n)',
        'name': 'Load Factor from Level Turn Rate',
        'inputs': ['Turn Rate (rad/s)', 'Velocity (m/s)'],
        'calculate': lambda v: math.sqrt( ((v['Turn Rate (rad/s)'] * v['Velocity (m/s)']) / G)**2 + 1 )
    },
    {
        'output': 'Velocity (m/s)',
        'name': 'Velocity from Level Turn Rate',
        'inputs': ['Turn Rate (rad/s)', 'Load Factor (n)'],
        'calculate': lambda v: (G * math.sqrt(v['Load Factor (n)']**2 - 1)) / v['Turn Rate (rad/s)'] if v['Turn Rate (rad/s)'] != 0 and v['Load Factor (n)'] > 1 else 0
    },
     # =========================================
     # MANEUVERING PERFORMANCE FAMILY 
     # =========================================
    {
        'output': 'Maximum Load Factor (n_max)',
        'name': 'From performance limits',
        'inputs': [
            'Air Density (kg/m^3)',
            'Velocity (m/s)',
            'K (Induced drag factor)',
            'w/s (Wing Loading)',
            'Maximum Thrust to Weight Ratio', 
            'CD0 (Zero-lift Drag Coefficient)'
        ],
        'conditions': ['Steady level flight'],
        'calculate': lambda v: (
            ( (0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2) / (v['K (Induced drag factor)'] * v['w/s (Wing Loading)']) ) *
            ( v['Maximum Thrust to Weight Ratio'] - (0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2 * v['CD0 (Zero-lift Drag Coefficient)'] / v['w/s (Wing Loading)']) )
        )**0.5 if v['K (Induced drag factor)'] > 0 and v['w/s (Wing Loading)'] > 0 else 0
    },
    {
        'output': 'Maximum Load Factor (n_max)',
        'name': 'From aerodynamic limits',
        'inputs': ['Dynamic Pressure (Pa)', 'Wing Area (m^2)', 'CLmax', 'Aircraft Weight (N)'],
        'calculate': lambda v: (v['Dynamic Pressure (Pa)'] * v['Wing Area (m^2)'] * v['CLmax']) / v['Aircraft Weight (N)'] if v['Aircraft Weight (N)'] > 0 else 0
    },
    {
        'output': 'Maximum Bank Angle (rad)',
        'name': 'From n_max',
        'inputs': ['Maximum Load Factor (n_max)'],
        'calculate': lambda v: math.acos(1 / v['Maximum Load Factor (n_max)']) if v['Maximum Load Factor (n_max)'] >= 1 else 0
    },
    {
        'output': 'Maximum Load Factor (n_max)',
        'name': 'From Max Bank Angle',
        'inputs': ['Maximum Bank Angle (rad)'],
        'calculate': lambda v: 1 / math.cos(v['Maximum Bank Angle (rad)']) if math.cos(v['Maximum Bank Angle (rad)']) != 0 else 0
    },
    # ========================
    # STALL SPEED FAMILY 
    # ========================
    {
        'output': 'Stall Velocity (m/s)',
        'name': 'Stall Speed Calculation',
        'inputs': ['Aircraft Weight (N)', 'Load Factor (n)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CLmax'],
        'calculate': lambda v: math.sqrt((2 * v['Aircraft Weight (N)'] * v['Load Factor (n)']) / (v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CLmax'])) if v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 and v['CLmax'] > 0 else 0
    },
    {
        'output': 'Aircraft Weight (N)',
        'name': 'From Stall Speed',
        'inputs': ['Stall Velocity (m/s)', 'Load Factor (n)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CLmax'],
        'calculate': lambda v: (v['Stall Velocity (m/s)']**2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CLmax']) / (2 * v['Load Factor (n)']) if v['Load Factor (n)'] != 0 else 0
    },
    {
        'output': 'Load Factor (n)',
        'name': 'From Stall Speed',
        'inputs': ['Stall Velocity (m/s)', 'Aircraft Weight (N)', 'Air Density (kg/m^3)', 'Wing Area (m^2)', 'CLmax'],
        'calculate': lambda v: (v['Stall Velocity (m/s)']**2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CLmax']) / (2 * v['Aircraft Weight (N)']) if v['Aircraft Weight (N)'] != 0 else 0
    },
    {
        'output': 'CLmax',
        'name': 'From Stall Speed',
        'inputs': ['Stall Velocity (m/s)', 'Aircraft Weight (N)', 'Load Factor (n)', 'Air Density (kg/m^3)', 'Wing Area (m^2)'],
        'calculate': lambda v: (2 * v['Aircraft Weight (N)'] * v['Load Factor (n)']) / (v['Stall Velocity (m/s)']**2 * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)']) if v['Stall Velocity (m/s)'] > 0 and v['Air Density (kg/m^3)'] > 0 and v['Wing Area (m^2)'] > 0 else 0
    },
    # =============================================
    # Minimum Sustained Turn Radius FAMILY 
    # =============================================
    {
        'output': 'Minimum Sustained Turn Radius (m)',
        'inputs': ['K (Induced drag factor)', 'w/s (Wing Loading)', 'Air Density (kg/m^3)', 'Thrust to Weight Ratio', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: (4 * v['K (Induced drag factor)'] * v['w/s (Wing Loading)']) / (G * v['Air Density (kg/m^3)'] * v['Thrust to Weight Ratio'] * math.sqrt(1 - ( (4 * v['K (Induced drag factor)'] * v['CD0 (Zero-lift Drag Coefficient)']) / v['Thrust to Weight Ratio']**2 ))) if v['Air Density (kg/m^3)'] > 0 and v['Thrust to Weight Ratio'] > 0 and (1 - ( (4 * v['K (Induced drag factor)'] * v['CD0 (Zero-lift Drag Coefficient)']) / v['Thrust to Weight Ratio']**2 )) > 0 else 0
    },
    {
        'output': 'Velocity at Min Turn Radius (m/s)',
        'name': 'At Minimum Sustained Turn Radius',
        'inputs': ['K (Induced drag factor)', 'w/s (Wing Loading)', 'Air Density (kg/m^3)', 'Thrust to Weight Ratio'],
        'calculate': lambda v: math.sqrt((4 * v['K (Induced drag factor)'] * v['w/s (Wing Loading)']) / (v['Air Density (kg/m^3)'] * v['Thrust to Weight Ratio'])) if v['Air Density (kg/m^3)'] > 0 and v['Thrust to Weight Ratio'] > 0 else 0
    },
    {
        'output': 'Load Factor at Min Turn Radius',
        'name': 'At Minimum Sustained Turn Radius',
        'inputs': ['K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)', 'Thrust to Weight Ratio'],
        'calculate': lambda v: math.sqrt(2 - ( (4 * v['K (Induced drag factor)'] * v['CD0 (Zero-lift Drag Coefficient)']) / v['Thrust to Weight Ratio']**2 )) if v['Thrust to Weight Ratio'] > 0 else 0
    },
    {
        'output': 'w/s (Wing Loading)',
        'name': 'From Min Turn Radius',
        'inputs': ['Velocity at Min Turn Radius (m/s)', 'Air Density (kg/m^3)', 'K (Induced drag factor)', 'Thrust to Weight Ratio'],
        'calculate': lambda v: (v['Velocity at Min Turn Radius (m/s)']**2 * v['Air Density (kg/m^3)'] * v['Thrust to Weight Ratio']) / (4 * v['K (Induced drag factor)']) if v['K (Induced drag factor)'] != 0 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'name': 'From Min Turn Radius',
        'inputs': ['Velocity at Min Turn Radius (m/s)', 'w/s (Wing Loading)', 'K (Induced drag factor)', 'Thrust to Weight Ratio'],
        'calculate': lambda v: (4 * v['K (Induced drag factor)'] * v['w/s (Wing Loading)']) / (v['Velocity at Min Turn Radius (m/s)']**2 * v['Thrust to Weight Ratio']) if v['Velocity at Min Turn Radius (m/s)'] > 0 and v['Thrust to Weight Ratio'] > 0 else 0
    },
    {
        'output': 'Thrust to Weight Ratio',
        'name': 'From Min Turn Radius',
        'inputs': ['Load Factor at Min Turn Radius', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: math.sqrt((4 * v['K (Induced drag factor)'] * v['CD0 (Zero-lift Drag Coefficient)']) / (2 - v['Load Factor at Min Turn Radius']**2)) if (2 - v['Load Factor at Min Turn Radius']**2) != 0 else 0
    },
    {
        'output': 'K (Induced drag factor)',
        'name': 'From Min Turn Radius',
        'inputs': ['Velocity at Min Turn Radius (m/s)', 'Air Density (kg/m^3)', 'w/s (Wing Loading)', 'Thrust to Weight Ratio'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['Velocity at Min Turn Radius (m/s)']**2 * v['Air Density (kg/m^3)'] * v['Thrust to Weight Ratio']) / (4 * v['w/s (Wing Loading)']) if v['w/s (Wing Loading)'] != 0 else 0
    },
    {
        'output': 'CD0 (Zero-lift Drag Coefficient)',
        'name': 'From Min Turn Radius',
        'inputs': ['Load Factor at Min Turn Radius', 'K (Induced drag factor)', 'Thrust to Weight Ratio'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: ((2 - v['Load Factor at Min Turn Radius']**2) * v['Thrust to Weight Ratio']**2) / (4 * v['K (Induced drag factor)']) if v['K (Induced drag factor)'] != 0 else 0
    },
    # ==================================================
    # Maximum Sustained Turn Rate FAMILY 
    # ==================================================
    {
        'output': 'Maximum Sustained Turn Rate (rad/s)',
        'inputs': ['Air Density (kg/m^3)', 'w/s (Wing Loading)', 'Thrust to Weight Ratio', 'CD0 (Zero-lift Drag Coefficient)', 'K (Induced drag factor)'],
        'calculate': lambda v: G * math.sqrt((v['Air Density (kg/m^3)'] / v['w/s (Wing Loading)']) * ( (v['Thrust to Weight Ratio'] / (2 * v['K (Induced drag factor)'])) - (v['CD0 (Zero-lift Drag Coefficient)'] / v['K (Induced drag factor)'])**0.5 )) if v['w/s (Wing Loading)'] > 0 and v['K (Induced drag factor)'] > 0 else 0
    },
    {
        'output': 'Velocity at Max Turn Rate (m/s)',
        'name': 'At Max Turn Rate',
        'inputs': ['w/s (Wing Loading)', 'Air Density (kg/m^3)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: ((2 * v['w/s (Wing Loading)'] / v['Air Density (kg/m^3)']) * (v['K (Induced drag factor)'] / v['CD0 (Zero-lift Drag Coefficient)'])**0.25)**0.5 if v['Air Density (kg/m^3)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'Load Factor at Max Turn Rate',
        'name': 'At Max Turn Rate',
        'inputs': ['Thrust to Weight Ratio', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: ((v['Thrust to Weight Ratio'] / math.sqrt(v['K (Induced drag factor)'] * v['CD0 (Zero-lift Drag Coefficient)'])) - 1)**0.5 if v['K (Induced drag factor)'] > 0 and v['CD0 (Zero-lift Drag Coefficient)'] > 0 else 0
    },
    {
        'output': 'Thrust to Weight Ratio',
        'name': 'From Max Turn Rate',
        'inputs': ['Maximum Sustained Turn Rate (rad/s)', 'Air Density (kg/m^3)', 'w/s (Wing Loading)', 'K (Induced drag factor)', 'CD0 (Zero-lift Drag Coefficient)'],
        'calculate': lambda v: (2 * v['K (Induced drag factor)']) * ( (v['Maximum Sustained Turn Rate (rad/s)'] / G)**2 * (v['w/s (Wing Loading)'] / v['Air Density (kg/m^3)']) + (v['CD0 (Zero-lift Drag Coefficient)'] / v['K (Induced drag factor)'])**0.5 ) if v['Air Density (kg/m^3)'] > 0 else 0
    },
    {
        'output': 'Air Density (kg/m^3)',
        'name': 'From Max Turn Rate',
        'inputs': ['Maximum Sustained Turn Rate (rad/s)', 'w/s (Wing Loading)', 'K (Induced drag factor)', 'Thrust to Weight Ratio', 'CD0 (Zero-lift Drag Coefficient)'],
        'conditions': ['Jet-propelled'],
        'calculate': lambda v: (v['w/s (Wing Loading)'] * ( (v['Maximum Sustained Turn Rate (rad/s)'] / G)**2 / ( (v['Thrust to Weight Ratio'] / (2*v['K (Induced drag factor)'])) - (v['CD0 (Zero-lift Drag Coefficient)']/v['K (Induced drag factor)'])**0.5 ) )) if v['K (Induced drag factor)'] > 0 else 0
    },
    # ============================================
    # PULL-UP/PULL-DOWN MANEUVER FAMILY 
    # ============================================
    {
        'output': 'Pull-up Turn Radius (m)',
        'name': 'Pull-up Maneuver Turn Radius',
        'inputs': ['Velocity (m/s)', 'Load Factor (n)'],
        'calculate': lambda v: (v['Velocity (m/s)']**2) / (G * (v['Load Factor (n)'] - 1)) if (v['Load Factor (n)'] - 1) > 0 and G > 0 else 0
    },
    {
        'output': 'Velocity (m/s)',
        'name': 'From Pull-up Turn Radius',
        'inputs': ['Pull-up Turn Radius (m)', 'Load Factor (n)'],
        'calculate': lambda v: math.sqrt(v['Pull-up Turn Radius (m)'] * G * (v['Load Factor (n)'] - 1)) if (v['Load Factor (n)'] - 1) > 0 else 0
    },
    {
        'output': 'Load Factor (n)',
        'name': 'From Pull-up Turn Radius',
        'inputs': ['Pull-up Turn Radius (m)', 'Velocity (m/s)'],
        'calculate': lambda v: ((v['Velocity (m/s)']**2) / (v['Pull-up Turn Radius (m)'] * G)) + 1 if v['Pull-up Turn Radius (m)'] > 0 and G > 0 else 0
    },
    {
        'output': 'Pull-up Turn Rate (rad/s)',
        'name': 'Pull-up Maneuver Turn Rate',
        'inputs': ['Load Factor (n)', 'Velocity (m/s)'],
        'calculate': lambda v: (G * (v['Load Factor (n)'] - 1)) / v['Velocity (m/s)'] if v['Velocity (m/s)'] > 0 else 0
    },
    {
        'output': 'Load Factor (n)',
        'name': 'From Pull-up Turn Rate',
        'inputs': ['Pull-up Turn Rate (rad/s)', 'Velocity (m/s)'],
        'calculate': lambda v: ((v['Pull-up Turn Rate (rad/s)'] * v['Velocity (m/s)']) / G) + 1
    },
    {
        'output': 'Velocity (m/s)',
        'name': 'From Pull-up Turn Rate',
        'inputs': ['Pull-up Turn Rate (rad/s)', 'Load Factor (n)'],
        'calculate': lambda v: (G * (v['Load Factor (n)'] - 1)) / v['Pull-up Turn Rate (rad/s)'] if v['Pull-up Turn Rate (rad/s)'] > 0 else 0
    },
    {
        'output': 'Pull-down Turn Radius (m)',
        'name': 'Pull-down Maneuver Turn Radius',
        'inputs': ['Velocity (m/s)', 'Load Factor (n)'],
        'calculate': lambda v: (v['Velocity (m/s)']**2) / (G * (v['Load Factor (n)'] + 1)) if G > 0 else 0
    },
    {
        'output': 'Velocity (m/s)',
        'name': 'From Pull-down Turn Radius',
        'inputs': ['Pull-down Turn Radius (m)', 'Load Factor (n)'],
        'calculate': lambda v: math.sqrt(v['Pull-down Turn Radius (m)'] * G * (v['Load Factor (n)'] + 1))
    },
    {
        'output': 'Load Factor (n)',
        'name': 'From Pull-down Turn Radius',
        'inputs': ['Pull-down Turn Radius (m)', 'Velocity (m/s)'],
        'calculate': lambda v: ((v['Velocity (m/s)']**2) / (v['Pull-down Turn Radius (m)'] * G)) - 1 if v['Pull-down Turn Radius (m)'] > 0 and G > 0 else 0
    },
    {
        'output': 'Pull-down Turn Rate (rad/s)',
        'name': 'Pull-down Maneuver Turn Rate',
        'inputs': ['Load Factor (n)', 'Velocity (m/s)'],
        'calculate': lambda v: (G * (v['Load Factor (n)'] + 1)) / v['Velocity (m/s)'] if v['Velocity (m/s)'] > 0 else 0
    },
    {
        'output': 'Load Factor (n)',
        'name': 'From Pull-down Turn Rate',
        'inputs': ['Pull-down Turn Rate (rad/s)', 'Velocity (m/s)'],
        'calculate': lambda v: ((v['Pull-down Turn Rate (rad/s)'] * v['Velocity (m/s)']) / G) - 1
    },
    {
        'output': 'Velocity (m/s)',
        'name': 'From Pull-down Turn Rate',
        'inputs': ['Pull-down Turn Rate (rad/s)', 'Load Factor (n)'],
        'calculate': lambda v: (G * (v['Load Factor (n)'] + 1)) / v['Pull-down Turn Rate (rad/s)'] if v['Pull-down Turn Rate (rad/s)'] > 0 else 0
    },
    # =================================================
    # MAXIMUM INSTANTANEOUS TURN PERFORMANCE 
    # =================================================
    {
        'output': 'Minimum Instantaneous Turn Radius (m)',
        'name': 'Aerodynamically-Limited Turn Radius',
        'inputs': ['w/s (Wing Loading)', 'Air Density (kg/m^3)', 'CLmax'],
        'calculate': lambda v: (2 * v['w/s (Wing Loading)']) / (G * v['Air Density (kg/m^3)'] * v['CLmax']) if v['Air Density (kg/m^3)'] > 0 and v['CLmax'] > 0 and G > 0 else 0
    },
    {
        'output': 'CLmax',
        'name': 'From min Instantaneous Turn Radius',
        'inputs': ['Minimum Instantaneous Turn Radius (m)', 'w/s (Wing Loading)', 'Air Density (kg/m^3)'],
        'calculate': lambda v: (2 * v['w/s (Wing Loading)']) / (G * v['Air Density (kg/m^3)'] * v['Minimum Instantaneous Turn Radius (m)']) if v['Air Density (kg/m^3)'] > 0 and v['Minimum Instantaneous Turn Radius (m)'] > 0 and G > 0 else 0
    },
    {
        'output': 'w/s (Wing Loading)',
        'name': 'From min Instantaneous Turn Radius',
        'inputs': ['Minimum Instantaneous Turn Radius (m)', 'Air Density (kg/m^3)', 'CLmax'],
        'calculate': lambda v: (v['Minimum Instantaneous Turn Radius (m)'] * G * v['Air Density (kg/m^3)'] * v['CLmax']) / 2
    },
    {
        'output': 'Maximum Instantaneous Turn Rate (rad/s)',
        'name': 'Structurally-Limited Turn Rate',
        'inputs': ['Maximum Load Factor (n_max)', 'w/s (Wing Loading)', 'Air Density (kg/m^3)', 'CLmax'],
        'calculate': lambda v: G * math.sqrt((v['Maximum Load Factor (n_max)'] * v['Air Density (kg/m^3)'] * v['CLmax']) / (2 * v['w/s (Wing Loading)'])) if v['w/s (Wing Loading)'] > 0 else 0
    },
    {
        'output': 'Maximum Load Factor (n_max)',
        'name': 'From max Instantaneous Turn Rate',
        'inputs': ['Maximum Instantaneous Turn Rate (rad/s)', 'w/s (Wing Loading)', 'Air Density (kg/m^3)', 'CLmax'],
        'calculate': lambda v: ( (v['Maximum Instantaneous Turn Rate (rad/s)'] / G)**2 * (2 * v['w/s (Wing Loading)']) ) / (v['Air Density (kg/m^3)'] * v['CLmax']) if v['Air Density (kg/m^3)'] > 0 and v['CLmax'] > 0 else 0
    },
    {
        'output': 'CLmax',
        'name': 'From max Instantaneous Turn Rate',
        'inputs': ['Maximum Instantaneous Turn Rate (rad/s)', 'w/s (Wing Loading)', 'Air Density (kg/m^3)', 'Maximum Load Factor (n_max)'],
        'calculate': lambda v: ( (v['Maximum Instantaneous Turn Rate (rad/s)'] / G)**2 * (2 * v['w/s (Wing Loading)']) ) / (v['Air Density (kg/m^3)'] * v['Maximum Load Factor (n_max)']) if v['Air Density (kg/m^3)'] > 0 and v['Maximum Load Factor (n_max)'] > 0 else 0
    },
    # =============================
    # CORNER VELOCITY FAMILY 
    # =============================
    {
        'output': 'Corner Velocity (m/s)',
        'name': 'Corner Velocity from n_max and CL_max',
        'inputs': ['Maximum Load Factor (n_max)', 'w/s (Wing Loading)', 'Air Density (kg/m^3)', 'CLmax'],
        'calculate': lambda v: math.sqrt((2 * v['Maximum Load Factor (n_max)'] * v['w/s (Wing Loading)']) / (v['Air Density (kg/m^3)'] * v['CLmax'])) if v['Air Density (kg/m^3)'] > 0 and v['CLmax'] > 0 else 0
    },
    {
        'output': 'CLmax',
        'name': 'From Corner Velocity',
        'inputs': ['Corner Velocity (m/s)', 'Maximum Load Factor (n_max)', 'w/s (Wing Loading)', 'Air Density (kg/m^3)'],
        'calculate': lambda v: (2 * v['Maximum Load Factor (n_max)'] * v['w/s (Wing Loading)']) / (v['Air Density (kg/m^3)'] * v['Corner Velocity (m/s)']**2) if v['Air Density (kg/m^3)'] > 0 and v['Corner Velocity (m/s)'] > 0 else 0
    },
    {
        'output': 'Maximum Load Factor (n_max)',
        'name': 'From Corner Velocity',
        'inputs': ['Corner Velocity (m/s)', 'w/s (Wing Loading)', 'Air Density (kg/m^3)', 'CLmax'],
        'calculate': lambda v: (v['Corner Velocity (m/s)']**2 * v['Air Density (kg/m^3)'] * v['CLmax']) / (2 * v['w/s (Wing Loading)']) if v['w/s (Wing Loading)'] > 0 else 0
    },
    # =============================
    # GROUND EFFECT FAMILY 
    # =============================
    {
        'output': 'Ground Effect Factor (phi)',
        'name': 'Ground effect factor calculation',
        'inputs': ['Height of wing above ground (h)', 'b (Wing Span)'],
        'calculate': lambda v: (16 * v['Height of wing above ground (h)'] / v['b (Wing Span)'])**2 / (1 + (16 * v['Height of wing above ground (h)'] / v['b (Wing Span)'])**2) if v['b (Wing Span)'] > 0 else 0
    },
    {
        'output': 'Drag During Ground Roll (N)',
        'name': 'Accounting for ground effect',
        'inputs': ['Air Density (kg/m^3)', 'Velocity (m/s)', 'Wing Area (m^2)', 'CD0 (Zero-lift Drag Coefficient)', 'Ground Effect Factor (phi)', 'CL (Lift Coefficient)', 'Oswald Efficiency (e)', 'Aspect Ratio (AR)'],
        'calculate': lambda v: 0.5 * v['Air Density (kg/m^3)'] * v['Velocity (m/s)']**2 * v['Wing Area (m^2)'] * (v['CD0 (Zero-lift Drag Coefficient)'] + v['Ground Effect Factor (phi)'] * (v['CL (Lift Coefficient)']**2 / (math.pi * v['Oswald Efficiency (e)'] * v['Aspect Ratio (AR)'])))
    },
    # ===================================
    # TAKEOFF PERFORMANCE FAMILY 
    # ===================================
    {
        'output': 'Ground Roll Distance (m)',
        'name': 'Takeoff Ground Roll (sg)',
        'inputs': [
            'Aircraft Weight (N)',
            'Air Density (kg/m^3)',
            'Wing Area (m^2)',
            'CLmax',
            'Thrust',
            'Drag During Ground Roll (N)',
            'Rolling Resistance Coefficient',
            'Lift' 
        ],
        'calculate': lambda v: (1.44 * v['Aircraft Weight (N)']**2) / (
            G * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CLmax'] * (v['Thrust'] - (v['Drag During Ground Roll (N)'] + v['Rolling Resistance Coefficient'] * (v['Aircraft Weight (N)'] - v['Lift'])))
        ) if (G * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CLmax'] * (v['Thrust'] - (v['Drag During Ground Roll (N)'] + v['Rolling Resistance Coefficient'] * (v['Aircraft Weight (N)'] - v['Lift'])))) != 0 else 0
    },
    {
        'output': 'Thrust',
        'name': 'From Takeoff Ground Roll',
        'inputs': [
            'Ground Roll Distance (m)',
            'Aircraft Weight (N)',
            'Air Density (kg/m^3)',
            'Wing Area (m^2)',
            'CLmax',
            'Drag During Ground Roll (N)',
            'Rolling Resistance Coefficient',
            'Lift' 
        ],
        'calculate': lambda v: (
            (1.44 * v['Aircraft Weight (N)']**2) / (v['Ground Roll Distance (m)'] * G * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CLmax']) +
            v['Drag During Ground Roll (N)'] + 
            v['Rolling Resistance Coefficient'] * (v['Aircraft Weight (N)'] - v['Lift'])
        ) if (v['Ground Roll Distance (m)'] * G * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CLmax']) != 0 else 0
    },
    # ============================================
    # AIRBORNE DISTANCE (TAKEOFF)
    # ============================================
    {
        'output': 'Airborne Distance (sa)',
        'name': 'Airborne distance to clear obstacle',
        'inputs': ['Turn Radius (R) (m)', 'Obstacle Angle (θob)'],
        'calculate': lambda v: v['Turn Radius (R) (m)'] * math.sin(v['Obstacle Angle (θob)'])
    },
    {
        'output': 'Obstacle Angle (θob)',
        'name': 'From Airborne Distance',
        'inputs': ['Airborne Distance (sa)', 'Turn Radius (R) (m)'],
        'calculate': lambda v: math.asin(v['Airborne Distance (sa)'] / v['Turn Radius (R) (m)']) if v['Turn Radius (R) (m)'] != 0 and -1 <= v['Airborne Distance (sa)'] / v['Turn Radius (R) (m)'] <= 1 else 0
    },
    {
        'output': 'Turn Radius (R) (m)',
        'name': 'From Airborne Distance',
        'inputs': ['Airborne Distance (sa)', 'Obstacle Angle (θob)'],
        'calculate': lambda v: v['Airborne Distance (sa)'] / math.sin(v['Obstacle Angle (θob)']) if math.sin(v['Obstacle Angle (θob)']) != 0 else 0
    },
    {
        'output': 'Obstacle Angle (θob)',
        'name': 'Obstacle angle from heights',
        'inputs': ['Obstacle Height (hob)', 'Turn Radius (R) (m)'],
        'calculate': lambda v: math.acos(1 - (v['Obstacle Height (hob)'] / v['Turn Radius (R) (m)'])) if v['Turn Radius (R) (m)'] != 0 and -1 <= (1 - (v['Obstacle Height (hob)'] / v['Turn Radius (R) (m)'])) <= 1 else 0
    },
    # ====================
    # TOTAL TAKEOFF 
    # ====================
    {
        'output': 'Total Takeoff Distance (m)',
        'name': 'Total Takeoff Distance (sg + sa)',
        'inputs': ['Ground Roll Distance (m)', 'Airborne Distance (sa)'],
        'calculate': lambda v: v['Ground Roll Distance (m)'] + v['Airborne Distance (sa)']
    },
    {
        'output': 'Ground Roll Distance (m)',
        'name': 'From Total Takeoff Distance - airborne distance',
        'inputs': ['Total Takeoff Distance (m)', 'Airborne Distance (sa)'],
        'calculate': lambda v: v['Total Takeoff Distance (m)'] - v['Airborne Distance (sa)']
    },
    {
        'output': 'Airborne Distance (sa)',
        'name': 'From Total Takeoff Distance - ground roll distance',
        'inputs': ['Total Takeoff Distance (m)', 'Ground Roll Distance (m)'],
        'calculate': lambda v: v['Total Takeoff Distance (m)'] - v['Ground Roll Distance (m)']
    },
    # ====================================
    # LANDING PERFORMANCE: APPROACH 
    # ====================================
    {
        'output': 'Approach Angle (θa)',
        'name': 'Approach Angle from forces',
        'inputs': ['Drag', 'Thrust', 'Aircraft Weight (N)'],
        'calculate': lambda v: math.asin((v['Drag'] - v['Thrust']) / v['Aircraft Weight (N)']) if v['Aircraft Weight (N)'] > 0 and -1 <= ((v['Drag'] - v['Thrust']) / v['Aircraft Weight (N)']) <= 1 else 0
    },
    {
        'output': 'Approach Angle (θa)',
        'name': 'Simplified Approach Angle (L=W)',
        'inputs': ['L/D (Lift to Drag ratio)', 'Thrust to Weight Ratio'],
        'calculate': lambda v: math.asin((1 / v['L/D (Lift to Drag ratio)']) - v['Thrust to Weight Ratio']) if v['L/D (Lift to Drag ratio)'] != 0 and -1 <= ((1 / v['L/D (Lift to Drag ratio)']) - v['Thrust to Weight Ratio']) <= 1 else 0
    },
    {
        'output': 'Approach Distance (sa_landing)',
        'name': 'Approach distance from flare height',
        'inputs': ['Obstacle Height (hob)', 'Flare Height (hf)', 'Approach Angle (θa)'],
        'calculate': lambda v: (v['Obstacle Height (hob)'] - v['Flare Height (hf)']) / math.tan(v['Approach Angle (θa)']) if math.tan(v['Approach Angle (θa)']) != 0 else 0
    },
    {
        'output': 'Flare Height (hf)',
        'name': 'Inverse Approach Distance',
        'inputs': ['Obstacle Height (hob)', 'Approach Distance (sa_landing)', 'Approach Angle (θa)'],
        'calculate': lambda v: v['Obstacle Height (hob)'] - (v['Approach Distance (sa_landing)'] * math.tan(v['Approach Angle (θa)']))
    },
    # ==============================================
    # LANDING PERFORMANCE: FLARE & GROUND ROLL 
    # ==============================================
    {
        'output': 'Flare Height (hf)',
        'name': 'Flare height from radius and angle',
        'inputs': ['Flare Radius (R_flare)', 'Approach Angle (θa)'],
        'calculate': lambda v: v['Flare Radius (R_flare)'] * (1 - math.cos(v['Approach Angle (θa)']))
    },
    {
        'output': 'Flare Radius (R_flare)',
        'name': 'From Flare Height',
        'inputs': ['Flare Height (hf)', 'Approach Angle (θa)'],
        'calculate': lambda v: v['Flare Height (hf)'] / (1 - math.cos(v['Approach Angle (θa)'])) if (1 - math.cos(v['Approach Angle (θa)'])) != 0 else 0
    },
    {
        'output': 'Flare Distance (s_flare)',
        'name': 'From radius and angle',
        'inputs': ['Flare Radius (R_flare)', 'Approach Angle (θa)'],
        'calculate': lambda v: v['Flare Radius (R_flare)'] * math.sin(v['Approach Angle (θa)'])
    },
    {
        'output': 'Landing Ground Roll (s_g,l)',
        'name': 'Landing Ground Roll',
        'inputs': [
            'Aircraft Weight (N)',
            'Air Density (kg/m^3)',
            'Wing Area (m^2)',
            'CLmax',
            'Thrust Reverser Force (T_rev)',
            'Average Drag over Ground Roll (N)',
            'Rolling Resistance Coefficient',
            'Average Lift over Ground Roll (N)'
        ],
        'calculate': lambda v: (1.69 * v['Aircraft Weight (N)']**2) / (
            G * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CLmax'] * (v['Thrust Reverser Force (T_rev)'] + v['Average Drag over Ground Roll (N)'] + v['Rolling Resistance Coefficient'] * (v['Aircraft Weight (N)'] - v['Average Lift over Ground Roll (N)']))
        ) if (G * v['Air Density (kg/m^3)'] * v['Wing Area (m^2)'] * v['CLmax'] * (v['Thrust Reverser Force (T_rev)'] + v['Average Drag over Ground Roll (N)'] + v['Rolling Resistance Coefficient'] * (v['Aircraft Weight (N)'] - v['Average Lift over Ground Roll (N)']))) != 0 else 0
    },
    {
        'output': 'Total Landing Distance (m)',
        'name': 'Total Landing Distance',
        'inputs': ['Approach Distance (sa_landing)', 'Flare Distance (s_flare)', 'Landing Ground Roll (s_g,l)'],
        'calculate': lambda v: v['Approach Distance (sa_landing)'] + v['Flare Distance (s_flare)'] + v['Landing Ground Roll (s_g,l)']
    },
    # ===========================================
    # ADVANCED CLIMB PERFORMANCE 
    # ===========================================
    {
        'output': 'Liftoff Speed (m/s)',
        'name': 'Assumes V_LO = 1.1* V_Stall',
        'inputs': ['Stall Velocity (m/s)'],
        # Based on the rule of thumb V_LO = 1.1 * V_stall
        'calculate': lambda v: 1.1 * v['Stall Velocity (m/s)']
    },
    {
        'output': 'Time to Climb (s)',
        'name': 'Time to climb from linear R/C approximation',
        'inputs': ['Time to Climb const (a)', 'Time to Climb const (b)', 'Altitude (m)'],
        'calculate': lambda v: (1 / v['Time to Climb const (b)']) * (math.log(v['Time to Climb const (a)'] + v['Time to Climb const (b)'] * v['Altitude (m)']) - math.log(v['Time to Climb const (a)'])) if v['Time to Climb const (b)'] != 0 and (v['Time to Climb const (a)'] + v['Time to Climb const (b)'] * v['Altitude (m)']) > 0 and v['Time to Climb const (a)'] > 0 else 0
    },
    # ==================================
    # STATIC LONGITUDINAL STABILITY 
    # ==================================
    {
        'output': 'Neutral Point (hn)',
        'name': 'Stick-Fixed Neutral Point',
        'inputs': ['AC Location (h_ac,wb)', 'Tail Volume Coefficient (VH)', 'Tail Lift Curve Slope (at)', 'Aircraft Lift Curve Slope (a)', 'Downwash Derivative (de/da)'],
        'calculate': lambda v: v['AC Location (h_ac,wb)'] + v['Tail Volume Coefficient (VH)'] * (v['Tail Lift Curve Slope (at)'] / v['Aircraft Lift Curve Slope (a)']) * (1 - v['Downwash Derivative (de/da)']) if v['Aircraft Lift Curve Slope (a)'] != 0 else 0
    },
    {
        'output': 'Static Margin',
        'name': 'Static Margin from Neutral Point and CG',
        'inputs': ['Neutral Point (hn)', 'CG Location (h)'],
        'calculate': lambda v: v['Neutral Point (hn)'] - v['CG Location (h)']
    },
    {
        'output': 'Neutral Point (hn)',
        'name': 'Inverse Static Margin',
        'inputs': ['Static Margin', 'CG Location (h)'],
        'calculate': lambda v: v['Static Margin'] + v['CG Location (h)']
    },
    {
        'output': 'CG Location (h)',
        'name': 'Inverse Static Margin',
        'inputs': ['Static Margin', 'Neutral Point (hn)'],
        'calculate': lambda v: v['Neutral Point (hn)'] - v['Static Margin']
    },
    # ==================
    # Assumptions 
    # ==================
    {
        'output': 'Thrust Available (N)',
        'inputs': ['Thrust'],
        'name': 'Assume Thrust Available equals Thrust',
        'alias': True
    },
    {
        'output': 'Power Available (W)',
        'inputs': ['Power Required (W)'],
        'name': 'Assume Power Available equals Power Required',
        'alias': True
    }, 
    {
        'output': 'Aircraft Weight (N)',
        'inputs': ['Gross Weight (W0) (N)'],
        'name': 'Assume Aircraft Weight equals Gross Weight',
        'alias': True
    }, 
    {
        'output': 'Gross Weight (W0) (N)',
        'inputs': ['Aircraft Weight (N)'],
        'name': 'Assume Aircraft Weight equals Gross Weight',
        'alias': True
    },  
]


# ---------------------------------------------------------------------------------
# 4. CALCULATION ENGINE
# ---------------------------------------------------------------------------------

#Loops through formula KB to find target parameter
def solve_for(target_param, known_values, formula_kb, verbose=False):
    local_known_values = known_values.copy()
    auto_values = {}
    engine_log = []

    conditional_rules = [r for r in formula_kb if 'conditions' in r]
    general_rules = [r for r in formula_kb if 'conditions' not in r]
    prioritized_rules = conditional_rules + general_rules

    while True:
        made_progress = False
        for rule in prioritized_rules:
            output_param = rule['output']
            if output_param in local_known_values: continue
            if 'conditions' in rule and not all(cond in local_known_values for cond in rule.get('conditions',[])): continue
            if 'inputs' in rule and not all(i in local_known_values for i in rule.get('inputs', [])): continue
            
            new_value = None
            try:
                if rule.get('alias') is True:
                    new_value = local_known_values[rule['inputs'][0]]
                else:
                    new_value = rule['calculate'](local_known_values)
            except (ValueError, ZeroDivisionError, TypeError, KeyError):
                continue

            local_known_values[output_param] = new_value
            auto_values[output_param] = {'value': new_value, 'name': rule.get('name')}
            if verbose:
                log_entry = f"Calculated: {output_param} = {new_value:.4f}" if isinstance(new_value, (int, float)) else f"Mapped alias to {output_param}"
                engine_log.append(log_entry)

            made_progress = True
            break
        
        if not made_progress:
            break
            
    status = 'Success' if target_param in local_known_values else 'Failed'
    return status, local_known_values, auto_values, engine_log

#Similar to solve for but for diagnosing pre calculating to check for missing inputs / conditions
def _simulate_solver(knowns, formula_kb):
    
    found_params = set(knowns)
    path = {}
    
    while True:
        made_progress = False
        
        conditional_rules = [r for r in formula_kb if 'conditions' in r]
        general_rules = [r for r in formula_kb if 'conditions' not in r]
        prioritized_rules = conditional_rules + general_rules

        for rule in prioritized_rules:
            output = rule['output']
            if output in found_params:
                continue

            if 'conditions' in rule and not all(c in found_params for c in rule.get('conditions',[])):
                continue
            
            if 'inputs' in rule and not all(i in found_params for i in rule.get('inputs', [])):
                continue

            found_params.add(output)
            path[output] = rule
            made_progress = True
            break
        
        if not made_progress:
            break
            
    return found_params, path

#Diagnoser determines which units are missing from which intended equation and checks if condition is not checked
def run_pre_flight_diagnoser(target_param, all_knowns_for_diag, formula_kb, parameters_dict):
    
    knowns_for_sim = list(all_knowns_for_diag)
    if 'Standard Sea Level' in knowns_for_sim:
        knowns_for_sim.extend(['Altitude (m)', 'Local Temperature (K)', 'Air Density (kg/m^3)'])
    
    # --- Stage 1: Standard Check ---
    found_params_standard, _ = _simulate_solver(knowns_for_sim, formula_kb)
    if target_param in found_params_standard:
        st.success("✅ A valid calculation path was found. Please proceed.")
        return 'Success', []
        
    unconditional_rules = [{k: v for k, v in r.items() if k != 'conditions'} for r in formula_kb]
    found_params_what_if, what_if_path = _simulate_solver(all_knowns_for_diag, unconditional_rules)
    
    if target_param in found_params_what_if:
        param_to_trace = target_param
        missing_condition = None
        while param_to_trace in what_if_path:
            rule_used = what_if_path[param_to_trace]
            original_rule = next((r for r in formula_kb if r.get('name') == rule_used.get('name') and r['output'] == rule_used['output']), None)
            if original_rule and 'conditions' in original_rule and not all(c in all_knowns_for_diag for c in original_rule['conditions']):
                missing_condition = [c for c in original_rule['conditions'] if c not in all_knowns_for_diag][0]
                break
            
            if 'inputs' in rule_used and rule_used['inputs']:
                param_to_trace = rule_used['inputs'][0]
            else:
                break
        
        if missing_condition:
            condition_list = ', '.join(f"**'{c}'**" for c in missing_condition)
            st.error(f"❌ Calculation Diagnosis: A solution for **{target_param}** may be possible, but it requires a specific flight condition or propulsion type.")
            st.warning(f"Did you forget to select **'{missing_condition}'**?")
            st.caption("*(Note: This is an assumption. Other ways to calculate may exist.)*")
        else: 
             st.error("❌ Calculation Diagnosis: A solution may be possible, but it appears to be blocked by a missing flight condition or propulsion type.")

        return 'Missing_Condition', []

    # --- Stage 2: "Best-Fit" Diagnosis for Missing Inputs ---
    candidate_rules = [r for r in formula_kb if r['output'] == target_param]
    if not candidate_rules:
        st.warning(f"No formulas were found in the knowledge base to calculate '{target_param}'.")
        return 'Failed', []
        
    best_score, best_fit_rules = -1, []
    for rule in candidate_rules:
        score = len(set(rule.get('inputs', [])).intersection(found_params_standard))
        if score > best_score:
            best_score, best_fit_rules = score, [rule]
        elif score == best_score and score != -1:
            best_fit_rules.append(rule)
    
    winner = None
    if len(best_fit_rules) == 1: winner = best_fit_rules[0]
    elif len(best_fit_rules) > 1:
        # Tie-breaker: prefer the formula with the highest completion percentage
        winner = max(best_fit_rules, key=lambda r: len(set(r.get('inputs', [])).intersection(found_params_standard)) / len(r.get('inputs',[])))
    
    if winner:
        missing_inputs = sorted([inp for inp in winner['inputs'] if inp not in found_params_standard])
        display_name = parameters_dict.get(target_param, {}).get('display_name', target_param)
        st.error("❌ Calculation Diagnosis: A solution may not be possible with the selected inputs.")
        st.info(f"The most likely path to find **{display_name}** is missing **{len(missing_inputs)}** input(s):")
        for inp in missing_inputs:
            st.write(f"  - `{inp}`")
        st.caption("*(Note: This is an assumption. Other ways to calculate may exist.)*")
        return 'Missing_Inputs', missing_inputs
    else:
        st.warning(f"No clear calculation path was found for **{target_param}**.")
        return 'Failed', []
    
# =================================================================================
# --- STREAMLIT USER INTERFACE ---
# =================================================================================

st.set_page_config(layout="wide", page_title="AeroCalc", initial_sidebar_state="expanded")

# This is used to store user selections and results across reruns.
if 'known_params_display' not in st.session_state:
    st.session_state.known_params_display = []
if 'calculation_results' not in st.session_state:
    st.session_state.calculation_results = None
if 'proceed_to_values' not in st.session_state:
    st.session_state.proceed_to_values = False

# --- UI Header ---
st.image("logo.png", width=300) 
st.title("The Advanced Aerospace Calculator")
st.markdown('This is a beta version, errors may exist')

# --- UI Functions ---
def format_choices_for_ui(params_dict, include_calculable_only=False, is_multiselect=False):
    choices = []
    categories = {}
    
    # Create a dictionary to group parameters by category
    for key, data in params_dict.items():
        if include_calculable_only and not data.get('is_calculable', False):
            continue
            
        category = data.get('category', 'Uncategorized')
        if category not in categories:
            categories[category] = []
        categories[category].append(data['display_name'])

    # Format the final list of choices
    for category, params in sorted(categories.items()):
        # For the multiselect 'knowns' list, add category headers
        if is_multiselect:
            choices.append(f"--- {category} ---")
        
        for param in sorted(params):
            choices.append(param)
            
    return choices

# --- Sidebar for Setup ---
with st.sidebar:
    st.header("1. Setup")
    
    calculable_choices = format_choices_for_ui(PARAMETERS, include_calculable_only=True, is_multiselect=True)
    target_display_name = st.selectbox("Parameter to Calculate:", calculable_choices, index=calculable_choices.index("Range"))
    
    def clear_known_params():
        st.session_state.known_params_display = []

    unit_system = st.radio(
       "Unit System:",
       ('SI', 'Imperial'),
       horizontal=True,
       on_change=clear_known_params # This line clears selections when the unit system is changed
    )
    selected_engine = st.selectbox("Propulsion Type:", ['Jet-propelled', 'Propeller-driven', 'Unknown/Not Applicable'])
    selected_conditions = st.multiselect("Flight Conditions:", ['Standard Sea Level', 'L/D ratio is maximum (Thrust required min)', 'Cl^3/2/Cd max (minimum power required)', 'Steady level flight', 'Steady climbing flight'])

    st.header("2. Known Parameters")
    known_choices = format_choices_for_ui(PARAMETERS, is_multiselect=True)
    st.session_state.known_params_display = st.multiselect("Select all knowns:", known_choices, default=st.session_state.get('known_params_display', []))

# --- Main Page ---


st.header("3. Pre-Flight Check")
st.info("Click 'Run Pre-Flight Check' to verify if a solution is possible with your selected inputs.")
# --- Pre-Flight Diagnoser Button ---
if st.button("Run Pre-Flight Check", type="secondary", use_container_width=True):
    is_valid_target = not target_display_name.startswith("---")
    if not is_valid_target:
        st.error("Please select a valid parameter to calculate, not a category header.")
    else:
        known_si_names = []
        for name in st.session_state.known_params_display:
            if not name.startswith("---"):
                si_name = next((si for si, data in PARAMETERS.items() if data['display_name'] == name), name)
                known_si_names.append(si_name)
        
        knowns_for_sim = known_si_names + selected_conditions
        if selected_engine != 'Unknown/Not Applicable':
            knowns_for_sim.append(selected_engine)
        target_param_si = next((si for si, data in PARAMETERS.items() if data['display_name'] == target_display_name), target_display_name)
        
        # Store the diagnosis result in the session state
        st.session_state.diag_status, st.session_state.diag_data = run_pre_flight_diagnoser(target_param_si, knowns_for_sim, FORMULA_KB, PARAMETERS)
        
        if st.session_state.diag_status == 'Success':
            st.session_state.proceed_to_values = True
        else:
            st.session_state.proceed_to_values = False


# --- Diagnostic Results & Interactive Menu ---
if 'diag_status' in st.session_state and st.session_state.diag_status is not None:
    
    # This block only runs if the diagnoser has failed
    if st.session_state.diag_status != 'Success':
        
        # Create columns for a cleaner layout
        col1, col2, col3 = st.columns([1, 1, 3])

        # If the failure was due to missing inputs, show the "Add" button
        if st.session_state.diag_status == 'Missing_Inputs':
            with col1:
                if st.button("Add Missing Parameters", key="add_missing"):
                    current_knowns = st.session_state.known_params_display
                    for missing_si_name in st.session_state.diag_data:
                        display_name = PARAMETERS.get(missing_si_name, {}).get('display_name', missing_si_name)
                        if display_name not in current_knowns:
                            current_knowns.append(display_name)
                    st.session_state.known_params_display = current_knowns
                    st.session_state.proceed_to_values = True
                    st.rerun()

        # Always show the developer override option on failure
        with col2:
            if st.button("Force Calculate", key="force_calc"):
                st.session_state.proceed_to_values = True
                st.session_state.diag_status = None # Reset diagnosis
                st.rerun()

    # After an action, this ensures the menu disappears
    else:
        st.session_state.diag_status = None


# --- Value Entry Section ---
st.header("4. Enter Values")
input_values = {}
if st.session_state.get('proceed_to_values', False):
    for param_name in st.session_state.known_params_display:
        if not param_name.startswith("---"):
            si_name_for_label = next((si for si, data in PARAMETERS.items() if data['display_name'] == param_name), param_name)
            label_with_units = get_unit_string(si_name_for_label, unit_system)
            input_values[param_name] = st.number_input(label_with_units, key=f"val_{param_name}", format="%.4f")
else:
    st.info("Run a successful Pre-Flight Check to enter numerical values.")

# --- Calculation Execution ---
st.header("5. Calculate & Review")
if st.button("Calculate", type="primary", use_container_width=True, disabled=not st.session_state.get('proceed_to_values', False)):
    with st.spinner('Running calculations...'):
        target_param_si = next((si for si, data in PARAMETERS.items() if data['display_name'] == target_display_name), target_display_name)
        
        values_si = {}
        for name, value in input_values.items():
            si_name = next((si for si, data in PARAMETERS.items() if data['display_name'] == name), name)
            if unit_system == 'Imperial':
                values_si[si_name] = to_si(value, si_name)
            else:
                values_si[si_name] = value

        values_si.update({cond: True for cond in selected_conditions})
        if selected_engine != 'Unknown/Not Applicable':
            values_si[selected_engine] = True
        if 'Standard Sea Level' in selected_conditions:
            values_si.update({'Altitude (m)': 0, 'Local Temperature (K)': 288.15, 'Air Density (kg/m^3)': 1.225})
        
        status, all_results_si, automatic_values_si, _ = solve_for(target_param_si, values_si, FORMULA_KB)
        
        st.session_state.calculation_done = True
        st.session_state.results = {
            "status": status, "target_param_si": target_param_si,
            "target_display_name": target_display_name,
            "final_answer_si": all_results_si.get(target_param_si),
            "automatic_values_si": automatic_values_si, "unit_system": unit_system
        }
        st.rerun()

# --- Display Results Section ---
if st.session_state.get('calculation_done', False):
    st.header("📊 Results")
    results = st.session_state.results
    
    final_answer_si = results.get('final_answer_si')
    target_param_si = results.get('target_param_si')
    unit_system = results.get('unit_system')

    if results['status'] == 'Success' and final_answer_si is not None:
        final_answer_display = from_si(final_answer_si, target_param_si) if unit_system == 'Imperial' else final_answer_si
        display_param_name = get_unit_string(target_param_si, unit_system)
        
        st.metric(label=display_param_name, value=f"{final_answer_display:.4f}")
        st.success("Calculation Successful!")
        
        with st.expander("View Background Calculations"):
            automatic_values_si = results.get('automatic_values_si', {})
            display_auto_values = {}
            if unit_system == 'Imperial':
                for k, v_data in automatic_values_si.items():
                    k_disp = get_unit_string(k, 'imperial')
                    v_disp = from_si(v_data.get('value'), k) if isinstance(v_data.get('value'), (int, float)) else v_data.get('value')
                    display_auto_values[k_disp] = {'value': v_disp, 'name': v_data.get('name')}
            else:
                display_auto_values = automatic_values_si
            
            if not display_auto_values:
                st.write("No background calculations were performed.")
            else:
                st.write("The following values were calculated automatically:")
                for key, data in sorted(display_auto_values.items()):
                   value = data.get('value'); name = data.get('name')
                   output_string = f" - **{key}**"
                   if name: output_string += f" `({name})`"
                   if isinstance(value, (int, float)): output_string += f": `{value:.4f}`"
                   st.markdown(output_string)
    else:
        st.error(f"Calculation Failed for '{results['target_display_name']}'. Please check your inputs.")