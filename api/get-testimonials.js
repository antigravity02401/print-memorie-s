const { neon } = require('@neondatabase/serverless');

module.exports = async function (req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ message: 'Method Not Allowed' });
  }

  try {
    const sql = neon(process.env.DATABASE_URL);
    
    // Ambil 6 testimoni terbaru
    const result = await sql`
      SELECT name, rating, message, created_at
      FROM testimonials
      ORDER BY created_at DESC
      LIMIT 6
    `;

    return res.status(200).json(result);
  } catch (error) {
    console.error('Database Error:', error);
    return res.status(500).json({ message: 'Gagal mengambil data dari database' });
  }
};
