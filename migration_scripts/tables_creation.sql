/*
create table appuser (
  appuser_id serial primary key,
  phone char(11) not null,
  passwd varchar, 
  firstname varchar(30),
  lastname varchar(30)
);

create table product (
  product_id serial primary key,
  price numeric(8,2) not null,
  description varchar, 
  params json
);

create table state_dict (
  state_id integer primary key,
  title varchar(50)
);

create table purchase (
  purchase_id serial primary key,
  appuser_id integer references appuser(appuser_id) not null,
  discount numeric(8,2),
  purchase_state integer references state_dict(state_id) not null, 
  purchase_datetime timestamp not null,
  total numeric(8,2)
);

create table purchase_product (
  purchase_id integer references purchase (purchase_id) not null,
  product_id integer references product (product_id) not null,
  quantity integer not null
);

create table shopping_cart (
  appuser_id integer references appuser (appuser_id) not null,
  product_id integer references product (product_id) not null,
  quantity integer not null
);

create table finance_log (
  transaction_id serial primary key,
  appuser_id integer references appuser (appuser_id) not null,
  transaction_datetime timestamp not null,
  purchase_id integer references purchase (purchase_id),
  debet numeric(8,2),
  credit numeric(8,2),
  saldo numeric(18,2)
);

insert into state_dict values
(1, 'В обработке'),
(2, 'Оплачено')
;
*/