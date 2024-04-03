create table transaction
(
    user_id   integer not null,
    timestamp integer not null,
    amount    integer not null
);
create index on transaction(user_id, timestamp);
