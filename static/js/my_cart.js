function increment(bookId) {
    var input = document.getElementById('myNumber_' + bookId);
    input.stepUp();
  }

  function decrement(bookId) {
    var input = document.getElementById('myNumber_' + bookId);
    input.stepDown();
  }
