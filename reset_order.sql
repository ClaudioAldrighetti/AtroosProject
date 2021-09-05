INSERT INTO Orders(id, articleId, userEmail, quantity) VALUES
	(145, 2, "rossimario72@gmail.com", 1);
    
INSERT INTO Orders(id, articleId, userEmail, quantity) VALUES
	(145, 3, "rossimario72@gmail.com", 1);

INSERT INTO Orders(id, articleId, userEmail, quantity) VALUES
    (145, 0, "rossimario72@gmail.com", 3);

UPDATE atroosproject.orders O
SET O.state = false
WHERE O.id = 145;
