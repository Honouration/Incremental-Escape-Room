"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const gameLoop_1 = require("./gameLoop");
const game = new gameLoop_1.GameLoop();
game.start().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
});
//# sourceMappingURL=index.js.map