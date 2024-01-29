CREATE TABLE IF NOT EXISTS {table} PARTITION of OvapiRawLineInformation
    FOR VALUES IN (%s);