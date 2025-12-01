import { GameEngine } from "./gameEngine";
import { ActionHandler } from "./actionHandler";
import { Room } from "./rooms/roomTypes";
import { darkCellar } from "./rooms/room1";
import { abandonedLibrary } from "./rooms/room2";
import { secretLaboratory } from "./rooms/room3";
import { forgottenAttic } from "./rooms/room4";
import { clockTower } from "./rooms/room5";

export class GameManager {
  private engine: GameEngine;
  private actionHandler: ActionHandler;
  private rooms: Map<number, Room>;

  constructor() {
    this.engine = new GameEngine();
    this.actionHandler = new ActionHandler(this.engine);
    this.rooms = new Map([
      [1, darkCellar],
      [2, abandonedLibrary],
      [3, secretLaboratory],
      [4, forgottenAttic],
      [5, clockTower],
    ]);
  }

  getCurrentRoom(): Room {
    const roomId = this.engine.getState().currentRoom;
    return this.rooms.get(roomId) || darkCellar;
  }

  getGameState() {
    return this.engine.getState();
  }

  performAction(actionId: string): { success: boolean; message: string } {
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

  isGameOver(): boolean {
    return this.engine.isGameOver();
  }

  getTurnsRemaining(): number {
    return this.engine.getRemainingTurns();
  }

  getInventory(): string[] {
    return this.engine.getState().inventory;
  }
}
