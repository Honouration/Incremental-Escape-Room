import { GameLoop } from "./gameLoop";

const game = new GameLoop();
game.start().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
