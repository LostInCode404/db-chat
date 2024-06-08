-- Select DB
USE dbchat;

-- Add tables
CREATE TABLE category (
    category_id INT PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);
CREATE TABLE brand (
    brand_id INT PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);
CREATE TABLE product_name (
    product_name_id INT PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);
CREATE TABLE product (
    product_id INT PRIMARY KEY,
    quantity INT NOT NULL,
    price INT NOT NULL,
    color VARCHAR(64),
    product_name_id INT NOT NULL,
    category_id INT NOT NULL,
    brand_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id),
    FOREIGN KEY (product_name_id) REFERENCES product_name(product_name_id),
    UNIQUE (product_name_id, brand_id, color)
);
CREATE TABLE discount (
    discount_id INT PRIMARY KEY,
    percent INT NOT NULL CHECK (percent >= 0 AND percent <= 100),
    product_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

-- Add categories
INSERT INTO category (category_id, name) VALUES
    (1, 'Topwear'),
    (2, 'Bottomwear'),
    (3, 'Footwear');

-- Add brands for each of these categories
INSERT INTO brand (brand_id, name)
VALUES
    (1, 'Nike'),
    (2, 'Adidas'),
    (3, 'Levi'),
    (4, 'Gucci');

-- Add product types
INSERT INTO product_name (product_name_id, name)
VALUES
    (1, 'Shirt'),
    (2, 'Jacket'),
    (3, 'Jeans'),
    (4, 'Shorts'),
    (5, 'Sneakers'),
    (6, 'Sandals'),
    (7, 'Boots');

-- Add products
INSERT INTO product (product_id, product_name_id, quantity, price, category_id, brand_id, color)
VALUES
    (1, 1, 100, 2000, 1, 1, 'Red'),
    (2, 1, 150, 2200, 1, 2, 'White'),
    (3, 1, 120, 1900, 1, 3, 'Blue'),
    (4, 1, 130, 2100, 1, 4, 'Green'),
    (5, 1, 140, 2500, 1, 1, 'Green'),
    (6, 1, 110, 2300, 1, 1, 'White'),
    (7, 1, 160, 2400, 1, 1, 'Blue'),
    (8, 1, 170, 2600, 1, 2, 'Green'),
    (9, 2, 80, 5000, 1, 1, 'Red'),
    (10, 2, 90, 5200, 1, 2, 'White'),
    (11, 2, 70, 4900, 1, 3, 'Red'),
    (12, 2, 85, 5100, 1, 4, 'Green'),
    (13, 2, 75, 5500, 1, 1, 'Blue'),
    (14, 2, 65, 5300, 1, 4, 'White'),
    (15, 2, 95, 5400, 1, 3, 'Blue'),
    (16, 2, 100, 5600, 1, 1, 'Green'),
    (17, 3, 200, 3000, 2, 1, 'Red'),
    (18, 3, 210, 3200, 2, 2, 'Green'),
    (19, 3, 190, 2900, 2, 3, 'Blue'),
    (20, 3, 220, 3100, 2, 4, 'White'),
    (21, 3, 230, 3500, 2, 2, 'Red'),
    (22, 3, 180, 3300, 2, 3, 'Green'),
    (23, 3, 240, 3400, 2, 4, 'Blue'),
    (24, 3, 250, 3600, 2, 4, 'Green'),
    (25, 3, 200, 3000, 2, 1, 'Blue'),
    (26, 3, 210, 3200, 2, 2, 'White'),
    (27, 4, 120, 1500, 2, 3, 'Blue'),
    (28, 4, 130, 1600, 2, 4, 'White'),
    (29, 4, 140, 1700, 2, 1, 'Red'),
    (30, 4, 150, 1800, 2, 2, 'White'),
    (31, 4, 160, 1900, 2, 3, 'Red'),
    (32, 4, 170, 2000, 2, 4, 'Blue'),
    (33, 5, 90, 6000, 3, 1, 'Red'),
    (34, 5, 85, 6200, 3, 2, 'Green'),
    (35, 5, 80, 5900, 3, 3, 'Red'),
    (36, 5, 95, 6100, 3, 4, 'Green'),
    (37, 5, 70, 6500, 3, 1, 'White'),
    (38, 5, 75, 6300, 3, 1, 'Green'),
    (39, 6, 60, 2500, 3, 3, 'Blue'),
    (40, 6, 65, 2600, 3, 4, 'Red'),
    (41, 6, 55, 2700, 3, 1, 'White'),
    (42, 6, 70, 2800, 3, 2, 'Green'),
    (43, 7, 50, 7000, 3, 3, 'Blue'),
    (44, 7, 45, 7200, 3, 4, 'White');

-- Add discounts
INSERT INTO discount (discount_id, percent, product_id)
VALUES
    (1, 10, 1),
    (2, 15, 2),
    (3, 20, 3),
    (4, 25, 4),
    (5, 5, 5),
    (6, 30, 6),
    (7, 10, 7),
    (8, 15, 8),
    (9, 20, 9),
    (10, 25, 10),
    (11, 5, 11),
    (12, 30, 12),
    (13, 10, 13),
    (14, 15, 14),
    (15, 20, 15),
    (16, 25, 16),
    (17, 5, 17),
    (18, 30, 18),
    (19, 10, 19),
    (20, 15, 20);
