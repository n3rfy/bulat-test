INSERT INTO transaction (user_id, timestamp, amount)
SELECT (random() * 10)::integer,
       1704201494 + (random() * 1000000)::integer,
       (random() * 70 + 10)::integer
FROM generate_series(1, 1000000);

delete from transaction;