from VPP.variable import Function, Variable

salt_water_density = Variable("ρ", 1025)
salt_water_dynamic_viscosity = Variable("μ", 0.1)


def KinematicViscosity(
    dynamic_viscosity: Variable = salt_water_dynamic_viscosity, density: Variable = salt_water_density
) -> Function:
    v = dynamic_viscosity / density
    v.name = "μ"
    return v


def ReynoldsNumber(speed: Variable, length: Variable, kinematic_viscosity: Variable = KinematicViscosity()) -> Function:
    re: Function = (speed * length) / kinematic_viscosity
    re.name = "Re"
    return re
