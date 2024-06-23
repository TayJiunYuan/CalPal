// eg. 2024-06 -> 2024-06-01 , 2024-07-01
// edge case 2024-12 -> 2024-12-01, 2025-01-01
const getMonthRange = (eventMonth) => {
  const [year, month] = eventMonth.split('-');

  // Calculate the start date of the month
  const startDate = `${year}-${month}-01`;

  // Calculate the end date of the month
  let endDate;
  if (month === '12') {
    // Edge case: December, move to the next year
    endDate = `${Number(year) + 1}-01-01`;
  } else {
    endDate = `${year}-${String(Number(month) + 1).padStart(2, '0')}-01`;
  }
  return {startDate, endDate};
}

module.exports = {
  getMonthRange
}