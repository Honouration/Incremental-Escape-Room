"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.GameLoop = void 0;
const readline = __importStar(require("readline"));
const gameManager_1 = require("./gameManager");
const ui_1 = require("./ui");
class GameLoop {
    constructor() {
        this.running = true;
        this.manager = new gameManager_1.GameManager();
        this.rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout,
        });
    }
    async start() {
        ui_1.GameUI.displayWelcome();
        await this.delay(2000);
        while (this.running && !this.manager.isGameOver()) {
            this.displayCurrentState();
            await this.promptUserAction();
        }
        if (this.manager.isGameOver()) {
            ui_1.GameUI.displayGameOver(this.manager.getGameState());
        }
        this.rl.close();
    }
    displayCurrentState() {
        const room = this.manager.getCurrentRoom();
        const state = this.manager.getGameState();
        ui_1.GameUI.displayRoom(room);
        ui_1.GameUI.displayGameState(state);
        const availableActions = this.manager.getAvailableActions();
        ui_1.GameUI.displayActions(availableActions);
    }
    async promptUserAction() {
        return new Promise((resolve) => {
            this.rl.question("Enter command (0-9, 'inventory', 'status', 'help', 'quit'): ", async (input) => {
                await this.handleInput(input.trim().toLowerCase());
                resolve();
            });
        });
    }
    async handleInput(input) {
        if (input === "quit") {
            this.running = false;
            console.log("👋 Thanks for playing!\n");
            return;
        }
        if (input === "help") {
            ui_1.GameUI.displayHelp();
            await this.promptUserAction();
            return;
        }
        if (input === "inventory") {
            const inventory = this.manager.getInventory();
            console.log(`\n📦 Inventory: ${inventory.length > 0 ? inventory.join(", ") : "Empty"}\n`);
            await this.promptUserAction();
            return;
        }
        if (input === "status") {
            const state = this.manager.getGameState();
            console.log(`\n📊 Current Status:`);
            console.log(`  Room: ${state.currentRoom}/5`);
            console.log(`  Turns: ${state.totalTurns}`);
            console.log(`  Items: ${state.inventory.length}`);
            console.log(`  Secrets: ${state.discoveredSecrets.size}\n`);
            await this.promptUserAction();
            return;
        }
        // Handle action selection
        const actionIndex = parseInt(input, 10);
        if (!isNaN(actionIndex)) {
            const availableActions = this.manager.getAvailableActions();
            if (actionIndex < 0 || actionIndex >= availableActions.length) {
                console.log("❌ Invalid action number.\n");
                return;
            }
            const action = availableActions[actionIndex];
            const result = this.manager.performAction(action.id);
            ui_1.GameUI.displayActionResult(result);
            // Check if player ran out of turns
            if (this.manager.getTurnsRemaining() <= 0 && !this.manager.getGameState().escaped) {
                console.log("⏰ TIME'S UP! You ran out of turns!\n");
                this.running = false;
            }
            return;
        }
        console.log("❌ Invalid command. Type 'help' for options.\n");
    }
    delay(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }
}
exports.GameLoop = GameLoop;
//# sourceMappingURL=gameLoop.js.map