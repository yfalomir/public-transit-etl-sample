CREATE TABLE IF NOT EXISTS OvapiRawLineInformation (
    id TEXT,
    DataOwnerCode TEXT,
    LinePlanningNumber TEXT,
    LineDirection INTEGER,
    LineWheelchairAccessible BOOLEAN,
    TransportType TRANSPORTTYPEENUM,
    DestinationName50 TEXT,
    DestinationCode TEXT,
    LinePublicNumber TEXT,
    LineName TEXT,
    updated_at TIMESTAMP,
    PRIMARY KEY (id, DataOwnerCode)

) PARTITION BY LIST (DataOwnerCode);

COMMENT ON TABLE OvapiRawLineInformation is 'Quasi-raw data from the Line endpoint of the OVAPI: https://github.com/koch-t/KV78Turbo-OVAPI/wiki/Line';
COMMENT ON COLUMN OvapiRawLineInformation.id is 'As specified in the OVAPI API, used as key for upsert';
COMMENT ON COLUMN OvapiRawLineInformation.LineWheelchairAccessible is 'True=Accessible, False=Not accessible, Null=Unknown';
COMMENT ON COLUMN OvapiRawLineInformation.updated_at is 'Timestamp of last update/insert';
COMMENT ON COLUMN OvapiRawLineInformation.TransportType is 'Describs transport type defined by OVAPI, stored as TRANSPORTTYPEENUM';