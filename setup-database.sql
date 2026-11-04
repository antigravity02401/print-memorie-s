-- Jalankan query ini di Neon Database Console (https://console.neon.tech)
-- Pilih project kamu → klik "SQL Editor" → paste dan run

CREATE TABLE IF NOT EXISTS testimonials (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  message TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- (Opsional) Masukkan data contoh untuk tes
INSERT INTO testimonials (name, rating, message) VALUES
  ('Nanang & Endang', 5, 'bagus banget undangannya.... dijamin puas');

