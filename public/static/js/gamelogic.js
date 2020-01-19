/*
-2 Border
-1 void
0 Ground
1 Team
2 Opponents largest
3 Second largest oponent
4 Other
Self place you're on
*/

d3.selection.prototype.size = function() {
  var n = 0;
  this.each(function() { ++n; });
  return n;
};

var level = 1;
window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
  if (key == "level") {
    level = +value;
  }
});

var w = 66*20, // width of map
  h = 66*20, // height of map
  sz = 20, // cell size
  r = sz / 2, // radius for circles based on cell
  sr = r * r, // radius^2
  ssz = sz * sz, // cell^2
  fogCells = 9,
  v = 3,
  n = level + 1,
  playerIds = new Set([]),
  myid = 0,
  mapRender = false,
  t = 5000;

var rows = Math.ceil(h / sz);
var cols = Math.ceil(w / sz);

function updateMap(map) {
  w = map.length * sz;
  h = map[0].length * sz;
  rows = Math.ceil(h / sz);
  cols = Math.ceil(w / sz);
}


// default map
var map = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -1, -1, -1],
[-1, -1, -1, -2,  0,  0,  0,  0,  0,  0,  0, -2, -1, -1, -1],
[-1, -1, -1, -2,  0,  0,  0,  0,  0,  0,  0, -2, -1, -1, -1],
[-1, -1, -1, -2,  0,  0,  0,  0,  0,  0,  0, -2, -1, -1, -1],
[-1, -1, -1, -2,  0,  0,  0,  0,  0,  0,  0, -2, -1, -1, -1],
[-1, -1, -1, -2,  0,  0,  0,  0,  0,  0,  0, -2, -1, -1, -1],
[-1, -1, -1, -2,  0,  0,  0,  0,  0,  0,  0, -2, -1, -1, -1],
[-1, -1, -1, -2,  0,  0,  0,  0,  0,  0,  0, -2, -1, -1, -1],
[-1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
 [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]];

//var ws = new WebSocket("ws://86737b81.eu.ngrok.io/");
var ws = new WebSocket("ws://2660d191.eu.ngrok.io");


// END OF GLOBAL VARIABLES
/* ----------------------------- */

// Count the number of messages received from websocket server
ws.onopen = function() {
  // this might have to go into onmessage
  var innit = JSON.stringify(
    {"type":"human", "request":"map", "playerid":"","action":null}
  );
  ws.send(innit);

  // TO DO: UPDATE THE MAP -- create a functions

  ws.onmessage = function(event) {
    var dataJSON = JSON.parse(event.data);
    console.log(dataJSON);
    if(dataJSON.type == "uID") myid = dataJSON.uID;

    if(dataJSON.response == "map") {
      //map = dataJSON.response_data;
      //updateDimensions(dataJSON.response_data);
      updateMap(dataJSON.response_data);
      createMap(dataJSON.response_data);
    }

    if(mapRender == true) {
      dataJSON.positions.forEach(e => {
        if(playerIds.has(e.id) == true) {         
          // the player is already on the canvas
          // update the player state
          updatePosition(e);
        } else {
          //console.log("onsmg", e);
          // We need to draw the player
          // [{'id': 1234321, 'x': 123, 'y': 321, 'team_id': 1234321}] ,{…},{…}]
          playerIds.add(e.id);
          addPlayer(e);
        }
      });
    }

  };
};

/* ----------------------------- */
// MAP SETUP

// main svg setup
var svg = d3.select("body").append("svg")
    .attr("width", w)
    .attr("height", h);

var rectx = function(d) { return d.x - r; };
var recty = function(d) { return d.y - r; };

