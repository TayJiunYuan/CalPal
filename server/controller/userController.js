const User = require('../models/Users');
const { decodeDate } = require('./utils')

/**
 * 
 * @route POST /api/user/createUser
 * @body {String} username
 * @response 200 - updated user obj
 * @response 409 - { message: 'Duplicate User!'}
 * @response 500 - { message: error.message }
 */
const createUser = async (req, res) => {
  try {
    const { username } = req.body;
    const dupeUser = await User.findOne({ username: username });
    if (dupeUser) {
      return res.status(409).json({ message: 'Duplicate User!' });
    }
    const newUser = new User({
      username: username,
      events: {}
    });
    const updatedUser = await newUser.save();
    return res.status(200).json(updatedUser);
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};


/**
 * Add event to user's event json field
 * @route PATCH /api/user/addEvent
 * @body {String} username 
 * @body {String} dateString 
 * @body {String} eventName
 * @response 200 - updated user obj
 * @response 400 - {message: 'User not found!'}
 * @response 500 - { message: error.message }
 */

const addEvent = async (req, res) => {
  try {
    const { username, dateString, eventName } = req.body;

    const dateObj = decodeDate(dateString);
    const { year, month, day } = dateObj;
    
    const user = await User.findOne({ username: username });
    if (!user) {
      return res.status(400).json({ message: 'User not found!' });
    }

    // deep clone current event obj
    let eventsObj = JSON.parse(JSON.stringify(user.events));

    // Ensure year field, month field, and day array exist in eventsObj
    eventsObj[year] = eventsObj[year] || {};
    eventsObj[year][month] = eventsObj[year][month] || {};
    eventsObj[year][month][day] = eventsObj[year][month][day] || [];

    // pushes new event into correct day array
    eventsObj[year][month][day].push(eventName);
 
    user.events = eventsObj;
    const updatedUser = await user.save();

    return res.status(200).json({ updatedUser });

  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};


/**
 * 
 * @route /GET /api/users/:username/day/:dateString
 * @param {String} username
 * @param {String} username
 * @response 200 - Array of event name strings
 * @response 400 - { message: 'User not found!' }
 * @response 404 - { message: 'No events for this date' }
 * @response 500 - { message: error.message }
 */
const getUserEventsDay = async (req, res) => {
  try {
    const username = req.params.username;
    const dateString = req.params.dateString;   
    const dateObj = decodeDate(dateString);
    const { year, month, day } = dateObj;
    console.log(dateObj)
    const user = await User.findOne({ username: username });
    if (!user) {
      return res.status(400).json({ message: 'User not found!' });
    }
    // deep copy
    let eventsObj = JSON.parse(JSON.stringify(user.events));

    const dayEventsArr = eventsObj[year]?.[month]?.[day];
    if (!dayEventsArr) {
      return res.status(404).json({ message: 'No events for this day' });
    }
    return res.status(200).json({ dayEventsArr });
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};


/**
 * 
 * @route /GET /api/users/:username/day/:dateString
 * @param {String} username
 * @param {String} dateString
 * @response 200 - Array of event name strings
 * @response 400 - { message: 'User not found!' }
 * @response 404 - { message: 'No events for this date' }
 * @response 500 - { message: error.message }
 */
const getUserEventsMonth = async (req, res) => {
  try {
    const username = req.params.username;
    const dateString = req.params.dateString;   
    const dateObj = decodeDate(dateString);
    const { year, month } = dateObj;

    const user = await User.findOne({ username: username });
    if (!user) {
      return res.status(400).json({ message: 'User not found!' });
    }
    // deep copy
    let eventsObj = JSON.parse(JSON.stringify(user.events));

    const monthEventsObj = eventsObj[year]?.[month];
    if (!monthEventsObj) {
      return res.status(404).json({ message: 'No events for this month' });
    }
    return res.status(200).json(monthEventsObj);
  } catch (error) {
    return res.status(500).json({ message: error.message });
  }
};

// deleteUserEvent

// moveUserEvent

module.exports = {
  createUser, addEvent, getUserEventsDay, getUserEventsMonth
}
