import "./App.css";
import Header from "./components/Header/Header";
import Canvas from "./components/Canvas/Canvas";
import { useWebsocketStore } from "./stores/websocket.store";
import { useBodiesStore } from "./stores/bodies.store";
import { useEffect } from "react";

function App() {
  const { connect } = useWebsocketStore();
  const { setBodies } = useBodiesStore();

  useEffect(() => {
    const onOpen = () => console.log("open");
    const onMessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setBodies(data);
        console.log("ws bodies", data);
      } catch (err) {
        console.error("❌ Failed to parse message", err);
      }
    };
    const onClose = () => console.log("close");
    connect(onOpen, onMessage, onClose);
  }, [connect, setBodies]);

  return (
    <>
      <Header />
      <Canvas />
    </>
  );
}

export default App;