/*

var tailx = function(d) { return d.dx > 0 ? d.sx - r : rectx(d) - d.dx * sz; };
var taily = function(d) { return d.dy > 0 ? d.sy - r : recty(d) - d.dy * sz; };
var tailw = function(d) { return d.dx == 0 ? sz : d.sz = (d.x - d.sx) * d.dx; };
var tailh = function(d) { return d.dy == 0 ? sz : d.sz = (d.y - d.sy) * d.dy; };

var ballCell = function(b) {
  var row = (b.y - b.y % sz) / sz;
  var col = (b.x - b.x % sz) / sz;
  return cells[row * cols + col];
};

var topCell = function(c) { return cells[Math.max(0, c.r - 1) * cols + c.c]; };
var leftCell = function(c) { return cells[c.r * cols + Math.max(0, c.c - 1)]; };
var bottomCell = function(c) { return cells[Math.min(rows - 1, c.r + 1) * cols + c.c]; };
var rightCell = function(c) { return cells[c.r * cols + Math.min(cols - 1, c.c + 1)]; };

var topLeftCell = function(c) { return cells[Math.max(0, c.r - 1) * cols + Math.max(0, c.c - 1)]; };
var bottomLeftCell = function(c) { return cells[Math.min(rows - 1, c.r + 1) * cols + Math.max(0, c.c - 1)]; };
var bottomRightCell = function(c) { return cells[Math.min(rows - 1, c.r + 1) * cols + Math.min(cols - 1, c.c + 1)]; };
var topRightCell = function(c) { return cells[Math.max(0, c.r - 1) * cols + Math.min(cols - 1, c.c + 1)]; };
*/
// Creating cells & walls
$(document).keydown(function(e) {
  //x_pos = parseInt(player.attr("x"));
  //y_pos = parseInt(player.attr("y"));
  duration = 50;
  switch(e.which) {
      case 37: // left
        var d = JSON.stringify(
          {"type":"human", "request":null, "playerid":myid,"action":"move_left"}
        );
        ws.send(d);
        /*
        player.transition()
        .ease(d3.easeLinear)
        .duration(duration)
        .attr("x",x_pos-sz);
        */
        break;

      case 38: // up
      d = JSON.stringify(
        {"type":"human", "request":null, "playerid":myid,"action":"move_up"}
      );
        ws.send(d);
        break;

      case 39: // right
      d = JSON.stringify(
        {"type":"human", "request":null, "playerid":myid,"action":"move_right"}
      );
        ws.send(d);
        break;

      case 40: // down
      d = JSON.stringify(
        {"type":"human", "request":null, "playerid":myid,"action":"move_down"}
      );
        ws.send(d);
        break;

      default: return; // exit this handler for other keys
  }
  e.preventDefault(); // prevent the default action (scroll / move caret)
  //fogRemoval();
});

function createMap(map) {
  // define the cells
  var cells = d3.range(0, rows * cols).map(function (d) {
  var col = d % cols;
  var row = (d - col) / cols;
  return {
    r: row,
    c: col,
    y: col * sz + r,
    x: row * sz + r,
    type: map[col][row]
  };
  });

  var cell = svg.selectAll(".cell")
  .data(cells)
  .enter().append("rect")
  .attr("class", function(d) {
    if(d.type == -2) {
      // is border
      return "cell " + "wall";
    }else if(d.type == -1) {
      // is void
      return "cell " + "void";
    }else if(d.type == 0) {
      // is solid ground
      return "cell " + "ground";
    } else {
      return "cell " + "unknown";
    }
  })
  .attr("layer", "main-layer")
  .attr("grid", function(d){return d.type;})
//  .attr("cellType", function(d) { return ((d.isWall = d.c == 0 || d.c == cols - 1 || d.r == 0 || d.r == rows - 1) ? "wall" : "ground"); })
  .attr("x", rectx)
  .attr("y", recty)
  .attr("width", sz)
  .attr("height", sz)
  .each(function(d) {
    d.elnt = d3.select(this);
  });

  mapRender = true;
  return cell;
}

var cell = createMap();



  /*
// Creating fog of war
var fog = svg.selectAll(".fog")
  .data(cells)
  .enter().append("rect")
  .attr("class", "fog-of-war")
  .attr("x", function(d){ d })
  .attr("y", recty)
  .attr("id", function(d){ return String(d.x-r)+String(d.y-r);})
  .attr("width", sz)
  .attr("height", sz)
  .each(function(d) {
    d.elnt = d3.select(this);
  });
*/

/*
var cellz = svg.selectAll('.cellz')
  .data(cells)
  .enter().append("rect")
  .attr("class", "fog-of-war")
  .attr("x", rectx)
  .attr("y", recty)
  .attr("id", function(d){ return String(d.x-r)+String(d.y-r);})
  .attr("width", sz)
  .attr("height", sz)
*/

