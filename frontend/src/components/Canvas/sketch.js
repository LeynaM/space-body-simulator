import { useBodiesStore } from "../../stores/bodies.store";

export function sketch(p) {
  p.setup = async () => {
    p.createCanvas(p.width, p.height);
    p.background(240);
  };

  p.draw = () => {
    p.background("darkblue");

    p.fill("yellow");
    p.noStroke();
    const diameter = 40;
    for (let body of useBodiesStore.getState().bodies) {
      p.circle(body.position.x, body.position.y, diameter);
    }
  };

  p.mousePressed = () => {
    if (p.mouseY >= 0 && p.mouseY <= p.height) {
      const position = { x: p.mouseX, y: p.mouseY };
      const velocity = {
        x: (Math.random() - 0.5) * 100,
        y: (Math.random() - 0.5) * 100,
      };
      useBodiesStore.getState().createBody({ position, velocity });
    }
  };
}
