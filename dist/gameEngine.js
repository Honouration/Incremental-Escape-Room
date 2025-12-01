"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.GameEngine = void 0;
class GameEngine {
    constructor() {
        this.STARTING_TURNS = 150;
        this.state = {
            totalTurns: this.STARTING_TURNS,
            currentRoom: 1,
            inventory: [],
            completedActions: new Set(),
            discoveredSecrets: new Set(),
            failureCount: 0,
            escaped: false,
        };
    }
    getState() {
        return this.state;
    }
    spendTurns(amount) {
        if (this.state.totalTurns >= amount) {
            this.state.totalTurns -= amount;
            return true;
        }
        return false;
    }
    addToInventory(item) {
        this.state.inventory.push(item);
    }
    markActionComplete(actionId) {
        this.state.completedActions.add(actionId);
    }
    isActionComplete(actionId) {
        return this.state.completedActions.has(actionId);
    }
    discoverSecret(secretId) {
        this.state.discoveredSecrets.add(secretId);
    }
    moveToRoom(roomNumber) {
        if (roomNumber >= 1 && roomNumber <= 5) {
            this.state.currentRoom = roomNumber;
            return true;
        }
        return false;
    }
    completeGame() {
        this.state.escaped = true;
    }
    incrementFailure() {
        this.state.failureCount++;
    }
    hasItem(itemName) {
        return this.state.inventory.includes(itemName);
    }
    getRemainingTurns() {
        return this.state.totalTurns;
    }
    isGameOver() {
        return this.state.escaped || this.state.totalTurns <= 0;
    }
}
exports.GameEngine = GameEngine;
//# sourceMappingURL=gameEngine.js.map