/* ------------------------------- */
// THE PLAYER

// {'id': 1234321, 'x': 123, 'y': 321, 'team_id': 1234321}
function updatePlayers() {

}

function updatePosition(e) {
  console.log(e);
  svg.select("#p"+e.id).transition()
  .ease(d3.easeLinear)
  .duration(50)
  .attr("x",e.y*sz)
  .attr("y", e.x*sz);
}

function addPlayer(playerLocs) {
  console.log(playerLocs);
  /*
  var playerLocs = [
    { "x_axis": 40, "y_axis": 40, "color" : "green" },
    { "x_axis": 80, "y_axis": 100, "color" : "purple"},
    { "x_axis": 400, "y_axis": 200, "color" : "red"}];
  */
  playerLocs = [playerLocs];
  var p = svg.selectAll("players")
    .data(playerLocs)
    .enter()
    .append("rect")
    .attr("id", function(d) { return "p"+d.id; })
    .attr("x", function (d) { return d.y * sz; })
    .attr("y", function (d) { return d.x * sz; })
    .attr("type", 'player')
    .attr("width", sz)
    .attr("height", sz)
    .style("fill", "red");
}


var playerLoc = [{ "x_axis": 200, "y_axis": 100, "color" : "green" }];
var player = svg.selectAll("player")
  .data(playerLoc)
  .enter()
  .append("rect")
  .attr("id", "main_player")
  .attr("transform", "translate(0,0)")
  .attr("x", function (d) { return d.x_axis; })
  .attr("y", function (d) { return d.y_axis; })
  .attr("type", 'player')
  .attr("width", 20)
  .attr("height", 20)
  .style("fill", "#fff");

function fogRemoval() {
  var px = parseInt(player.attr("x"));
  var py = parseInt(player.attr("y"));
  
  var ii = px - ((fogCells-1)/2 * sz) - sz;
  for (var i=0; i < fogCells; i++) {
    ii = ii+sz;
    var jj = py - ((fogCells-1)/2 * sz) - sz;
    for (var j=0; j < fogCells; j++) {
      jj = jj+sz;
      document.getElementById(String(ii)+String(jj)).style.fill = "#fff0";
    }
  }
}
//fogRemoval();

// Using jQuery for keydown functions


/* ------------------------------- */
// BORDER CLOSING IN
/*
var wallThickness = 1;
setInterval(wallsMovingIn, 10000);

function wallsMovingIn() {
  cell.attr("class", function(d) {
    if((d.c <= wallThickness+1) || (d.r <=wallThickness+1)) {
      return "cell wall";
    } else {
      return "cell ground";
    }
  });
  wallThickness++;
}
*/

/* ------------------------------- */

/*
var playerz = d3.selectAll(players);
var simulation = d3.forceSimulation(players)
  .force('charge', d3.forceManyBody().strength(5))
//  .force('center', d3.forceCenter())
  .force('collision', d3.forceCollide().radius(function(d) {
    return d.r;
  }))
  .on('tick', ticked);

function ticked() {
  var u = d3.select('svg')
    .selectAll('circle')
    .data(players)

  u.enter()
    .append('circle')
    .attr('r', function(d) {
      return d.radius
    })
    .merge(u)
    .attr('cx', function(d) {
      return d.x
    })
    .attr('cy', function(d) {
      return d.y
    })

  u.exit().remove();
}
*/
/* ------------------------------- */
function previewLocation(c1, p) {
  if (blue) blue.classed("blue", false);
  if (red) red.classed("red", false);
  var c2, d;
  if (s) {
    d = p[0] - c1.x;
    c2 = d > 0 ? rightCell(c1) : leftCell(c1);
  } else {
    d = p[1] - c1.y;
    c2 = d > 0 ? bottomCell(c1) : topCell(c1);
  }
  if (c1.isWall || c2.isWall) {
    blue = null;
    red = null;
  } else if (d > 0) {
    blue = c1.elnt;
    red = c2.elnt;
  } else {
    blue = c2.elnt;
    red = c1.elnt;
  }
  if (blue) blue.classed("blue", function(d) { return !d.isWall; });
  if (red) red.classed("red", function(d) { return !d.isWall; });
}

// Creating the ground grid
var blue, red;

