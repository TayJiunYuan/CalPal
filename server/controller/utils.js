const decodeDate = (dateString) => {
  const year = dateString.slice(0, 4);
  const month = dateString.slice(4, 6);
  // if yyyy-mm-dd
  if (dateString.length === 8) {
    const day = dateString.slice(6, 8);
    const dateObj = { year: year, month: month, day: day };
    return dateObj;
    // if yyyy-mm 
  } else {
    const dateObj = { year: year, month: month};
    return dateObj;
  }
};

module.exports = {
  decodeDate
}