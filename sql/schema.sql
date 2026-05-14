DROP TABLE IF EXISTS marketing_campaigns;

CREATE TABLE marketing_campaigns (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    channel VARCHAR(50) NOT NULL,
    spend NUMERIC(10,2),
    impressions INTEGER,
    clicks INTEGER,
    conversions INTEGER,
    revenue NUMERIC(10,2)
);