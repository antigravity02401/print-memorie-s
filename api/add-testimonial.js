const { neon } = require('@neondatabase/serverless');

module.exports = async function (req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method Not Allowed' });
  }

  const { name, rating, message } = req.body;

  if (!name || !rating || !message) {
    return res.status(400).json({ message: 'Semua field wajib diisi' });
  }

  if (rating < 1 || rating > 5) {
    return res.status(400).json({ message: 'Rating tidak valid' });
  }

  try {
    const sql = neon(process.env.DATABASE_URL);
    
    await sql`
      INSERT INTO testimonials (name, rating, message) 
      VALUES (${name}, ${rating}, ${message})
    `;

    return res.status(200).json({ message: 'Testimoni berhasil ditambahkan' });
  } catch (error) {
    console.error('Database Error:', error);
    return res.status(500).json({ message: 'Gagal menyimpan ke database' });
  }
};
