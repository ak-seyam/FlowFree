// import { wall_img, player_img, space_img, box_img } from "./assets_loader.js";
import { draw_map_element, draw_map_element_arc, colors } from "./drawer.js";

const step_x = 50,
  step_y = 50;

function create_canvas(height, width) {
  const container = document.getElementById("canvas_container");
  // remove old canvas
  container.innerHTML = "";

  var canvas_back = document.createElement("canvas");
  canvas_back.setAttribute("width", width);
  canvas_back.setAttribute("height", height);
  canvas_back.setAttribute("class", "back_canv");
  container.appendChild(canvas_back);
  var ctx_back = canvas_back.getContext("2d");

  var canvas_flow = document.createElement("canvas");
  canvas_flow.setAttribute("width", width);
  canvas_flow.setAttribute("height", height);
  container.appendChild(canvas_flow);
  var ctx_flow = canvas_flow.getContext("2d");

  document.getElementById("variable_selection").style.left = `${
    canvas_back.width + 50
  }px`;
  return [ctx_back, ctx_flow];
}

function draw_map(map_meta, canv) {
  for (let x of Array(map_meta.width).keys()) {
    for (let y of Array(map_meta.height).keys()) {
      draw_map_element(x, y, step_x, step_y, "w", canv);
    }
  }
}

function draw_flow(assigments, ctx) {
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

  assigments.forEach((point) => {
    let drawer;
    if (point.color == point.color.toUpperCase()) {
      drawer = draw_map_element;
    } else {
      drawer = draw_map_element_arc;
    }
    drawer(point.x, point.y, step_x, step_y, point.color.toUpperCase(), ctx);
  });
}

function write_domains(variable_domains) {
  let domains_table = document.getElementById("colors_table");
  domains_table.innerHTML =
    "<tr> <th> point</th><th colspan='12'>colors</th></tr>";
  for (let index in variable_domains) {
    let point = variable_domains[index];

    let row = domains_table.insertRow();
    let coord_cell = row.insertCell();
    coord_cell.innerHTML = `(${point.x}, ${point.y})`;
    for (let color of point.color) {
      let cell = row.insertCell();
      cell.innerHTML = color;
      cell.style.backgroundColor = colors[color.toUpperCase()];
    }
  }
}

async function main() {
  const selector = document.getElementById("map_selector");
  const map_id = selector[selector.selectedIndex].value;
  const map_meta = await fetch(
    `http://127.0.0.1:5000/map/${map_id}`
  ).then((res) => res.json());

  const [ctx_back, ctx_flow] = create_canvas(
    map_meta.height * step_y,
    map_meta.width * step_x
  );

  draw_map(map_meta, ctx_back);

  const sol_selector = document.getElementById("sloution_method");
  const selected_sol = sol_selector[sol_selector.selectedIndex].value;

  socket.on("assigment", (assigments) => {
    draw_flow(assigments, ctx_flow);
  });

  socket.on("variable_domain", (variables_domains) =>
    write_domains(variables_domains)
  );
  socket.on("var", (point) => {
    document.getElementById(
      "select_point"
    ).innerHTML = `(${point.x}, ${point.y}) ${point.color}`;
  });
  const animate_selector = document.getElementById("animation_select");
  const animation_selection =
    animate_selector[animate_selector.selectedIndex].value;

  if (animation_selection == "animate") {
    socket.emit("animate", { map_id: map_id, method: selected_sol });
  } else if (animation_selection == "sol") {
    const assigments = await fetch(
      `http://127.0.0.1:5000/map/sol/${map_id}`
    ).then((res) => res.json());
    console.log(assigments);
    draw_flow(assigments, ctx_flow);
  }
}

const map_selector = document.getElementById("map_selector");
const sol_selector = document.getElementById("sloution_method");
const animate_selector = document.getElementById("animation_select");

animate_selector.addEventListener("change", () => {
  main();
});

map_selector.addEventListener("change", () => {
  main();
});

sol_selector.addEventListener("change", (e) => {
  if (e.target.value == "dump") {
    document.getElementById("colors_table").style.display = "none";
  } else {
    document.getElementById("colors_table").style.display = "unset";
  }
  main();
});
document.getElementById("reset").onclick = () => {
  main();
};

document.getElementById("send_one").onclick = () =>
  socket.emit("send_more", true);

var interval;
var delay_ms = 100;
document.getElementById("auto_send").onclick = () => {
  interval = setInterval(() => socket.emit("send_more", true), delay_ms);
};
document.getElementById("stop").onclick = () => clearInterval(interval);
socket.on("done", () => clearInterval(interval));

document.getElementById("delay").onchange = (e) => {
  clearInterval(interval);
  delay_ms = e.target.value;
};
socket.on("message", function () {
  console.log("m");
});

main();