var areaCleared = 0;
var totalArea = svg.selectAll(".ground").size();
var percentageCleared = 0;

var lives = n;
svg.append("text")
  .attr("x", 50)
  .attr("y", 15)
  .attr("class", "smallText")
  .attr("id", "livesText")
  .text("Lives: " + lives);

var gameStartedAt = new Date().getTime();
var timeLeft = t;
svg.append("text")
  .attr("x", w - 130)
  .attr("y", 15)
  .attr("class", "smallText")
  .attr("id", "timeLeftText")
  .text("Time left: " + timeLeft);

var force = d3.layout.force()
  .gravity(0)
  .charge(0)
  .friction(1)
  .size([w, h]);


force.on("tick", function () {
      
  var ball = svg.selectAll(".ball");
  ball.attr("cx", function (d) { return d.x; })
    .attr("cy", function (d) { return d.y; })
    .each(function(b) {
      detectCollisions(b);
      
      var cc = ballCell(b);
      var tc = topCell(cc);
      var lc = leftCell(cc);
      var bc = bottomCell(cc);
      var rc = rightCell(cc);
      if (cc.isWall || (tc.isWall && bc.isWall) || (lc.isWall && rc.isWall)) {
        cc.elnt
          .classed("ground", true)
          .classed("wall", false);
        b.px = b.x = cc.x;
        b.py = b.y = cc.y;
        cc.isWall = b.isMoving = false;
      }
  });
  
  var head = svg.selectAll(".head");
  head.attr("x", function(d) { d.x += d.dx * (v * .4); return rectx(d); })
    .attr("y", function(d) { d.y += d.dy * (v * .4); return recty(d); })
    .each(function(d) {
      svg.select("." + d.cl + ".tail")
        .attr("x", tailx)
        .attr("y", taily)
        .attr("width", tailw)
        .attr("height", tailh);
    });
  
  var ground = svg.selectAll(".ground");
  var tail = svg.selectAll(".tail");
  var wallWasBuilt = false;
  head.filter(function(h) {
      var hc = ballCell(h);
      if (h.dy < 0) {
        var tc = topCell(hc);
        return tc.isWall && h.y - tc.y < sz;
      }
      if (h.dx < 0) {
        var lc = leftCell(hc);
        return lc.isWall && h.x - lc.x < sz;
      }
      if (h.dy > 0) {
        var bc = bottomCell(hc);
        return bc.isWall && bc.y - h.y < sz;
      }
      if (h.dx > 0) {
        var rc = rightCell(hc);
        return rc.isWall && rc.x - h.x < sz;
      }
    }).each(function(h) {
      ground.filter(function(a) {
          return h.dx == 0 ? h.x == a.x && Math.min(h.sy, h.y) <= a.y && a.y <= Math.max(h.sy, h.y) : h.y == a.y && Math.min(h.sx, h.x) <= a.x && a.x <= Math.max(h.sx, h.x);
        })
        .classed("newWall", true)
        .classed("ground", false)
        .each(function(d) { if (!d.isWall) { ++areaCleared; d.isWall = true; } });
      tail.filter("." + h.cl)
        .remove();
      wallWasBuilt = true;
    }).remove();
  
  if (wallWasBuilt) {
    fillEmptyRooms();
  }
  
  var timePlayed = Math.floor(((new Date().getTime()) - gameStartedAt) / 100);
  timeLeft = timePlayed > t ? 0 : t - timePlayed;
  svg.select("#timeLeftText")
    .text("Time left: " + timeLeft);
  if (percentageCleared < 75 && lives >= 0 && timeLeft > 0) {
    force.resume();
  } else {
    force.stop();
    var text, textWidth;
    if (percentageCleared >= 75 && lives >= 0 && timeLeft > 0) {
      text = "Level complete !";
      textWidth = 188;
      d3.select("#nextLevelButton")
        .style("visibility", "visible");
    } else {
      text = "Game over !";
      textWidth = 138;
      d3.select("#playAgainButton")
        .style("visibility", "visible");
    }
    svg.append("text")
      .attr("x", w / 2 - textWidth / 2)
      .attr("y", h / 2)
      .attr("class", "bigTextStroke")
      .text(text);
    svg.append("text")
      .attr("x", w / 2 - textWidth / 2)
      .attr("y", h / 2)
      .attr("class", "bigText")
      .text(text);
  }
});

