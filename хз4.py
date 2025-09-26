class BuildingError(Exception):
    def __str__(self):
        return f"With so much materials u cannot build house!"

def check_material(amount_of_material, limit_value):
    if amount_of_material > limit_value:
        return "Enough materials"
    else:
        raise BuildingError(amount_of_material)

material = 123
check_material(material, limit_value=300)