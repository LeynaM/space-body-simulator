import styles from "./Canvas.module.css";
import p5 from "p5";
import { sketch } from "./sketch";
import { useEffect, useRef } from "react";
import { useBodiesStore } from "../../stores/bodies.store";

function Canvas() {
  const canvasContainerRef = useRef(null);
  const pfiveRef = useRef(null);
  const { loadBodies } = useBodiesStore();

  useEffect(() => {
    setInterval(() => loadBodies(), 1000);
  }, [loadBodies]);

  useEffect(() => {
    if (!canvasContainerRef.current) return;

    const observer = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      console.log("Width:", width, "Height:", height);
      pfiveRef.current.resizeCanvas(width, height);
    });
    observer.observe(canvasContainerRef.current);

    if (pfiveRef.current === null) {
      pfiveRef.current = new p5(sketch, canvasContainerRef.current);
    }

    return () => {
      observer.disconnect();
    };
  }, []);

  return <div className={styles.container} ref={canvasContainerRef}></div>;
}

export default Canvas;