force.start();

function detectCollisions(b) {
  var dx = b.x - b.px > 0 ? 1 : -1;
  var dy = b.y - b.py > 0 ? 1 : -1;
  var d, sd;

  // tail collision
  svg.selectAll(".tail").filter(function(t) {
      var w = tailw(t);
      var h = tailh(t);
      var x0 = tailx(t);
      var x1 = x0 + w;
      var y0 = taily(t);
      var y1 = y0 + h;
      
      return x0 - r < b.x && b.x < x1 - r && y0 - r < b.y && b.y < y1 + r;
    })
    .each(function(t) {
        --lives;
        svg.select("#livesText")
          .text("Lives: " + (lives < 0 ? 0 : lives));
        svg.selectAll(".head." + t.cl).remove();
      })
    .remove();
  
  // wall borders collision
  var cc = ballCell(b);
  var tc = topCell(cc);
  if (tc.isWall && dy < 0 && (d = b.y - tc.y) <= sz) {
    bounceY(b, sz, d, dy);
  }
  var lc = leftCell(cc);
  if (lc.isWall && dx < 0 && (d = b.x - lc.x) <= sz) {
    bounceX(b, sz, d, dx);
  }
  var bc = bottomCell(cc);
  if (bc.isWall && dy > 0 && (d = bc.y - b.y) <= sz) {
    bounceY(b, sz, d, dy);
  }
  var rc = rightCell(cc);
  if (rc.isWall && dx > 0 && (d = rc.x - b.x) <= sz) {
    bounceX(b, sz, d, dx);
  }
  svg.selectAll(".head").each(function(h) {
    if (h.y - r <= b.y && b.y <= h.y + r) {
      if (dx < 0 && (d = b.x - h.x) <= sz && d > 0) {
        bounceX(b, sz, d, dx);
      }
      if (dx > 0 && (d = h.x - b.x) <= sz && d > 0) {
        bounceX(b, sz, d, dx);
      }
    }
    if (h.x - r <= b.x && b.x <= h.x + r) {
      if (dy < 0 && (d = b.y - h.y) <= sz && d > 0) {
        bounceY(b, sz, d, dy);
      }
      if (dy > 0 && (d = h.y - b.y) <= sz && d > 0) {
        bounceY(b, sz, d, dy);
      }
    }
  });
  
  // wall corners collision
  var tlc = topLeftCell(cc);
  if (!tc.isWall && !lc.isWall && tlc.isWall && (sd = cornerSquareDistance(b.x, b.y, tlc.x + r, tlc.y + r)) <= sr) {
    d = Math.sqrt(sd);
    if (dx < 0) {
      bounceX(b, r, d, dx);
    }
    if (dy < 0) {
      bounceY(b, r, d, dy);
    }
  }
  var blc = bottomLeftCell(cc);
  if (!bc.isWall && !lc.isWall && blc.isWall && (sd = cornerSquareDistance(b.x, b.y, blc.x + r, blc.y - r)) <= sr) {
    d = Math.sqrt(sd);
    if (dx < 0) {
      bounceX(b, r, d, dx);
    }
    if (dy > 0) {
      bounceY(b, r, d, dy);
    }
  }
  var brc = bottomRightCell(cc);
  if (!bc.isWall && !rc.isWall && brc.isWall && (sd = cornerSquareDistance(b.x, b.y, brc.x - r, brc.y - r)) <= sr) {
    d = Math.sqrt(sd);
    if (dx > 0) {
      bounceX(b, r, d, dx);
    }
    if (dy > 0) {
      bounceY(b, r, d, dy);
    }
  }
  var trc = topRightCell(cc);
  if (!tc.isWall && !rc.isWall && trc.isWall && (sd = cornerSquareDistance(b.x, b.y, trc.x - r, trc.y + r)) <= sr) {
    d = Math.sqrt(sd);
    if (dx > 0) {
      bounceX(b, r, d, dx);
    }
    if (dy < 0) {
      bounceY(b, r, d, dy);
    }
  }
  svg.selectAll(".head").each(function(h) {
    if ((sd = cornerSquareDistance(b.x, b.y, h.x + r, h.y + r)) <= sr && sd > 0) {
      d = Math.sqrt(sd);
      if (dx < 0) {
        bounceX(b, r, d, dx);
      }
      if (dy < 0) {
        bounceY(b, r, d, dy);
      }
    }
    if ((sd = cornerSquareDistance(b.x, b.y, h.x + r, h.y - r)) <= sr && sd > 0) {
      d = Math.sqrt(sd);
      if (dx < 0) {
        bounceX(b, r, d, dx);
      }
      if (dy > 0) {
        bounceY(b, r, d, dy);
      }
    }
    if ((sd = cornerSquareDistance(b.x, b.y, h.x - r, h.y - r)) <= sr && sd > 0) {
      d = Math.sqrt(sd);
      if (dx > 0) {
        bounceX(b, r, d, dx);
      }
      if (dy > 0) {
        bounceY(b, r, d, dy);
      }
    }
    if ((sd = cornerSquareDistance(b.x, b.y, h.x - r, h.y + r)) <= sr && sd > 0) {
      d = Math.sqrt(sd);
      if (dx > 0) {
        bounceX(b, r, d, dx);
      }
      if (dy < 0) {
        bounceY(b, r, d, dy);
      }
    }
  });

  // ball collision
  svg.selectAll(".ball").each(function(b2) {
      if (b.id == b2.id) {
        return;
      }
      var sd = cornerSquareDistance(b.x, b.y, b2.x, b2.y);
      if (sd <= ssz) {
        var dx2 = b2.x - b2.px > 0 ? 1 : -1;
        var dy2 = b2.y - b2.py > 0 ? 1 : -1;
        var d = Math.sqrt(sd);
        if (b.isMoving && (b2.x - b.x) * dx > r / 2) {
          bounceX(b, sz, d, dx);
        }
        if (b2.isMoving && (b.x - b2.x) * dx2 > r / 2) {
          bounceX(b2, sz, d, dx2);
        }
        if (b.isMoving && (b2.y - b.y) * dy > r / 2) {
          bounceY(b, sz, d, dy);
        }
        if (b2.isMoving && (b.y - b2.y) * dy2 > r / 2) {
          bounceY(b2, sz, d, dy2);
        }
      }
    });
}

