// import { wall_img, player_img, space_img, box_img } from "./assets_loader.js";
import {
  draw_map_element,
  draw_map_element_arc,
  getRandomColor,
  colors,
} from "./drawer.js";

const step_x = 50, step_y = 50


function create_canvas(height, width) {
  const container = document.getElementById("canvas_container")
  // remove old canvas
  container.innerHTML = ""


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


  return [ctx_back, ctx_flow]
}


// async function draw_routes(node_id, last_draw, map_id, canv) {
//   const res = await fetch(`http://127.0.0.1:5000/map/${map_id}/path?from=${node_id}`);

//   const routes = await res.json();
//   for (node_id in routes) {
//     let element = element_types.TRAGET;
//     if (parseInt(node_id) === last_draw) {
//       element = element_types.PLAYER;
//     }
//     const route = routes[node_id];
//     route.forEach((point) => {
//       const x = point.location.x;
//       const y = point.location.y;
//       draw_map_element(x, y, step_x, step_y, element, canv);
//     });
//   }
// }


// async function draw_expantion(map_data, search_type, map_id, canv) {
//   let data = await fetch(`/map/${map_id}/expand/?search_type=${search_type}`).then((res) => res.json());
//   const expantion = data.expantion
//   for (let i = 0; i < expantion.length; i++) {
//     const p = get_point_by_node_id(map_data, expantion[i]);
//     const x = p.location.x;
//     const y = p.location.y;
//     let last_draw = NaN;
//     if (i > 0) last_draw = expantion[i - 1];
//     setTimeout(async () => {
//       draw_map_element(x, y, step_x, step_y, element_types.PLAYER, canv);
//       await draw_routes(expantion[i], last_draw, map_id, canv);
//       // TODO delete the route after time
//     }, 800 * i);
//   }
//   expantion.forEach(async (node_id) => { });
// }






// function get_point_by_node_id(maze_map, node_id) {
//   const points = maze_map.map;
//   for (let p in points) {
//     const id = parseInt(points[p].node_id);
//     if (id == node_id) {
//       return points[p];
//     }
//   }
// }
// function draw_path(points, canv, color) {
//   color = color ? color : element_colors.PLAYER;
//   points.forEach((point) => {
//     draw_map_element_arc(
//       point.location.x,
//       point.location.y,
//       step_x,
//       step_y,
//       color,
//       canv
//     );
//   });
// }

function draw_map(map_meta, canv) {
  for (let x of Array(map_meta.height).keys()) {
    for (let y of Array(map_meta.width).keys()) {
      draw_map_element(
        x,
        y,
        step_x,
        step_y,
        'W',
        canv
      );

    }
  }
}

function draw_flow(assigments, canv) {
  canv.clearRect(0, 0, canv.width, canv.height);

  assigments.forEach(point => {
    let drawer
    if (point.color == point.color.toUpperCase()) {
      drawer = draw_map_element
    }
    else {
      drawer = draw_map_element_arc
    }
    drawer(
      point.x,
      point.y,
      step_x,
      step_y,
      point.color.toUpperCase(),
      canv
    );
  })
}

function clear() {
  // ctx.clearRect(0, 0, canvas.width, canvas.height);
  // draw_element(0, 0,"wall");
  // points.forEach(element => {
  //
  // });
  requestAnimationFrame(draw);
}

// draw_element(50, 50, "wall", ctx);
// draw();

// function wipe_all(canvas_list,height,width) {
//   canvas_list.forEach(canv => {
//     canv.clearRect(0, 0, height, width);
//   })  
// }


// async function draw_path_multi_single(multi, map_id, selected_sol, canv) {
//   if (multi) {
//     var sol_data = await fetch(
//       `http://127.0.0.1:5000/map/${map_id}/sol/multi/?search_type=${selected_sol}`
//     ).then((res) => res.json());

//     const points_routes = sol_data.points;
//     const order = sol_data.order;

//     // update cost
//     const cost = sol_data.cost;
//     document.getElementById("distance_cost").innerHTML = "cost: " + cost;

//     for (let i = 0; i < order.length; i++) {
//       const path_points = points_routes[order[i]];

//       setTimeout(() => {
//         draw_path(path_points, canv, getRandomColor());
//       }, 1000 * i);
//     }
//   } else {
//     var sol_data = await fetch(
//       `http://127.0.0.1:5000/map/${map_id}/sol/single/?search_type=${selected_sol}`
//     ).then((res) => res.json());
//     const points = sol_data.points;
//     const cost = sol_data.cost;
//     document.getElementById("distance_cost").innerHTML = "cost: " + cost;
//     draw_path(points, canv);
//   }
// }


async function main() {
  const selector = document.getElementById("map_selector");
  const map_id = selector[selector.selectedIndex].value;
  const map_meta = await fetch(`http://127.0.0.1:5000/map/${map_id}`).then((res) =>
    res.json()
  );

  const [ctx_back, ctx_flow] = create_canvas(map_meta.height * step_y, map_meta.width * step_x)

  draw_map(map_meta, ctx_back);

  const sol_selector = document.getElementById("sloution_method");
  const selected_sol = sol_selector[sol_selector.selectedIndex].value;

  socket.on('assigment', assigments => {
    draw_flow(assigments, ctx_flow)
    // console.log(assigments)
  })

  const animate_selector = document.getElementById("animation_select")
  const animation_selection = animate_selector[animate_selector.selectedIndex].value;

  if (animation_selection == "animate") {
    const assigments = await fetch(`http://127.0.0.1:5000/map/animate/${map_id}`).then(res => res.json())
  }
  else if (animation_selection == "sol") { 
    const assigments = await fetch(`http://127.0.0.1:5000/map/sol/${map_id}`).then(res => res.json())
    console.log(assigments)
    draw_flow(assigments, ctx_flow)
  }
  // draw_flow(assigments, ctx_flow)

}

const map_selector = document.getElementById("map_selector");
const sol_selector = document.getElementById("sloution_method");
const animate_selector = document.getElementById("animation_select")

animate_selector.addEventListener("change", () => {
  main()
})

map_selector.addEventListener("change", () => {
  main();
});

sol_selector.addEventListener("change", () => {
  main();
})

var socket = io();
socket.on('connect', function () {
  console.log("connected")
  // socket.emit('my event', { data: 'I\'m connected!' });
});

socket.on('message', function () {
  console.log("m")

});

main();
