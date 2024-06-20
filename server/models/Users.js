const mongoose = require('mongoose')

const UserSchema = mongoose.Schema({
  username: {
    type: String,
    required: true
  },
  events: {
    type: Object,
    required: true,
  }
})

const User = mongoose.model('users', UserSchema)
module.exports = User