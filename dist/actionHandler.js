"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ActionHandler = void 0;
class ActionHandler {
    constructor(engine) {
        this.engine = engine;
    }
    canExecuteAction(action, room, checkOnly = true) {
        const state = this.engine.getState();
        // Check if already completed
        if (this.engine.isActionComplete(action.id)) {
            return { can: false, reason: "Action already completed" };
        }
        // Check turn cost (but don't spend yet if just checking)
        if (state.totalTurns < action.turnCost) {
            return { can: false, reason: "Not enough turns remaining" };
        }
        // Check prerequisites
        if (action.requires) {
            for (const prereq of action.requires) {
                if (!this.engine.isActionComplete(prereq) && !this.engine.hasItem(prereq)) {
                    return { can: false, reason: `Requires: ${prereq}` };
                }
            }
        }
        // Only spend turns if actually executing (not just checking)
        if (!checkOnly) {
            this.engine.spendTurns(action.turnCost);
        }
        return { can: true };
    }
    executeAction(action) {
        // Turns already spent in canExecuteAction when checkOnly=false
        this.engine.markActionComplete(action.id);
        // Add rewards
        if (action.rewards) {
            for (const reward of action.rewards) {
                this.engine.addToInventory(reward);
            }
        }
        // Handle room transitions
        if (action.unlocks) {
            if (action.unlocks === "ESCAPE") {
                this.engine.completeGame();
            }
            else if (!isNaN(Number(action.unlocks))) {
                this.engine.moveToRoom(Number(action.unlocks));
            }
            else {
                this.engine.discoverSecret(action.unlocks);
            }
        }
        // Handle consequences
        if (action.consequence) {
            if (action.consequence.type === "turnLoss") {
                // Turns already spent, but this indicates extra loss
                this.engine.incrementFailure();
            }
        }
    }
    getAvailableActions(room) {
        const allActions = [...room.mainActions, ...room.optionalActions];
        return allActions.filter((action) => this.canExecuteAction(action, room).can);
    }
}
exports.ActionHandler = ActionHandler;
//# sourceMappingURL=actionHandler.js.map