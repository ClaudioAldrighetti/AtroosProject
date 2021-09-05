insert into Articles(id, name, price, quantity) values
	(0, "USB Flash Drive 128 GB, USB 3.0", 45.90, 10),
	(1, "Computer HP IntelCore-i7", 950.50, 12),
    (2, "OneOdio Headset", 80.99, 27),
    (3, "Samsung Galaxy A51 - Black", 619.99, 3),
    (4, "Xiaomi RedMi Note 8 Pro - 128GB", 320.00, 13);

insert into Users(name, surname, email, birthDate, country, city, address, civicN, cap) values
	("Mario", "Rossi", "rossimario72@gmail.com", "1972-09-13", "Italy", "Rome", "Via Garibaldi", 34, 00125);

insert into Orders(id, articleId, userEmail, quantity) values 
	(145, 2, "rossimario72@gmail.com", 1),
	(145, 3, "rossimario72@gmail.com", 1),
    (145, 0, "rossimario72@gmail.com", 3);

# For testing
insert into Users(name, surname, email, birthDate, country, city, address, civicN, cap) values
	("Paolo", "Bianchi", "bianchipaolo3@gmail.com", "1981-05-22", "Italy", "Pisa", "Via Girolamo Dalla Corte", 3, 56122);

insert into Orders(id, articleId, userEmail, quantity) values 
	(138, 1, "rossimario72@gmail.com", 1),
    (138, 4, "rossimario72@gmail.com", 1);

insert into Orders(id, articleId, userEmail, quantity) values 
    (144, 0, "bianchipaolo3@gmail.com", 5);
