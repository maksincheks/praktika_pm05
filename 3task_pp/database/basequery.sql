-- Исполнитель
CREATE TABLE IF NOT EXISTS executor (
    id     SERIAL PRIMARY KEY,
    name   VARCHAR(255) NOT NULL,
    inn    VARCHAR(20),
    address TEXT,
    phone  VARCHAR(30)
);

-- Заказчик
CREATE TABLE IF NOT EXISTS customers (
    id       VARCHAR(20) PRIMARY KEY,
    name     VARCHAR(255) NOT NULL,
    inn      VARCHAR(20),
    address  TEXT,
    phone    VARCHAR(30),
    salesman BOOLEAN NOT NULL DEFAULT FALSE,
    buyer    BOOLEAN NOT NULL DEFAULT FALSE
);

-- Материал
CREATE TABLE IF NOT EXISTS materials (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cost NUMERIC(15, 2) NOT NULL DEFAULT 0,
    unit VARCHAR(50)
);

-- Цены
CREATE TABLE IF NOT EXISTS prices (
    id          SERIAL PRIMARY KEY,
    material_id INTEGER NOT NULL REFERENCES materials(id) ON DELETE CASCADE,
    cost        NUMERIC(15, 2) NOT NULL,
    date        DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Продукт
CREATE TABLE IF NOT EXISTS product (
    id   SERIAL PRIMARY KEY,
    code VARCHAR(50),
    name VARCHAR(255) NOT NULL,
    unit VARCHAR(50)
);

-- Спецификация
CREATE TABLE IF NOT EXISTS specification (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    product_id INTEGER NOT NULL REFERENCES product(id) ON DELETE CASCADE
);

-- Состав спецификации
CREATE TABLE IF NOT EXISTS specification_items (
    id          SERIAL PRIMARY KEY,
    spec_id     INTEGER NOT NULL REFERENCES specification(id) ON DELETE CASCADE,
    material_id INTEGER NOT NULL REFERENCES materials(id) ON DELETE RESTRICT,
    quantity    NUMERIC(15, 4) NOT NULL DEFAULT 0
);

-- Заказ
CREATE TABLE IF NOT EXISTS buyer_order (
    id           SERIAL PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL,
    date         DATE NOT NULL DEFAULT CURRENT_DATE,
    executor_id  INTEGER NOT NULL REFERENCES executor(id) ON DELETE RESTRICT,
    customer_id  VARCHAR(20) NOT NULL REFERENCES customers(id) ON DELETE RESTRICT
);

-- Состав заказа
CREATE TABLE IF NOT EXISTS order_items (
    id         SERIAL PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES buyer_order(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES product(id) ON DELETE RESTRICT,
    quantity   NUMERIC(15, 4) NOT NULL DEFAULT 1,
    price      NUMERIC(15, 2) NOT NULL DEFAULT 0
);

-- Производство
CREATE TABLE IF NOT EXISTS production (
    id               SERIAL PRIMARY KEY,
    number           VARCHAR(50) NOT NULL,
    date             DATE NOT NULL DEFAULT CURRENT_DATE,
    specification_id INTEGER NOT NULL REFERENCES specification(id) ON DELETE RESTRICT
);

-- =====================================================
-- ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ (по заданию)
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Пользователь',
    is_locked BOOLEAN NOT NULL DEFAULT FALSE,
    failed_attempts INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Добавление тестовых пользователей
INSERT INTO users (username, password_hash, role) 
VALUES 
    ('admin', '4321', 'Администратор'),
    ('user', '1234', 'Пользователь')
ON CONFLICT (username) DO NOTHING;

-- =====================================================
-- ИМПОРТ ДАННЫХ
-- =====================================================
INSERT INTO customers (id, name, inn, address, phone, salesman, buyer)
VALUES
    ('000000001', 'ООО "Поставка"',        '',            'г.Пятигорск',                    '+79198634592', TRUE,  TRUE),
    ('000000002', 'ООО "Кинотеатр Квант"', '26320045123', 'г. Железноводск, ул. Мира, 123', '+79884581555', TRUE,  FALSE),
    ('000000008', 'ООО "Новый JDTO"',      '26320045111', 'г. Железноводсу',                '+79884581555', TRUE,  FALSE),
    ('000000003', 'ООО "Ромашка"',         '4140784214',  'г. Омск, ул. Строителей, 294',   '+79882584546', FALSE, TRUE),
    ('000000009', 'ООО "Ипподром"',        '5874045632',  'г. Уфа, ул. Набережная, 37',     '+79627486389', TRUE,  TRUE),
    ('000000010', 'ООО "Ассоль"',          '2629011278',  'г. Калуга, ул. Пушкина, 94',     '+79184572398', FALSE, TRUE)
ON CONFLICT (id) DO NOTHING;