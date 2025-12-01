import { GameState } from "./gameEngine";
import { Room, Action } from "./rooms/roomTypes";
export declare class GameUI {
    static displayWelcome(): void;
    static displayRoom(room: Room): void;
    static displayGameState(state: GameState): void;
    static displayActions(actions: Action[]): void;
    static displayActionResult(result: {
        success: boolean;
        message: string;
    }): void;
    static displayGameOver(state: GameState): void;
    static displayHelp(): void;
}
//# sourceMappingURL=ui.d.ts.map