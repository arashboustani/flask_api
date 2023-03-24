CREATE TABLE IF NOT EXISTS tor_ip (
    id integer GENERATED ALWAYS AS IDENTITY,
    ip text
);

CREATE UNIQUE INDEX IF NOT EXISTS tor_ip_pkey ON tor_ip(id int4_ops);