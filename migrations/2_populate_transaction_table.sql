insert into transaction (user_id, timestamp, amount)
select (random() * 10)::integer,
       1704201494 + (random() * 1000000)::integer,
       (random() * 70 + 10)::integer
from generate_series(1, 1000000);