CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO todos (title, done)
SELECT 'настроить terraform', true
WHERE NOT EXISTS (SELECT 1 FROM todos);

INSERT INTO todos (title, done)
VALUES ('накатить ansible на бэкенд', false);
