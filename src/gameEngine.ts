export interface GameState {
  totalTurns: number;
  currentRoom: number;
  inventory: string[];
  completedActions: Set<string>;
  discoveredSecrets: Set<string>;
  failureCount: number;
  escaped: boolean;
}

export class GameEngine {
  private state: GameState;
  private readonly STARTING_TURNS = 150;

  constructor() {
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

  getState(): GameState {
    return this.state;
  }

  spendTurns(amount: number): boolean {
    if (this.state.totalTurns >= amount) {
      this.state.totalTurns -= amount;
      return true;
    }
    return false;
  }

  addToInventory(item: string): void {
    this.state.inventory.push(item);
  }

  markActionComplete(actionId: string): void {
    this.state.completedActions.add(actionId);
  }

  isActionComplete(actionId: string): boolean {
    return this.state.completedActions.has(actionId);
  }

  discoverSecret(secretId: string): void {
    this.state.discoveredSecrets.add(secretId);
  }

  moveToRoom(roomNumber: number): boolean {
    if (roomNumber >= 1 && roomNumber <= 5) {
      this.state.currentRoom = roomNumber;
      return true;
    }
    return false;
  }

  completeGame(): void {
    this.state.escaped = true;
  }

  incrementFailure(): void {
    this.state.failureCount++;
  }

  hasItem(itemName: string): boolean {
    return this.state.inventory.includes(itemName);
  }

  getRemainingTurns(): number {
    return this.state.totalTurns;
  }

  isGameOver(): boolean {
    return this.state.escaped || this.state.totalTurns <= 0;
  }
}
