export function sketch(p) {
  let circles = [];

  p.setup = () => {
    p.createCanvas(p.width, p.height);
    p.background(240);
  };

  p.draw = () => {
    p.background("darkblue");
    for (let c of circles) {
      p.fill("yellow");
      p.noStroke();
      p.circle(c.x, c.y, c.r * 2);
    }
  };

  p.mousePressed = () => {
    if (p.mouseY >= 0 && p.mouseY <= p.height) {
      circles.push({ x: p.mouseX, y: p.mouseY, r: 20 });
    }
  };
}
