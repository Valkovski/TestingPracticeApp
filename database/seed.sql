BEGIN TRANSACTION;

DELETE FROM order_items;
DELETE FROM orders;
DELETE FROM cart_items;
DELETE FROM products;
DELETE FROM users;

INSERT INTO users (email, password_hash, full_name, created_at) VALUES
('alex.student@example.com', 'demo_hash_1', 'Alex Student', '2026-04-01 09:00:00'),
('sam.tester@example.com', 'demo_hash_2', 'Sam Tester', '2026-04-02 10:30:00'),
('test@test.com', 'test', 'Test User', '2026-04-03 12:00:00');

INSERT INTO products (name, description, category, price_cents, stock_qty) VALUES
('USB-C Cable 1m', 'Durable USB-C to USB-C cable, 1 meter.', 'Accessories', 899, 120),
('Wireless Mouse', 'Compact wireless mouse with 2.4GHz dongle.', 'Electronics', 1599, 55),
('Mechanical Keyboard', 'Entry-level mechanical keyboard (blue switches).', 'Electronics', 4999, 18),
('Laptop Stand', 'Aluminum stand for 13–17 inch laptops.', 'Office', 2999, 40),
('Notebook A5', 'A5 dotted notebook, 120 pages.', 'Stationery', 499, 200),
('Gel Pen Set', 'Pack of 6 smooth-writing gel pens.', 'Stationery', 699, 90),
('Water Bottle 750ml', 'Reusable bottle with leak-proof cap.', 'Lifestyle', 1299, 65),
('Backpack', 'Everyday backpack with padded laptop sleeve.', 'Lifestyle', 5499, 22),
('Headphones', 'On-ear headphones with inline microphone.', 'Electronics', 2399, 35),
('Phone Case', 'Shock-absorbing case (fits popular 6.1 inch phones).', 'Accessories', 1199, 80),
('Screen Protector', 'Tempered glass screen protector, 2-pack.', 'Accessories', 999, 150),
('Power Bank 10k', '10000mAh power bank with USB-C input/output.', 'Electronics', 3299, 28),
('Bluetooth Speaker', 'Portable speaker with 10-hour battery life.', 'Electronics', 2799, 33),
('Webcam 1080p', 'Full HD webcam for online classes and calls.', 'Electronics', 3499, 26),
('LED Desk Lamp', 'Adjustable desk lamp with 3 brightness levels.', 'Home', 2199, 44);

COMMIT;
