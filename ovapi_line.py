
class OvapiLine:
    def __init__(self, id, ovapi_line_data):
        self.id = id
        self.data_owner_code = str(ovapi_line_data["DataOwnerCode"])
        self.line_planning_number = str(ovapi_line_data["LinePlanningNumber"])
        self.line_direction = int(ovapi_line_data["LineDirection"])
        if ovapi_line_data["LineWheelchairAccessible"] == "ACCESSIBLE":
            self.line_wheelchair_accessible = True
        elif ovapi_line_data["LineWheelchairAccessible"] == "NOTACCESSIBLE":
            self.line_wheelchair_accessible = False
        else:
            self.line_wheelchair_accessible = None

        self.transport_type = str(ovapi_line_data["TransportType"])
        self.destination_name_50 = str(ovapi_line_data["DestinationName50"])
        self.destination_code = str(ovapi_line_data["DestinationCode"])
        self.line_public_number = str(ovapi_line_data["LinePublicNumber"])
        self.line_name = str(ovapi_line_data["LineName"])

    def format_for_insert(self):
        return (
            self.id,
            self.data_owner_code,
            self.line_planning_number,
            self.line_direction,
            self.line_wheelchair_accessible,
            self.transport_type,
            self.destination_name_50,
            self.destination_code,
            self.line_public_number,
            self.line_name
        )
