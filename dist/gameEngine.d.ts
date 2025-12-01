export interface GameState {
    totalTurns: number;
    currentRoom: number;
    inventory: string[];
    completedActions: Set<string>;
    discoveredSecrets: Set<string>;
    failureCount: number;
    escaped: boolean;
}
export declare class GameEngine {
    private state;
    private readonly STARTING_TURNS;
    constructor();
    getState(): GameState;
    spendTurns(amount: number): boolean;
    addToInventory(item: string): void;
    markActionComplete(actionId: string): void;
    isActionComplete(actionId: string): boolean;
    discoverSecret(secretId: string): void;
    moveToRoom(roomNumber: number): boolean;
    completeGame(): void;
    incrementFailure(): void;
    hasItem(itemName: string): boolean;
    getRemainingTurns(): number;
    isGameOver(): boolean;
}
//# sourceMappingURL=gameEngine.d.ts.map