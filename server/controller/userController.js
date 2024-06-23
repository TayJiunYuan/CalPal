const pool = require('../config/db');

/**
 *
 * @route POST /api/user/createUser
 * @body {String} user_id
 * @body {String} username
 * @response 200 - { message: 'Success'}
 * @response 409 - { message: 'Duplicate user'}
 * @response 500 - { message: error.message }
 */
const createUser = async (req, res) => {
  try {
    const userId = req.body.user_id;
    const username = req.body.username;
    const checkDupeQuery = 'SELECT * FROM users WHERE user_id = $1';
    const checkDupeQueryValues = [userId];
    const { rows } = await pool.query(checkDupeQuery, checkDupeQueryValues);
    if (rows.length) {
      return res.status(409).json({ message: 'Duplicate user' });
    }

    const createUserQuery = 'INSERT INTO users (user_id, username) VALUES ($1, $2)';
    const createUserQueryValues = [userId, username];
    await pool.query(createUserQuery, createUserQueryValues);
    return res.status(200).json({ message: 'Success' });
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

module.exports = {
  createUser,
};
