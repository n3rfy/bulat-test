insert into transaction (user_id, timestamp, amount)
select (random() * 1000)::integer,
       1704201494 + (random() * 1000000)::integer,
       (random() * 70 + 10)::integer
from generate_series(1, 10000000);