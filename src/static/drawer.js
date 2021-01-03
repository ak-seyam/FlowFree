
var colors = {
  A: "AntiqueWhite",
  B: "Blue",
  C: "CadetBlue",
  D: "DarkGoldenRod",
  F: "Fuchsia",
  G: "Green",
  H: "HotPink",
  I: "IndianRed",
  K: "Khaki",
  L: "Lavender",
  M: "MediumOrchid",
  N: "Navy",
  O: "Orange",
  P: "Purple",
  R: "Red",
  S: "Sienna",
  S: "SteelBlue",
  T: "Tan",
  Q: "Turquoise",
  V: "Violet",
  W: "Gainsboro",
  Y: "Yellow",
  RANDOM: getRandomColor
};

function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}


function draw_map_element_arc(x, y, x_size, y_size, color, canv) {
  (x = x * x_size), (y = y * y_size);

  canv.beginPath();
  canv.arc(x + x_size / 2, y + y_size / 2, x_size / 3, 0, 2 * Math.PI);
  canv.fillStyle = colors[color];
  canv.stroke();
  canv.fill();
  canv.closePath();
}



function draw_map_element(x, y, x_size, y_size, color, canv) {
  x = x * x_size, y = y * y_size;

  canv.beginPath();
  canv.rect(x, y, x_size, y_size);
  canv.fillStyle = colors[color];
  canv.stroke();
  canv.fill();
  canv.closePath();
}


export { draw_map_element, draw_map_element_arc, getRandomColor, colors };