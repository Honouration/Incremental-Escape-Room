import { GameEngine } from "./gameEngine";
import { Room, Action } from "./rooms/roomTypes";
export declare class ActionHandler {
    private engine;
    constructor(engine: GameEngine);
    canExecuteAction(action: Action, room: Room, checkOnly?: boolean): {
        can: boolean;
        reason?: string;
    };
    executeAction(action: Action): void;
    getAvailableActions(room: Room): Action[];
}
//# sourceMappingURL=actionHandler.d.ts.map