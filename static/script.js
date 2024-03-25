const dropArea = document.getElementById('dropArea');
const fileInput = document.getElementById('fileInput');

dropArea.addEventListener('click', () => fileInput.click());

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
  dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
  dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight() {
  dropArea.classList.add('dragover');
}

function unhighlight() {
  dropArea.classList.remove('dragover');
}

fileInput.addEventListener('change', handleFile, false);

function handleFile(e) {
  let file = e.target.files[0];

  uploadFile(file);
}

function uploadFile(file) {
  const formData = new FormData();
  formData.append('to_calculate', file);

  fetch('/api/v1/calculateprice', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error(error);
    });
}

$(function() {
  const sparkleSettings = {
    color: "#FFFFFF",
    count: 30,
    overlap: 0,
    speed: 1
  };

  $('#dropArea').hover(function() {
    $(this).sparkleh(sparkleSettings);
  }, function() {
    $(this).find('.sparkle-canvas').remove();
  });
});

$.fn.sparkleh = function(options) {
  const settings = $.extend({
    width: $(this).outerWidth(),
    height: $(this).outerHeight(),
    color: "#FFFFFF",
    count: 30,
    overlap: 0,
    speed: 1,
  }, options);

  return this.each(function() {
    const $this = $(this).css("position", "relative");
    const sparkle = new Sparkle($this, settings);
  });
};

function Sparkle($parent, options) {
  this.options = options;
  this.init($parent);
}

Sparkle.prototype = {
  init: function($parent) {
    const canvas = $('<canvas>').addClass('sparkle-canvas').css({
      position: "absolute",
      top: 0,
      left: 0,
      "pointer-events": "none",
      width: '100%',
      height: '100%'
    }).appendTo($parent);

    const context = canvas[0].getContext('2d');

    canvas[0].width = $parent.width();
    canvas[0].height = $parent.height();

    const draw = () => {
      context.clearRect(0, 0, canvas.width(), canvas.height());
      for (let i = 0; i < this.options.count; i++) {
        context.beginPath();
        context.arc(Math.random() * canvas.width(), Math.random() * canvas.height(), Math.random() * 3, 0, 2 * Math.PI, false);
        context.fillStyle = this.options.color;
        context.fill();
      }
    };

    setInterval(draw, 80);
  }
};