function bounceX(b, m, d, dx) {
  if (b.isMoving) {
    b.x -= (m - d) * dx;
    b.px = b.x + dx * v;
  }
}

function bounceY(b, m, d, dy) {
  if (b.isMoving) {
    b.y -= (m - d) * dy;
    b.py = b.y + dy * v;
  }
}

function cornerSquareDistance(x0, y0, x1, y1) {
  var w = x1 - x0;
  var h = y1 - y0;
  return (w * w + h * h);
}

function visit(c) {
  var tc = topCell(c);
  if (!tc.isWall && !tc.visited) {
    tc.visited = true;
    visit(tc);
  }
  var lc = leftCell(c);
  if (!lc.isWall && !lc.visited) {
    lc.visited = true;
    visit(lc);
  }
  var bc = bottomCell(c);
  if (!bc.isWall && !bc.visited) {
    bc.visited = true;
    visit(bc);
  }
  var rc = rightCell(c);
  if (!rc.isWall && !rc.visited) {
    rc.visited = true;
    visit(rc);
  }
}

function startWall(cell, cl, dx, dy) {
  var wallHead = {
    sx: cell.x,
    sy: cell.y,
    x: cell.x,
    y: cell.y,
    dx: dx,
    dy: dy,
    cl: cl
  };
  if (svg.selectAll("." + cl + ".head").empty()) {
    svg.selectAll("." + cl + ".head")
      .data([wallHead]).enter().append("rect")
      .classed("builder", true)
      .classed(cl, true)
      .classed("head", true)
      .attr("x", rectx)
      .attr("y", recty)
      .attr("width", sz)
      .attr("height", sz);
    var tail = svg.selectAll("." + cl + ".tail")
      .data([wallHead]);
    tail.enter().append("rect")
      .classed("builder", true)
      .classed(cl, true)
      .classed("tail", true)
      .attr("x", tailx)
      .attr("y", taily)
      .attr("width", tailw)
      .attr("height", tailh);
    tail.exit().remove();
  }
}
