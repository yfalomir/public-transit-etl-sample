INSERT INTO OvapiRawLineInformation (
    id,
    DataOwnerCode,
    LinePlanningNumber,
    LineDirection,
    LineWheelchairAccessible,
    TransportType,
    DestinationName50,
    DestinationCode,
    LinePublicNumber,
    LineName,
    updated_at
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp)
ON CONFLICT (id, DataOwnerCode)
DO UPDATE SET
    DataOwnerCode = EXCLUDED.DataOwnerCode,
    LinePlanningNumber = EXCLUDED.LinePlanningNumber,
    LineDirection = EXCLUDED.LineDirection,
    LineWheelchairAccessible = EXCLUDED.LineWheelchairAccessible,
    TransportType = EXCLUDED.TransportType,
    DestinationName50 = EXCLUDED.DestinationName50,
    DestinationCode = EXCLUDED.DestinationCode,
    LinePublicNumber = EXCLUDED.LinePublicNumber,
    LineName = EXCLUDED.LineName,
    updated_at = current_timestamp