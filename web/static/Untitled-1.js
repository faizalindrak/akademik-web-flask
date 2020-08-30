var $dropdowna = getAll('#dropdowna:not(.is-hoverable)');

  if ($dropdowna.length > 0) {
    $dropdowna.forEach(function ($el) {
      $el.addEventListener('click', function (event) {
        event.stopPropagation();
        $el.classList.toggle('is-active');
      });
    });

    document.addEventListener('click', function (event) {
      closedropdowna();
    });
  }

  function closedropdowna() {
    $dropdowna.forEach(function ($el) {
      $el.classList.remove('is-active');
    });
  }

  // Close dropdowna if ESC pressed
  document.addEventListener('keydown', function (event) {
    var e = event || window.event;
    if (e.keyCode === 27) {
      closedropdowna();
    }
  });

  // Functions

  function getAll(selector) {
    return Array.prototype.slice.call(document.querySelectorAll(selector), 0);
  }
