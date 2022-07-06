import math


class Kettle(object):
    """A simulated kettle.
    It is assumed the kettle is made from metal (brass) and an electric heating element is sitting inside the
    kettle and it is submerged in the (fresh) water.
    The kettle is heated with the heating element and cools from conductivity to the ambient air.

    Args:
        diameter (float): Kettle diameter in centimeters.
        volume (float): Content volume in liters.
        temp (float): Initial content temperature in degree celsius.
    """

    DENSITY_WATER = 0.997

    # specific heat capacity of water: c = 4.1796 kJ / kg * K (20°C)
    # 4.2160 (100°)
    SPECIFIC_HEAT_CAP_WATER = 4.200

    # specific heat capacity of brass: c = 0.387 kJ / kg * K (20°C)
    # (increased a bit for higher temperature and varying values depending on source)
    SPECIFIC_HEAT_CAP_BRASS = 0.400

    # thermal conductivity of steel: lambda = 15 W / m * K
    # (TODO: wrong? should be 25 for stainless or 50 for normal steel)
    #THERMAL_CONDUCTIVITY_STEEL = 15

    # conductivity of brass, adjusted from 96 for open brass boiler to be less conductive
    # within boiler enclosure etc.
    THERMAL_CONDUCTIVITY_BRASS = 96
    THERMAL_CONDUCTIVITY_KETTLE = THERMAL_CONDUCTIVITY_BRASS * 0.5

    def __init__(self, diameter, volume, temp, kettleMass):
        self._waterMass = volume * Kettle.DENSITY_WATER
        self._temp = temp
        radius = diameter / 2

        # height in cm
        height = (volume * 1000) / (math.pi * math.pow(radius, 2))

        # surface in m^2
        self._surface = (2 * math.pi * math.pow(radius, 2) + 2 * math.pi * radius * height) / 10000

        self._kettleMass = kettleMass

    @property
    def temperature(self):
        """Get the content's temperature"""
        return self._temp

    def heat(self, power, duration, efficiency=0.98):
        """Heat the kettle's content.

        Args:
            power (float): The power in kW.
            duration (float): The duration in seconds.
            efficiency (float): The efficiency as number between 0 and 1.
        """
        self._temp += self._get_deltaT(power * efficiency, duration)
        return self._temp

    def cool(self, duration, ambient_temp, heat_loss_factor=1):
        """Make the content loose heat.

        Args:
            duration (float): The duration in seconds.
            ambient_temp (float): The ambient temperature in degree celsius.
            heat_loss_factor (float): Increase or decrease the heat loss by a
            specified factor.
        """
        # Q = k_w * A * (T_kettle - T_ambient)
        # P = Q / t
        power = ((Kettle.THERMAL_CONDUCTIVITY_KETTLE * self._surface
                 * (self._temp - ambient_temp)) / duration)

        # W to kW
        power /= 1000
        self._temp -= self._get_deltaT(power, duration) * heat_loss_factor
        return self._temp

    def _get_deltaT(self, power, duration):
        # P = Q / t
        # Q = (c_water * m_water + c_kettle * m_kettle) * delta T
        # => delta(T) = (P * t) / (c_water * m_water + c_kettle * m_kettle)

        #temperature difference of water after applying power for duration
        return ((power * duration) / (Kettle.SPECIFIC_HEAT_CAP_WATER * self._waterMass +
                                      Kettle.SPECIFIC_HEAT_CAP_BRASS * self._kettleMass))

