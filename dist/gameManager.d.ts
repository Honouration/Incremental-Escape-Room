import { Room } from "./rooms/roomTypes";
export declare class GameManager {
    private engine;
    private actionHandler;
    private rooms;
    constructor();
    getCurrentRoom(): Room;
    getGameState(): import("./gameEngine").GameState;
    performAction(actionId: string): {
        success: boolean;
        message: string;
    };
    getAvailableActions(): import("./rooms/roomTypes").Action[];
    isGameOver(): boolean;
    getTurnsRemaining(): number;
    getInventory(): string[];
}
//# sourceMappingURL=gameManager.d.ts.map