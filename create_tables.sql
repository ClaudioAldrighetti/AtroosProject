-- Articles: list of articles
create table if not exists Articles (
	-- Every article has an associated unique id
	id integer primary key check(id >= 0),

	-- Article information
	name varchar(70) not null,    
    price numeric(6,2) not null check(price > 0.0),
    quantity smallint not null check(quantity >= 0)
);

-- Users: list of registered users to the web site
create table if not exists Users (
	-- Personal information
    name varchar(20) not null,
    surname varchar(30) not null,
    -- fc char(16),						-- fiscal code could be an unique value to identify users
    email varchar(320) primary key,		-- email is used as primary key, only one account is allowed for the same email
    phoneN varchar(10),
    birthDate date,

	-- Domicile for delivery
    country varchar(20) not null,
    city varchar(30) not null,
    address varchar(70) not null,
    civicN smallint not null check(civicN > 0),
    cap char(5) not null							-- CAP could also be an integer
);

-- Orders: every entry associates order id with an article id included in the order. The same order could be associated with
-- more than one entry, because users can add to single orders many articles.
create table if not exists Orders (
	-- Order id and article id identify the entry
	id integer check(id >= 0),
    articleId integer references Articles(id),
    primary key(id, articleId),
    
    -- User that creates the order
    userEmail varchar(320) not null references Users(email),
    
    -- Order status: could be pending (false) or settled (true), the initial state is pending
    state bool not null default false,
    
    -- Article quantity requested
    quantity smallint not null check(quantity > 0)
);
