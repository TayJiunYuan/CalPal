const pool = require('../config/db');
const { getMonthRange } = require('./utils');

/**
 * Add event to user's event json field
 * @route PATCH /api/event/add_event
 * @body {String} user_id
 * @body {String} event_date yyyy-mm-dd
 * @body {String} event_name
 * @response 200 - { message: 'Success' }
 * @response 404 - {message: 'User not found'}
 * @response 500 - { message: error.message }
 */

const addEvent = async (req, res) => {
  try {
    const userId = req.body.user_id;
    const eventName = req.body.event_name;
    const eventDate = new Date(req.body.event_date);
    console.log(eventDate);
    const checkUserExistQuery = 'SELECT * FROM users WHERE user_id = $1';
    const checkUserExistQueryValues = [userId];
    const { rows } = await pool.query(checkUserExistQuery, checkUserExistQueryValues);
    if (!rows.length) {
      return res.status(404).json({ message: 'User not found' });
    }

    const addEventQuery = 'INSERT INTO events (event_name, event_date, user_id) VALUES ($1, $2, $3)';
    const addEventQueryValues = [eventName, eventDate, userId];
    await pool.query(addEventQuery, addEventQueryValues);
    return res.status(200).json({ message: 'Success' });
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

/**
 *
 * @route /GET /api/event/:user_id/day/:event_date
 * @param {String} user_id
 * @param {String} event_date yyyy-mm-dd
 * @response 200 - Array of event objs eg. [{"event_id":3,"event_name":"lunchies","user_id":"a1b2c7","event_date":"2019-06-06T16:00:00.000Z"},{"event_id":4,"event_name":"dinners","user_id":"a1b2c7","event_date":"2019-06-06T16:00:00.000Z"}]
 * @response 404 - { message: 'User not found' }
 * @response 404 - { message: 'Event not found' }
 * @response 500 - { message: error.message }
 */
const getUserEventsDay = async (req, res) => {
  try {
    const userId = req.params.user_id;
    const eventDate = req.params.event_date;

    const checkUserExistQuery = 'SELECT * FROM users WHERE user_id = $1';
    const checkUserExistQueryValues = [userId];
    const { rows } = await pool.query(checkUserExistQuery, checkUserExistQueryValues);
    if (!rows.length) {
      return res.status(404).json({ message: 'User not found' });
    }

    const getEventsDayQuery = 'SELECT * FROM events WHERE user_id = $1 AND event_date = $2';
    const getEventsDayQueryValues = [userId, eventDate];
    const events = await pool.query(getEventsDayQuery, getEventsDayQueryValues);

    if (!events.rows.length) {
      return res.status(404).json({ message: 'Event not found' });
    }

    return res.status(200).json(events.rows);
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

/**
 *
 * @route /GET /api/event/:user_id/month/:event_month
 * @param {String} user_id
 * @param {String} event_month yyyy-mm
 * @response 200 - Array of event objs eg. [{"event_id":3,"event_name":"lunchies","user_id":"a1b2c7","event_date":"2019-06-06T16:00:00.000Z"},{"event_id":4,"event_name":"dinners","user_id":"a1b2c7","event_date":"2019-06-06T16:00:00.000Z"}]
 * @response 404 - { message: 'User not found' }
 * @response 404 - { message: 'Event not found' }
 * @response 500 - { message: error.message }
 */
const getUserEventsMonth = async (req, res) => {
  try {
    const userId = req.params.user_id;
    const eventMonth = req.params.event_month;

    const checkUserExistQuery = 'SELECT * FROM users WHERE user_id = $1';
    const checkUserExistQueryValues = [userId];
    const { rows } = await pool.query(checkUserExistQuery, checkUserExistQueryValues);
    if (!rows.length) {
      return res.status(404).json({ message: 'User not found' });
    }

    const { startDate, endDate } = getMonthRange(eventMonth);
    const getEventsMonthQuery = 'SELECT * FROM events WHERE user_id = $1 AND event_date >= $2 AND event_date < $3';
    const getEventsMonthQueryValues = [userId, startDate, endDate];
    const events = await pool.query(getEventsMonthQuery, getEventsMonthQueryValues);

    if (!events.rows.length) {
      return res.status(404).json({ message: 'Event not found' });
    }

    let sorted_events = {};
    events.rows.forEach((eventObj) => {
      /*
      Note: When saving into Date in Postgre, the timezone and time is not saved. Thus, when JS loads the event_date, it will load it as 00:00:00 GMT+8 BUT display in UTC thus the date will not look correct. getDate() will still work as it takes local timezone GMT +8.
      */
      const day = new Date(eventObj.event_date).getDate();
      console.log('day: ' + day);
      if (day in sorted_events) {
        sorted_events[day].push(eventObj);
      } else {
        sorted_events[day] = [eventObj];
      }
    });
    return res.status(200).json(sorted_events);
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

/**
 * Delete Event by id
 * @route PATCH /api/event/delete_event
 * @body {String} event_id
 * @response 200 - { message: 'Success' }
 * @response 404 - { message: 'Event ID not found' }
 * @response 500 - { message: error.message }
 */

const deleteEvent = async (req, res) => {
  try {
    const eventId = req.body.event_id;

    const deleteEventQuery = 'DELETE FROM events WHERE event_id = $1';
    const deleteEventQueryValues = [eventId];
    const result = await pool.query(deleteEventQuery, deleteEventQueryValues);
    // check if delete was successful
    if (result.rowCount == 0) {
      return res.status(404).json({ message: 'Event not found' });
    }
    return res.status(200).json({ message: 'Success' });
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

module.exports = { addEvent, getUserEventsDay, getUserEventsMonth, deleteEvent };
