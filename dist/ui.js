"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.GameUI = void 0;
const roomTypes_1 = require("./rooms/roomTypes");
class GameUI {
    static displayWelcome() {
        console.clear();
        console.log(`
╔════════════════════════════════════════════════════════╗
║        BLACKOUT ESCAPE - 5 Room Progression            ║
║                                                        ║
║  Starting Turns: 150 (30 seconds each + 1 action)     ║
║  Main Path: ~90 turns | Extra Exploration: ~25 turns  ║
║  Efficient players: ~10 turns remaining                ║
╚════════════════════════════════════════════════════════╝
    `);
    }
    static displayRoom(room) {
        console.log(`\n${"═".repeat(60)}`);
        console.log(`🏚️  ROOM ${room.id}: ${room.name.toUpperCase()}`);
        console.log(`Theme: ${room.theme}`);
        console.log(`${"═".repeat(60)}`);
        console.log(`\n${room.description}\n`);
    }
    static displayGameState(state) {
        console.log(`\n${"─".repeat(60)}`);
        console.log(`⏱️  TURNS REMAINING: ${state.totalTurns}`);
        console.log(`📍 CURRENT ROOM: ${state.currentRoom}/5`);
        console.log(`📦 INVENTORY (${state.inventory.length}): ${state.inventory.join(", ") || "Empty"}`);
        console.log(`🎯 ACTIONS COMPLETED: ${state.completedActions.size}`);
        console.log(`🔓 SECRETS DISCOVERED: ${state.discoveredSecrets.size}`);
        console.log(`${"─".repeat(60)}\n`);
    }
    static displayActions(actions) {
        if (actions.length === 0) {
            console.log("❌ No actions available. You may have run out of turns!\n");
            return;
        }
        console.log(`📋 AVAILABLE ACTIONS (${actions.length}):\n`);
        actions.forEach((action, index) => {
            const typeIcon = {
                [roomTypes_1.ActionType.MAIN]: "⭐",
                [roomTypes_1.ActionType.OPTIONAL]: "✨",
                [roomTypes_1.ActionType.RISK]: "⚠️",
            }[action.type];
            console.log(`  [${index}] ${typeIcon} ${action.description}`);
            console.log(`      └─ Cost: ${action.turnCost} turn(s) | ID: ${action.id}`);
            if (action.requires && action.requires.length > 0) {
                console.log(`      └─ Requires: ${action.requires.join(", ")}`);
            }
        });
        console.log();
    }
    static displayActionResult(result) {
        if (result.success) {
            console.log(`✅ SUCCESS: ${result.message}\n`);
        }
        else {
            console.log(`❌ FAILED: ${result.message}\n`);
        }
    }
    static displayGameOver(state) {
        console.log(`\n${"═".repeat(60)}`);
        console.log(`🎮 GAME OVER`);
        console.log(`${"═".repeat(60)}`);
        if (state.escaped) {
            console.log(`\n🎉 CONGRATULATIONS! YOU ESCAPED!\n`);
            console.log(`Final Stats:`);
            console.log(`  • Turns Remaining: ${state.totalTurns}`);
            console.log(`  • Total Items Collected: ${state.inventory.length}`);
            console.log(`  • Secrets Discovered: ${state.discoveredSecrets.size}`);
            console.log(`  • Failures Encountered: ${state.failureCount}\n`);
        }
        else {
            console.log(`\n💀 TIME'S UP! YOU DIDN'T ESCAPE IN TIME.\n`);
            console.log(`Final Stats:`);
            console.log(`  • Room Reached: ${state.currentRoom}/5`);
            console.log(`  • Total Items Collected: ${state.inventory.length}`);
            console.log(`  • Secrets Discovered: ${state.discoveredSecrets.size}\n`);
        }
    }
    static displayHelp() {
        console.log(`
Commands:
  [number]  - Execute action (0-9, depending on available actions)
  inventory - Show current inventory
  status    - Show game status
  help      - Show this help menu
  quit      - Exit game
    `);
    }
}
exports.GameUI = GameUI;
//# sourceMappingURL=ui.js.map