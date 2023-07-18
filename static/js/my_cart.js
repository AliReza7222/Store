function increment(bookId) {
  var input = document.getElementById('myNumber_' + bookId);
  var maxValue = parseInt(input.getAttribute('max'));
  var currentValue = parseInt(input.value);

  if (currentValue < maxValue) {
    input.value = currentValue + 1;
  }
}

function decrement(bookId) {
  var input = document.getElementById('myNumber_' + bookId);
  var minValue = parseInt(input.getAttribute('min'));
  var currentValue = parseInt(input.value);

  if (currentValue > minValue) {
    input.value = currentValue - 1;
  }
}
