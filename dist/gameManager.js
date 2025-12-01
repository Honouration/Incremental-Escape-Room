"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.GameManager = void 0;
const gameEngine_1 = require("./gameEngine");
const actionHandler_1 = require("./actionHandler");
const room1_1 = require("./rooms/room1");
const room2_1 = require("./rooms/room2");
const room3_1 = require("./rooms/room3");
const room4_1 = require("./rooms/room4");
const room5_1 = require("./rooms/room5");
class GameManager {
    constructor() {
        this.engine = new gameEngine_1.GameEngine();
        this.actionHandler = new actionHandler_1.ActionHandler(this.engine);
        this.rooms = new Map([
            [1, room1_1.darkCellar],
            [2, room2_1.abandonedLibrary],
            [3, room3_1.secretLaboratory],
            [4, room4_1.forgottenAttic],
            [5, room5_1.clockTower],
        ]);
    }
    getCurrentRoom() {
        const roomId = this.engine.getState().currentRoom;
        return this.rooms.get(roomId) || room1_1.darkCellar;
    }
    getGameState() {
        return this.engine.getState();
    }
    performAction(actionId) {
        const currentRoom = this.getCurrentRoom();
        const allActions = [...currentRoom.mainActions, ...currentRoom.optionalActions];
        const action = allActions.find((a) => a.id === actionId);
        if (!action) {
            return { success: false, message: "Action not found" };
        }
        const canExecute = this.actionHandler.canExecuteAction(action, currentRoom, false);
        if (!canExecute.can) {
            return { success: false, message: canExecute.reason || "Cannot execute action" };
        }
        this.actionHandler.executeAction(action);
        return { success: true, message: `${action.description} - ${action.turnCost} turns spent` };
    }
    getAvailableActions() {
        return this.actionHandler.getAvailableActions(this.getCurrentRoom());
    }
    isGameOver() {
        return this.engine.isGameOver();
    }
    getTurnsRemaining() {
        return this.engine.getRemainingTurns();
    }
    getInventory() {
        return this.engine.getState().inventory;
    }
}
exports.GameManager = GameManager;
//# sourceMappingURL=gameManager.js.map